import itertools

import numpy as np
import pandas as pd

import piso.docstrings.ndframe as docstrings
from piso import intervalarray
from piso._decorators import Appender


@Appender(docstrings.lookup_docstring, join="\n", indents=1)
def lookup(frame_or_series, x):
    if not isinstance(frame_or_series.index, pd.IntervalIndex):
        raise ValueError("DataFrame or Series must be indexed by an IntervalIndex")
    if not hasattr(x, "__len__"):
        x = np.array(x, ndmin=1)
    indexer = frame_or_series.index.get_indexer(x)
    result = frame_or_series.copy().iloc[indexer].set_axis(x)
    set_nan = indexer == -1
    if set_nan.any():
        result.loc[set_nan] = np.nan
    return result


def _assert_has_disjoint_interval_index(frame_or_series):
    if not isinstance(frame_or_series.index, pd.IntervalIndex):
        raise ValueError(
            "Dataframe, or Series, should have IntervalIndex only.  Found {type(frame_or_series.index)}."
        )
    if frame_or_series.index.is_overlapping:
        raise ValueError(
            "IntervalIndex of DataFrame, or Series, cannot contain overlapping intervals."
        )


def _get_valid_closed(indexes):
    if not all([indexes[0].closed == index.closed for index in indexes[1:]]):
        raise ValueError("All IntervalIndex must have the same closed attribute.")
    closed = indexes[0].closed
    if closed not in ("left", "right"):
        raise ValueError(
            f"Only IntervalIndex with closed attribute of 'left' or 'right' supported.  Found '{closed}'."
        )
    return closed


def _get_indexers(*dfs):
    closed = _get_valid_closed([df.index for df in dfs])
    breaks = itertools.chain(
        itertools.chain.from_iterable(df.index.left.values for df in dfs),
        itertools.chain.from_iterable(df.index.right.values for df in dfs),
    )
    tiling_index = pd.IntervalIndex.from_breaks(sorted(set(breaks)))
    lookups = tiling_index.left if closed == "left" else tiling_index.right
    indexers = [df.index.get_indexer(lookups) for df in dfs]
    return tiling_index, indexers


def _handle_overlapping_columns(frames, suffixes):
    col_counts = pd.Series.value_counts(list(itertools.chain.from_iterable(frames)))
    common_columns = col_counts[col_counts > 1].index
    if len(common_columns) > 0:
        if len(suffixes) != len(frames):
            raise ValueError(
                "Overlapping column names found.  A suffix must be supplied for every join argument."
            )
        frames = [
            df.rename(columns=dict(zip(common_columns, common_columns + suffix)))
            for df, suffix in zip(frames, suffixes)
        ]
    return frames


@Appender(docstrings.join_docstring, join="\n", indents=1)
def join(*frames_or_series, how="left", suffixes=None, sort=False):
    if len(frames_or_series) < 2:
        raise ValueError("Join operation requires more than one operand.")
    for obj in frames_or_series:
        _assert_has_disjoint_interval_index(obj)

    def frameify(obj):
        if isinstance(obj, pd.Series):
            if obj.name is None:
                raise ValueError("Series arguments to join must be named.")
            obj = obj.to_frame()
        return obj

    if suffixes is None:
        suffixes = []
    new_frames = [frameify(obj) for obj in frames_or_series]
    return _join(*new_frames, how=how, suffixes=suffixes, sort=sort)


def _join(*frames, how, suffixes, sort):

    tiling_index, indexers = _get_indexers(*frames)

    if how in ("left", "right"):
        i = 0 if how == "left" else -1
        final_indexer = indexers[i] >= 0
    else:
        stacked_indexers = np.stack(indexers) >= 0
        log_func = np.any if how == "outer" else np.all
        final_indexer = log_func(stacked_indexers, axis=0)

    def _reindex(df, indexer):
        adjusted_indexer = final_indexer & (indexer >= 0)
        return df.iloc[indexer[adjusted_indexer]].set_index(
            tiling_index[adjusted_indexer]
        )

    new_frames = [_reindex(df, indexer) for df, indexer in zip(frames, indexers)]
    new_frames = _handle_overlapping_columns(new_frames, suffixes)

    if how == "right":
        # hack for pandas not working with right joins on interval index (for unknown reasons)
        columns = list(itertools.chain.from_iterable([df.columns for df in new_frames]))
        return new_frames[-1].join(new_frames[:-1], how="left", sort=sort)[columns]
    return pd.DataFrame.join(new_frames[0], new_frames[1:], how=how, sort=sort)
