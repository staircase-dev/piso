from piso.graph import adjacency_matrix
from piso.intervalarray import (
    bridge,
    complement,
    contains,
    coverage,
    difference,
    intersection,
    isdisjoint,
    issubset,
    issuperset,
    split,
    symmetric_difference,
    union,
)
from piso.ndframe import join, lookup


def register_accessors():
    """
    When called this function will register the "piso" ArrayAccessor on :class:`pandas.IntervalIndex` and :class:`pandas.arrays.IntervalArray`.

    Examples
    --------

    >>> import piso
    >>> piso.register_accessors()
    >>> arr = pd.arrays.IntervalArray.from_tuples(
    ...     [(0, 4), (2, 5), (3, 6), (7, 8), (8, 9), (10, 12)],
    ... )

    >>> arr.piso.union()
    <IntervalArray>
    [(0.0, 6.0], (7.0, 9.0], (10.0, 12.0]]
    Length: 3, closed: right, dtype: interval[float64]

    >>> arr = pd.IntervalIndex(arr)
    >>> arr.piso.union()
    IntervalIndex([(0.0, 2.0], (5.0, 6.0], (7.0, 9.0], (10.0, 12.0]],
                closed='right',
                dtype='interval[float64]')
    """
    from piso import accessor

    accessor._register_accessors()


def get_version():
    try:
        from importlib.metadata import version  # type: ignore

        return version(__name__)
    except Exception:
        return "unknown"


__version__ = get_version()
