.. _case_studies:


***************
Case studies
***************

.. panels::

    **Finding common gaps in daily calendars**

    This case study introduces the use of :mod:`piso` for set operations such as :func:`piso.intersection` and :func:`piso.union` and applies it to an example where personal calendars are represented by interval arrays.

    .. link-button:: calendar
        :type: ref
        :text: 
        :classes: stretched-link

    ---

    **Verifying a maintenance schedule**

    This case study introduces the use of :mod:`piso` for analysis with functions that return scalars, such as :func:`piso.issuperset` and :func:`piso.coverage`.  In this example maintenance schedules and windows of opportunity are represented by interval arrays.

    .. link-button:: maintenance
        :type: ref
        :text: 
        :classes: stretched-link

    ---

    **Estimating tax payable**

    This case study demonstrates the use of :func:`piso.lookup` where tax brackets are represented by a :class:`pandas.DataFrame`, indexed by a :class:`pandas.IntervalIndex`.  The tax payable for an array of income values is calculated by efficiently finding the corresponding tax brackets.

    .. link-button:: tax
        :type: ref
        :text: 
        :classes: stretched-link


    ---

    **Analysis of scores in a football match**

    This case study introduces the idea of *joins* using :class:`pandas.IntervalIndex`.  Using :func:`piso.join` a dataframe is constructed, indexed by intervals for unique score combinations in the 2009 Chelsea vs Liverpool Champions League quarter-final.

    .. link-button:: football
        :type: ref
        :text: 
        :classes: stretched-link


 .. toctree::
    :hidden:
    :maxdepth: 1

    calendar
    maintenance
    tax
    football