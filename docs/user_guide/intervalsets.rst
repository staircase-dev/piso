.. _userguide.intervalsets:

Intervals and sets
=================================

Below is a brief discussion on the mathematical definition of intervals and sets, and how they relate to :mod:`piso` - aside from making up half of the acronym!

Sets
-----

A set is a collection of elements where each element, or member, of the set is unique, i.e. a set does not contain duplicated elements. There may be an infinite number of members, such as the set of positive integers, or it could be empty.  There is both standard notation and standard operations for sets.

For example:

- :math:`A = \{1, 2, 3\}` is a set containing three numbers
- :math:`B = \{3, 4\}` is a set containing two numbers

The union of these sets, :math:`A \cup B`, is the set containing all elements in :math:`A` and :math:`B`.  That is, :math:`A \cup B = \{1, 2, 3, 4\}`.

The intersection of these sets, :math:`A \cap B`, is the set containing elements both in :math:`A` and :math:`B`.  That is, :math:`A \cap B = \{3\}`.

The difference of :math:`A` and :math:`B` = :math:`A \setminus B`, is the set containing all elements in :math:`A` but not in :math:`B`.  That is, :math:`A \setminus B = \{1, 2\}`.

The symmetric difference of these sets, :math:`A \Delta B`, is the set containing all elements in :math:`A` and in :math:`B`, but not in both.  That is, :math:`A \Delta B = \{1, 2, 4\}`.  Symmetric difference of sets is equivalent to the difference between the union and the intersection.

Python is no stranger to set operations, with the :py:class:`set` class being a built-in data structure (for sets with a finite number of elements) with the following methods:

    - :py:meth:`set.union <frozenset.union>`
    - :py:meth:`set.intersection <frozenset.intersection>`
    - :py:meth:`set.difference <frozenset.difference>`
    - :py:meth:`set.symmetric_difference <frozenset.symmetric_difference>`
    - :py:meth:`set.isdisjoint <frozenset.isdisjoint>`
    - :py:meth:`set.issubset <frozenset.issubset>`
    - :py:meth:`set.issuperset <frozenset.issuperset>`


Set operations, for sets with a finite number of elements, also exist for :class:`pandas.Index`:

    - :meth:`pandas.Index.union`
    - :meth:`pandas.Index.intersection`
    - :meth:`pandas.Index.difference`
    - :meth:`pandas.Index.symmetric_difference`

To continue a gentle introduction to sets, please refer to `math is fun <https://www.mathsisfun.com/sets/sets-introduction.html>`_.


Intervals
----------

An interval is a set of (real) numbers that contains all real numbers lying between any two numbers (endpoints).  The notion of an interval can be applied to other domains in which a "total ordering" exists, such as time-related domains modelled by :class:`pandas.Timestamp` and :class:`pandas.Timedelta`.

Intervals are classified as being open, closed, or half-open.  An open interval does not include its endpoints.  For example, the set of numbers between 0 and 1 (but not including 0 and 1) is an open interval.  In set notation it is written as :math:`\{x | 0 < x < 1\}`.  In interval notation it is written as :math:`(0,1)`. A closed interval contains both of its endpoints, while a half-closed interval contains only one of its endpoints.  The notation is as follows:

- :math:`[0,1] = \{x | 0 \leq x \leq 1\}` (closed)
- :math:`[0,1) = \{x | 0 \leq x < 1\}` (left-closed)
- :math:`(0,1] = \{x | 0 < x \leq 1\}` (right-closed)

The length of an interval is defined by subtracting the smaller end point from the larger.  Intervals could have an infinite length, such as the set of numbers greater than zero, or they could have zero length such as the set containing a single number (known as a degenerate interval). 

The definitions of set operations, outlined above, follow through to intervals, however the result of set operations with intervals may not be an interval - but it will be a set!  For example, 

- :math:`[0,2] \cup [1,3] = \{x | 1 \leq x \leq 3\} = [0,3]`
- :math:`[0,2] \cap [1,3] = \{x | 1 \leq x \leq 2\} = [1,2]`
- :math:`[0,2] \setminus [1,3] = \{x | 0 \leq x < 1\} = [0,1)`
- :math:`[0,2] \Delta [1,3] = \{x | 0 \leq x < 1 \text{ or } 2 < x \leq 3\} = [0,1) \cup (2,3]`

The result in the last of these examples above cannot be expressed as an interval.  It can however be expressed as the union of two disjoint (non-overlapping) intervals.  Modelling intervals in :mod:`pandas` is facilitated through :class:`pandas.Interval`, while representing the union of disjoint intervals can be achieved through an interval array such as :class:`pandas.arrays.IntervalArray` or :class:`pandas.IntervalIndex`.  The intervals contained in one of these interval arrays do not have to be disjoint, so with respect to set operations an interval array can be interpreted in one of two ways:

a) a collection of intervals, which become operands in a set operation, or
b) a set itself, formed by the union of disjoint intervals, and used as an operand in a set operation.

An example of a) is applying an intersection operation to a interval array containing the intervals

    :math:`[0, 5), [4, 6), [7, 9), [8, 12)`

which results in an in interval array containing the intervals

    :math:`[4, 5), [8, 9)`

An example of b) is applying an intersection operation to two interval arrays (of disjoint intervals)

    :math:`[0, 5), [7, 9) \hspace{6 mm} \text{and} \hspace{6 mm} [2, 3), [6, 8)`

which results in an in interval array containing 

    :math:`[0, 2), [3, 5), [8, 9)`


Both of these interpretations are supported by methods in :mod:`piso`.  The methods will switch interpretations depending on the number of interval array arguments supplied to the methods.  Note that if a interval array is used as an operand (as shown in the example for b) above) then any overlapping intervals will be merged to create a set of disjoint intervals before the operation is applied.

It is important to note that :mod:`piso` does not support all types of intervals. Specifically, intervals must have a length which is non-zero and finite.  It must be either left-closed, or right-closed.  Any :class:`pandas.Interval`, :class:`pandas.IntervalIndex` and :class:`pandas.array.IntervalArray` arguments supplied to :mod:`piso` methods must have the same value for their *closed* attribute (either "left" or "right").

For code examples involving :mod:`piso` set operations please see the small :ref:`case study <user_guide.calendar_example>` or examples provided in the :ref:`api`.

