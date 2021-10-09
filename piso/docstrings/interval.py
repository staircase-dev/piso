union_examples = """
Examples
-----------

>>> import pandas as pd
>>> import piso.interval

>>> piso.interval.union(
...    pd.Interval(0, 3),
...    pd.Interval(2, 4),
... )
Interval(0.0, 4.0, closed='right')

>>> piso.interval.union(
...    pd.Interval(0, 3),
...    pd.Interval(2, 4),
...    squeeze=False,
... )
<IntervalArray>
[(0.0, 4.0]]
Length: 1, closed: right, dtype: interval[float64]

>>> piso.interval.union(
...    pd.Interval(0, 3, closed="left"),
...    pd.Interval(2, 4, closed="left"),
... )
Interval(0.0, 4.0, closed='left')

>>> piso.interval.union(
...    pd.Interval(0, 1),
...    pd.Interval(3, 4),
... )
<IntervalArray>
[(0.0, 1.0], (3.0, 4.0]]
Length: 2, closed: right, dtype: interval[float64]
"""

intersection_examples = """
Examples
-----------

>>> import pandas as pd
>>> import piso.interval

>>> piso.interval.intersection(
...    pd.Interval(0, 3),
...    pd.Interval(2, 4),
... )
Interval(2.0, 3.0, closed='right')

>>> piso.interval.intersection(
...    pd.Interval(0, 3),
...    pd.Interval(2, 4),
...    squeeze=False,
... )
<IntervalArray>
[(2.0, 3.0]]
Length: 1, closed: right, dtype: interval[float64]

>>> piso.interval.intersection(
...    pd.Interval(0, 3, closed="left"),
...    pd.Interval(2, 4, closed="left"),
... )
Interval(2.0, 3.0, closed='left')

>>> piso.interval.intersection(
...    pd.Interval(0, 1),
...    pd.Interval(3, 4),
... )
<IntervalArray>
[]
Length: 0, closed: right, dtype: interval[int64]
"""

difference_examples = """
Examples
-----------

>>> import pandas as pd
>>> import piso.interval

>>> piso.interval.difference(
...    pd.Interval(0, 3),
...    pd.Interval(2, 4),
... )
Interval(0.0, 2.0, closed='right')

>>> piso.interval.difference(
...    pd.Interval(0, 3),
...    pd.Interval(2, 4),
...    squeeze=False,
... )
<IntervalArray>
[(0.0, 2.0]]
Length: 1, closed: right, dtype: interval[float64]

>>> piso.interval.difference(
...    pd.Interval(0, 4, closed="left"),
...    pd.Interval(2, 3, closed="left"),
... )
<IntervalArray>
[[0.0, 2.0), [3.0, 4.0)]
Length: 2, closed: left, dtype: interval[float64]

>>> piso.interval.difference(
...    pd.Interval(2, 3),
...    pd.Interval(0, 4),
... )
<IntervalArray>
[]
Length: 0, closed: right, dtype: interval[int64]
"""


symmetric_difference_examples = """
Examples
-----------

>>> import pandas as pd
>>> import piso.interval

>>> piso.interval.symmetric_difference(
...    pd.Interval(0, 3),
...    pd.Interval(2, 4),
... )
<IntervalArray>
[(0.0, 2.0], (3.0, 4.0]]
Length: 2, closed: right, dtype: interval[float64]

>>> piso.interval.symmetric_difference(
...    pd.Interval(0, 3),
...    pd.Interval(2, 3),
... )
Interval(0.0, 2.0, closed='right')

>>> piso.interval.symmetric_difference(
...    pd.Interval(0, 3, closed="left"),
...    pd.Interval(2, 4, closed="left"),
... )
<IntervalArray>
[[0.0, 2.0), [3.0, 4.0)]
Length: 2, closed: left, dtype: interval[float64]

>>> piso.interval.symmetric_difference(
...    pd.Interval(2, 3),
...    pd.Interval(0, 4),
... )
<IntervalArray>
[(0.0, 2.0], (3.0, 4.0]]
Length: 2, closed: right, dtype: interval[float64]
"""

template_doc = """
Performs the {operation} of two pandas.Intervals

Parameters
----------
interval1 : pandas.Interval
    the first operand
interval2 : pandas.Interval
    the second operand
squeeze : boolean, default True
    If True, will try to coerce the return value to a pandas.Interval

Returns
----------
:class:`pandas.Interval` or :class:`pandas.arrays.IntervalArray`

{examples}
"""

union_docstring = template_doc.format(operation="union", examples=union_examples)
intersection_docstring = template_doc.format(
    operation="intersection", examples=intersection_examples
)
difference_docstring = template_doc.format(
    operation="set difference", examples=difference_examples
)
symmetric_difference_docstring = template_doc.format(
    operation="symmetric difference", examples=symmetric_difference_examples
)
