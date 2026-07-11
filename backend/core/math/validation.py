"""Decimal validation functions for reusable scientific mathematics."""

from decimal import Decimal

from backend.core.math.exceptions import ValidationError


def _finite_decimal(value: Decimal, name: str) -> Decimal:
    if not isinstance(value, Decimal):
        raise ValidationError(f"{name} must be a Decimal; float values are not accepted.")
    if not value.is_finite():
        raise ValidationError(f"{name} must be finite.")
    return value


def validate_positive(value: Decimal, name: str = "value") -> Decimal:
    """Validate a finite Decimal greater than zero.

    Args:
        value: Value to validate.
        name: Human-readable field name for exception messages.
    """

    value = _finite_decimal(value, name)
    if value <= Decimal("0"):
        raise ValidationError(f"{name} must be greater than zero.")
    return value


def validate_non_negative(value: Decimal, name: str = "value") -> Decimal:
    """Validate a finite Decimal that is zero or greater."""

    value = _finite_decimal(value, name)
    if value < Decimal("0"):
        raise ValidationError(f"{name} must be non-negative.")
    return value


def validate_probability(value: Decimal, name: str = "probability") -> Decimal:
    """Validate a finite Decimal probability on the inclusive zero-to-one basis."""

    value = _finite_decimal(value, name)
    if not Decimal("0") <= value <= Decimal("1"):
        raise ValidationError(f"{name} must be between 0 and 1 inclusive.")
    return value


def validate_pH(value: Decimal, name: str = "pH") -> Decimal:
    """Validate a finite Version 1 cosmetic aqueous-formulation pH value."""

    value = _finite_decimal(value, name)
    if not Decimal("0.00") <= value <= Decimal("14.00"):
        raise ValidationError(f"{name} must be between 0.00 and 14.00 inclusive.")
    return value


def validate_concentration(value: Decimal, name: str = "concentration") -> Decimal:
    """Validate a finite non-negative Decimal concentration without unit checks."""

    return validate_non_negative(value, name)
