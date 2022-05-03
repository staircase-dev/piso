import itertools

import numpy as np
import pandas as pd

from piso.intervalarray import _validate_array_of_intervals_arrays


def _adj_mat_intersection(lefts, rights, closed, fill_diagonal=True):
    result = np.greater.outer(rights, lefts) & np.less.outer(lefts, rights)
    if closed == "both":
        result = result | np.equal.outer(rights, lefts) | np.equal.outer(lefts, rights)
    if fill_diagonal:
        np.fill_diagonal(result, False)
    return result


def _adjacency_matrix_set_of_intervals(interval_array, edges, include_index):
    if edges == "intersect":
        result = _adj_mat_intersection(
            interval_array.left, interval_array.right, interval_array.closed
        )
    elif edges == "disjoint":
        result = ~_adj_mat_intersection(
            interval_array.left,
            interval_array.right,
            interval_array.closed,
            fill_diagonal=False,
        )
    else:
        raise ValueError(f"Invalid value for edges parameter: {edges}")

    if include_index:
        result = pd.DataFrame(result, index=interval_array, columns=interval_array)

    return result


def _adjacency_matrix_set_of_sets(*interval_arrays, edges, include_index):
    _validate_array_of_intervals_arrays(*interval_arrays, validate_intervals=False)
    lefts = list(itertools.chain.from_iterable([ia.left for ia in interval_arrays]))
    rights = list(itertools.chain.from_iterable([ia.right for ia in interval_arrays]))
    closed = interval_arrays[0].closed

    if edges == "intersect":
        component_result = _adj_mat_intersection(lefts, rights, closed)
        numpy_logical = np.logical_or
    elif edges == "disjoint":
        component_result = ~_adj_mat_intersection(
            lefts, rights, closed, fill_diagonal=False
        )
        numpy_logical = np.logical_and
    else:
        raise ValueError(f"Invalid value for edges parameter: {edges}")

    index = np.cumsum([0] + [len(ia) for ia in interval_arrays[:-1]])
    result = numpy_logical.reduceat(
        numpy_logical.reduceat(component_result, index, axis=0), index, axis=1
    )
    np.fill_diagonal(result, False)

    if include_index:
        result = pd.DataFrame(
            result,
            index=range(len(interval_arrays)),
            columns=range(len(interval_arrays)),
        )

    return result


def adjacency_matrix(
    interval_array, *interval_arrays, edges="intersect", include_index=True
):
    """
    Returns a 2D array (or dataframe) of boolean values indicating edges between nodes in a graph.

    The nodes correspond to sets and the edges are defined by the relationship
    defined by the *edges* parameter.

    What is considered a set is determined by the number of positional arguments used, that is, determined by the
    size of *interval_arrays*.

    If *interval_arrays* is empty then the sets are considered to be the intervals contained in *interval_array*.

    If *interval_arrays* is not empty then the sets are considered to be *interval_array* and the elements in *interval_arrays*.
    Each of these arrays is assumed to contain disjoint intervals (and satisfy the definition of a set).  Any array containing
    overlaps between intervals will be mapped to one with disjoint intervals via a union operation.

    Note that the diagonal is defined with False values by default.

    Parameters
    ----------
    interval_array : :class:`pandas.arrays.IntervalArray` or :class:`pandas.IntervalIndex`
        The first (and possibly only) operand.
    *interval_arrays : argument list of :class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`
        Must contain at least one argument.
    edges : {"intersect", "disjoint"}, default "intersect"
        Defines the relationship that edges between nodes represent.
    include_index : bool, default True
        If True then a :class:`pandas.DataFrame`, indexed by the intervals, is returned.
        If False then a :class:`numpy.ndarray` is returned.

    Returns
    -------
    :class:`pandas.DataFrame` or :class:`numpy.ndarray`
        Boolean valued, symmetrical, with False along diagonal.

    Examples
    ---------

    >>> import pandas as pd
    >>> import piso

    >>> arr = pd.arrays.IntervalArray.from_tuples(
    ...    [(0,4), (3,6), (5, 7), (8,9), (9,10)],
    ...    closed="both",
    ... )

    >>> piso.adjacency_matrix(arr)
             [0, 4]  [3, 6]  [5, 7]  [8, 9]  [9, 10]
    [0, 4]    False    True   False   False    False
    [3, 6]     True   False    True   False    False
    [5, 7]    False    True   False   False    False
    [8, 9]    False   False   False   False     True
    [9, 10]   False   False   False    True    False

    >>> piso.adjacency_matrix(arr, include_index=False)
    array([[False,  True, False, False, False],
           [ True, False,  True, False, False],
           [False,  True, False, False, False],
           [False, False, False, False,  True],
           [False, False, False,  True, False]])

    >>> piso.adjacency_matrix(arr, edges="disjoint")
             [0, 4]  [3, 6]  [5, 7]  [8, 9]  [9, 10]
    [0, 4]    False   False    True    True     True
    [3, 6]    False   False   False    True     True
    [5, 7]     True   False   False    True     True
    [8, 9]     True    True    True   False    False
    [9, 10]    True    True    True   False    False

    >>> ii1 = pd.IntervalIndex.from_tuples([(0,3), (2,8), (11,15)], closed="left")
    >>> ii2 = pd.IntervalIndex.from_tuples([(3,5), (7,12), (16,20)], closed="left")
    >>> ii3 = pd.IntervalIndex.from_tuples([(9,11), (25,26)], closed="left")
    >>> ii4 = pd.IntervalIndex.from_tuples([(23,24)], closed="left")

    >>> piso.adjacency_matrix(ii1,ii2,ii3,ii4)
                0	    1   	2   	3
    0	False	True	False	False
    1	True	False	True	False
    2	False	True	False	False
    3	False	False	False	False

    >>> piso.adjacency_matrix(ii1,ii2,ii3,ii4, edges="disjoint", include_index=False)
    array([[False, False,  True,  True],
           [False, False, False,  True],
           [ True, False, False,  True],
           [ True,  True,  True, False]])
    """

    if len(interval_arrays) == 0:
        return _adjacency_matrix_set_of_intervals(interval_array, edges, include_index)
    else:
        return _adjacency_matrix_set_of_sets(
            interval_array, *interval_arrays, edges=edges, include_index=include_index
        )
