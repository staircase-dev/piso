.. _user_guide.calendar_example:


Finding common gaps in daily calendars
=======================================

In this example we are given the following scenario:

    Alice, Bob, and Carol are busy people, after all they appear in their fair
    share of computing examples.  They wish to meet on the 5th of October 2021
    to discuss their next appearance.  Given calendar data which details their 
    scheduled meetings, find the gaps during business hours (9am to 5pm) that
    they can meet.


We start by importing :mod:`pandas` and :mod:`piso`

.. ipython:: python

    import pandas as pd
    import piso


Running the :func:`piso.register_accessors` function will add "piso" accessors to :class:`pandas.IntervalIndex`
and :class:`pandas.arrays.IntervalArray`. Using accessors allows us to extend the functionality
associated with these classes, without adding the methods directly.

.. ipython:: python

    piso.register_accessors()


Next we load the data from a csv file and store it into a :class:`pandas.DataFrame`.
Each row of the dataframe corresponds to a meeting that has been booked for
the 5th of October, and is characterised by the attendee, a start time and an 
end time.


.. ipython:: python

    data = pd.read_csv("./data/calendar.csv", parse_dates=["start", "end"])
    data


This data is reasonably readable however to work with :mod:`piso` we need it in interval arrays.
The following code creates a :class:`pandas.Series`, indexed by the names Alice, Bob and Carol,
and where the values are instances of :class:`pandas.arrays.IntervalArray` and hold the data corresponding to each person.

.. ipython:: python

    meetings = (
        data
        .groupby("name")
        .apply(
            lambda df: pd.arrays.IntervalArray.from_arrays(
                df["start"],
                df["end"],
                closed="left",
            ),
        )
    )
    meetings


We define a method `print_intervals` which is designed to make it easy for us to display interval array data.
It prints a heading, then each interval in an array.

.. ipython:: python

    def print_intervals(header, interval_array):
        print(header)
        print("-------------")
        for interval in interval_array:
            print(interval)
        print()

Let's see this method in action by printing the meeting times for each person.

.. ipython:: python

    for person in ("Alice", "Bob", "Carol"):
        print_intervals(person, meetings[person])


**Where are the overlaps in meetings for each person?**

You may notice that there seems to be some overlaps in the individual calendars for each person.  Who amongst us can say they've never double booked?

We will examine these overlaps using :func:`piso.intersection` - but we will use it via the piso accessor.  We will not supply any additional array arguments, so the sets are those intervals belonging to the IntervalArray. The *min_overlaps* parameter value of 2 indicates that we are looking for overlaps between two or more intervals.  If we do not specify this parameter then the default behaviour is to find regions where every interval in the interval array overlaps (there are no such cases in this data).

.. ipython:: python

    print("******** Individual Meeting Clashes ********\n")

    for person in ("Alice", "Bob", "Carol"):
        print_intervals(
            person,
            meetings[person].piso.intersection(min_overlaps=2),
        )


As you can see Bob and Carol each have an interval of time where they have meeting clashes.


**What are the busy times for each person?**

Let's not worry about the meeting clashes, they are irrelevant for finding the schedule gaps shared by Alice, Bob and Carol.
We can simplify the "busy" times in each calendar with the :func:`piso.union` method (via the piso accessor).

.. ipython:: python

    print("*************** Busy periods ***************\n")

    for person in ("Alice", "Bob", "Carol"):
        print_intervals(
            person,
            meetings[person].piso.union(),
        )

So these are the disjoint intervals, in each person's calendar, in which they are busy.  But we are interested in the complement of these intervals.  That is, the times (between 9am and 5pm) that each person is free.


**Where are the gaps in the schedule for each person?**

We'll create an interval array holding a single `pandas.Interval` which represents the business day.  For each person we can use the :func:`piso.difference` method (via the piso accessor), to remove the busy intervals from the business day interval.  We do this using :meth:`pandas.Series.map` and a lambda function but there are more verbose ways to perform this calculation.  The result will be a :class:`pandas.Series` called *gaps* which is indexed by the names, and whose values are interval arrays containing the "free" intervals in each person's calendar.

.. ipython:: python

    business_day = pd.arrays.IntervalArray.from_breaks(
        [pd.Timestamp("2021-10-5 9:00"), pd.Timestamp("2021-10-5 17:00")],
        closed="left",
    )
    gaps = meetings.map(lambda ia: business_day.piso.difference(ia))

    print("************* Gaps in schedule *************\n")

    for person in ("Alice", "Bob", "Carol"):
        print_intervals(person, gaps[person])


**Where can we schedule a meeting between Alice, Bob and Carol?**

All that remains to do is find the intersection between the interval array of gaps calculated above.
We do this with :func:`piso.intersection`, but we will provide it with multiple :class:`pandas.arrays.IntervalArray` operands, which indicates that each IntervalArray is interpreted as a set (as opposed to the intervals contained within.).  We use python's "*" unpack operator to transform the values of the *gaps* series - which is a :mod:`numpy` array of :class:`pandas.arrays.IntervalArray` - into the arguments in the method call.

.. ipython:: python

    print_intervals(
        "Potential meetings times",
        piso.intersection(*gaps.values)
    )

So there we have it.  There is a one-hour opportunity at 1:30pm and a half-hour opportunity at 3:30pm.  

This has not been an exhaustive illustration of the functions in :mod:`piso`.  There are many methods and parameters which have not been demonstrated above, but hopefully it has whet your appetite.  For details of all the full functionality offered by :mod:`piso` refer to the :ref:`api`.