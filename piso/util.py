import staircase as sc

from piso._exceptions import ClosedValueError, DegenerateIntervalError


def _validate_intervals(interval_array):
    if not all(interval_array.length):  # test for degenerate intervals
        raise DegenerateIntervalError(interval_array)
    if interval_array.closed not in ("left", "right"):
        raise ClosedValueError


def _interval_x_to_stairs(interval_array):
    # can be used with interval, interval array, interval index
    assert interval_array.closed in {"left", "right"}
    return sc.Stairs(
        start=interval_array.left,
        end=interval_array.right,
        closed=interval_array.closed,
    )


def _boolean_stairs_to_interval_array(stairs, cls):
    if stairs.identical(0):
        return cls([], closed=stairs.closed)
    return cls.from_arrays(
        stairs.step_changes.index[::2],
        stairs.step_changes.index[1::2],
        closed=stairs.closed,
    )
