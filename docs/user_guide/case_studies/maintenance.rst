.. _user_guide.maintenance_example:


Verifying a maintenance schedule
=================================

In this example we are given the following scenario:

    There are three identical assets `X`, `Y` and `Z` which require
    periodic maintenance.  No more than one asset should be under
    maintenance at any time, in order to handle the workload.
    Futhermore any maintenance should occur within windows of
    opportunity which represent when maintenance will be least
    disruptive.  Given a proposed schedule for 2021, verify these
    rules are respected, and analyse time usage.


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
Each row of the dataframe corresponds to an interval of maintenance for a particular asset.

.. ipython:: python

    data = pd.read_csv("./data/asset_maintenance.csv", parse_dates=["start", "end"], dayfirst=True)
    data

To work with :mod:`piso` we need the data in interval arrays.  The following code creates a :class:`pandas.Series`, indexed by the assets *X*, *Y* and *Z*,
where the values are instances of :class:`pandas.arrays.IntervalArray`.

.. ipython:: python

    maintenance = (
        data
        .groupby("asset")
        .apply(
            lambda df: pd.arrays.IntervalArray.from_arrays(
                df["start"],
                df["end"],
                closed="left",
            ),
            include_groups=False,
        )
    )
    maintenance

Checking that no more than one asset is under maintenance at any time is equivalent to checking that the sets corresponding to each interval array are disjoint.  This is as simple as the following code, where we unpack the values of the maintenance `Series` as arguments to :func:`piso.isdisjoint`.

.. ipython:: python

   piso.isdisjoint(*maintenance.values)

The windows in which maintenance is preferred is described by the following data

.. ipython:: python

    window_df = pd.read_csv(
        "./data/maintenance_windows.csv",
        parse_dates=["start", "end"],
        dayfirst=True,
    )
    window_df

As before, we transform this to an interval array

.. ipython:: python

    windows = pd.arrays.IntervalArray.from_arrays(
        window_df["start"],
        window_df["end"],
        closed="left",
    )
    windows

Checking that the maintenance occurs within the preferred windows can be done by checking that the set corresponding to the *windows* interval array is a superset of each of the sets corresponding to the asset interval arrays.  Instead of doing this for each asset we can check against the union of these sets.

.. ipython:: python
    
    combined_maintenance = piso.union(*maintenance.values)
    windows.piso.issuperset(combined_maintenance, squeeze=True)

Now let's answer some questions using :mod:`piso`, specifically :func:`piso.coverage` and its accessor counterpart.

**What fraction of the year 2021 constitutes maintenance window opportunities?**

.. ipython:: python

    windows.piso.coverage(pd.Interval(pd.Timestamp("2021"), pd.Timestamp("2022")))

**How many days in each month in 2021 constitute maintenance window opportunities?**

For this we'll create a :class:`pandas.IntervalIndex` for the months, then construct a :class:`pandas.Series` with a monthly :class:`pandas.PeriodIndex`.

.. ipython:: python

    months = pd.IntervalIndex.from_breaks(pd.date_range("2021", "2022", freq="MS"))
    pd.Series(
        [windows.piso.coverage(month)*month.length for month in months],
        index = months.left.to_period()
    )

**What fraction of the time in window opportunities is utilised by the combined maintenance?**

.. ipython:: python

    combined_maintenance.piso.coverage(windows)


**What fraction of the combined maintenance is occupied by each asset**

.. ipython:: python

    maintenance.apply(piso.coverage, domain=combined_maintenance)