"""Dissociation-step data model."""

from dataclasses import dataclass
from decimal import Decimal

from backend.core.chemistry.polyprotic.validation import validate_pka, validate_step_number


@dataclass(frozen=True, slots=True)
class DissociationStep:
    """Explicit structural link between two consecutive dissociation species.

    Args:
        step_number: One-based contiguous dissociation ordinal.
        pka: Finite, supplied pKa value.
        acid_species_id: Identifier of the preceding species.
        base_species_id: Identifier of the next species.
    """

    step_number: int
    pka: Decimal
    acid_species_id: str
    base_species_id: str

    def __post_init__(self) -> None:
        """Validate the independently supplied step metadata."""

        validate_step_number(self.step_number)
        validate_pka(self.pka)
