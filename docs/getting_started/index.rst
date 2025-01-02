.. _getting_started:

Getting Started
===============

Installation
----------------

`piso` can be installed from PyPI or Anaconda.

To install the latest version from PyPI::

    python -m pip install piso

To install the latest version through conda-forge::

    conda install -c conda-forge piso


Package overview
----------------

`piso` exists to bring set operations (union, intersection, difference + more), analytical methods, and lookup and join functionality to :mod:`pandas` interval classes, specifically

    - :class:`pandas.Interval`
    - :class:`pandas.arrays.IntervalArray`
    - :class:`pandas.IntervalIndex`

Currently, there is a lack of such functionality in `pandas`, although it has been earmarked for development.  Until this eventuates, `piso` aims to fill the void.  Many of the methods can be used via accessors, which can be registered to :class:`pandas.arrays.IntervalArray` and :class:`pandas.IntervalIndex` classes.

An array of intervals can be interpreted in two different ways.  It can be seen as a container for intervals, which are sets, or if the intervals are disjoint it may be seen as a set itself.  Both interpretations are supported by the methods introduced by :mod:`piso`.

The domain of the intervals can be either numerical, :class:`pandas.Timestamp` or :class:`pandas.Timedelta`.  Currently, most of the set operaitons in :mod:`piso` are limited to intervals which:

    - have a non-zero length
    - have a finite, length
    - are left-closed right-open, or right-closed left-open

To check if these restrictions apply to a particular method, please consult the :ref:`api`.

Several :ref:`case studies <case_studies>` using :mod:`piso` can be found in the :ref:`user guide <user_guide>`.  Further examples, and a detailed explanation of functionality, are provided in the :ref:`api`.


Versioning
-----------

`SemVer <http://semver.org/>`_ is used by :mod:`piso` for versioning releases.  For versions available, see the `tags on this repository <https://github.com/staircase-dev/piso/tags>`_.


License
--------

This project is licensed under the MIT License::

    Copyright © 2021-2025 <Riley Clement>

    Permission is hereby granted, free of charge, to any person obtaining a copy of this
    software and associated documentation files (the “Software”), to deal in the Software
    without restriction, including without limitation the rights to use, copy, modify, 
    merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
    permit persons to whom the Software is furnished to do so, subject to the following 
    conditions:

    The above copyright notice and this permission notice shall be included in all copies 
    or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
    PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
    FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
    DEALINGS IN THE SOFTWARE.


Acknowledgments
----------------

Currently, :mod:`piso` is a pure-python implentation which relies heavily on :mod:`staircase` and :mod:`pandas`.
It is clearly designed to operate as part of the *pandas ecosystem*.  The colours for the piso logo have been assimilated from pandas as a homage, and is not to intended to imply and affiliation with, or endorsement by, pandas.

Additionally, two classes have been borrowed, almost verbatim, from the pandas source code:

    - :class:`pandas.util._decorators.Appender`
    - :class:`pandas.core.accessor.CachedAccessor`


