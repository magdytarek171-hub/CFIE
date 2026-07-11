"""Explicit Decimal context management for ES-004."""

from contextlib import contextmanager
from decimal import Context, Decimal, localcontext
from typing import Iterator

from backend.core.math.constants import DECIMAL_PRECISION, DECIMAL_ROUNDING


def decimal_context() -> Context:
    """Return a fresh Context implementing CFIE's 50-digit rounding policy.

    Returns:
        A Decimal context with 50 significant digits and half-even rounding.
    """

    return Context(prec=DECIMAL_PRECISION, rounding=DECIMAL_ROUNDING)


@contextmanager
def scientific_context() -> Iterator[Context]:
    """Apply the CFIE Decimal policy for one explicit calculation scope.

    Yields:
        The active 50-digit Decimal context.
    """

    with localcontext(decimal_context()) as context:
        yield context


def apply_precision(value: Decimal) -> Decimal:
    """Apply the global Decimal policy to an explicitly supplied Decimal.

    Args:
        value: Finite Decimal value to normalize under the policy.

    Returns:
        Value rounded only according to the configured global policy.
    """

    with scientific_context() as context:
        return context.plus(value)
