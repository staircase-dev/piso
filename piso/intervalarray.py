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
    return_type="infer"
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
