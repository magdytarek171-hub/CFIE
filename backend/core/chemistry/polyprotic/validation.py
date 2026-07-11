"""Structural validation helpers for ES-007."""

from decimal import Decimal


def validate_pka(value: Decimal) -> Decimal:
    """Validate that a pKa value is a finite Decimal."""

    if not isinstance(value, Decimal) or not value.is_finite():
        raise ValueError("pKa values must be finite Decimal values.")
    return value


def validate_step_number(value: int) -> int:
    """Validate a positive, one-based dissociation-step number."""

    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError("Dissociation step numbers must be positive integers starting at 1.")
    return value
