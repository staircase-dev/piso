import pandas as pd
import pytest

import piso.util


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

    return pd.arrays.IntervalArray.from_arrays(
        interval_array.left.map(make_date),
        interval_array.right.map(make_date),
    )


def make_interval_array(interval_index, closed, date_type):
    ia = pd.arrays.IntervalArray.from_tuples(
        [(2, 4), (5, 6), (7, 8), (10, 12)],
        closed=closed,
    )
    if date_type is not None:
        ia = map_to_dates(ia, date_type)
    if interval_index:
        ia = pd.IntervalIndex(ia)
    return ia


def assert_interval_array_equal(interval_array, expected, interval_index):
    if interval_index:
        pd.testing.assert_index_equal(
            interval_array,
            expected,
        )
    else:
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
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
def test_conversion(interval_index, closed, date_type):
    ia = make_interval_array(interval_index, closed, date_type)
    stairs = piso.util._interval_x_to_stairs(ia)
    klass = pd.IntervalIndex if interval_index else pd.arrays.IntervalArray
    ia2 = piso.util._boolean_stairs_to_interval_array(stairs, klass)
    print(ia)
    print(ia2)
    assert_interval_array_equal(
        ia,
        ia2,
        interval_index=interval_index,
    )
