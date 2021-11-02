.. _user_guide.faq:


Frequently asked questions
==========================

.. dropdown:: Can any interval be used with piso?
    :container: + shadow

    Unfortunately no.  The intervals must
    
        - have a non-zero length
        - have a finite, length
        - either be left-closed right-open, or right-closed left-open

    Operations between Intervals, IntervalIndex and IntervalArray objects must have the same value for their *closed* attribute.

.. dropdown:: Are there plans to add support for intervals which are either degenerate (contain a single point), infinite length, or not half-closed?
    :container: + shadow

    At this stage no, but this may change depending on the popularity of the package and the demand for this functionality.

.. dropdown:: Are there existing set operations for intervals in pandas?
    :container: + shadow

    Yes, but currently there are very few:

    :class:`pandas.Interval`:

        - :attr:`pandas.Interval.is_empty`
        - :meth:`pandas.Interval.overlaps`

    :class:`pandas.arrays.IntervalArray`:

        - :attr:`pandas.arrays.IntervalArray.is_empty`
        - :attr:`pandas.arrays.IntervalArray.is_non_overlapping_monotonic`
        - :meth:`pandas.arrays.IntervalArray.contains`
        - :meth:`pandas.arrays.IntervalArray.overlaps`

    :class:`pandas.IntervalIndex`:

        - :attr:`pandas.IntervalIndex.is_empty`
        - :attr:`pandas.IntervalIndex.is_non_overlapping_monotonic`
        - :attr:`pandas.IntervalIndex.is_overlapping`
        - :meth:`pandas.IntervalIndex.contains`
        - :meth:`pandas.IntervalIndex.overlaps`


    Additional set operations for intervals, like those implemented in `piso`, are earmarked for development in :mod:`pandas` at some time in the future.

.. dropdown:: Can I work with datetime/timestamp data?
    :container: + shadow

    Yes :mod:`piso` will work with :class:`pandas.Timestamp` and :class:`pandas.Timedelta` data.  Users who wish to use :class:`numpy.datetime64` and :class:`datetime.datetime` (and timedelta counterparts) should be aware that: 
    
        - :class:`pandas.Interval` can only be constructed  with numeric, :class:`pandas.Timestamp` or :class:`pandas.Timedelta` data
        - when using construction class methods, such as :meth:`pandas.IntervalIndex.from_arrays`, any datetime objects from :mod:`numpy` or :mod:`datetime` modules will be converted by :mod:`pandas` to the :mod:`pandas` equivalent.

.. dropdown:: Why is there no `piso` accessor for `pandas.Interval`?
    :container: + shadow

    Objects of type :class:`pandas.Interval` are immutable, meaning they cannot be changed (incuding the addition of an accessor).

.. dropdown:: Why use accessors?
    :container: + shadow

    Accessors provide a nice way of carving out a seperate namespace for `piso`, as opposed to monkey patching.  This is particularly important for :class:`pandas.IntervalIndex`, which inherits methods from :class:`pandas.Index`, which are set based operations:

        - :meth:`pandas.Index.union`
        - :meth:`pandas.Index.intersection`
        - :meth:`pandas.Index.difference`
        - :meth:`pandas.Index.symmetric_difference`

    however these methods consider the elements of the to be the intervals themselves - there is no notion as the intervals being sets.


.. dropdown:: What if I want to map intervals with a scalar?

    This question may arise if, for example, a :class:`pandas.Series` with a numerical dtype, was indexed with a :class:`pandas.IntervalIndex`.
    Given two intervals, and their associated scalar values, a user may wish to find the overlap of these intervals, and map it to the minimum of the two scalar values - or perhaps the addition of the scalar values.  These sorts of manipulations can be achieved via :mod:`staircase`.  There is a one-to-one mapping between sets of disjoint intervals (with associated scalars) and step functions, which is what motivates the internal implementations of `piso`.  :mod:`staircase` provides a comprehensive range of arithmetic, logical, relational and statistical methods for working with step functions.   For related case studies see the :ref:`football case study with piso <user_guide.football_example>` and the :ref:`football case study with staircase <user_guide.football_staircase_example>`
