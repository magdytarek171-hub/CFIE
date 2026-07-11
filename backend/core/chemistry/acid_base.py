"""Immutable acid-base relationship data models for ES-003."""

from dataclasses import dataclass
from decimal import Decimal

from backend.core.chemistry.compound import Compound, _require_finite_decimal, _require_string_tuple

DecimalRange = tuple[Decimal, Decimal]


@dataclass(frozen=True, slots=True)
class AcidBasePair:
    """An explicit acid and conjugate-base relationship.

    Args:
        acid: Compound representing the acid form.
        conjugate_base: Compound representing the conjugate-base form.
        pka: Supplied pKa value for this dissociation step.
        dissociation_step: Positive integer ordinal for the dissociation step.
    """

    acid: Compound
    conjugate_base: Compound
    pka: Decimal
    dissociation_step: int

    def __post_init__(self) -> None:
        """Validate supplied relationship metadata without deriving any values."""

        if not isinstance(self.acid, Compound):
            raise TypeError("acid must be a Compound.")
        if not isinstance(self.conjugate_base, Compound):
            raise TypeError("conjugate_base must be a Compound.")
        _require_finite_decimal("pka", self.pka)
        if isinstance(self.dissociation_step, bool) or not isinstance(self.dissociation_step, int):
            raise TypeError("dissociation_step must be an integer.")
        if self.dissociation_step < 1:
            raise ValueError("dissociation_step must be a positive integer.")


@dataclass(frozen=True, slots=True)
class BufferSystem:
    """An immutable buffer-system description based on an acid-base pair.

    Args:
        name: Traceable name of the buffer system.
        acid_base_pair: Fundamental acid-base relationship for the system.
        valid_pH_range: Inclusive ``(lower_bound, upper_bound)`` pH range.
        optimal_buffer_range: Inclusive ``(lower_bound, upper_bound)`` range.
        references: Immutable source references for traceability.
    """

    name: str
    acid_base_pair: AcidBasePair
    valid_pH_range: DecimalRange
    optimal_buffer_range: DecimalRange
    references: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate structural range metadata without performing calculations."""

        if not isinstance(self.acid_base_pair, AcidBasePair):
            raise TypeError("acid_base_pair must be an AcidBasePair.")
        _validate_decimal_range("valid_pH_range", self.valid_pH_range)
        _validate_decimal_range("optimal_buffer_range", self.optimal_buffer_range)
        _require_string_tuple("references", self.references)


def _validate_decimal_range(field_name: str, value: DecimalRange) -> None:
    """Validate an inclusive two-value Decimal range.

    Args:
        field_name: Model field being validated.
        value: Expected lower and upper Decimal bounds.
    """

    if not isinstance(value, tuple) or len(value) != 2:
        raise TypeError(f"{field_name} must be an immutable two-item tuple.")
    lower_bound, upper_bound = value
    _require_finite_decimal(field_name, lower_bound)
    _require_finite_decimal(field_name, upper_bound)
    if lower_bound > upper_bound:
        raise ValueError(f"{field_name} lower bound must not exceed its upper bound.")
