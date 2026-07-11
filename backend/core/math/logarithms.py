"""High-precision base-10 logarithm operations."""

from decimal import Decimal, InvalidOperation

from backend.core.math.exceptions import MathematicalDomainError, PrecisionError
from backend.core.math.precision import scientific_context
from backend.core.math.validation import validate_positive


def log10_decimal(value: Decimal) -> Decimal:
    """Return the base-10 logarithm of a positive Decimal at 50-digit precision.

    Args:
        value: Positive finite Decimal input.

    Raises:
        MathematicalDomainError: If ``value`` is not finite and greater than zero.
        PrecisionError: If Decimal cannot produce the logarithm under policy.
    """

    try:
        value = validate_positive(value, "log10 input")
    except Exception as error:
        raise MathematicalDomainError("log10 input must be a finite Decimal greater than zero.") from error
    try:
        with scientific_context() as context:
            return value.log10(context=context)
    except (InvalidOperation, ValueError) as error:
        raise PrecisionError("Unable to calculate log10 under the configured Decimal policy.") from error
