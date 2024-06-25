.. _release_notes:

========================
Release notes
========================


**v1.1.0 2024-06-25**

- support for Python 3.12 added
- support for Python 3.7 removed


**v1.0.0 2023-07-05**

- Compatibility with pandas 2
- Better handling of empty intervals in set operations (#GH56)


**v0.9.0 2022-05-04**

- Extended :func:`piso.adjacency_matrix` and :meth:`ArrayAccessor.adjacency_matrix() <piso.accessor.ArrayAccessor.adjacency_matrix>` to take multiple interval array parameters

Added the following methods

- :func:`piso.bridge`
- :meth:`ArrayAccessor.bridge() <piso.accessor.ArrayAccessor.bridge>`


**v0.8.0 2022-01-29**

- Added `bins` parameter to :func:`piso.coverage` and :meth:`ArrayAccessor.coverage() <piso.accessor.ArrayAccessor.coverage>`
- Added `how` parameter to :func:`piso.coverage` and :meth:`ArrayAccessor.coverage() <piso.accessor.ArrayAccessor.coverage>`
- Added `result` parameter to :func:`piso.contains` and :meth:`ArrayAccessor.contains() <piso.accessor.ArrayAccessor.contains>`
- Added `how` parameter to :func:`piso.contains` and :meth:`ArrayAccessor.contains() <piso.accessor.ArrayAccessor.contains>`


**v0.7.0 2021-11-20**

Added the following methods

- :func:`piso.split`
- :func:`piso.adjacency_matrix`
- :meth:`ArrayAccessor.split() <piso.accessor.ArrayAccessor.split>`
- :meth:`ArrayAccessor.adjacency_matrix() <piso.accessor.ArrayAccessor.adjacency_matrix>`

Removed the following methods

- removed :func:`piso.get_indexer` in favour of :meth:`pandas.IntervalIndex.get_indexer`


**v0.6.0 2021-11-05**

The following methods were extended to accommodate intervals with *closed = "both"* or *"neither"*

- :func:`piso.contains` (and :meth:`ArrayAccessor.contains() <piso.accessor.ArrayAccessor.contains>`)
- :func:`piso.get_indexer` (and :meth:`ArrayAccessor.get_indexer() <piso.accessor.ArrayAccessor.get_indexer>`)
- :func:`piso.lookup`
- :func:`piso.isdisjoint` (and :meth:`ArrayAccessor.isdisjoint() <piso.accessor.ArrayAccessor.isdisjoint>`)


**v0.5.0 2021-11-02**

Added the following methods

- :func:`piso.join` for *join operations* with interval indexes
- :func:`piso.contains`
- :meth:`ArrayAccessor.contains() <piso.accessor.ArrayAccessor.contains>`

Performance improvements for

- :func:`piso.lookup`
- :func:`piso.get_indexer`


**v0.4.0 2021-10-30**

Added the following methods

- :func:`piso.lookup`
- :func:`piso.get_indexer`
- :meth:`ArrayAccessor.get_indexer`


**v0.3.0 2021-10-23**

Added the following methods

- :func:`piso.coverage`
- :func:`piso.complement`
- :meth:`ArrayAccessor.coverage() <piso.accessor.ArrayAccessor.coverage>`
- :meth:`ArrayAccessor.complement() <piso.accessor.ArrayAccessor.complement>`


**v0.2.0 2021-10-15**

Added the following methods

- :func:`piso.isdisjoint`
- :func:`piso.issuperset`
- :func:`piso.issubset`
- :meth:`ArrayAccessor.isdisjoint() <piso.accessor.ArrayAccessor.isdisjoint>`
- :meth:`ArrayAccessor.issuperset() <piso.accessor.ArrayAccessor.issuperset>`
- :meth:`ArrayAccessor.issubset() <piso.accessor.ArrayAccessor.issubset>`
- :meth:`piso.interval.issuperset`
- :meth:`piso.interval.issubset`


**v0.1.0 2021-10-10**

The following methods are included in the initial release of `piso`

- :func:`piso.register_accessors`
- :func:`piso.union`
- :func:`piso.intersection`
- :func:`piso.difference`
- :func:`piso.symmetric_difference`
- :meth:`ArrayAccessor.union() <piso.accessor.ArrayAccessor.union>`
- :meth:`ArrayAccessor.intersection() <piso.accessor.ArrayAccessor.intersection>`
- :meth:`ArrayAccessor.difference() <piso.accessor.ArrayAccessor.difference>`
- :meth:`ArrayAccessor.symmetric_difference() <piso.accessor.ArrayAccessor.symmetric_difference>`
- :func:`piso.interval.union`
- :func:`piso.interval.intersection`
- :func:`piso.interval.difference`
- :func:`piso.interval.symmetric_difference`

