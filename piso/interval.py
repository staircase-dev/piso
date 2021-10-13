import numpy as np
import pandas as pd

import piso.docstrings.interval as docstrings
from piso._decorators import Appender
from piso._exceptions import (
    ClosedMismatchError,
    ClosedValueError,
    DegenerateIntervalError,
)


def _validate_args(interval1, interval2):
    for obj in (interval1, interval2):
        if obj.length == 0:
            raise DegenerateIntervalError(obj)
        if obj.closed not in {"left", "right"}:
            raise ClosedValueError(obj)
    if interval1.closed != interval2.closed:
        raise ClosedMismatchError


@Appender(docstrings.union_docstring, join="\n", indents=1)
def union(interval1, interval2, squeeze=True):
    _validate_args(interval1, interval2)
    l1, r1 = interval1.left, interval1.right
    l2, r2 = interval2.left, interval2.right

    if r1 < l2:
        result = pd.arrays.IntervalArray([interval1, interval2])
    elif r2 < l1:
        result = pd.arrays.IntervalArray([interval2, interval1])
    else:
        result = pd.Interval(min(l1, l2), max(r1, r2), closed=interval1.closed)
        if not squeeze:
            result = pd.arrays.IntervalArray([result])
    return result


@Appender(docstrings.intersection_docstring, join="\n", indents=1)
def intersection(interval1, interval2, squeeze=True):
    _validate_args(interval1, interval2)
    l1, r1 = interval1.left, interval1.right
    l2, r2 = interval2.left, interval2.right

    if r1 <= l2 or r2 <= l1:
        result = pd.arrays.IntervalArray([], closed=interval1.closed)
    else:
        result = pd.Interval(max(l1, l2), min(r1, r2), closed=interval1.closed)
        if not squeeze:
            result = pd.arrays.IntervalArray([result])
    return result


@Appender(docstrings.difference_docstring, join="\n", indents=1)
def difference(interval1, interval2, squeeze=True):
    _validate_args(interval1, interval2)
    l1, r1 = interval1.left, interval1.right
    l2, r2 = interval2.left, interval2.right

    if r1 <= l2 or r2 <= l1:
        result = interval1
        if not squeeze:
            result = pd.arrays.IntervalArray([result])
    elif l2 <= l1 < r1 <= r2:
        result = pd.arrays.IntervalArray([], closed=interval1.closed)
    elif l1 < l2 < r2 < r1:
        result = pd.arrays.IntervalArray.from_tuples(
            [(l1, l2), (r2, r1)],
            closed=interval1.closed,
        )
    elif l1 < l2:
        result = pd.Interval(l1, l2, closed=interval1.closed)
        if not squeeze:
            result = pd.arrays.IntervalArray([result])
    else:  # r2 < l1
        result = pd.Interval(r2, r1, closed=interval1.closed)
        if not squeeze:
            result = pd.arrays.IntervalArray([result])
    return result


@Appender(docstrings.symmetric_difference_docstring, join="\n", indents=1)
def symmetric_difference(interval1, interval2, squeeze=True):
    _validate_args(interval1, interval2)
    l1, r1 = interval1.left, interval1.right
    l2, r2 = interval2.left, interval2.right

    if r1 < l2:  # separated
        result = pd.arrays.IntervalArray([interval1, interval2])
    elif r2 < l1:  # separated
        result = pd.arrays.IntervalArray([interval2, interval1])
    elif r1 == l2 or r2 == l1:  # adjacent
        result = pd.Interval(min(l1, l2), max(r1, r2), closed=interval1.closed)
        if not squeeze:
            result = pd.arrays.IntervalArray([result])
    elif l1 == l2 and r1 == r2:
        result = pd.arrays.IntervalArray([], closed=interval1.closed)
    elif l1 == l2:
        result = pd.Interval(min(r1, r2), max(r1, r2), closed=interval1.closed)
        if not squeeze:
            result = pd.arrays.IntervalArray([result])
    elif r1 == r2:
        result = pd.Interval(min(l1, l2), max(l1, l2), closed=interval1.closed)
        if not squeeze:
            result = pd.arrays.IntervalArray([result])
    else:
        result = pd.arrays.IntervalArray.from_tuples(
            [(min(l1, l2), max(l1, l2)), (min(r1, r2), max(r1, r2))],
            closed=interval1.closed,
        )
    return result


def _make_is_sub_or_superset(which, docstring):

    left_bound_comparator = {"super": np.less_equal, "sub": np.greater_equal}[which]
    right_bound_comparator = {"super": np.greater_equal, "sub": np.less_equal}[which]

    @Appender(docstring, join="\n", indents=1)
    def func(interval, *intervals, squeeze=True):
        assert intervals
        lefts = np.array([i.left for i in intervals])
        rights = np.array([i.right for i in intervals])

        result = np.logical_and(
            left_bound_comparator(interval.left, lefts),
            right_bound_comparator(interval.right, rights),
        )

        if len(result) == 1 and squeeze:
            result = result[0]

        return result

    return func


issuperset = _make_is_sub_or_superset("super", docstrings.issuperset_docstring)
issubset = _make_is_sub_or_superset("sub", docstrings.issubset_docstring)
