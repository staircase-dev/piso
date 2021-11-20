import numpy as np
import pandas as pd
from pandas.core.indexes import interval


def adjacency_matrix(interval_array, edges="intersect", include_index=True):
    """
    Returns a 2D array (or dataframe) of boolean values indicating edges between nodes in a graph.

    The set of nodes correspond to intervals and the edges are defined by the relationship
    defined by the *edges* parameter.

    Note that the diagonal is defined with False values by default.

    Parameters
    ----------
    interval_array : :class:`pandas.arrays.IntervalArray` or :class:`pandas.IntervalIndex`
        Contains the intervals.
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
    """
    if edges == "intersect":
        result = _adj_mat_intersection(interval_array)
    elif edges == "disjoint":
        result = ~_adj_mat_intersection(interval_array, fill_diagonal=False)
    else:
        raise ValueError(f"Invalid value for edges parameter: {edges}")

    if include_index:
        result = pd.DataFrame(result, index=interval_array, columns=interval_array)

    return result


def _adj_mat_intersection(interval_array, fill_diagonal=True):
    result = np.greater.outer(
        interval_array.right, interval_array.left
    ) & np.less.outer(interval_array.left, interval_array.right)
    if interval_array.closed == "both":
        result = (
            result
            | np.equal.outer(interval_array.right, interval_array.left)
            | np.equal.outer(interval_array.left, interval_array.right)
        )
    if fill_diagonal:
        np.fill_diagonal(result, False)
    return result
