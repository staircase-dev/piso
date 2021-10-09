import pandas as pd
import pytest

import piso
import piso.intervalarray as piso_intervalarray
from piso import register_accessors

register_accessors()


def get_accessor_method(self, function):
    return {
        piso_intervalarray.union: self.piso.union,
        piso_intervalarray.intersection: self.piso.intersection,
        piso_intervalarray.difference: self.piso.difference,
        piso_intervalarray.symmetric_difference: self.piso.symmetric_difference,
    }[function]


def get_package_method(function):
    return {
        piso_intervalarray.union: piso.union,
        piso_intervalarray.intersection: piso.intersection,
        piso_intervalarray.symmetric_difference: piso.symmetric_difference,
        piso_intervalarray.difference: piso.difference,
    }[function]


def perform_op(*args, how, function, **kwargs):
    # how = "supplied, accessor, or package"
    if how == "accessor":
        self, *args = args
        return get_accessor_method(self, function)(*args, **kwargs)
    elif how == "package":
        return get_package_method(function)(*args, **kwargs)
    else:
        return function(*args, **kwargs)


def make_ia1(interval_index, closed):
    ia1 = pd.arrays.IntervalArray.from_tuples(
        [(0, 4), (2, 5), (3, 6), (7, 8), (8, 9), (10, 12)],
        closed=closed,
    )
    if interval_index:
        ia1 = pd.IntervalIndex(ia1)
    return ia1


def make_ia2(interval_index, closed):
    ia2 = pd.arrays.IntervalArray.from_tuples(
        [(0, 4), (2, 5), (3, 6)],
        closed=closed,
    )
    if interval_index:
        ia2 = pd.IntervalIndex(ia2)
    return ia2


def make_ia3(interval_index, closed):
    ia3 = pd.arrays.IntervalArray.from_tuples(
        [(3, 4), (8, 11)],
        closed=closed,
    )
    if interval_index:
        ia3 = pd.IntervalIndex(ia3)
    return ia3


def assert_interval_array_equal(interval_array, expected, interval_index):
    if interval_index:
        interval_array = interval_array.values

    pd._testing.assert_interval_array_equal(
        interval_array,
        expected,
        exact=False,
    )


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "return_type",
    ["infer", pd.arrays.IntervalArray, pd.IntervalIndex],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_union(interval_index, closed, return_type, how):
    arr = [func(interval_index, closed) for func in (make_ia1, make_ia2, make_ia3)]
    result = perform_op(
        *arr,
        return_type=return_type,
        how=how,
        function=piso_intervalarray.union,
    )
    expected = pd.arrays.IntervalArray.from_tuples(
        [(0, 6), (7, 12)],
        closed=closed,
    )
    interval_index = (
        interval_index if return_type == "infer" else (return_type == pd.IntervalIndex)
    )
    assert_interval_array_equal(
        result,
        expected,
        interval_index,
    )


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "return_type",
    ["infer", pd.arrays.IntervalArray, pd.IntervalIndex],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_intersection(interval_index, closed, return_type, how):
    arr = [func(interval_index, closed) for func in (make_ia1, make_ia2, make_ia3)]
    result = perform_op(
        *arr,
        return_type=return_type,
        how=how,
        function=piso_intervalarray.intersection,
    )
    expected = pd.arrays.IntervalArray.from_tuples(
        [(3, 4)],
        closed=closed,
    )
    interval_index = (
        interval_index if return_type == "infer" else (return_type == pd.IntervalIndex)
    )
    assert_interval_array_equal(
        result,
        expected,
        interval_index,
    )


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "return_type",
    ["infer", pd.arrays.IntervalArray, pd.IntervalIndex],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_intersection_2(interval_index, closed, return_type, how):
    arr = [func(interval_index, closed) for func in (make_ia1, make_ia2, make_ia3)]
    result = perform_op(
        *arr,
        min_overlaps=2,
        return_type=return_type,
        how=how,
        function=piso_intervalarray.intersection,
    )
    expected = pd.arrays.IntervalArray.from_tuples(
        [(0, 6), (8, 9), (10, 11)],
        closed=closed,
    )
    interval_index = (
        interval_index if return_type == "infer" else (return_type == pd.IntervalIndex)
    )
    assert_interval_array_equal(
        result,
        expected,
        interval_index,
    )


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "return_type",
    ["infer", pd.arrays.IntervalArray, pd.IntervalIndex],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_symmetric_difference(interval_index, closed, return_type, how):
    arr = [func(interval_index, closed) for func in (make_ia1, make_ia2, make_ia3)]
    result = perform_op(
        *arr,
        return_type=return_type,
        how=how,
        function=piso_intervalarray.symmetric_difference,
    )

    expected = pd.arrays.IntervalArray.from_tuples(
        [(7, 8), (9, 10), (11, 12)],
        closed=closed,
    )
    interval_index = (
        interval_index if return_type == "infer" else (return_type == pd.IntervalIndex)
    )
    assert_interval_array_equal(
        result,
        expected,
        interval_index,
    )


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "return_type",
    ["infer", pd.arrays.IntervalArray, pd.IntervalIndex],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_symmetric_difference_2(interval_index, closed, return_type, how):
    arr = [func(interval_index, closed) for func in (make_ia1, make_ia2, make_ia3)]
    result = perform_op(
        *arr,
        min_overlaps="all",
        return_type=return_type,
        how=how,
        function=piso_intervalarray.symmetric_difference,
    )

    expected = pd.arrays.IntervalArray.from_tuples(
        [(0, 3), (4, 6), (7, 12)],
        closed=closed,
    )
    interval_index = (
        interval_index if return_type == "infer" else (return_type == pd.IntervalIndex)
    )
    assert_interval_array_equal(
        result,
        expected,
        interval_index,
    )


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "return_type",
    ["infer", pd.arrays.IntervalArray, pd.IntervalIndex],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_difference_1(closed, interval_index, return_type, how):
    interval_array1 = make_ia1(interval_index, closed)
    interval_array2 = make_ia2(interval_index, closed)
    result = perform_op(
        interval_array1,
        interval_array2,
        return_type=return_type,
        how=how,
        function=piso_intervalarray.difference,
    )
    expected = pd.arrays.IntervalArray.from_tuples(
        [(7, 9), (10, 12)],
        closed=closed,
    )
    interval_index = (
        interval_index if return_type == "infer" else (return_type == pd.IntervalIndex)
    )
    assert_interval_array_equal(
        result,
        expected,
        interval_index,
    )


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "return_type",
    ["infer", pd.arrays.IntervalArray, pd.IntervalIndex],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_difference_2(closed, interval_index, return_type, how):
    interval_array1 = make_ia1(interval_index, closed)
    interval_array2 = make_ia2(interval_index, closed)
    result = perform_op(
        interval_array2,
        interval_array1,
        return_type=return_type,
        how=how,
        function=piso_intervalarray.difference,
    )
    expected = pd.arrays.IntervalArray([], closed=closed)
    interval_index = (
        interval_index if return_type == "infer" else (return_type == pd.IntervalIndex)
    )
    assert_interval_array_equal(
        result,
        expected,
        interval_index,
    )


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "return_type",
    ["infer", pd.arrays.IntervalArray, pd.IntervalIndex],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_difference_3(closed, interval_index, return_type, how):
    interval_array1 = make_ia1(interval_index, closed)
    interval_array3 = make_ia3(interval_index, closed)
    result = perform_op(
        interval_array1,
        interval_array3,
        return_type=return_type,
        how=how,
        function=piso_intervalarray.difference,
    )
    expected = pd.arrays.IntervalArray.from_tuples(
        [(0, 3), (4, 6), (7, 8), (11, 12)],
        closed=closed,
    )
    interval_index = (
        interval_index if return_type == "infer" else (return_type == pd.IntervalIndex)
    )
    assert_interval_array_equal(
        result,
        expected,
        interval_index,
    )


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "return_type",
    ["infer", pd.arrays.IntervalArray, pd.IntervalIndex],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_difference_4(closed, interval_index, return_type, how):
    interval_array1 = make_ia1(interval_index, closed)
    interval_array2 = make_ia2(interval_index, closed)
    interval_array3 = make_ia3(interval_index, closed)
    result = perform_op(
        interval_array1,
        interval_array2,
        interval_array3,
        return_type=return_type,
        how=how,
        function=piso_intervalarray.difference,
    )
    expected = pd.arrays.IntervalArray.from_tuples(
        [(7, 8), (11, 12)],
        closed=closed,
    )
    interval_index = (
        interval_index if return_type == "infer" else (return_type == pd.IntervalIndex)
    )
    assert_interval_array_equal(
        result,
        expected,
        interval_index,
    )
