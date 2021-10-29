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
