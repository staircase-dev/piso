<p align="center"><a href="https://github.com/staircase-dev/piso"><img src="https://github.com/staircase-dev/piso/blob/master/docs/img/piso_social_transparent.svg" title="piso logo" alt="piso logo"></a></p>

<p align="center">
    <a href="https://www.python.org/" alt="Python version">
        <img src="https://img.shields.io/pypi/pyversions/piso" /></a>
    <a href="https://pypi.org/project/piso/" alt="PyPI version">
        <img src="https://img.shields.io/pypi/v/piso" /></a>
    <a href="https://anaconda.org/conda-forge/piso" alt="Conda Forge version">
        <img src="https://anaconda.org/conda-forge/piso/badges/version.svg?branch=master&kill_cache=1" /></a>
	<a href="https://github.com/staircase-dev/piso/actions/workflows/ci.yml" alt="Github CI">
		<img src="https://github.com/staircase-dev/piso/actions/workflows/ci.yml/badge.svg"/></a>
    <a href="https://piso.readthedocs.io" alt="Documentation">
        <img src="https://readthedocs.org/projects/piso/badge/?version=latest" /></a>
</p>

# piso - pandas interval set operations

**piso** exists to bring set operations (union, intersection, difference + more), analytical methods, and lookup and join functionality to [pandas'](https://pandas.pydata.org/) interval classes, specifically

    - pandas.Interval
    - pandas.arrays.IntervalArray
    - pandas.IntervalIndex

Currently, there is a lack of such functionality in pandas, although it has been earmarked for development.  Until this eventuates, piso aims to fill the void.  Many of the methods can be used via accessors, which can be registered to `pandas.arrays.IntervalArray` and `pandas.IntervalIndex` classes, for example:

```python
>>> import pandas as pd
>>> import piso
>>> piso.register_accessors()

>>> arr = pd.arrays.IntervalArray.from_tuples(
...        [(1,5), (3,6), (2,4)]
...    )

>>> arr.piso.intersection()
<IntervalArray>
[(3, 4]]
Length: 1, closed: right, dtype: interval[int64]

>>> arr.piso.contains([2, 3, 5])
            2      3      5
(1, 5]   True   True   True
(3, 6]  False  False   True
(2, 4]  False   True  False

>>> df = pd.DataFrame(
...     {"A":[4,3], "B":["x","y"]},
...     index=pd.IntervalIndex.from_tuples([(1,3), (5,7)]),
... )

>>> s = pd.Series(
...     [True, False],
...     index=pd.IntervalIndex.from_tuples([(2,4), (5,6)]),
...     name="C",
... )

>>> piso.join(df, s)
        A  B      C
(1, 2]  4  x    NaN
(2, 3]  4  x   True
(5, 6]  3  y  False
(6, 7]  3  y    NaN

>>> piso.join(df, s, how="inner")
        A  B      C
(2, 3]  4  x   True
(5, 6]  3  y  False
```

The domain of the intervals can be either numerical, `pandas.Timestamp` or `pandas.Timedelta`.

Several [case studies](https://piso.readthedocs.io/en/latest/user_guide/case_studies/index.html) using piso can be found in the [user guide](https://piso.readthedocs.io/en/latest/user_guide/index.html).  Further examples, and a detailed explanation of functionality, are provided in the [API reference](https://piso.readthedocs.io/en/latest/reference/index.html).

Visit [https://piso.readthedocs.io](https://piso.readthedocs.io/) for the documentation.

## Installation

`piso` can be installed from PyPI or Anaconda.

To install the latest version from PyPI::

```sh
python -m pip install piso
```

To install the latest version through conda-forge::

```sh
conda install -c conda-forge piso
```

## Versioning

[SemVer](http://semver.org/) is used by piso for versioning releases.  For versions available, see the [tags on this repository](https://github.com/staircase-dev/piso/tags).

## License

This project is licensed under the [MIT License](https://github.com/staircase-dev/piso/blob/master/LICENSE)

## Acknowledgments

Currently, piso is a pure-python implentation which relies heavily on [staircase](https://www.staircase.dev) and [pandas](https://pandas.pydata.org/).  It is designed to operate as part of the *pandas ecosystem*.  The colours for the piso logo have been assimilated from pandas as a homage, and is not to intended to imply and affiliation with, or endorsement by, pandas.

Additionally, two classes have been borrowed, almost verbatim, from the pandas source code:

    - `pandas.util._decorators.Appender`
    - `pandas.core.accessor.CachedAccessor`