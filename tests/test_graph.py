import numpy as np
import pandas as pd
import pytest

import piso
import piso.graph as piso_graph
from piso import register_accessors

register_accessors()


def get_accessor_method(self, function):
    return {
        piso_graph.adjacency_matrix: self.piso.adjacency_matrix,
    }[function]


def get_package_method(function):
    return {
        piso_graph.adjacency_matrix: piso.adjacency_matrix,
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


def map_to_dates(obj, date_type):
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
    "closed",
    ["left", "right", "neither"],
)
@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "include_index",
    [True, False],
)
@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_adjacency_matrix_intersects_1(
    closed, interval_index, include_index, date_type, how
):
    interval_array = pd.arrays.IntervalArray.from_tuples(
        [(0, 4), (3, 6), (5, 7), (8, 9), (9, 10)],
        closed=closed,
    )
    if interval_index:
        interval_array = pd.IntervalIndex(interval_array)

    if date_type:
        interval_array = map_to_dates(interval_array, date_type)

    expected = np.array(
        [
            [False, True, False, False, False],
            [True, False, True, False, False],
            [False, True, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False],
        ]
    )

    result = perform_op(
        interval_array,
        how=how,
        function=piso_graph.adjacency_matrix,
        edges="intersect",
        include_index=include_index,
    )
    if include_index:
        expected = pd.DataFrame(expected, columns=interval_array, index=interval_array)
        pd.testing.assert_frame_equal(result, expected)
    else:
        assert np.array_equal(result, expected)


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "include_index",
    [True, False],
)
@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_adjacency_matrix_intersects_2(interval_index, include_index, date_type, how):
    interval_array = pd.arrays.IntervalArray.from_tuples(
        [(0, 4), (3, 6), (5, 7), (8, 9), (9, 10)],
        closed="both",
    )
    if interval_index:
        interval_array = pd.IntervalIndex(interval_array)

    if date_type:
        interval_array = map_to_dates(interval_array, date_type)

    expected = np.array(
        [
            [False, True, False, False, False],
            [True, False, True, False, False],
            [False, True, False, False, False],
            [False, False, False, False, True],
            [False, False, False, True, False],
        ]
    )

    result = perform_op(
        interval_array,
        how=how,
        function=piso_graph.adjacency_matrix,
        edges="intersect",
        include_index=include_index,
    )
    if include_index:
        expected = pd.DataFrame(expected, columns=interval_array, index=interval_array)
        pd.testing.assert_frame_equal(result, expected)
    else:
        assert np.array_equal(result, expected)


@pytest.mark.parametrize(
    "closed",
    ["left", "right", "neither"],
)
@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "include_index",
    [True, False],
)
@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_adjacency_matrix_disjoint_1(
    closed, interval_index, include_index, date_type, how
):
    interval_array = pd.arrays.IntervalArray.from_tuples(
        [(0, 4), (3, 6), (5, 7), (8, 9), (9, 10)],
        closed=closed,
    )
    if interval_index:
        interval_array = pd.IntervalIndex(interval_array)

    if date_type:
        interval_array = map_to_dates(interval_array, date_type)

    expected = np.array(
        [
            [False, False, True, True, True],
            [False, False, False, True, True],
            [True, False, False, True, True],
            [True, True, True, False, True],
            [True, True, True, True, False],
        ]
    )

    result = perform_op(
        interval_array,
        how=how,
        function=piso_graph.adjacency_matrix,
        edges="disjoint",
        include_index=include_index,
    )
    if include_index:
        expected = pd.DataFrame(expected, columns=interval_array, index=interval_array)
        pd.testing.assert_frame_equal(result, expected)
    else:
        assert np.array_equal(result, expected)


@pytest.mark.parametrize(
    "interval_index",
    [True, False],
)
@pytest.mark.parametrize(
    "include_index",
    [True, False],
)
@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_adjacency_matrix_disjoint_2(interval_index, include_index, date_type, how):
    interval_array = pd.arrays.IntervalArray.from_tuples(
        [(0, 4), (3, 6), (5, 7), (8, 9), (9, 10)],
        closed="both",
    )
    if interval_index:
        interval_array = pd.IntervalIndex(interval_array)

    if date_type:
        interval_array = map_to_dates(interval_array, date_type)

    expected = np.array(
        [
            [False, False, True, True, True],
            [False, False, False, True, True],
            [True, False, False, True, True],
            [True, True, True, False, False],
            [True, True, True, False, False],
        ]
    )

    result = perform_op(
        interval_array,
        how=how,
        function=piso_graph.adjacency_matrix,
        edges="disjoint",
        include_index=include_index,
    )
    if include_index:
        expected = pd.DataFrame(expected, columns=interval_array, index=interval_array)
        pd.testing.assert_frame_equal(result, expected)
    else:
        assert np.array_equal(result, expected)


@pytest.mark.parametrize(
    "closed",
    ["left", "right", "both", "neither"],
)
@pytest.mark.parametrize(
    "how",
    ["supplied", "accessor", "package"],
)
def test_adjacency_matrix_edges_exception(closed, how):
    interval_array = pd.arrays.IntervalArray.from_tuples(
        [(0, 4), (3, 6), (5, 7), (8, 9), (9, 10)],
        closed=closed,
    )
    with pytest.raises(ValueError):
        perform_op(
            interval_array,
            how=how,
            function=piso_graph.adjacency_matrix,
            edges="not_an_option",
        )
