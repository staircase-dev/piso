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


isdisjoint_examples = """
Examples
-----------

>>> import pandas as pd
>>> import piso

>>> arr1 = pd.arrays.IntervalArray.from_tuples(
...     [(0, 3), (2, 4)],
... )
>>> arr2 = pd.arrays.IntervalArray.from_tuples(
...     [(4, 7), (8, 11)],
... )
>>> arr3 = pd.arrays.IntervalArray.from_tuples(
...     [(2, 4), (7, 8)],
... )

>>> piso.isdisjoint(arr1)
False

>>> piso.isdisjoint(arr2)
True

>>> piso.isdisjoint(arr1, arr2)
True

>>> piso.isdisjoint(arr1, arr3)
False
"""


issuperset_examples = """
Examples
-----------

>>> import pandas as pd
>>> import piso

>>> arr1 = pd.arrays.IntervalArray.from_tuples(
...     [(0, 4), (3, 6), (7, 8), (10, 12)],
... )
>>> arr2 = pd.arrays.IntervalArray.from_tuples(
...     [(2, 5), (7, 8)],
... )
>>> arr3 = pd.arrays.IntervalArray.from_tuples(
...     [(3, 4), (10, 11)],
... )

>>> piso.issuperset(arr1, arr2)
True

>>> piso.issuperset(arr1, arr2, squeeze=False)
array([ True])

>>> piso.issuperset(arr1, arr2, arr3)
array([ True, True])

>>> piso.issuperset(arr2, arr3)
False
"""


issubset_examples = """
Examples
-----------

>>> import pandas as pd
>>> import piso

>>> arr1 = pd.arrays.IntervalArray.from_tuples(
...     [(2, 5), (7, 8)],
... )
>>> arr2 = pd.arrays.IntervalArray.from_tuples(
...     [(0, 4), (3, 6), (7, 8), (10, 12)],
... )
>>> arr3 = pd.arrays.IntervalArray.from_tuples(
...     [(3, 4), (10, 11)],
... )

>>> piso.issubset(arr1, arr2)
True

>>> piso.issubset(arr1, arr2, squeeze=False)
array([ True])

>>> piso.issubset(arr1, arr2, arr3)
array([ True, False])

>>> piso.issubset(arr1, arr3)
False
"""


def join_params(list_of_param_strings):
    return "".join(list_of_param_strings).replace("\n\n", "\n")


param_interval_array = """
interval_array : :class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`
    The first (and possibly only) operand to the {operation} operation.
"""

param_interval_array_non_optional = """
interval_array : :class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`
    The first operand to the {operation} operation.
"""

param_interval_sub_super_set = """
interval_array : :class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`
    The first operand to which all others are compared operation.
"""

param_optional_args = """
*interval_arrays : argument list of :class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`
    May contain zero or more arguments.
"""

param_optional_args_min_one = """
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
squeeze : boolean, default {default}
    If True, will try to coerce the return value to a single pandas.Interval.
    If supplied, must be done so as a keyword argument.
"""

param_return_type = """
return_type : {"infer", :class:`pandas.IntervalIndex`, :class:`pandas.arrays.IntervalArray`}, default "infer"
    If "infer" the return type will be the same as *interval_array*.
    If supplied, must be done so as a keyword argument.
"""


template_doc = """
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
{return_type}

{examples}
"""


operation_template_doc = (
    """
Performs a set {operation} operation.
"""
    + template_doc
)


doc_difference_template = """
Performs a set difference operation.

The argument *interval_array* and the array elements of *interval_arrays* are all considered to be the sets over which
the operation is performed.  Each of these arrays is assumed to contain disjoint intervals (and satisfy the definition of a set).
Any array containing overlaps between intervals will be mapped to one with disjoint intervals via a union operation.

The list *interval_arrays* must contain at least one element.  If *interval_arrays* contains a single element then
the result is the set difference between *interval_array* and this single element. If *interval_arrays* contains
multiple elements then the result is the set difference between *interval_array* and the union of the sets in *interval_arrays*.
This is equivalent to iteratively applying a set difference operation with each array in *interval_arrays* as the second operand.

{extra_desc}
Parameters
----------
{params}

Returns
----------
:class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`

{examples}
"""

doc_is_sub_super_set_template = """
Indicates whether a set is a {operation} of one, or more, other sets.

The argument *interval_array* and the array elements of *interval_arrays* are all considered to be the sets for the purposes
of this set method.  Each of these arrays is assumed to contain disjoint intervals (and satisfy the definition of a set).
Any array containing overlaps between intervals will be mapped to one with disjoint intervals via a union operation.

The list *interval_arrays* must contain at least one element.  The {operation} comparison is iteratively applied between
*interval_array* and each array in *interval_arrays*.  When *interval_arrays* contains multiple interval arrays, the return
type will be a numpy array.  If it contains one interval array then the result can be coerced to a single boolean using the
*squeeze* parameter.

{extra_desc}
Parameters
----------
{params}

Returns
----------
boolean, or :class:`numpy.ndarray` of boolean

{examples}
"""


array_return_type = (
    ":class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`"
)

union_params = join_params(
    [
        param_interval_array.format(operation="union"),
        param_optional_args,
        param_squeeze.format(default="False"),
        param_return_type,
    ]
)
union_docstring = operation_template_doc.format(
    operation="union",
    extra_desc="",
    params=union_params,
    return_type=array_return_type,
    examples=union_examples,
)

intersection_params = join_params(
    [
        param_interval_array.format(operation="intersection"),
        param_optional_args,
        param_min_overlaps,
        param_squeeze.format(default="False"),
        param_return_type,
    ]
)
intersection_docstring = operation_template_doc.format(
    operation="intersection",
    extra_desc="",
    params=intersection_params,
    return_type=array_return_type,
    examples=intersection_examples,
)

difference_params = join_params(
    [
        param_interval_array_non_optional.format(operation="difference"),
        param_optional_args_min_one,
        param_squeeze.format(default="False"),
        param_return_type,
    ]
)
difference_docstring = doc_difference_template.format(
    operation="difference",
    extra_desc="",
    params=difference_params,
    return_type=array_return_type,
    examples=difference_examples,
)


symmetric_difference_params = join_params(
    [
        param_interval_array.format(operation="symmetric difference"),
        param_optional_args,
        param_min_overlaps,
        param_squeeze.format(default="False"),
        param_return_type,
    ]
)
symmetric_difference_extra_desc = """
The symmetric difference can be defined as the set difference, of the union and the intersection.
The parameter *min_overlaps* in :meth:`piso.intersection`, which defines the minimum number of intervals
in an overlap required to constitute an intersection, follows through to symmetric difference under this definition.
"""
symmetric_difference_docstring = operation_template_doc.format(
    operation="symmetric difference",
    extra_desc=symmetric_difference_extra_desc,
    params=symmetric_difference_params,
    return_type=array_return_type,
    examples=symmetric_difference_examples,
)


isdisjoint_doc = (
    """
Indicates whether one, or more, sets are disjoint or not.
"""
    + template_doc
)

isdisjoint_params = join_params(
    [
        param_interval_array.format(operation="isdisjoint"),
        param_optional_args,
    ]
)
isdisjoint_docstring = isdisjoint_doc.format(
    extra_desc="",
    params=isdisjoint_params,
    return_type="boolean",
    examples=isdisjoint_examples,
)


issuperset_params = join_params(
    [
        param_interval_sub_super_set,
        param_optional_args_min_one,
        param_squeeze.format(default="True"),
    ]
)
issuperset_docstring = doc_is_sub_super_set_template.format(
    operation="superset",
    extra_desc="",
    params=issuperset_params,
    examples=issuperset_examples,
)


issubset_params = join_params(
    [
        param_interval_sub_super_set,
        param_optional_args_min_one,
        param_squeeze.format(default="True"),
    ]
)
issubset_docstring = doc_is_sub_super_set_template.format(
    operation="subset",
    extra_desc="",
    params=issubset_params,
    examples=issubset_examples,
)


coverage_docstring = """
Calculates the fraction of a domain covered by a collection of intervals.

Parameters
----------
interval_array : :class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`
    Contains the (possibly overlapping) intervals which partially, or wholly cover the domain.
domain : :py:class:`tuple`, :class:`pandas.Interval`, :class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`, optional
    Specifies the domain over which to calculate the "coverage".  If *domain* is `None`,
    then the domain is considered to be the extremities of the intervals contained in *interval_array*
    If *domain* is a tuple then it should specify lower and upper bounds, and be equivalent to a
    :class:`pandas.Interval`.  If *domain* is a :class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`
    then the intervals it contains define a possibly disconnected domain.

Returns
----------
float
    a number between 0 and 1, representing the fraction of the domain covered.

Examples
-----------

>>> import pandas as pd
>>> import piso

>>> arr1 = pd.arrays.IntervalArray.from_tuples(
...     [(0, 4), (3, 5), (7, 8)],
... )

>>> piso.coverage(arr1)
0.75

>>> piso.coverage(arr1, (0, 10))
0.6

>>> piso.coverage(arr1, pd.Interval(-10, 10))
0.3

>>> domain = pd.arrays.IntervalArray.from_tuples(
...     [(4,6), (7, 9)],
... )
>>> piso.coverage(arr1, domain)
0.5
"""


complement_docstring = """
Calculates the complement of a collection of intervals (in an array) over some domain.

Equivalent to the set difference of the domain and the intervals in the array.

Parameters
----------
interval_array : :class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`
    Contains the (possibly overlapping) intervals.
domain : :py:class:`tuple`, :class:`pandas.Interval`, :class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`, optional
    Specifies the domain over which to calculate the "complement".  If *domain* is `None`,
    then the domain is considered to be the extremities of the intervals contained in *interval_array*
    If *domain* is a tuple then it should specify lower and upper bounds, and be equivalent to a
    :class:`pandas.Interval`.  If *domain* is a :class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`
    then the intervals it contains define a possibly disconnected domain.

Returns
----------
:class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`
    The return type will be the same as *interval_array*.

Examples
-----------

>>> import pandas as pd
>>> import piso

>>> arr1 = pd.arrays.IntervalArray.from_tuples(
...     [(0, 4), (3, 5), (7, 8)],
... )

>>> piso.complement(arr1)
<IntervalArray>
[(5, 7]]
Length: 1, closed: right, dtype: interval[int64]

>>> piso.complement(arr1, (-5, 10))
<IntervalArray>
[(-5, 0], (5, 7], (8, 10]]
Length: 3, closed: right, dtype: interval[int64]

>>> piso.complement(arr1, pd.Interval(-5, 6))
<IntervalArray>
[(-5, 0], (5, 6]]
Length: 2, closed: right, dtype: interval[int64]

>>> domain = pd.arrays.IntervalArray.from_tuples(
...     [(-5,-2), (7,10)],
... )

>>> piso.complement(arr1, domain)
<IntervalArray>
[(-5, -2], (8, 10]]
Length: 2, closed: right, dtype: interval[int64]
"""


get_indexer_docstring = """
Given a set of disjoint intervals and a value, or vector, *x* returns the
index positions of the interval which contains each value in x.

Parameters
----------
interval_array : :class:`pandas.IntervalIndex` or :class:`pandas.arrays.IntervalArray`
    Contains the disjoint intervals.
x : scalar, or array-like of scalars
    Values in *x* should belong to the same domain as the intervals in *interval_array*.

Returns
----------
:class:`numpy.ndarray`
    Values will be integer.  If a point is not contained in any interval then the corresponding
    value is -1.

Examples
-----------

>>> import pandas as pd
>>> import piso

>>> arr = pd.arrays.IntervalArray.from_tuples(
...     [(0, 4), (6, 8), (10, 12)],
... )

>>> piso.get_indexer(arr, 11)
2

>>> piso.get_indexer(arr, 8)
1

>>> piso.get_indexer(arr, 9)
-1

>>> piso.get_indexer(arr, [1,2,7,13])
array([ 0,  0,  1, -1], dtype=int64)
"""
