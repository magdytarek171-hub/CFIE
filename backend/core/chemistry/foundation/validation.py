"""Structural validation for ES-005 models."""
from decimal import Decimal
def validate_pka(value: Decimal) -> Decimal:
    """Validate a finite Decimal pKa value."""
    if not isinstance(value, Decimal) or not value.is_finite(): raise ValueError("pKa must be a finite Decimal.")
    return value
def validate_step(value: int) -> int:
    """Validate a positive integer dissociation step."""
    if isinstance(value, bool) or not isinstance(value, int) or value < 1: raise ValueError("dissociation_step must be a positive integer.")
    return value
