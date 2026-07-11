"""Tests for ES-003 immutable chemistry data models."""

from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from backend.core.chemistry import AcidBasePair, BufferSystem, Compound, DensityMeasurement


def _compound(*, purity: Decimal = Decimal("0.980")) -> Compound:
    """Build a structural test record without using real chemical data."""

    return Compound(
        common_name="Test", inci_name="Test", chemical_formula="Test", cas_number="Test",
        molecular_weight=Decimal("100"), purity=purity, hydration_state="Test", charge=-1,
        pka_values=(Decimal("4"),), aliases=("Alias",), references=("Reference",),
        density=DensityMeasurement(Decimal("1"), Decimal("20")), supplier_name="Supplier",
    )


def test_compound_is_immutable_and_preserves_explicit_metadata() -> None:
    """Compound fields retain approved Decimal and tuple metadata unchanged."""

    compound = _compound()

    assert compound.density == DensityMeasurement(Decimal("1"), Decimal("20"))
    assert compound.pka_values == (Decimal("4"),)
    with pytest.raises(FrozenInstanceError):
        compound.purity = Decimal("1")  # type: ignore[misc]


@pytest.mark.parametrize("purity", [Decimal("-0.001"), Decimal("1.001"), Decimal("NaN")])
def test_compound_rejects_invalid_purity(purity: Decimal) -> None:
    """Purity must be a finite Decimal on the approved zero-to-one basis."""

    with pytest.raises(ValueError):
        _compound(purity=purity)


def test_compound_rejects_mutable_pka_values() -> None:
    """Ordered scientific values must be immutable tuples."""

    with pytest.raises(TypeError, match="immutable tuple"):
        Compound(
            common_name="Test", inci_name="Test", chemical_formula="Test", cas_number="Test",
            molecular_weight=Decimal("100"), purity=Decimal("1"), hydration_state="Test", charge=0,
            pka_values=[Decimal("4")], aliases=(), references=(),  # type: ignore[arg-type]
        )


def test_acid_base_pair_and_buffer_system_preserve_relationships() -> None:
    """Relationship records accept only explicit compounds and ordered ranges."""

    acid = _compound()
    pair = AcidBasePair(acid, acid, Decimal("4"), 1)
    system = BufferSystem("Test", pair, (Decimal("3"), Decimal("5")),
                          (Decimal("3.5"), Decimal("4.5")), ("Reference",))

    assert system.acid_base_pair is pair
    with pytest.raises(ValueError, match="positive"):
        AcidBasePair(acid, acid, Decimal("4"), 0)
    with pytest.raises(ValueError, match="lower bound"):
        BufferSystem("Test", pair, (Decimal("5"), Decimal("3")),
                     (Decimal("3"), Decimal("5")), ())
