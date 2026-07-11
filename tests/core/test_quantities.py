"""Tests for ES-002 quantities and unit conversion boundaries."""

from decimal import Decimal

import pytest

from backend.core import Quantity
from backend.core.exceptions import IncompatibleUnitError, InvalidUnitError


@pytest.mark.parametrize(
    ("source_value", "source_unit", "target_unit", "expected_value"),
    [
        ("1", "kg", "g", Decimal("1000")),
        ("1", "g", "mg", Decimal("1000")),
        ("1", "mg", "µg", Decimal("1000")),
        ("1000", "mL", "L", Decimal("1")),
        ("1", "mol", "mmol", Decimal("1000")),
        ("1", "mol/L", "mmol/L", Decimal("1000")),
        ("1", "% w/w", "ppm", Decimal("10000")),
        ("1", "ppm", "ppb", Decimal("1000")),
        ("1000000", "ppb", "% w/w", Decimal("1")),
    ],
)
def test_convert_approved_compatible_units(
    source_value: str,
    source_unit: str,
    target_unit: str,
    expected_value: Decimal,
) -> None:
    """Approved unit families convert exactly with Decimal values."""

    assert Quantity(source_value, source_unit).to(target_unit).value == expected_value


@pytest.mark.parametrize("unit", ["% w/v", "pH", "pKa"])
def test_identity_only_units_convert_to_themselves(unit: str) -> None:
    """Dimensions without a conversion partner permit identity conversion only."""

    quantity = Quantity("7.5", unit)

    assert quantity.to(unit) == quantity


@pytest.mark.parametrize(
    ("source_unit", "target_unit"),
    [
        ("g", "mL"),
        ("mol", "mol/L"),
        ("% w/w", "% w/v"),
        ("pH", "pKa"),
        ("pKa", "ppm"),
    ],
)
def test_cross_dimension_conversion_is_rejected(source_unit: str, target_unit: str) -> None:
    """Conversions requiring missing information are rejected, never inferred."""

    with pytest.raises(IncompatibleUnitError, match="No density"):
        Quantity("1", source_unit).to(target_unit)


def test_unknown_target_unit_is_rejected() -> None:
    """A target outside the approved set cannot be converted to."""

    with pytest.raises(InvalidUnitError, match="Unsupported unit"):
        Quantity("1", "g").to("oz")


@pytest.mark.parametrize("value", [1.5, True, None, object()])
def test_quantity_rejects_non_exact_numeric_input(value: object) -> None:
    """Floats and unsupported values cannot introduce precision ambiguity."""

    with pytest.raises(TypeError, match="Decimal, int, or decimal string"):
        Quantity(value, "g")  # type: ignore[arg-type]


@pytest.mark.parametrize("value", ["not-a-number", "NaN", "Infinity"])
def test_quantity_rejects_invalid_or_non_finite_values(value: str) -> None:
    """Scientific quantities must always contain finite decimal values."""

    with pytest.raises(ValueError):
        Quantity(value, "g")
