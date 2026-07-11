"""High-precision base-10 exponent operations."""

from decimal import Decimal, InvalidOperation

from backend.core.math.exceptions import PrecisionError
from backend.core.math.precision import scientific_context
from backend.core.math.validation import _finite_decimal


def pow10_decimal(value: Decimal) -> Decimal:
    """Return 10 raised to a finite Decimal exponent at 50-digit precision.

    Args:
        value: Finite Decimal exponent.

    Raises:
        PrecisionError: If the exponent is invalid or cannot be evaluated.
    """

    try:
        value = _finite_decimal(value, "pow10 exponent")
        with scientific_context() as context:
            return context.power(Decimal("10"), value)
    except (InvalidOperation, ValueError) as error:
        raise PrecisionError("Unable to calculate 10 raised to the supplied exponent.") from error
