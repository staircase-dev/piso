lookup_docstring = """
Given a :class:`pandas.DataFrame`, or :class:`pandas.Series`, indexed by a `pandas.IntervalIndex`,
finds the intervals which contain each point in an array and returns the associated rows/elements.

Parameters
----------
frame_or_series : :class:`pandas.DataFrame` or :class:`pandas.Series`
    Must be indexed by a :class:`pandas.IntervalIndex` containing disjoint intervals
x : scalar, or array-like of scalars
    Values in *x* should belong to the same domain as the intervals in the interval index.

Returns
----------
:class:`pandas.DataFrame` or :class:`pandas.Series`
    Will be the same type as *frame_or_series*

Examples
-----------

>>> import pandas as pd
>>> import piso

>>> arr = pd.arrays.IntervalArray.from_tuples(
...     [(0, 4), (6, 8), (10, 12)],
... )
>>> df = pd.DataFrame({"A":[3, 2, 1],"B":["x", "y", "z"]}, index=arr)
>>> df
          A  B
(0, 4]    3  x
(6, 8]    2  y
(10, 12]  1  z

>>> piso.lookup(df, 1)
   A  B
1  3  x

>>> piso.lookup(df, [1, 6, 5, 12])
      A    B
1   3.0    x
6   NaN  NaN
5   NaN  NaN
12  1.0    z

>>> piso.lookup(df["A"], [1, 2, 6])
1     3.0
2     3.0
6     NaN
Name: A, dtype: float64
"""


join_docstring = """
Joins multiple dataframes or series by their :class:`pandas.IntervalIndex`.

Each interval in a :class:`pandas.IntervalIndex` is considered a set, and the interval index containing them a set defined by their union.
Join types are as follows:

- left: the set defined by the interval index of the result is the same as the set defined by the index of the first argument in *frames_or_series*

- right: the set defined by the interval index of the result is the same as the set defined by the index of the last argument in *frames_or_series*

- inner: the set defined by the interval index of the result is the intersection of sets defined by interval indexes from all join arguments

- outer: the set defined by the interval index of the result is the union of sets defined by interval indexes from all join arguments

Parameters
----------
*frames_or_series : argument list of :class:`pandas.DataFrame` or :class:`pandas.Series`
    May contain two or more arguments, all of which must be indexed by a
    :class:`pandas.IntervalIndex` containing disjoint intervals.  The index can have any *closed* value.
    Every :class:`pandas.Series` must have a name.
how : {"left", "right", "inner", "outer"}, default "left"
    What sort of join to perform.
suffixes : list of str or None, default None
    Suffixes to use for overlapping columns.  If used then should be same length as *frames_or_series*.
sort : bool, default False
    Order result DataFrame lexicographically by the join key. If False, the order of the join key depends on the join type.

Returns
----------
:class:`pandas.DataFrame`
    A dataframe containing columns from elements of *frames_or_series*

Examples
----------

>>> import pandas as pd
>>> import piso

>>> df = pd.DataFrame(
...     {"A":[4,3], "B":["x","y"]},
...     index=pd.IntervalIndex.from_tuples([(1,3), (5,7)]),
... )
>>> s = pd.Series(
...     [True, False],
...     index=pd.IntervalIndex.from_tuples([(2,4), (5,6)]),
...     name="C",
... )

>>> piso.join(df, s)
        A  B      C
(1, 2]  4  x    NaN
(2, 3]  4  x   True
(5, 6]  3  y  False
(6, 7]  3  y    NaN

>>> piso.join(df, s, how="right")
          A    B      C
(2, 3]  4.0    x   True
(3, 4]  NaN  NaN   True
(5, 6]  3.0    y  False

>>> piso.join(df, s, how="inner")
        A  B      C
(2, 3]  4  x   True
(5, 6]  3  y  False

>>> piso.join(df, s, how="outer")
          A    B      C
(1, 2]  4.0    x    NaN
(2, 3]  4.0    x   True
(5, 6]  3.0    y  False
(6, 7]  3.0    y    NaN
(3, 4]  NaN  NaN   True

>>> piso.join(df, s, how="outer", sort=True)
          A    B      C
(1, 2]  4.0    x    NaN
(2, 3]  4.0    x   True
(3, 4]  NaN  NaN   True
(5, 6]  3.0    y  False
(6, 7]  3.0    y    NaN

>>> piso.join(df, df, suffixes=["", "2"])
        A  B  A2 B2
(1, 3]  4  x   4  x
(5, 7]  3  y   3  y

>>> df2 = pd.DataFrame(
...     {"D":[1,2]},
...     index=pd.IntervalIndex.from_tuples([(1,2), (6,7)]),
... )

>>> piso.join(df, s, df2)
        A  B      C    D
(1, 2]  4  x    NaN  1.0
(2, 3]  4  x   True  NaN
(5, 6]  3  y  False  NaN
(6, 7]  3  y    NaN  2.0

>>> piso.join(df, s, df2, how="right")
        D  A  B    C
(1, 2]  1  4  x  NaN
(6, 7]  2  3  y  NaN
"""
