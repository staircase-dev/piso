import operator

import numpy as np
import pandas as pd
import pytest

import piso.interval as piso_interval
from piso._exceptions import ClosedMismatchError, ClosedValueError


def make_overlapping_intervals(closed):
    return [
        (pd.Interval(0, 3, closed=closed), pd.Interval(2, 4, closed=closed)),
        (pd.Interval(2, 4, closed=closed), pd.Interval(0, 3, closed=closed)),
        (pd.Interval(0, 4, closed=closed), pd.Interval(2, 3, closed=closed)),
        (pd.Interval(2, 3, closed=closed), pd.Interval(0, 4, closed=closed)),
    ]


def make_overlapping_intervals_equal_endpoint(closed):
    return [
        (pd.Interval(0, 3, closed=closed), pd.Interval(0, 4, closed=closed)),
        (pd.Interval(0, 4, closed=closed), pd.Interval(0, 3, closed=closed)),
        (pd.Interval(0, 4, closed=closed), pd.Interval(2, 4, closed=closed)),
        (pd.Interval(2, 4, closed=closed), pd.Interval(0, 4, closed=closed)),
        (pd.Interval(0, 4, closed=closed), pd.Interval(0, 4, closed=closed)),
    ]


def make_all_overlapping_intervals(closed):
    return make_overlapping_intervals(
        closed
    ) + make_overlapping_intervals_equal_endpoint(closed)


def make_adjacent_intervals(closed):
    return (pd.Interval(0, 3, closed=closed), pd.Interval(3, 4, closed=closed))


def make_disjoint_intervals(closed):
    return (pd.Interval(0, 2, closed=closed), pd.Interval(3, 5, closed=closed))


@pytest.mark.parametrize(
    "intervals",
    make_all_overlapping_intervals("left"),
)
def test_union_of_overlapping_closed_left(intervals):
    result = piso_interval.union(*intervals, squeeze=True)
    assert result == pd.Interval(0, 4, closed="left")


@pytest.mark.parametrize(
    "intervals",
    make_all_overlapping_intervals("right"),
)
def test_union_of_overlapping_closed_right(intervals):
    result = piso_interval.union(*intervals, squeeze=True)
    assert result == pd.Interval(0, 4, closed="right")


@pytest.mark.parametrize(
    "intervals",
    make_all_overlapping_intervals("left") + make_all_overlapping_intervals("right"),
)
@pytest.mark.parametrize(
    "squeeze",
    [True, False],
)
def test_union_of_overlapping_return_type(intervals, squeeze):
    result = piso_interval.union(*intervals, squeeze)
    expected_type = pd.Interval if squeeze else pd.arrays.IntervalArray
    assert isinstance(result, expected_type)


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
def test_union_of_adjacent(closed):
    intervals = make_adjacent_intervals(closed)
    result = piso_interval.union(*intervals, squeeze=True)
    assert result == pd.Interval(0, 4, closed=closed)


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "squeeze",
    [True, False],
)
def test_union_of_adjacent_return_type(closed, squeeze):
    intervals = make_adjacent_intervals(closed)
    result = piso_interval.union(*intervals, squeeze)
    expected_type = pd.Interval if squeeze else pd.arrays.IntervalArray
    assert isinstance(result, expected_type)


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "squeeze",
    [True, False],
)
def test_union_of_disjoint(closed, squeeze):
    intervals = make_disjoint_intervals(closed)
    result = piso_interval.union(*intervals, squeeze)
    pd._testing.assert_interval_array_equal(
        result,
        pd.arrays.IntervalArray.from_tuples([(0, 2), (3, 5)], closed=closed),
        exact=False,
    )


@pytest.mark.parametrize(
    "closed_values",
    [
        ("left", "right"),
        ("right", "left"),
    ],
)
def test_union_closed_mismatch(closed_values):
    intervals = (
        pd.Interval(0, 3, closed=closed_values[0]),
        pd.Interval(2, 4, closed=closed_values[1]),
    )
    with pytest.raises(ClosedMismatchError):
        piso_interval.union(*intervals)


@pytest.mark.parametrize(
    "closed_values",
    [
        ("neither", "neither"),
        ("both", "both"),
    ],
)
def test_union_closed_value_error(closed_values):
    intervals = (
        pd.Interval(0, 3, closed=closed_values[0]),
        pd.Interval(2, 4, closed=closed_values[1]),
    )
    with pytest.raises(ClosedValueError):
        piso_interval.union(*intervals)


# intersection ------------------------


@pytest.mark.parametrize(
    "intervals",
    make_overlapping_intervals("left"),
)
def test_intersection_of_overlapping_closed_left(intervals):
    result = piso_interval.intersection(*intervals, squeeze=True)
    assert result == pd.Interval(2, 3, closed="left")


@pytest.mark.parametrize(
    "intervals",
    make_overlapping_intervals("right"),
)
def test_intersection_of_overlapping_closed_right(intervals):
    result = piso_interval.intersection(*intervals, squeeze=True)
    assert result == pd.Interval(2, 3, closed="right")


@pytest.mark.parametrize(
    "intervals, expected",
    zip(
        make_overlapping_intervals_equal_endpoint("left"),
        [
            pd.Interval(0, 3, closed="left"),
            pd.Interval(0, 3, closed="left"),
            pd.Interval(2, 4, closed="left"),
            pd.Interval(2, 4, closed="left"),
            pd.Interval(0, 4, closed="left"),
        ],
    ),
)
def test_intersection_of_overlapping_equal_endpoint_closed_left(intervals, expected):
    result = piso_interval.intersection(*intervals, squeeze=True)
    assert result == expected


@pytest.mark.parametrize(
    "intervals, expected",
    zip(
        make_overlapping_intervals_equal_endpoint("right"),
        [
            pd.Interval(0, 3, closed="right"),
            pd.Interval(0, 3, closed="right"),
            pd.Interval(2, 4, closed="right"),
            pd.Interval(2, 4, closed="right"),
            pd.Interval(0, 4, closed="right"),
        ],
    ),
)
def test_intersection_of_overlapping_equal_endpoint_closed_right(intervals, expected):
    result = piso_interval.intersection(*intervals, squeeze=True)
    assert result == expected


@pytest.mark.parametrize(
    "intervals",
    make_all_overlapping_intervals("left") + make_all_overlapping_intervals("right"),
)
@pytest.mark.parametrize(
    "squeeze",
    [True, False],
)
def test_intersection_of_overlapping_return_type(intervals, squeeze):
    result = piso_interval.intersection(*intervals, squeeze)
    expected_type = pd.Interval if squeeze else pd.arrays.IntervalArray
    assert isinstance(result, expected_type)


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "squeeze",
    [True, False],
)
def test_intersection_of_adjacent(closed, squeeze):
    intervals = make_adjacent_intervals(closed)
    result = piso_interval.intersection(*intervals, squeeze)
    pd._testing.assert_interval_array_equal(
        result,
        pd.arrays.IntervalArray([], closed=closed),
        exact=False,
    )


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "squeeze",
    [True, False],
)
def test_intersection_of_disjoint(closed, squeeze):
    intervals = make_disjoint_intervals(closed)
    result = piso_interval.intersection(*intervals, squeeze)
    pd._testing.assert_interval_array_equal(
        result,
        pd.arrays.IntervalArray([], closed=closed),
        exact=False,
    )


@pytest.mark.parametrize(
    "closed_values",
    [
        ("left", "right"),
        ("right", "left"),
    ],
)
def test_intersection_closed_mismatch(closed_values):
    intervals = (
        pd.Interval(0, 3, closed=closed_values[0]),
        pd.Interval(2, 4, closed=closed_values[1]),
    )
    with pytest.raises(ClosedMismatchError):
        piso_interval.intersection(*intervals)


@pytest.mark.parametrize(
    "closed_values",
    [
        ("neither", "neither"),
        ("both", "both"),
    ],
)
def test_intersection_closed_value_error(closed_values):
    intervals = (
        pd.Interval(0, 3, closed=closed_values[0]),
        pd.Interval(2, 4, closed=closed_values[1]),
    )
    with pytest.raises(ClosedValueError):
        piso_interval.intersection(*intervals)


# difference ------------------------


@pytest.mark.parametrize(
    "intervals, expected",
    zip(
        make_overlapping_intervals("left") + make_overlapping_intervals("right"),
        [
            pd.arrays.IntervalArray([pd.Interval(0, 2, closed="left")]),
            pd.arrays.IntervalArray([pd.Interval(3, 4, closed="left")]),
            pd.arrays.IntervalArray(
                [pd.Interval(0, 2, closed="left"), pd.Interval(3, 4, closed="left")]
            ),
            pd.arrays.IntervalArray([], closed="left"),
            pd.arrays.IntervalArray([pd.Interval(0, 2, closed="right")]),
            pd.arrays.IntervalArray([pd.Interval(3, 4, closed="right")]),
            pd.arrays.IntervalArray(
                [pd.Interval(0, 2, closed="right"), pd.Interval(3, 4, closed="right")]
            ),
            pd.arrays.IntervalArray([], closed="right"),
        ],
    ),
)
def test_difference_of_overlapping(intervals, expected):
    result = piso_interval.difference(*intervals, squeeze=False)
    pd._testing.assert_interval_array_equal(
        result,
        expected,
        exact=False,
    )


@pytest.mark.parametrize(
    "intervals, expected",
    zip(
        make_overlapping_intervals_equal_endpoint("left")
        + make_overlapping_intervals_equal_endpoint("right"),
        [
            pd.arrays.IntervalArray([], closed="left"),
            pd.arrays.IntervalArray([pd.Interval(3, 4)], closed="left"),
            pd.arrays.IntervalArray([pd.Interval(0, 2)], closed="left"),
            pd.arrays.IntervalArray([], closed="left"),
            pd.arrays.IntervalArray([], closed="left"),
            pd.arrays.IntervalArray([], closed="right"),
            pd.arrays.IntervalArray([pd.Interval(3, 4)], closed="right"),
            pd.arrays.IntervalArray([pd.Interval(0, 2)], closed="right"),
            pd.arrays.IntervalArray([], closed="right"),
            pd.arrays.IntervalArray([], closed="right"),
        ],
    ),
)
def test_difference_of_overlapping_equal_endpoint(intervals, expected):
    result = piso_interval.difference(*intervals, squeeze=False)
    pd._testing.assert_interval_array_equal(
        result,
        expected,
        exact=False,
    )


@pytest.mark.parametrize(
    "intervals, single_interval",
    zip(
        make_all_overlapping_intervals("left")
        + make_all_overlapping_intervals("right"),
        [
            True,
            True,
            False,
            False,
            False,
            True,
            True,
            False,
            False,
            True,
            True,
            False,
            False,
            False,
            True,
            True,
            False,
            False,
        ],
    ),
)
@pytest.mark.parametrize(
    "squeeze",
    [True, False],
)
def test_difference_of_overlapping_return_type(intervals, single_interval, squeeze):
    result = piso_interval.difference(*intervals, squeeze)
    if squeeze and single_interval:
        expected_type = pd.Interval
    else:
        expected_type = pd.arrays.IntervalArray
    assert isinstance(result, expected_type)


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
def test_difference_of_adjacent(closed):
    intervals = make_adjacent_intervals(closed)
    result = piso_interval.difference(*intervals, squeeze=True)
    assert result == intervals[0]


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "squeeze",
    [True, False],
)
def test_difference_of_adjacent_return_type(closed, squeeze):
    intervals = make_adjacent_intervals(closed)
    result = piso_interval.difference(*intervals, squeeze)
    expected_type = pd.Interval if squeeze else pd.arrays.IntervalArray
    assert isinstance(result, expected_type)


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
def test_difference_of_disjoint(closed):
    intervals = make_disjoint_intervals(closed)
    result = piso_interval.difference(*intervals, squeeze=True)
    assert result == intervals[0]


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "squeeze",
    [True, False],
)
def test_difference_of_disjoint_return_type(closed, squeeze):
    intervals = make_disjoint_intervals(closed)
    result = piso_interval.difference(*intervals, squeeze)
    expected_type = pd.Interval if squeeze else pd.arrays.IntervalArray
    assert isinstance(result, expected_type)


@pytest.mark.parametrize(
    "closed_values",
    [
        ("left", "right"),
        ("right", "left"),
    ],
)
def test_difference_closed_mismatch(closed_values):
    intervals = (
        pd.Interval(0, 3, closed=closed_values[0]),
        pd.Interval(2, 4, closed=closed_values[1]),
    )
    with pytest.raises(ClosedMismatchError):
        piso_interval.difference(*intervals)


@pytest.mark.parametrize(
    "closed_values",
    [
        ("neither", "neither"),
        ("both", "both"),
    ],
)
def test_difference_closed_value_error(closed_values):
    intervals = (
        pd.Interval(0, 3, closed=closed_values[0]),
        pd.Interval(2, 4, closed=closed_values[1]),
    )
    with pytest.raises(ClosedValueError):
        piso_interval.difference(*intervals)


# symmetric_difference -----------------------------------------------


@pytest.mark.parametrize(
    "squeeze",
    [True, False],
)
@pytest.mark.parametrize(
    "intervals",
    make_overlapping_intervals("left"),
)
def test_symmetric_difference_of_overlapping_closed_left(intervals, squeeze):
    result = piso_interval.symmetric_difference(*intervals, squeeze)
    pd._testing.assert_interval_array_equal(
        result,
        pd.arrays.IntervalArray([pd.Interval(0, 2), pd.Interval(3, 4)], closed="left"),
        exact=False,
    )


@pytest.mark.parametrize(
    "squeeze",
    [True, False],
)
@pytest.mark.parametrize(
    "intervals",
    make_overlapping_intervals("right"),
)
def test_symmetric_difference_of_overlapping_closed_right(intervals, squeeze):
    result = piso_interval.symmetric_difference(*intervals, squeeze)
    pd._testing.assert_interval_array_equal(
        result,
        pd.arrays.IntervalArray([pd.Interval(0, 2), pd.Interval(3, 4)], closed="right"),
        exact=False,
    )


@pytest.mark.parametrize(
    "intervals, expected",
    zip(
        make_overlapping_intervals_equal_endpoint("left"),
        [
            pd.arrays.IntervalArray([pd.Interval(3, 4)], closed="left"),
            pd.arrays.IntervalArray([pd.Interval(3, 4)], closed="left"),
            pd.arrays.IntervalArray([pd.Interval(0, 2)], closed="left"),
            pd.arrays.IntervalArray([pd.Interval(0, 2)], closed="left"),
            pd.arrays.IntervalArray([], closed="left"),
        ],
    ),
)
def test_symmetric_difference_of_overlapping_equal_endpoint_closed_left(
    intervals, expected
):
    result = piso_interval.symmetric_difference(*intervals, squeeze=False)
    pd._testing.assert_interval_array_equal(
        result,
        expected,
        exact=False,
    )


@pytest.mark.parametrize(
    "intervals, expected",
    zip(
        make_overlapping_intervals_equal_endpoint("right"),
        [
            pd.arrays.IntervalArray([pd.Interval(3, 4)], closed="right"),
            pd.arrays.IntervalArray([pd.Interval(3, 4)], closed="right"),
            pd.arrays.IntervalArray([pd.Interval(0, 2)], closed="right"),
            pd.arrays.IntervalArray([pd.Interval(0, 2)], closed="right"),
            pd.arrays.IntervalArray([], closed="right"),
        ],
    ),
)
def test_symmetric_difference_of_overlapping_equal_endpoint_closed_right(
    intervals, expected
):
    result = piso_interval.symmetric_difference(*intervals, squeeze=False)
    pd._testing.assert_interval_array_equal(
        result,
        expected,
        exact=False,
    )


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
def test_symmetric_difference_of_adjacent(closed):
    intervals = make_adjacent_intervals(closed)
    result = piso_interval.symmetric_difference(*intervals, squeeze=True)
    assert result == pd.Interval(0, 4, closed=closed)


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "squeeze",
    [True, False],
)
def test_symmetric_difference_of_adjacent_return_type(closed, squeeze):
    intervals = make_adjacent_intervals(closed)
    result = piso_interval.symmetric_difference(*intervals, squeeze)
    expected_type = pd.Interval if squeeze else pd.arrays.IntervalArray
    assert isinstance(result, expected_type)


@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "squeeze",
    [True, False],
)
def test_symmetric_difference_of_disjoint(closed, squeeze):
    intervals = make_disjoint_intervals(closed)
    result = piso_interval.symmetric_difference(*intervals, squeeze)
    pd._testing.assert_interval_array_equal(
        result,
        pd.arrays.IntervalArray(intervals),
        exact=False,
    )


@pytest.mark.parametrize(
    "closed_values",
    [
        ("left", "right"),
        ("right", "left"),
    ],
)
def test_symmetric_difference_closed_mismatch(closed_values):
    intervals = (
        pd.Interval(0, 3, closed=closed_values[0]),
        pd.Interval(2, 4, closed=closed_values[1]),
    )
    with pytest.raises(ClosedMismatchError):
        piso_interval.symmetric_difference(*intervals)


@pytest.mark.parametrize(
    "closed_values",
    [
        ("neither", "neither"),
        ("both", "both"),
    ],
)
def test_symmetric_difference_closed_value_error(closed_values):
    intervals = (
        pd.Interval(0, 3, closed=closed_values[0]),
        pd.Interval(2, 4, closed=closed_values[1]),
    )
    with pytest.raises(ClosedValueError):
        piso_interval.symmetric_difference(*intervals)


@pytest.mark.parametrize(
    "tuples, squeeze, expected",
    [
        ([(1, 2), (1, 2)], True, True),
        ([(1, 3), (0, 2)], True, False),
        ([(1, 3), (1, 2), (0, 1)], True, np.array([True, False])),
        ([(1, 2), (1, 2)], False, np.array([True])),
        ([(1, 3), (0, 2)], False, np.array([False])),
        ([(1, 3), (1, 2), (0, 1)], False, np.array([True, False])),
    ],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
def test_issuperset(tuples, squeeze, expected, closed):
    intervals = [pd.Interval(*i, closed=closed) for i in tuples]
    result = piso_interval.issuperset(*intervals, squeeze=squeeze)
    equal_op = np.array_equal if isinstance(expected, np.ndarray) else operator.eq
    assert equal_op(result, expected)


@pytest.mark.parametrize(
    "tuples, squeeze, expected",
    [
        ([(1, 2), (1, 2)], True, True),
        ([(1, 3), (0, 2)], True, False),
        ([(1, 3), (1, 4), (0, 1)], True, np.array([True, False])),
        ([(1, 2), (1, 2)], False, np.array([True])),
        ([(1, 3), (0, 2)], False, np.array([False])),
        ([(1, 3), (1, 4), (0, 1)], False, np.array([True, False])),
    ],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
def test_issubset(tuples, squeeze, expected, closed):
    intervals = [pd.Interval(*i, closed=closed) for i in tuples]
    result = piso_interval.issubset(*intervals, squeeze=squeeze)
    equal_op = np.array_equal if isinstance(expected, np.ndarray) else operator.eq
    assert equal_op(result, expected)
