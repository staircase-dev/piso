import warnings

import pandas as pd

import piso.docstrings.accessor as docstrings
from piso import intervalarray
from piso._decorators import Appender


class CachedAccessor:
    """
    Custom property-like object.
    A descriptor for caching accessors.

    Parameters
    ----------
    name : str
        Namespace that will be accessed under, e.g. ``df.foo``.
    accessor : cls
        Class with the extension methods.

    Notes
    -----
    The definition for CachedAccessor has been borrowed, almost verbatim, from :mod:`pandas`
    """

    def __init__(self, name: str, accessor) -> None:
        self._name = name
        self._accessor = accessor

    def __get__(self, obj, cls):
        if obj is None:
            # we're accessing the attribute of the class, i.e., IntervalIndex.piso
            return self._accessor
        accessor_obj = self._accessor(obj)
        # Replace the property with the accessor object. Inspired by:
        # https://www.pydanny.com/cached-property.html
        object.__setattr__(obj, self._name, accessor_obj)
        return accessor_obj


def _register_accessor(name, cls):
    """
    Notes
    -----
    The definition for this method has been borrowed, almost verbatim, from :mod:`pandas`
    """

    def decorator(accessor):
        if hasattr(cls, name) and getattr(cls, name) != ArrayAccessor:
            warnings.warn(
                f"registration of accessor {repr(accessor)} under name "
                f"{repr(name)} for type {repr(cls)} is overriding a preexisting "
                f"attribute with the same name.",
                UserWarning,
                stacklevel=2,
            )
        setattr(cls, name, CachedAccessor(name, accessor))
        if not hasattr(cls, "_accessors"):
            cls._accessors = set()
        cls._accessors.add(name)
        return accessor

    return decorator


class ArrayAccessor:
    """
    The piso accessor for :class:`pandas.arrays.IntervalArray` and :class:`pandas.IntervalIndex`

    Parameters
    ----------
    _interval_array : :class:`pandas.arrays.IntervalArray` or :class:`pandas.IntervalIndex`
    """

    def __init__(self, _interval_array):
        self._interval_array = _interval_array

    @Appender(docstrings.union_docstring, join="\n", indents=1)
    def union(self, *interval_arrays, squeeze=False, return_type="infer"):
        return intervalarray.union(
            self._interval_array,
            *interval_arrays,
            squeeze=squeeze,
            return_type=return_type,
        )

    @Appender(docstrings.intersection_docstring, join="\n", indents=1)
    def intersection(
        self, *interval_arrays, min_overlaps="all", squeeze=False, return_type="infer"
    ):
        return intervalarray.intersection(
            self._interval_array,
            *interval_arrays,
            min_overlaps=min_overlaps,
            squeeze=squeeze,
            return_type=return_type,
        )

    @Appender(docstrings.difference_docstring, join="\n", indents=1)
    def difference(self, *interval_arrays, squeeze=False, return_type="infer"):
        return intervalarray.difference(
            self._interval_array,
            *interval_arrays,
            squeeze=squeeze,
            return_type=return_type,
        )

    @Appender(docstrings.symmetric_difference_docstring, join="\n", indents=1)
    def symmetric_difference(
        self, *interval_arrays, min_overlaps=2, squeeze=False, return_type="infer"
    ):
        return intervalarray.symmetric_difference(
            self._interval_array,
            *interval_arrays,
            min_overlaps=min_overlaps,
            squeeze=squeeze,
            return_type=return_type,
        )

    @Appender(docstrings.isdisjoint_docstring, join="\n", indents=1)
    def isdisjoint(self, *interval_arrays):
        return intervalarray.isdisjoint(
            self._interval_array,
            *interval_arrays,
        )

    @Appender(docstrings.issuperset_docstring, join="\n", indents=1)
    def issuperset(self, *interval_arrays, squeeze=False):
        return intervalarray.issuperset(
            self._interval_array,
            *interval_arrays,
            squeeze=squeeze,
        )

    @Appender(docstrings.issubset_docstring, join="\n", indents=1)
    def issubset(self, *interval_arrays, squeeze=False):
        return intervalarray.issubset(
            self._interval_array,
            *interval_arrays,
            squeeze=squeeze,
        )

    @Appender(docstrings.coverage_docstring, join="\n", indents=1)
    def coverage(self, domain=None):
        return intervalarray.coverage(
            self._interval_array,
            domain,
        )

    @Appender(docstrings.complement_docstring, join="\n", indents=1)
    def complement(self, domain=None):
        return intervalarray.complement(
            self._interval_array,
            domain,
        )

    @Appender(docstrings.get_indexer_docstring, join="\n", indents=1)
    def get_indexer(self, x):
        return intervalarray.get_indexer(
            self._interval_array,
            x,
        )


def _register_accessors():
    _register_accessor("piso", pd.IntervalIndex)(ArrayAccessor)
    _register_accessor("piso", pd.arrays.IntervalArray)(ArrayAccessor)
