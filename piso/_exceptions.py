class ClosedMismatchError(ValueError):
    def __init__(self):
        """
        Create a `ClosedMismatchError` indicating that interval objects did not have same `closed` values.
        """
        super().__init__(
            "The arguments must have the same value for the `closed` attribute"
        )


class ClosedValueError(ValueError):
    def __init__(self, param):
        """
        Create a `ClosedValueError` indicating that interval object did not have valid `closed` value.
        """
        super().__init__(f"Unsupported value for `closed` attribute: {param.closed}")


class DegenerateIntervalError(ValueError):
    def __init__(self, param):
        """
        Create a `DegenerateIntervalError` indicating that interval has zero length.
        """
        super().__init__(f"Zero lengths intervals: {param} - not supported by piso.")
