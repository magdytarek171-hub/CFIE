"""Tests for ES-004 mathematical utilities."""

from decimal import Decimal

import pytest

from backend.core.math import log10_decimal, pow10_decimal
from backend.core.math.exceptions import MathematicalDomainError, ValidationError
from backend.core.math.precision import apply_precision, decimal_context
from backend.core.math.validation import validate_concentration, validate_pH, validate_probability


def test_logarithm_and_power() -> None:
    assert log10_decimal(Decimal("100")) == Decimal("2")
    assert pow10_decimal(Decimal("2")) == Decimal("100")


@pytest.mark.parametrize("value", [Decimal("0"), Decimal("-1"), Decimal("NaN")])
def test_logarithm_rejects_invalid_domain(value: Decimal) -> None:
    with pytest.raises(MathematicalDomainError):
        log10_decimal(value)


def test_precision_policy() -> None:
    assert decimal_context().prec == 50
    assert apply_precision(Decimal("1.23456789012345678901234567890123456789012345678901"))


@pytest.mark.parametrize("value", [Decimal("0"), Decimal("1")])
def test_probability_bounds(value: Decimal) -> None:
    assert validate_probability(value) == value


@pytest.mark.parametrize("value", [Decimal("-0.01"), Decimal("1.01")])
def test_probability_rejects_outside_bounds(value: Decimal) -> None:
    with pytest.raises(ValidationError):
        validate_probability(value)


def test_ph_and_concentration_validators() -> None:
    assert validate_pH(Decimal("14.00")) == Decimal("14.00")
    assert validate_concentration(Decimal("0")) == Decimal("0")
    with pytest.raises(ValidationError):
        validate_pH(Decimal("14.01"))
