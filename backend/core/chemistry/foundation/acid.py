"""Acid species model."""
from dataclasses import dataclass
from decimal import Decimal
from backend.core.chemistry.foundation.validation import validate_pka, validate_step
@dataclass(frozen=True, slots=True)
class AcidSpecies:
    """Immutable acid species with an identifier for its conjugate base."""
    name: str; formula: str; charge: int; dissociation_step: int; pka: Decimal; conjugate_species_id: str
    def __post_init__(self) -> None:
        validate_step(self.dissociation_step); validate_pka(self.pka)
