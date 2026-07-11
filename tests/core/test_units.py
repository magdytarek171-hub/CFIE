"""Tests for ES-002 unit validation and definitions."""

import pytest

from backend.core.exceptions import InvalidUnitError
from backend.core.units import Unit
from backend.core.units.definitions import parse_unit


@pytest.mark.parametrize("unit", list(Unit))
def test_parse_unit_accepts_every_approved_unit(unit: Unit) -> None:
    """Every approved unit is accepted as an enum member and exact text."""

    assert parse_unit(unit) is unit
    assert parse_unit(unit.value) is unit


@pytest.mark.parametrize("unit", ["ug", "%w/w", "M", "density", ""])
def test_parse_unit_rejects_unknown_text(unit: str) -> None:
    """Unapproved text produces the domain validation exception."""

    with pytest.raises(InvalidUnitError, match="Unsupported unit"):
        parse_unit(unit)


@pytest.mark.parametrize("unit", [None, 1, object()])
def test_parse_unit_rejects_non_text_values(unit: object) -> None:
    """Non-text, non-enum values cannot be silently treated as units."""

    with pytest.raises(InvalidUnitError, match="Unsupported unit"):
        parse_unit(unit)  # type: ignore[arg-type]
