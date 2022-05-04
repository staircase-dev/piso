import numpy as np
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
        piso_intervalarray.contains: self.piso.contains,
        piso_intervalarray.split: self.piso.split,
        piso_intervalarray.bridge: self.piso.bridge,
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
        piso_intervalarray.contains: piso.contains,
        piso_intervalarray.split: piso.split,
        piso_intervalarray.bridge: piso.bridge,
    }[function]


def perform_op(*args, method, function, **kwargs):
    # method = "supplied, accessor, or package"
    if method == "accessor":
        self, *args = args
        return get_accessor_method(self, function)(*args, **kwargs)
    elif method == "package":
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


def make_ia4(interval_index, closed):
    ia4 = pd.arrays.IntervalArray.from_tuples(
        [(1, 4), (2, 5), (3, 6)],
        closed=closed,
    )
    if interval_index:
        ia4 = pd.IntervalIndex(ia4)
    return ia4


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
    "method",
    ["supplied", "accessor", "package"],
)
def test_union(closed, interval_index, return_type, method):
    interval_array = make_ia1(interval_index, closed)
    # result = piso_intervalarray.union(interval_array, return_type)
    result = perform_op(
        interval_array,
        return_type=return_type,
        method=method,
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
    "method",
    ["supplied", "accessor", "package"],
)
def test_intersection_overlaps_all_empty_result(
    closed, interval_index, return_type, method
):
    interval_array = make_ia1(interval_index, closed)
    result = perform_op(
        interval_array,
        return_type=return_type,
        method=method,
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
    "method",
    ["supplied", "accessor", "package"],
)
def test_intersection_overlaps_all_nonempty_result(
    closed, interval_index, return_type, method
):
    interval_array = make_ia2(interval_index, closed=closed)
    result = perform_op(
        interval_array,
        return_type=return_type,
        method=method,
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
    "method",
    ["supplied", "accessor", "package"],
)
def test_intersection_overlaps_2(closed, interval_index, return_type, method):
    interval_array = make_ia1(interval_index, closed)
    result = perform_op(
        interval_array,
        min_overlaps=2,
        return_type=return_type,
        method=method,
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
    "method",
    ["supplied", "accessor", "package"],
)
def test_intersection_overlaps_3(closed, interval_index, return_type, method):
    interval_array = make_ia1(interval_index, closed)
    result = perform_op(
        interval_array,
        min_overlaps=3,
        return_type=return_type,
        method=method,
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
    "method",
    ["supplied", "accessor", "package"],
)
def test_symmetric_difference(closed, interval_index, return_type, method):
    interval_array = make_ia1(interval_index, closed)
    result = perform_op(
        interval_array,
        return_type=return_type,
        method=method,
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
    "method",
    ["supplied", "accessor", "package"],
)
def test_symmetric_difference_min_overlaps_3(
    closed, interval_index, return_type, method
):
    interval_array = make_ia1(interval_index, closed)
    result = perform_op(
        interval_array,
        min_overlaps=3,
        return_type=return_type,
        method=method,
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
    "method",
    ["supplied", "accessor", "package"],
)
def test_symmetric_difference_min_overlaps_all_1(
    closed, interval_index, return_type, method
):
    interval_array = make_ia1(interval_index, closed)
    result = perform_op(
        interval_array,
        min_overlaps="all",
        return_type=return_type,
        method=method,
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
    "method",
    ["supplied", "accessor", "package"],
)
def test_symmetric_difference_min_overlaps_all_2(
    closed, interval_index, return_type, method
):
    interval_array = make_ia2(interval_index, closed)
    result = perform_op(
        interval_array,
        min_overlaps="all",
        return_type=return_type,
        method=method,
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


def map_to_dates(obj, date_type):
    if date_type is None:
        return obj

    def make_date(x):
        ts = pd.to_datetime(x, unit="d", origin="2021-09-30")
        if date_type == "numpy":
            return ts.to_numpy()
        if date_type == "datetime":
            return ts.to_pydatetime()
        if date_type == "timedelta":
            return ts - pd.Timestamp("2021-10-1")
        return ts

    if isinstance(obj, (pd.IntervalIndex, pd.arrays.IntervalArray)):
        return obj.from_arrays(
            obj.left.map(make_date),
            obj.right.map(make_date),
            obj.closed,
        )
    elif isinstance(obj, list):
        return [make_date(x) for x in obj]


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
    ["left", "right", "neither"],
)
@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "method",
    ["supplied", "accessor", "package"],
)
def test_isdisjoint_left_right_neither(
    interval_index, tuples, expected, closed, date_type, method
):

    interval_array = make_ia_from_tuples(interval_index, tuples, closed)
    interval_array = map_to_dates(interval_array, date_type)
    result = perform_op(
        interval_array, method=method, function=piso_intervalarray.isdisjoint
    )
    assert result == expected


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "tuples, expected",
    [
        ([], True),
        ([(1, 2), (2, 3)], False),
        ([(1, 2), (3, 3)], True),
        ([(1, 2), (3, 4)], True),
        ([(1, 3), (2, 4)], False),
        ([(1, 4), (2, 3)], False),
        ([(1, 2), (2, 3), (3, 4)], False),
        ([(1, 2), (3, 4), (5, 6)], True),
        ([(1, 3), (2, 4), (5, 6)], False),
        ([(1, 4), (2, 3), (5, 6)], False),
    ],
)
@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "method",
    ["supplied", "accessor", "package"],
)
def test_isdisjoint_both(interval_index, tuples, expected, date_type, method):

    interval_array = make_ia_from_tuples(interval_index, tuples, "both")
    interval_array = map_to_dates(interval_array, date_type)
    result = perform_op(
        interval_array, method=method, function=piso_intervalarray.isdisjoint
    )
    assert result == expected


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "domain, expected_fraction, expected_sum",
    [
        (None, 10 / 12, 10),
        ((0, 10), 0.8, 8),
        (pd.Interval(0, 10), 0.8, 8),
        ((15, 20), 0, 0),
        (pd.IntervalIndex.from_tuples([(0, 6), (10, 12)]), 1, 8),
        (pd.IntervalIndex.from_tuples([(6, 7), (9, 10)]), 0, 0),
    ],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "method",
    ["supplied", "accessor", "package"],
)
@pytest.mark.parametrize(
    "how",
    ["fraction", "sum"],
)
def test_coverage(
    interval_index, domain, expected_fraction, expected_sum, closed, method, how
):
    if hasattr(domain, "set_closed"):
        domain = domain.set_closed(closed)
    ia = make_ia1(interval_index, closed)
    result = perform_op(
        ia,
        method=method,
        function=piso_intervalarray.coverage,
        domain=domain,
        how=how,
    )
    expected = expected_fraction if how == "fraction" else expected_sum
    assert result == expected


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "domain_interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "method",
    ["supplied", "accessor", "package"],
)
@pytest.mark.parametrize(
    "how",
    ["fraction", "sum"],
)
def test_coverage_bins(interval_index, domain_interval_index, closed, method, how):
    domain = pd.arrays.IntervalArray.from_tuples(
        [(0, 2), (3, 7), (8, 10)],
        closed=closed,
    )
    if domain_interval_index:
        domain = pd.IntervalIndex(domain)
    ia = make_ia1(interval_index, closed)
    result = perform_op(
        ia,
        method=method,
        function=piso_intervalarray.coverage,
        domain=domain,
        bins=True,
        how=how,
    )
    values = [1, 0.75, 0.5] if how == "fraction" else [2.0, 3.0, 1.0]
    expected = pd.Series(values, index=domain)
    pd.testing.assert_series_equal(result, expected)


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "method",
    ["supplied", "accessor", "package"],
)
def test_coverage_edge_case(interval_index, closed, method):
    ia = make_ia_from_tuples(interval_index, [], closed)
    result = perform_op(
        ia,
        method=method,
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
    "method",
    ["supplied", "accessor", "package"],
)
def test_coverage_exception(interval_index, closed, method):
    domain = (1, 2, 3)
    with pytest.raises(ValueError):
        ia = make_ia1(interval_index, closed)
        perform_op(
            ia,
            method=method,
            function=piso_intervalarray.coverage,
            domain=domain,
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
    "method",
    ["supplied", "accessor", "package"],
)
def test_coverage_exception2(interval_index, closed, method):
    domain = (1, 2)
    with pytest.raises(ValueError):
        ia = make_ia1(interval_index, closed)
        perform_op(
            ia,
            method=method,
            function=piso_intervalarray.coverage,
            domain=domain,
            bins=True,
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
    "method",
    ["supplied", "accessor", "package"],
)
def test_coverage_exception3(interval_index, closed, method):
    domain = pd.IntervalIndex.from_tuples([(1, 3), (2, 4)])
    with pytest.raises(ValueError):
        ia = make_ia1(interval_index, closed)
        perform_op(
            ia,
            method=method,
            function=piso_intervalarray.coverage,
            domain=domain,
            bins=True,
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
    "method",
    ["supplied", "accessor", "package"],
)
def test_complement(interval_index, domain, expected_tuples, closed, method):
    if hasattr(domain, "set_closed"):
        domain = domain.set_closed(closed)
    ia = make_ia1(interval_index, closed)
    expected = make_ia_from_tuples(False, expected_tuples, closed)
    result = perform_op(
        ia,
        method=method,
        function=piso_intervalarray.complement,
        domain=domain,
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
    "x, closed, expected",
    [
        (0, "left", [[True], [False], [False]]),
        (0, "right", [[False], [False], [False]]),
        (0, "both", [[True], [False], [False]]),
        (0, "neither", [[False], [False], [False]]),
        (6, "left", [[False], [False], [False]]),
        (6, "right", [[False], [False], [True]]),
        (6, "neither", [[False], [False], [False]]),
        (6, "both", [[False], [False], [True]]),
        (
            [2, 4, 5],
            "left",
            [[True, False, False], [True, True, False], [False, True, True]],
        ),
        (
            [2, 4, 5],
            "right",
            [[True, True, False], [False, True, True], [False, True, True]],
        ),
        (
            [2, 4, 5],
            "both",
            [[True, True, False], [True, True, True], [False, True, True]],
        ),
        (
            [2, 4, 5],
            "neither",
            [[True, False, False], [False, True, False], [False, True, True]],
        ),
    ],
)
@pytest.mark.parametrize(
    "method",
    ["supplied", "accessor", "package"],
)
@pytest.mark.parametrize(
    "include_index",
    [True, False],
)
def test_contains(interval_index, x, closed, expected, method, include_index):
    ia = make_ia2(interval_index, closed)
    result = perform_op(
        ia,
        x,
        include_index,
        method=method,
        function=piso_intervalarray.contains,
    )
    if include_index:
        expected_result = pd.DataFrame(expected, index=ia, columns=np.array(x, ndmin=1))
        pd.testing.assert_frame_equal(result, expected_result, check_dtype=False)
    else:
        expected_result = np.array(expected)
        assert (result == expected_result).all()


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "x, closed, expected",
    [
        (0, "left", [[True], [False], [False]]),
        (0, "right", [[False], [False], [False]]),
        (0, "both", [[True], [False], [False]]),
        (0, "neither", [[False], [False], [False]]),
        (6, "left", [[False], [False], [False]]),
        (6, "right", [[False], [False], [True]]),
        (6, "neither", [[False], [False], [False]]),
        (6, "both", [[False], [False], [True]]),
        (
            [2, 4, 5],
            "left",
            [[True, False, False], [True, True, False], [False, True, True]],
        ),
        (
            [2, 4, 5],
            "right",
            [[True, True, False], [False, True, True], [False, True, True]],
        ),
        (
            [2, 4, 5],
            "both",
            [[True, True, False], [True, True, True], [False, True, True]],
        ),
        (
            [2, 4, 5],
            "neither",
            [[True, False, False], [False, True, False], [False, True, True]],
        ),
    ],
)
@pytest.mark.parametrize(
    "method",
    ["supplied", "accessor", "package"],
)
@pytest.mark.parametrize(
    "include_index",
    [True, False],
)
@pytest.mark.parametrize("result_type", ["points", "intervals"])
@pytest.mark.parametrize("how", ["any", "all"])
def test_contains_non_cartesian(
    interval_index, x, closed, expected, method, include_index, result_type, how
):
    ia = make_ia2(interval_index, closed)
    result = perform_op(
        ia,
        x,
        include_index,
        method=method,
        function=piso_intervalarray.contains,
        result=result_type,
        how=how,
    )
    axis = 0 if result_type == "points" else 1
    logical_func = np.all if how == "all" else np.any
    expected_result = logical_func(np.array(expected), axis=axis)
    if include_index:
        index = np.array(x, ndmin=1) if result_type == "points" else ia
        expected_result = pd.Series(expected_result, index=index)
        pd.testing.assert_series_equal(result, expected_result, check_dtype=False)
    else:
        assert (result == expected_result).all()


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "x, expected_tuples",
    [
        ([4], [(1, 4), (2, 4), (4, 5), (3, 4), (4, 6)]),
        ([3.5], [(1, 3.5), (3.5, 4), (2, 3.5), (3.5, 5), (3, 3.5), (3.5, 6)]),
        ([3, 4], [(1, 3), (3, 4), (2, 3), (3, 4), (4, 5), (3, 4), (4, 6)]),
        ([0, 3, 4, 7], [(1, 3), (3, 4), (2, 3), (3, 4), (4, 5), (3, 4), (4, 6)]),
        ([0], [(1, 4), (2, 5), (3, 6)]),
        ([4, 4], [(1, 4), (2, 4), (4, 5), (3, 4), (4, 6)]),
        ([4, 3], [(1, 3), (3, 4), (2, 3), (3, 4), (4, 5), (3, 4), (4, 6)]),
    ],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right", "both", "neither"],
)
@pytest.mark.parametrize(
    "method",
    ["supplied", "accessor", "package"],
)
@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
def test_split(interval_index, x, expected_tuples, closed, method, date_type):
    ia = make_ia4(interval_index, closed)
    ia = map_to_dates(ia, date_type)

    expected = make_ia_from_tuples(False, expected_tuples, closed)
    expected = map_to_dates(expected, date_type)
    x = map_to_dates(x, date_type)

    result = perform_op(
        ia,
        x,
        method=method,
        function=piso_intervalarray.split,
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
    "threshold, expected_tuples",
    [
        (1, [(0, 4), (7, 8), (10, 12)]),
        (2, [(0, 4), (7, 12)]),
        (3, [(0, 12)]),
    ],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "method",
    ["supplied", "accessor", "package"],
)
@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
def test_bridge(interval_index, threshold, expected_tuples, closed, method, date_type):
    ia = make_ia_from_tuples(interval_index, [(0, 4), (7, 8), (10, 12)], closed)
    ia = map_to_dates(ia, date_type)

    expected = make_ia_from_tuples(False, expected_tuples, closed)
    expected = map_to_dates(expected, date_type)
    if date_type is not None:
        threshold = map_to_dates([threshold + 1], "timedelta")[0]

    result = perform_op(
        ia,
        threshold,
        method=method,
        function=piso_intervalarray.bridge,
    )
    assert_interval_array_equal(
        result,
        expected,
        interval_index,
    )
