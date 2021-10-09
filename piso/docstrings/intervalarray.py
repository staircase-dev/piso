union_examples = """
Examples
-----------

>>> import pandas as pd
>>> import piso


Examples with *interval_arrays* empty:

>>> arr = pd.arrays.IntervalArray.from_tuples(
...     [(0, 4), (2, 5), (3, 6), (7, 8), (8, 9), (10, 12)],
... )

>>> piso.union(arr)
<IntervalArray>
[(0.0, 6.0], (7.0, 9.0], (10.0, 12.0]]
Length: 3, closed: right, dtype: interval[float64]

>>> piso.union(arr.set_closed("left"))
<IntervalArray>
[[0, 4), [2, 5), [3, 6), [7, 8), [8, 9), [10, 12)]
Length: 6, closed: left, dtype: interval[int64]

>>> piso.union(pd.IntervalIndex(arr))
IntervalIndex([(0.0, 6.0], (7.0, 9.0], (10.0, 12.0]],
              closed='right',
              dtype='interval[float64]')

>>> piso.union(arr, return_type=pd.IntervalIndex)
IntervalIndex([(0.0, 6.0], (7.0, 9.0], (10.0, 12.0]],
              closed='right',
              dtype='interval[float64]')


Examples with *interval_arrays* non empty:

>>> arr1 = pd.arrays.IntervalArray.from_tuples(
...     [(0, 4), (5, 6), (7, 8), (10, 12)],
... )
>>> arr2 = pd.arrays.IntervalArray.from_tuples(
...     [(3, 5), (8, 9)],
... )
>>> arr3 = pd.arrays.IntervalArray.from_tuples(
...     [(6, 8), (9, 11)],
... )

>>> piso.union(arr1, arr2)
<IntervalArray>
[(0.0, 6.0], (7.0, 9.0], (10.0, 12.0]]
Length: 3, closed: right, dtype: interval[float64]

>>> piso.union(arr2, arr3, return_type=pd.IntervalIndex)
IntervalIndex([(3.0, 5.0], (6.0, 11.0]],
              closed='right',
              dtype='interval[float64]')

>>> piso.union(arr1, arr2, arr3)
<IntervalArray>
[(0.0, 12.0]]
Length: 1, closed: right, dtype: interval[float64]

>>> piso.union(arr1, arr2, arr3, squeeze=True)
Interval(0.0, 12.0, closed='right')
"""

intersection_examples = """
Examples
-----------

>>> import pandas as pd
>>> import piso

Examples with *interval_arrays* empty:

>>> arr = pd.arrays.IntervalArray.from_tuples(
...     [(0, 4), (2, 5), (3, 6)],
... )

>>> piso.intersection(arr)
<IntervalArray>
[(3.0, 4.0]]
Length: 1, closed: right, dtype: interval[float64]

>>> piso.intersection(pd.IntervalIndex(arr))
IntervalIndex([(3.0, 4.0]],
              closed='right',
              dtype='interval[float64]')

>>> piso.intersection(arr, return_type=pd.IntervalIndex)
IntervalIndex([(3.0, 4.0]],
              closed='right',
              dtype='interval[float64]')

>>> piso.intersection(arr)
<IntervalArray>
[]
Length: 0, closed: right, dtype: interval[int64]

>>> piso.intersection(arr, min_overlaps=2)
<IntervalArray>
[(2.0, 5.0]]
Length: 1, closed: right, dtype: interval[float64]

Examples with *interval_arrays* not empty:

>>> arr1 = pd.arrays.IntervalArray.from_tuples(
...     [(0, 4), (5, 6), (7, 8), (10, 12)],
... )
>>> arr2 = pd.arrays.IntervalArray.from_tuples(
...     [(3, 5), (8, 9)],
... )
>>> arr3 = pd.arrays.IntervalArray.from_tuples(
...     [(6, 8), (9, 11)],
... )

>>> piso.intersection(arr1, arr2)
<IntervalArray>
[(3.0, 4.0]]
Length: 1, closed: right, dtype: interval[float64]

>>> piso.intersection(arr1, arr2, squeeze=True)
Interval(3.0, 4.0, closed='right')

>>> piso.intersection(arr1, arr2, arr3)
<IntervalArray>
[]
Length: 0, closed: right, dtype: interval[float64]

>>> piso.intersection(arr1, arr2, arr3, min_overlaps=2)
<IntervalArray>
[(3.0, 4.0], (10.0, 11.0]]
Length: 2, closed: right, dtype: interval[float64]
"""

difference_examples = """
Examples
-----------

>>> import pandas as pd
>>> import piso

>>> arr1 = pd.arrays.IntervalArray.from_tuples(
...     [(0, 4), (2, 5), (3, 6), (7, 8), (8, 9), (10, 12)],
... )
>>> arr2 = pd.arrays.IntervalArray.from_tuples(
...     [(4, 7), (8, 11)],
... )
>>> arr3 = pd.arrays.IntervalArray.from_tuples(
...     [(2, 5), (7, 13)],
... )

>>> piso.difference(arr1, arr2)
<IntervalArray>
[(0.0, 4.0], (7.0, 8.0], (11.0, 12.0]]
Length: 3, closed: right, dtype: interval[float64]

>>> piso.difference(arr1.set_closed("left"), arr2.set_closed("left"))
<IntervalArray>
[[0.0, 4.0), [7.0, 8.0), [11.0, 12.0)]
Length: 3, closed: left, dtype: interval[float64]

>>> piso.difference(arr1, arr2, return_type=pd.IntervalIndex)
IntervalIndex([(0.0, 4.0], (7.0, 8.0], (11.0, 12.0]],
              closed='right',
              dtype='interval[float64]')

>>> piso.difference(arr1, arr2, arr3)
<IntervalArray>
[(0.0, 2.0]]
Length: 1, closed: right, dtype: interval[float64]

>>> piso.difference(arr1, arr2, arr3, squeeze=True)
Interval(0.0, 2.0, closed='right')
"""

symmetric_difference_examples = """
Examples
-----------

>>> import pandas as pd
>>> import piso

Examples with *interval_arrays* empty:

>>> arr = pd.arrays.IntervalArray.from_tuples(
...     [(0, 4), (2, 5), (3, 6), (7, 8), (8, 9), (10, 12)],
... )

>>> piso.symmetric_difference(arr)
<IntervalArray>
[(0.0, 2.0], (5.0, 6.0], (7.0, 9.0], (10.0, 12.0]]
Length: 4, closed: right, dtype: interval[float64]

>>> piso.symmetric_difference(pd.IntervalIndex(arr))
IntervalIndex([(0.0, 2.0], (5.0, 6.0], (7.0, 9.0], (10.0, 12.0]],
              closed='right',
              dtype='interval[float64]')

>>> piso.symmetric_difference(arr, return_type=pd.IntervalIndex)
IntervalIndex([(0.0, 2.0], (5.0, 6.0], (7.0, 9.0], (10.0, 12.0]],
              closed='right',
              dtype='interval[float64]')

>>> piso.symmetric_difference(arr, min_overlaps=3)
<IntervalArray>
[(0.0, 3.0], (4.0, 6.0], (7.0, 9.0], (10.0, 12.0]]
Length: 4, closed: right, dtype: interval[float64]

>>> piso.symmetric_difference(arr, min_overlaps="all")
<IntervalArray>
[(0.0, 6.0], (7.0, 9.0], (10.0, 12.0]]
Length: 3, closed: right, dtype: interval[float64]

Examples with *interval_arrays* non-empty:

>>> arr1 = pd.arrays.IntervalArray.from_tuples(
...     [(0, 4), (5, 6), (7, 8), (10, 12)],
... )
>>> arr2 = pd.arrays.IntervalArray.from_tuples(
...     [(3, 5), (8, 9)],
... )
>>> arr3 = pd.arrays.IntervalArray.from_tuples(
...     [(6, 8), (9, 11)],
... )

>>> piso.symmetric_difference(arr1, arr2)
<IntervalArray>
[(0.0, 3.0], (4.0, 6.0], (7.0, 9.0], (10.0, 12.0]]
Length: 4, closed: right, dtype: interval[float64]

>>> piso.symmetric_difference(arr1, arr2, arr3)
<IntervalArray>
[(0.0, 3.0], (4.0, 7.0], (8.0, 10.0], (11.0, 12.0]]
Length: 4, closed: right, dtype: interval[float64]

>>> piso.symmetric_difference(arr1, arr2, arr3, min_overlaps="all")
<IntervalArray>
[(0.0, 12.0]]
Length: 1, closed: right, dtype: interval[float64]
"""


def join_params(list_of_param_strings):
    return "".join(list_of_param_strings).replace("\n\n", "\n")


param_interval_array = """
interval_array : :class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`
    The first (and possibly only) operand to the {operation} operation.
"""

param_optional_args = """
*interval_arrays : argument list of :class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`
    May contain zero or more arguments.
"""

param_optional_args_difference = """
*interval_arrays : argument list of :class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`
    Must contain at least one argument.
"""

param_min_overlaps = """
min_overlaps : int or "all", default "all"
    Specifies the minimum number of intervals which overlap in order to define an *intersection*.
    If *min_overlaps* is an int then it must be no smaller than 2.  If *min_overlaps* is all then
    an intersection is only defined where every interval overlaps.
    If supplied, must be done so as a keyword argument.
"""

param_squeeze = """
squeeze : boolean, default True
    If True, will try to coerce the return value to a pandas.Interval.
    If supplied, must be done so as a keyword argument.
"""

param_return_type = """
return_type : {"infer", :class:`pandas.IntervalIndex`, :class:`pandas.arrays.IntervalArray`}, default "infer"
    If "infer" the return type will be the same as *interval_array*.
    If supplied, must be done so as a keyword argument.
"""


template_doc = """
Performs a set {operation} operation.

What is considered a set is determined by the number of positional arguments used, that is, determined by the
size of *interval_arrays*.

If *interval_arrays* is empty then the sets are considered to be the intervals contained in *interval_array*.

If *interval_arrays* is not empty then the sets are considered to be *interval_array* and the elements in *interval_arrays*.
Each of these arrays is assumed to contain disjoint intervals (and satisfy the definition of a set).  Any array containing
overlaps between intervals will be mapped to one with disjoint intervals via a union operation.

{extra_desc}
Parameters
----------
{params}

Returns
----------
:class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`

{examples}
"""

doc_difference_template = """
Performs a set difference operation.

The argument *interval_array* and the array elements of *interval_arrays* are all considered to be the sets over which
the operation is performed.  Each of these arrays is assumed to contain disjoint intervals (and satisfy the definition of a set).
Any array containing overlaps between intervals will be mapped to one with disjoint intervals via a union operation.

The list *interval_arrays* must contain at least one element.  If *interval_arrays* contains a single element then
the result is the set difference between *interval_array* and this single element. If *interval_arrays* contains
multiple elements then the result is the set difference between *interval_array* and the union of the sets in *interval_arrays*.
This is equivalent to iteratively applying a set difference operation with each array in *interval_arrays* as the second operand.

Each of these array operands is assumed to contain disjoint intervals (and satisfy the definition of a set).  Any array containing
overlaps between intervals will be mapped to one with disjoint intervals via a union operation.

{extra_desc}
Parameters
----------
{params}

Returns
----------
:class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`

{examples}
"""


union_params = join_params(
    [
        param_interval_array.format(operation="union"),
        param_optional_args,
        param_squeeze,
        param_return_type,
    ]
)
union_docstring = template_doc.format(
    operation="union",
    extra_desc="",
    params=union_params,
    examples=union_examples,
)

intersection_params = join_params(
    [
        param_interval_array.format(operation="intersection"),
        param_optional_args,
        param_min_overlaps,
        param_squeeze,
        param_return_type,
    ]
)
intersection_docstring = template_doc.format(
    operation="intersection",
    extra_desc="",
    params=intersection_params,
    examples=intersection_examples,
)

difference_params = join_params(
    [
        param_interval_array.format(operation="difference"),
        param_optional_args_difference,
        param_squeeze,
        param_return_type,
    ]
)
difference_docstring = doc_difference_template.format(
    operation="difference",
    extra_desc="",
    params=difference_params,
    examples=difference_examples,
)


symmetric_difference_params = join_params(
    [
        param_interval_array.format(operation="symmetric difference"),
        param_optional_args,
        param_min_overlaps,
        param_squeeze,
        param_return_type,
    ]
)
symmetric_difference_extra_desc = """
The symmetric difference can be defined as the set difference, of the union and the intersection.
The parameter *min_overlaps* in :meth:`piso.intersection`, which defines the minimum number of intervals
in an overlap required to constitute an intersection, follows through to symmetric difference under this definition.
"""
symmetric_difference_docstring = template_doc.format(
    operation="symmetric difference",
    extra_desc=symmetric_difference_extra_desc,
    params=symmetric_difference_params,
    examples=symmetric_difference_examples,
)
