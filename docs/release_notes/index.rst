.. _release_notes:

========================
Release notes
========================


- added :func:`piso.join` for *join operations* with interval indexes
- faster implementation for :func:`piso.get_indexer`

ADD UNRELEASED CHANGES ABOVE THIS LINE


**v0.4.0 2021-10-30**

Added the following methods

- :meth:`piso.lookup`
- :meth:`piso.get_indexer`
- :meth:`ArrayAccessor.get_indexer() <piso.accessor.ArrayAccessor.get_indexer>`


**v0.3.0 2021-10-23**

Added the following methods

- :meth:`piso.coverage`
- :meth:`piso.complement`
- :meth:`ArrayAccessor.coverage() <piso.accessor.ArrayAccessor.coverage>`
- :meth:`ArrayAccessor.complement() <piso.accessor.ArrayAccessor.complement>`


**v0.2.0 2021-10-15**

Added the following methods

- :meth:`piso.isdisjoint`
- :meth:`piso.issuperset`
- :meth:`piso.issubset`
- :meth:`ArrayAccessor.isdisjoint() <piso.accessor.ArrayAccessor.isdisjoint>`
- :meth:`ArrayAccessor.issuperset() <piso.accessor.ArrayAccessor.issuperset>`
- :meth:`ArrayAccessor.issubset() <piso.accessor.ArrayAccessor.issubset>`
- :meth:`piso.interval.issuperset`
- :meth:`piso.interval.issubset`


**v0.1.0 2021-10-10**

The following methods are included in the initial release of `piso`

- :meth:`piso.register_accessors`
- :meth:`piso.union`
- :meth:`piso.intersection`
- :meth:`piso.difference`
- :meth:`piso.symmetric_difference`
- :meth:`ArrayAccessor.union() <piso.accessor.ArrayAccessor.union>`
- :meth:`ArrayAccessor.intersection() <piso.accessor.ArrayAccessor.intersection>`
- :meth:`ArrayAccessor.difference() <piso.accessor.ArrayAccessor.difference>`
- :meth:`ArrayAccessor.symmetric_difference() <piso.accessor.ArrayAccessor.symmetric_difference>`
- :meth:`piso.interval.union`
- :meth:`piso.interval.intersection`
- :meth:`piso.interval.difference`
- :meth:`piso.interval.symmetric_difference`

