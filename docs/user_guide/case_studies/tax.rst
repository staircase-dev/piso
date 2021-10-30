.. _user_guide.tax_example:


Estimating tax payable
=======================================

.. ipython:: python
    :suppress:

    import matplotlib.pyplot as plt
    plt.style.use('seaborn')

In this example we are given the following scenario:

    Personal tax (before deductions) in Australia is based on the
    table below.  The tax payable at the end of the financial year
    depends on the individual's income.  The higher the income, the
    higher the tax rate, as defined by tax brackets (or tiers).
    Given a list of incomes, calculate the corresponding tax payable
    for each income.

|

+---------------------+--------+--------------------------------------------+
| Income Thresholds   |   Rate |                                Tax payable |
+=====================+========+============================================+
| $0 - $18,200        |     0% |                                        Nil |
+---------------------+--------+--------------------------------------------+
| $18,200 - $45,000   |    19% |               19c for each $1 over $18,200 |
+---------------------+--------+--------------------------------------------+
| $45,000 - $120,000  |  32.5% | $5,092 plus 32.5c for each $1 over $45,000 |
+---------------------+--------+--------------------------------------------+
| $120,000 - $180,000 |    37% | $29,467 plus 37c for each $1 over $120,000 |
+---------------------+--------+--------------------------------------------+
| $180,000 and over   |    45% | $51,667 plus 45c for each $1 over $180,000 |
+---------------------+--------+--------------------------------------------+

|

We start by importing :mod:`pandas`, :mod:`numpy` and :mod:`piso`, and creating an interval index for the tax brackets.

.. ipython:: python

    import pandas as pd
    import numpy as np
    import piso

    tax_brackets = pd.IntervalIndex.from_breaks(
        [0,18200,45000,120000,180000,np.inf],
        closed="left",
    )
    tax_brackets

With each interval in the tax bracket, we'll associate three values:

    1) the lower threshold for the tax bracket
    2) the fixed amount payable
    3) the tax rate for each dollar above the threshold (as a fraction)
    
We describe this data as a :class:`pandas.DataFrame` indexed by `tax_brackets`.

.. ipython:: python

    tax_rates = pd.DataFrame(
        {
            "threshold":tax_brackets.left,
            "fixed":[0, 0, 5092, 29467, 51667],
            "rate":[0, 0.19, 0.325, 0.37, 0.45],
        },
        index = tax_brackets,
    )
    tax_rates


For the income, we'll generate some random integers (and plot the distribution) corresponding to 100,000 individuals.

.. ipython:: python

    income = pd.Series(np.random.beta(5,50, size=100000)*1e6).astype(int)
    @savefig case_study_tax_income_dist.png
    income.plot.hist(bins=20);

We are now in a position to use :func:`piso.lookup`, which take two parameters:

1) a :class:`pandas.DataFrame` or :class:`pandas.Series` which is indexed by a :class:`pandas.IntervalIndex`
2) the values which are will be compared to the interval index

.. ipython:: python

    tax_params = piso.lookup(tax_rates, income)
    tax_params

The result is a dataframe, indexed by the values of `income`, sharing the same columns as `tax_rates`.

We can then use a vectorised calculation for the tax payable:

.. ipython:: python

   tax_params["fixed"] + (tax_params.index-tax_params["threshold"])*tax_params["rate"]


Alternative approaches
-----------------------

There are a couple of alternative solutions which do not require :mod:`piso` which we detail below.

**Alternative 1: pandas.cut**

The `tax_params` dataframe that was produced above by :func:`piso.lookup` can be reproduced using :func:`pandas.cut` which can be used to assign bins to data with an interval index.

.. ipython:: python

    tax_params = tax_rates.loc[pd.cut(income, tax_brackets)].set_index(income)
    tax_params

This approach however runs approximately 3 times slower than :func:`piso.lookup`.


**Alternative 2: applying function**

The second approach involves writing a function which takes a single value (an income for an individual) and returns the tax payable.
The function can then used with `pandas.Series.apply`

.. ipython:: python

    def calc_tax(value):
        if value <= 18200:
            tax = 0
        elif value <= 45000:
            tax = (value-18200)*0.19
        elif value <= 120000:
            tax = 5092 + (value-45000)*0.325
        elif value <= 180000:
            tax = 29467 + (value-120000)*0.37
        else:
            tax = 51667 + (value-180000)*0.45
        return tax

    income.apply(calc_tax)

This approach is the fastest - approximately 3 times faster than :func:`piso.lookup` - but it does a function to be defined which is relatively cumbersome to implement.  This approach becomes increasingly unattractive, and error prone, as the number of tax brackets increases.



