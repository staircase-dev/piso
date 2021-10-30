import numpy as np
import pandas as pd
import staircase as sc

import piso.docstrings.intervalarray as docstrings
from piso._decorators import Appender
from piso.util import (
    _boolean_stairs_to_interval_array,
    _interval_x_to_stairs,
    _validate_intervals,
)


def _check_matched_closed(interval_arrays):
    closed_values = [arr.closed for arr in interval_arrays]
    assert closed_values.count(closed_values[0]) == len(closed_values)


def _validate_array_of_intervals_arrays(*interval_arrays):
    assert len(interval_arrays) > 0
    _check_matched_closed(interval_arrays)
    for arr in interval_arrays:
        _validate_intervals(arr)


def _get_return_type(interval_array, return_type):
    assert return_type in ("infer", pd.IntervalIndex, pd.arrays.IntervalArray)
    return interval_array.__class__ if return_type == "infer" else return_type


def _make_stairs(*interval_arrays):
    if len(interval_arrays) == 1:
        stairs = _interval_x_to_stairs(*interval_arrays)
    else:
        stairs = sc.sum(
            [_interval_x_to_stairs(arr).make_boolean() for arr in interval_arrays]
        )
    return stairs


@Appender(docstrings.union_docstring, join="\n", indents=1)
def union(interval_array, *interval_arrays, squeeze=False, return_type="infer"):
    _validate_array_of_intervals_arrays(interval_array, *interval_arrays)
    klass = _get_return_type(interval_array, return_type)
    stairs = _make_stairs(interval_array, *interval_arrays)
    result = _boolean_stairs_to_interval_array(stairs.make_boolean(), klass)
    if squeeze and len(result) == 1:
        result = result[0]
    return result


@Appender(docstrings.intersection_docstring, join="\n", indents=1)
def intersection(
    interval_array,
    *interval_arrays,
    min_overlaps="all",
    squeeze=False,
    return_type="infer",
):
    _validate_array_of_intervals_arrays(interval_array, *interval_arrays)
    klass = _get_return_type(interval_array, return_type)
    if min_overlaps == "all":
        min_overlaps = (
            len(interval_arrays) + 1 if interval_arrays else len(interval_array)
        )
    stairs = _make_stairs(interval_array, *interval_arrays)
    result = _boolean_stairs_to_interval_array(stairs >= min_overlaps, klass)
    if squeeze and len(result) == 1:
        result = result[0]
    return result


@Appender(docstrings.difference_docstring, join="\n", indents=1)
def difference(interval_array, *interval_arrays, squeeze=False, return_type="infer"):
    assert interval_arrays
    _validate_array_of_intervals_arrays(interval_array, *interval_arrays)
    klass = _get_return_type(interval_array, return_type)
    stairs_operand1 = _interval_x_to_stairs(interval_array)
    stairs_operand2 = _make_stairs(*interval_arrays)
    stairs = stairs_operand1 & (~stairs_operand2)
    result = _boolean_stairs_to_interval_array(stairs, klass)
    if squeeze and len(result) == 1:
        result = result[0]
    return result


@Appender(docstrings.symmetric_difference_docstring, join="\n", indents=1)
def symmetric_difference(
    interval_array, *interval_arrays, min_overlaps=2, squeeze=False, return_type="infer"
):
    _validate_array_of_intervals_arrays(interval_array, *interval_arrays)
    klass = _get_return_type(interval_array, return_type)
    if min_overlaps == "all":
        min_overlaps = (
            len(interval_arrays) + 1 if interval_arrays else len(interval_array)
        )
    stairs = _make_stairs(interval_array, *interval_arrays)

    if min_overlaps == 2:
        stairs = stairs == 1
    else:
        stairs = (stairs >= 1) & (stairs <= min_overlaps - 1)
    result = _boolean_stairs_to_interval_array(stairs, klass)
    if squeeze and len(result) == 1:
        result = result[0]
    return result


@Appender(docstrings.isdisjoint_docstring, join="\n", indents=1)
def isdisjoint(interval_array, *interval_arrays):
    _validate_array_of_intervals_arrays(interval_array, *interval_arrays)
    if interval_arrays:
        stairs = _make_stairs(interval_array, *interval_arrays)
        result = stairs.max() <= 1
    elif len(interval_array) == 0:
        result = True
    else:
        arr = np.stack([interval_array.left.values, interval_array.right.values])
        arr = arr[arr[:, 0].argsort()]
        result = np.all(arr[0, 1:] >= arr[1, :-1])
    return result


def _create_is_super_or_sub(which, docstring):

    comparator_func = {"superset": sc.Stairs.ge, "subset": sc.Stairs.le}[which]

    @Appender(docstring, join="\n", indents=1)
    def func(interval_array, *interval_arrays, squeeze=True):
        _validate_array_of_intervals_arrays(interval_array, *interval_arrays)
        assert interval_arrays
        stepfunction = _interval_x_to_stairs(interval_array).make_boolean()

        def _comp(ia):
            return bool(
                comparator_func(
                    stepfunction,
                    _interval_x_to_stairs(ia).make_boolean(),
                )
            )

        result = np.array([_comp(ia) for ia in interval_arrays])

        if squeeze and len(result) == 1:
            result = result[0]
        return result

    return func


issuperset = _create_is_super_or_sub("superset", docstrings.issuperset_docstring)
issubset = _create_is_super_or_sub("subset", docstrings.issubset_docstring)


def _get_domain_tuple(interval_array, domain):
    if domain is None and len(interval_array) > 0:
        domain = (interval_array.left.min(), interval_array.right.max())
    elif domain is None and len(interval_array) == 0:
        domain = (0, 1)  # dummy domain to ensure no failure
    elif isinstance(domain, tuple):
        if len(domain) != 2:
            raise ValueError(
                f"If domain parameter is tuple then it must have length 2.  Supplied argument has length {len(domain)}."
            )
    elif isinstance(domain, pd.Interval):
        domain = (domain.left, domain.right)
    else:
        raise ValueError(
            "The domain parameter must be either a 2-tuple, pandas.Interval, or None."
        )
    return domain


@Appender(docstrings.coverage_docstring, join="\n", indents=1)
def coverage(interval_array, domain=None):
    stepfunction = _interval_x_to_stairs(interval_array).make_boolean()
    if isinstance(domain, (pd.IntervalIndex, pd.arrays.IntervalArray)):
        domain = _interval_x_to_stairs(domain)
        result = stepfunction.where(domain).mean()
    else:
        domain = _get_domain_tuple(interval_array, domain)
        result = stepfunction.clip(*domain).mean()
    return result


@Appender(docstrings.complement_docstring, join="\n", indents=1)
def complement(interval_array, domain=None):
    stepfunction = _interval_x_to_stairs(interval_array).invert()
    if isinstance(domain, (pd.IntervalIndex, pd.arrays.IntervalArray)):
        domain = _interval_x_to_stairs(domain)
        result = stepfunction.where(domain).fillna(0)
    else:
        domain = _get_domain_tuple(interval_array, domain)
        result = stepfunction.clip(*domain).fillna(0)
    return _boolean_stairs_to_interval_array(result, interval_array.__class__)


@Appender(docstrings.get_indexer_docstring, join="\n", indents=1)
def get_indexer(interval_array, x):
    if not isdisjoint(interval_array):
        raise ValueError("get_indexer method is only valid for disjoint intervals.")
    return sc.Stairs(
        start=interval_array.left,
        end=interval_array.right,
        value=range(1, len(interval_array) + 1),
        initial_value=-1,
        closed=interval_array.closed,
    )(x)
