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
        piso_intervalarray.symmetric_difference: self.piso.symmetric_difference,
        piso_intervalarray.isdisjoint: self.piso.isdisjoint,
        piso_intervalarray.issuperset: self.piso.issuperset,
        piso_intervalarray.issubset: self.piso.issubset,
        piso_intervalarray.coverage: self.piso.coverage,
        piso_intervalarray.complement: self.piso.complement,
    }[function]


def get_package_method(function):
    return {
        piso_intervalarray.union: piso.union,
        piso_intervalarray.intersection: piso.intersection,
        piso_intervalarray.symmetric_difference: piso.symmetric_difference,
        piso_intervalarray.isdisjoint: piso_intervalarray.isdisjoint,
        piso_intervalarray.issuperset: piso.issuperset,
        piso_intervalarray.issubset: piso.issubset,
        piso_intervalarray.coverage: piso.coverage,
        piso_intervalarray.complement: piso.complement,
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


def make_ia_from_tuples(interval_index, tuples, closed):
    klass = pd.IntervalIndex if interval_index else pd.arrays.IntervalArray
    return klass.from_tuples(tuples, closed=closed)


def assert_interval_array_equal(interval_array, expected, interval_index):
    if interval_index:
        interval_array = interval_array.values

    pd._testing.assert_interval_array_equal(
        interval_array,
        expected,
        exact=False,
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
def test_union(closed, interval_index, return_type, how):
    interval_array = make_ia1(interval_index, closed)
    # result = piso_intervalarray.union(interval_array, return_type)
    result = perform_op(
        interval_array,
        return_type=return_type,
        how=how,
        function=piso_intervalarray.union,
    )
    expected = pd.arrays.IntervalArray.from_tuples(
        [(0, 6), (7, 9), (10, 12)],
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
def test_intersection_overlaps_all_empty_result(
    closed, interval_index, return_type, how
):
    interval_array = make_ia1(interval_index, closed)
    result = perform_op(
        interval_array,
        return_type=return_type,
        how=how,
        function=piso_intervalarray.intersection,
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
def test_intersection_overlaps_all_nonempty_result(
    closed, interval_index, return_type, how
):
    interval_array = make_ia2(interval_index, closed=closed)
    result = perform_op(
        interval_array,
        return_type=return_type,
        how=how,
        function=piso_intervalarray.intersection,
    )
    expected = pd.arrays.IntervalArray.from_tuples([(3, 4)], closed=closed)
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
def test_intersection_overlaps_2(closed, interval_index, return_type, how):
    interval_array = make_ia1(interval_index, closed)
    result = perform_op(
        interval_array,
        min_overlaps=2,
        return_type=return_type,
        how=how,
        function=piso_intervalarray.intersection,
    )
    expected = pd.arrays.IntervalArray.from_tuples([(2, 5)], closed=closed)
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
def test_intersection_overlaps_3(closed, interval_index, return_type, how):
    interval_array = make_ia1(interval_index, closed)
    result = perform_op(
        interval_array,
        min_overlaps=3,
        return_type=return_type,
        how=how,
        function=piso_intervalarray.intersection,
    )
    expected = pd.arrays.IntervalArray.from_tuples([(3, 4)], closed=closed)
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
def test_symmetric_difference(closed, interval_index, return_type, how):
    interval_array = make_ia1(interval_index, closed)
    result = perform_op(
        interval_array,
        return_type=return_type,
        how=how,
        function=piso_intervalarray.symmetric_difference,
    )
    expected = pd.arrays.IntervalArray.from_tuples(
        [(0, 2), (5, 6), (7, 9), (10, 12)],
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
def test_symmetric_difference_min_overlaps_3(closed, interval_index, return_type, how):
    interval_array = make_ia1(interval_index, closed)
    result = perform_op(
        interval_array,
        min_overlaps=3,
        return_type=return_type,
        how=how,
        function=piso_intervalarray.symmetric_difference,
    )
    expected = pd.arrays.IntervalArray.from_tuples(
        [(0, 3), (4, 6), (7, 9), (10, 12)],
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
def test_symmetric_difference_min_overlaps_all_1(
    closed, interval_index, return_type, how
):
    interval_array = make_ia1(interval_index, closed)
    result = perform_op(
        interval_array,
        min_overlaps="all",
        return_type=return_type,
        how=how,
        function=piso_intervalarray.symmetric_difference,
    )
    expected = pd.arrays.IntervalArray.from_tuples(
        [(0, 6), (7, 9), (10, 12)],
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
def test_symmetric_difference_min_overlaps_all_2(
    closed, interval_index, return_type, how
):
    interval_array = make_ia2(interval_index, closed)
    result = perform_op(
        interval_array,
        min_overlaps="all",
        return_type=return_type,
        how=how,
        function=piso_intervalarray.symmetric_difference,
    )
    expected = pd.arrays.IntervalArray.from_tuples(
        [(0, 3), (4, 6)],
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


def map_to_dates(interval_array, date_type):
    def make_date(x):
        ts = pd.Timestamp(f"2021-10-{x}")
        if date_type == "numpy":
            return ts.to_numpy()
        if date_type == "datetime":
            return ts.to_pydatetime()
        if date_type == "timedelta":
            return ts - pd.Timestamp("2021-10-1")
        return ts

    return interval_array.from_arrays(
        interval_array.left.map(make_date),
        interval_array.right.map(make_date),
    )


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "tuples, expected",
    [
        ([], True),
        ([(1, 2), (2, 3)], True),
        ([(1, 2), (3, 4)], True),
        ([(1, 3), (2, 4)], False),
        ([(1, 4), (2, 3)], False),
        ([(1, 2), (2, 3), (3, 4)], True),
        ([(1, 2), (3, 4), (5, 6)], True),
        ([(1, 3), (2, 4), (5, 6)], False),
        ([(1, 4), (2, 3), (5, 6)], False),
    ],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_isdisjoint(interval_index, tuples, expected, closed, date_type, how):

    interval_array = make_ia_from_tuples(interval_index, tuples, closed)
    interval_array = map_to_dates(interval_array, date_type)
    result = perform_op(interval_array, how=how, function=piso_intervalarray.isdisjoint)
    assert result == expected


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "domain, expected",
    [(None, 10 / 12), ((0, 10), 0.8), (pd.Interval(0, 10), 0.8), ((15, 20), 0)],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_coverage(interval_index, domain, expected, closed, how):
    ia = make_ia1(interval_index, closed)
    result = perform_op(
        ia,
        how=how,
        function=piso_intervalarray.coverage,
        domain=domain,
    )
    assert result == expected


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_coverage_edge_case(interval_index, closed, how):
    ia = make_ia_from_tuples(interval_index, [], closed)
    result = perform_op(
        ia,
        how=how,
        function=piso_intervalarray.coverage,
        domain=None,
    )
    assert result == 0.0


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_coverage_exception(interval_index, closed, how):
    domain = (1, 2, 3)
    with pytest.raises(ValueError):
        ia = make_ia1(interval_index, closed)
        perform_op(
            ia,
            how=how,
            function=piso_intervalarray.coverage,
            domain=domain,
        )


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "domain, expected_tuples",
    [
        (None, [(6, 7), (9, 10)]),
        ((-5, 15), [(-5, 0), (6, 7), (9, 10), (12, 15)]),
        (pd.Interval(-5, 15), [(-5, 0), (6, 7), (9, 10), (12, 15)]),
        ((6.5, 9.5), [(6.5, 7), (9, 9.5)]),
        ((12, 15), [(12, 15)]),
        ((6, 7), [(6, 7)]),
        ((3, 4), []),
        (pd.IntervalIndex.from_tuples([(-5, 5), (9, 11)]), [(-5, 0), (9, 10)]),
    ],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_complement(interval_index, domain, expected_tuples, closed, how):
    if hasattr(domain, "set_closed"):
        domain = domain.set_closed(closed)
    ia = make_ia1(interval_index, closed)
    expected = make_ia_from_tuples(False, expected_tuples, closed)
    result = perform_op(
        ia,
        how=how,
        function=piso_intervalarray.complement,
        domain=domain,
    )
    assert_interval_array_equal(
        result,
        expected,
        interval_index,
    )
