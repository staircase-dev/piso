.. _user_guide.football_staircase_example:


Analysis of scores in a football match (using staircase)
===========================================================

.. ipython:: python
    :suppress:

    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    plt.style.use('seaborn-v0_8')

This example demonstrates how :mod:`staircase` can be used to mirror the functionality
and analysis presented in the :ref:`corresponding example with piso <user_guide.football_example>`.

    The Champions League quarter-final between Chelsea and Liverpool
    in 2009 is recognised as among the best games of all time.
    Liverpool scored twice in the first half in the 19th and 28th minute.
    Chelsea then opened their account in the second half with three
    unanswered goals in the 51st, 57th and 76th minute.  Liverpool
    responded with two goals in the 81st and 83rd minute to put themselves
    ahead, however Chelsea drew with a goal in the 89th minute and advanced
    to the next stage on aggregate.


We start by importing :mod:`pandas` and :mod:`staircase`

.. ipython:: python

    import pandas as pd
    import staircase as sc


For the analysis we will create a :class:`staircase.Stairs` for each team, and wrap them up in a :class:`pandas.Series` which is indexed by the club names.  Using a Series in this way is by no means necessary but can be useful.  We'll create a function `make_stairs` which takes the minute marks of the goals and returns a :class:`staircase.Stairs`.  Each step function will be monotonically non-decreasing.

.. ipython:: python

    def make_stairs(goal_time_mins):
        breaks = pd.to_timedelta(goal_time_mins, unit="min")
        return sc.Stairs(start=breaks).clip(pd.Timedelta(0), pd.Timedelta("90m"))

    scores = pd.Series(
        {
            "chelsea":make_stairs([51,57,76,89]),
            "liverpool":make_stairs([19,28,81,83]),
        }
    )
    scores


To clarify we plot these step functions below.

.. ipython:: python
    :suppress:

    fig, axes = plt.subplots(ncols=2, figsize=(8,3), sharey=True)
    vals = scores["chelsea"].step_values
    vals.index = vals.index/pd.Timedelta("1min")
    sc.Stairs.from_values(0, vals).plot(axes[0])
    axes[0].set_title("Chelsea")
    axes[0].set_xlabel("time (mins)")
    axes[0].set_ylabel("score")
    axes[0].yaxis.set_major_locator(ticker.MultipleLocator())
    axes[0].set_xlim(0,90)
    vals = scores["liverpool"].step_values
    vals.index = vals.index/pd.Timedelta("1min")
    sc.Stairs.from_values(0, vals).plot(axes[1])
    axes[1].set_title("Liverpool")
    axes[1].set_xlabel("time (mins)")
    axes[1].set_ylabel("score")
    @savefig case_study_football_staircase.png
    plt.tight_layout();


To enable analysis for separate halves of the game we'll define a similar Series which defines the time intervals for each half with tuples of :class:`pandas.Timedeltas`.

.. ipython:: python

    halves = pd.Series(
        {
            "1st":(pd.Timedelta(0), pd.Timedelta("45m")),
            "2nd":(pd.Timedelta("45m"), pd.Timedelta("90m")),
        }
    )
    halves


We can now use our *scores* and *halves* Series to provide answers for miscellaneous questions.  Note that comparing :class:`staircase.Stairs` objects with relational operators produces boolean-valued step functions (Stairs objects).  Finding the integral of these boolean step functions is equivalent to summing up lengths of intervals in the domain where the step function is equal to one.

**How much game time did Chelsea lead for?**

.. ipython:: python

    (scores["chelsea"] > scores["liverpool"]).integral()


**How much game time did Liverpool lead for?**

.. ipython:: python

    (scores["chelsea"] < scores["liverpool"]).integral()

**How much game time were the teams tied for?**

.. ipython:: python

    (scores["chelsea"] == scores["liverpool"]).integral()

**How much game time in the first half were the teams tied for?**

.. ipython:: python

    (scores["chelsea"] == scores["liverpool"]).where(halves["1st"]).integral()

**For how long did Liverpool lead Chelsea by exactly one goal (split by half)?**

.. ipython:: python

    halves.apply(lambda x:
        (scores["liverpool"]==scores["chelsea"]+1).where(x).integral()
    )

**What was the score at the 80 minute mark?**

.. ipython:: python

    sc.sample(scores, pd.Timedelta("80m"))