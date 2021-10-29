import numpy as np
import pandas as pd
import pytest

import piso


def make_ndframe(is_frame, closed, date_type):

    ia = pd.IntervalIndex.from_tuples([(1, 3), (5, 7)], closed=closed)
    if date_type:
        ia = map_to_dates(ia, date_type)
    df = pd.DataFrame(
        {"A": [4, 3], "B": ["x", "y"]},
        index=ia,
    )
    if is_frame:
        return df
    return df["A"]


def make_date(x, date_type):
    ts = pd.Timestamp(f"2021-10-{x}")
    if date_type == "numpy":
        return ts.to_numpy()
    if date_type == "datetime":
        return ts.to_pydatetime()
    if date_type == "timedelta":
        return ts - pd.Timestamp("2021-10-1")
    return ts


def map_to_dates(obj, date_type):
    if isinstance(obj, (pd.IntervalIndex, pd.arrays.IntervalArray)):
        return obj.from_arrays(
            [make_date(x, date_type) for x in obj.left],
            [make_date(x, date_type) for x in obj.right],
        )
    elif hasattr(obj, "__len__"):
        return [make_date(x, date_type) for x in obj]
    else:
        return make_date(obj, date_type)


@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "x, closed, a_col, b_col",
    [
        (4, "left", [np.nan], [np.nan]),
        (3, "right", [4], ["x"]),
        ([3, 4], "right", [4, np.nan], ["x", np.nan]),
        ([2, 4, 6, 8], "left", [4, np.nan, 3, np.nan], ["x", np.nan, "y", np.nan]),
    ],
)
def test_lookup_frame(x, closed, date_type, a_col, b_col):

    ndframe = make_ndframe(True, closed, date_type)
    points = map_to_dates(x, date_type) if date_type else x
    result = piso.lookup(ndframe, points)
    if not hasattr(points, "__len__"):
        points = [points]
    expected = pd.DataFrame({"A": a_col, "B": b_col}, index=points)
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "x, closed, a_col",
    [
        (4, "left", [np.nan]),
        (3, "right", [4]),
        ([3, 4], "right", [4, np.nan]),
        ([2, 4, 6, 8], "left", [4, np.nan, 3, np.nan]),
    ],
)
def test_lookup_series(x, closed, date_type, a_col):
    ndframe = make_ndframe(False, closed, date_type)
    points = map_to_dates(x, date_type) if date_type else x
    result = piso.lookup(ndframe, points)
    if not hasattr(points, "__len__"):
        points = [points]
    expected = pd.Series(a_col, index=points)
    pd.testing.assert_series_equal(result, expected, check_names=False)


def test_lookup_exception():
    df = pd.DataFrame([1, 2, 3])
    with pytest.raises(ValueError):
        piso.lookup(df, [1, 2])
