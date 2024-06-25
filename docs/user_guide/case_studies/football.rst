.. _user_guide.football_example:


Analysis of scores in a football match
=======================================

In this example we will look at a football match from 2009:

    The Champions League quarter-final between Chelsea and Liverpool
    in 2009 is recognised as among the best games of all time.
    Liverpool scored twice in the first half in the 19th and 28th minute.
    Chelsea then opened their account in the second half with three
    unanswered goals in the 51st, 57th and 76th minute.  Liverpool
    responded with two goals in the 81st and 83rd minute to put themselves
    ahead, however Chelsea drew with a goal in the 89th minute and advanced
    to the next stage on aggregate.


We start by importing :mod:`pandas` and :mod:`piso`

.. ipython:: python

    import pandas as pd
    import piso


For the analysis we will create a :class:`pandas.Series`, indexed by a :class:`pandas.IntervalIndex` for each team.  The values of each series will be the team's score and the interval index, defined by :class:`pandas.Timedelta`, will describe the durations corresponding to each score.  We define the following function which creates such a Series, given the minute marks for each score.

.. ipython:: python

    def make_series(goal_time_mins):
        breaks = pd.to_timedelta([0] + goal_time_mins + [90], unit="min")
        ii = pd.IntervalIndex.from_breaks(breaks)
        return pd.Series(range(len(ii)), index = ii, name="score")

We can now create each Series.

.. ipython:: python

    chelsea = make_series([51,57,76,89])
    liverpool = make_series([19,28,81,83])

For reference, the Series corresponding to `chelsea` is

.. ipython:: python

    chelsea

To enable analysis for separate halves of the game we'll define a similar Series which defines the time intervals for each half

.. ipython:: python

    halves = pd.Series(
        ["1st", "2nd"],
        pd.IntervalIndex.from_breaks(pd.to_timedelta([0, 45, 90], unit="min")),
        name="half",
    )
    halves

We can now perform a join on these three Series.  Since `chelsea` and `liverpool` Series have the same name it will be necessary to provide suffixes to differentiate the columns in the result.  The `halves` Series does not have the same name, but a suffix must be defined for each of the join operands if there are any overlaps.

.. ipython:: python

    CvsL = piso.join(chelsea, liverpool, halves, suffixes=["_chelsea", "_liverpool", ""])
    CvsL

By default, the :func:`piso.join` function performs a left-join.  Since every interval index represents the same domain, that is `(0', 90']`, all join types - *left*, *right*, *inner*, *outer* - will give the same result.

Using this dataframe we will now provide answers for miscellaneous questions.  In particular we will filter the dataframe based on values in the columns, then sum the lengths of the intervals in the filtered index.


**How much game time did Chelsea lead for?**

.. ipython:: python

    CvsL.query("score_chelsea > score_liverpool").index.length.sum()


**How much game time did Liverpool lead for?**

.. ipython:: python

    CvsL.query("score_liverpool > score_chelsea").index.length.sum()

**How much game time were the teams tied for?**

.. ipython:: python

    CvsL.query("score_liverpool == score_chelsea").index.length.sum()

**How much game time in the first half were the teams tied for?**

.. ipython:: python

    CvsL.query("score_chelsea == score_liverpool and half == '1st'").index.length.sum()

**For how long did Liverpool lead Chelsea by exactly one goal (split by half)?**

.. ipython:: python

    CvsL.groupby("half").apply(
        lambda df: df.query("score_liverpool - score_chelsea == 1").index.length.sum(),
        include_groups=False,
    )

**What was the score at the 80 minute mark?**

.. ipython:: python

    piso.lookup(CvsL, pd.Timedelta(80, unit="min"))


This analysis is also straightforward using :mod:`staircase`.  For more information on this please see the :ref:`corresponding example with staircase <user_guide.football_staircase_example>`