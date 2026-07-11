"""Base species model."""
from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class BaseSpecies:
    """Immutable base species with an identifier for its conjugate acid."""
    name: str; formula: str; charge: int; conjugate_species_id: str
