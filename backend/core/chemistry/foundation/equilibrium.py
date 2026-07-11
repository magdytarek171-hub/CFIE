"""Equilibrium-reaction object model without reaction calculations."""
from dataclasses import dataclass
from enum import Enum
class EquilibriumType(str, Enum):
    ACID_DISSOCIATION="acid_dissociation"; BASE_PROTONATION="base_protonation"; WATER_AUTOIONIZATION="water_autoionization"; GENERIC_EQUILIBRIUM="generic_equilibrium"
@dataclass(frozen=True, slots=True)
class EquilibriumReaction:
    """Immutable structural reaction record; no balance checks are performed."""
    reactants: tuple[str, ...]; products: tuple[str, ...]; equilibrium_type: EquilibriumType; reversible: bool
    def __post_init__(self) -> None:
        if not self.reactants or not self.products: raise ValueError("Reaction requires non-empty reactants and products.")
        if not isinstance(self.equilibrium_type, EquilibriumType): raise ValueError("equilibrium_type must be an approved EquilibriumType.")
        if not isinstance(self.reversible, bool): raise ValueError("reversible must be boolean.")
