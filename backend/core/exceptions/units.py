"""Exceptions for validation and compatibility failures in unit operations."""


class InvalidUnitError(ValueError):
    """Raised when a value does not identify a unit supported by CFIE.

    Args:
        unit: Value supplied where a supported unit was required.
    """

    def __init__(self, unit: object) -> None:
        super().__init__(f"Unsupported unit: {unit!r}.")


class IncompatibleUnitError(ValueError):
    """Raised when conversion is requested across different unit dimensions.

    Args:
        source_unit: Unit held by the source quantity.
        target_unit: Unit requested for the conversion.
        reason: Optional additional explanation of the missing information.
    """

    def __init__(self, source_unit: str, target_unit: str, reason: str | None = None) -> None:
        message = (
            f"Cannot convert from {source_unit!r} to {target_unit!r}: incompatible dimensions."
        )
        if reason is not None:
            message = f"{message} {reason}"
        super().__init__(message)
