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


def make_ndframe2(is_frame, closed, date_type):

    ia = pd.IntervalIndex.from_tuples([(2, 4), (5, 6), (8, 9)], closed=closed)
    if date_type:
        ia = map_to_dates(ia, date_type)
    df = pd.DataFrame(
        {"C": [8, 7, 6], "D": [True, False, True]},
        index=ia,
    )
    if is_frame:
        return df
    return df["C"]


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


@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
def test_left_join_frame(closed, date_type):

    ndframe = make_ndframe(True, closed, date_type)
    ndframe2 = make_ndframe2(True, closed, date_type)

    index = pd.IntervalIndex.from_tuples([(1, 2), (2, 3), (5, 6), (6, 7)])
    if date_type:
        index = map_to_dates(index, date_type)

    result = piso.join(ndframe, ndframe2, how="left")
    expected = pd.DataFrame(
        {
            "A": [4, 4, 3, 3],
            "B": ["x", "x", "y", "y"],
            "C": [np.nan, 8, 7, np.nan],
            "D": [np.nan, True, False, np.nan],
        },
        index=index,
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
def test_right_join_frame(closed, date_type):

    ndframe = make_ndframe(True, closed, date_type)
    ndframe2 = make_ndframe2(True, closed, date_type)

    index = pd.IntervalIndex.from_tuples([(2, 3), (3, 4), (5, 6), (8, 9)])
    if date_type:
        index = map_to_dates(index, date_type)

    result = piso.join(ndframe, ndframe2, how="right")
    expected = pd.DataFrame(
        {
            "A": [4, np.nan, 3, np.nan],
            "B": ["x", np.nan, "y", np.nan],
            "C": [8, 8, 7, 6],
            "D": [True, True, False, True],
        },
        index=index,
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
def test_inner_join_frame(closed, date_type):

    ndframe = make_ndframe(True, closed, date_type)
    ndframe2 = make_ndframe2(True, closed, date_type)

    index = pd.IntervalIndex.from_tuples([(2, 3), (5, 6)])
    if date_type:
        index = map_to_dates(index, date_type)

    result = piso.join(ndframe, ndframe2, how="inner")
    expected = pd.DataFrame(
        {
            "A": [4, 3],
            "B": ["x", "y"],
            "C": [8, 7],
            "D": [True, False],
        },
        index=index,
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
def test_outer_join_frame(closed, date_type):

    ndframe = make_ndframe(True, closed, date_type)
    ndframe2 = make_ndframe2(True, closed, date_type)

    index = pd.IntervalIndex.from_tuples(
        [(1, 2), (2, 3), (3, 4), (5, 6), (6, 7), (8, 9)]
    )
    if date_type:
        index = map_to_dates(index, date_type)

    result = piso.join(ndframe, ndframe2, how="outer", sort=True)
    expected = pd.DataFrame(
        {
            "A": [4, 4, np.nan, 3, 3, np.nan],
            "B": ["x", "x", np.nan, "y", "y", np.nan],
            "C": [np.nan, 8, 8, 7, np.nan, 6],
            "D": [np.nan, True, True, False, np.nan, True],
        },
        index=index,
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "how",
    ["left", "right", "inner", "outer"],
)
def test_join_frame_lsuffix(closed, date_type, how):

    ndframe = make_ndframe(True, closed, date_type)

    index = pd.IntervalIndex.from_tuples([(1, 3), (5, 7)])
    if date_type:
        index = map_to_dates(index, date_type)

    result = piso.join(ndframe, ndframe, how=how, suffixes=["_1", ""])
    expected = pd.DataFrame(
        {
            "A_1": [4, 3],
            "B_1": ["x", "y"],
            "A": [4, 3],
            "B": ["x", "y"],
        },
        index=index,
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False, check_like=True)


@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "how",
    ["left", "right", "inner", "outer"],
)
def test_join_frame_rsuffix(closed, date_type, how):

    ndframe = make_ndframe(True, closed, date_type)

    index = pd.IntervalIndex.from_tuples([(1, 3), (5, 7)])
    if date_type:
        index = map_to_dates(index, date_type)

    result = piso.join(ndframe, ndframe, how=how, suffixes=["", "_1"])
    expected = pd.DataFrame(
        {
            "A_1": [4, 3],
            "B_1": ["x", "y"],
            "A": [4, 3],
            "B": ["x", "y"],
        },
        index=index,
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False, check_like=True)


# ------ joins with Series ----------------


@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
def test_left_join_series(closed, date_type):

    ndframe = make_ndframe(False, closed, date_type)
    ndframe2 = make_ndframe2(False, closed, date_type)

    index = pd.IntervalIndex.from_tuples([(1, 2), (2, 3), (5, 6), (6, 7)])
    if date_type:
        index = map_to_dates(index, date_type)

    result = piso.join(ndframe, ndframe2, how="left")
    expected = pd.DataFrame(
        {
            "A": [4, 4, 3, 3],
            "C": [np.nan, 8, 7, np.nan],
        },
        index=index,
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
def test_right_join_series(closed, date_type):

    ndframe = make_ndframe(False, closed, date_type)
    ndframe2 = make_ndframe2(False, closed, date_type)

    index = pd.IntervalIndex.from_tuples([(2, 3), (3, 4), (5, 6), (8, 9)])
    if date_type:
        index = map_to_dates(index, date_type)

    result = piso.join(ndframe, ndframe2, how="right")
    expected = pd.DataFrame(
        {
            "A": [4, np.nan, 3, np.nan],
            "C": [8, 8, 7, 6],
        },
        index=index,
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
def test_inner_join_series(closed, date_type):

    ndframe = make_ndframe(False, closed, date_type)
    ndframe2 = make_ndframe2(False, closed, date_type)

    index = pd.IntervalIndex.from_tuples([(2, 3), (5, 6)])
    if date_type:
        index = map_to_dates(index, date_type)

    result = piso.join(ndframe, ndframe2, how="inner")
    expected = pd.DataFrame(
        {
            "A": [4, 3],
            "C": [8, 7],
        },
        index=index,
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
def test_outer_join_series(closed, date_type):

    ndframe = make_ndframe(False, closed, date_type)
    ndframe2 = make_ndframe2(False, closed, date_type)

    index = pd.IntervalIndex.from_tuples(
        [(1, 2), (2, 3), (3, 4), (5, 6), (6, 7), (8, 9)]
    )
    if date_type:
        index = map_to_dates(index, date_type)

    result = piso.join(ndframe, ndframe2, how="outer", sort=True)
    expected = pd.DataFrame(
        {
            "A": [4, 4, np.nan, 3, 3, np.nan],
            "C": [np.nan, 8, 8, 7, np.nan, 6],
        },
        index=index,
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False)


@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "how",
    ["left", "right", "inner", "outer"],
)
def test_join_series_lsuffix(closed, date_type, how):

    ndframe = make_ndframe(False, closed, date_type)

    index = pd.IntervalIndex.from_tuples([(1, 3), (5, 7)])
    if date_type:
        index = map_to_dates(index, date_type)

    result = piso.join(ndframe, ndframe, how=how, suffixes=["_1", ""])
    expected = pd.DataFrame(
        {
            "A_1": [4, 3],
            "A": [4, 3],
        },
        index=index,
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False, check_like=True)


@pytest.mark.parametrize(
    "date_type",
    ["timestamp", "numpy", "datetime", "timedelta", None],
)
@pytest.mark.parametrize(
    "closed",
    ["left", "right"],
)
@pytest.mark.parametrize(
    "how",
    ["left", "right", "inner", "outer"],
)
def test_join_series_rsuffix(closed, date_type, how):

    ndframe = make_ndframe(False, closed, date_type)

    index = pd.IntervalIndex.from_tuples([(1, 3), (5, 7)])
    if date_type:
        index = map_to_dates(index, date_type)

    result = piso.join(ndframe, ndframe, how=how, suffixes=["", "_1"])
    expected = pd.DataFrame(
        {
            "A_1": [4, 3],
            "A": [4, 3],
        },
        index=index,
    )
    pd.testing.assert_frame_equal(result, expected, check_dtype=False, check_like=True)


# ---------- join exceptions ---------------------------------


def test_lookup_exception_1():
    df = pd.DataFrame([1, 2, 3])
    with pytest.raises(ValueError):
        piso.join(df, df)


def test_lookup_exception_2():
    df = pd.DataFrame([1, 2, 3])
    with pytest.raises(ValueError):
        piso.join(df, df, suffixes=[""])


def test_lookup_exception_3():
    df = pd.DataFrame([1, 2], pd.IntervalIndex.from_tuples([(1, 3), (2, 4)]))
    df2 = pd.DataFrame({"col": [1, 2]}, pd.IntervalIndex.from_tuples([(1, 2), (3, 4)]))
    with pytest.raises(ValueError):
        piso.join(df, df2)


def test_lookup_exception_4():
    df = pd.DataFrame({"col1": [1, 2]}, pd.IntervalIndex.from_tuples([(1, 2), (3, 4)]))
    with pytest.raises(ValueError):
        piso.join(df, df)


def test_lookup_exception_5():
    s = pd.Series([1, 2], pd.IntervalIndex.from_tuples([(1, 2), (3, 4)]), name="col")
    with pytest.raises(ValueError):
        piso.join(s, s)


def test_lookup_exception_6():
    df = pd.DataFrame({"col1": [1, 2]}, pd.IntervalIndex.from_tuples([(1, 2), (3, 4)]))
    s = pd.Series([1, 2], pd.IntervalIndex.from_tuples([(1, 2), (3, 4)]))
    with pytest.raises(ValueError):
        piso.join(df, s)


def test_lookup_exception_7():
    df = pd.DataFrame({"col1": [1, 2]}, pd.IntervalIndex.from_tuples([(1, 2), (3, 4)]))
    with pytest.raises(ValueError):
        piso.join(df)


def test_lookup_exception_8():
    df = pd.DataFrame(
        {"col1": [1, 2]}, pd.IntervalIndex.from_tuples([(1, 2), (3, 4)], closed="both")
    )
    df2 = pd.DataFrame(
        {"col2": [1, 2]}, pd.IntervalIndex.from_tuples([(1, 2), (3, 4)], closed="both")
    )
    with pytest.raises(ValueError):
        piso.join(df, df2)


def test_lookup_exception_9():
    df = pd.DataFrame(
        {"col1": [1, 2]}, pd.IntervalIndex.from_tuples([(1, 2), (3, 4)], closed="left")
    )
    df2 = pd.DataFrame(
        {"col2": [1, 2]}, pd.IntervalIndex.from_tuples([(1, 2), (3, 4)], closed="right")
    )
    with pytest.raises(ValueError):
        piso.join(df, df2)
