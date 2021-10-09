.. _userguide.accessors:

The piso accessors
=================================

Applying set operations to interval array objects: :class:`pandas.arrays.Interval` and :class:`pandas.IntervalIndex` can be done with top-level functions:

    - :func:`piso.union`
    - :func:`piso.intersection`
    - :func:`piso.difference`
    - :func:`piso.symmetric_difference`

The exact same functionality is available through accessors on these classes.  Using accessors allows us to extend the functionality
associated with these classes, without adding the methods directly.  Before the accessors can be used they must be registered:

.. ipython:: python
    :suppress:

    import pandas as pd

.. ipython:: python

    import piso
    piso.register_accessors()

Registering the accessors adds a *piso* property to the classes which can be used like so:

.. ipython:: python

    arr = pd.arrays.IntervalArray.from_tuples(
        [(1,5), (3,6), (2,4)]
    )

    arr.piso.intersection()

Further examples using the *piso* accessors can be found in the :ref:`api`.





    