import numpy as np
import pandas as pd

import piso.docstrings.ndframe as docstrings
from piso import intervalarray
from piso._decorators import Appender


@Appender(docstrings.lookup_docstring, join="\n", indents=1)
def lookup(frame_or_series, x):
    if not isinstance(frame_or_series.index, pd.IntervalIndex):
        raise ValueError("DataFrame or Series must be indexed by an IntervalIndex")
    indexer = intervalarray.get_indexer(frame_or_series.index, x)
    if not hasattr(indexer, "__len__"):
        indexer = np.array([indexer])
    if not hasattr(x, "__len__"):
        x = [x]
    return (
        frame_or_series.__class__(
            data=frame_or_series,
            index=x,
        )
        .iloc[indexer >= 0]
        .reindex(x)
    )
