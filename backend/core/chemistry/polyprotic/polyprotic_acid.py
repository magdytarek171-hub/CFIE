"""Polyprotic acid structural model."""

from dataclasses import dataclass
from decimal import Decimal

from backend.core.chemistry.polyprotic.dissociation import DissociationStep
from backend.core.chemistry.polyprotic.species import SpeciesSequence
from backend.core.chemistry.polyprotic.validation import validate_pka, validate_step_number


@dataclass(frozen=True, slots=True)
class PolyproticAcid:
    """Immutable polyprotic acid and its complete structural dissociation chain.

    Molecular weight is a supplied Decimal in g/mol. This model performs no
    chemistry calculations, hydration adjustments, or species distributions.
    """

    name: str
    formula: str
    molecular_weight: Decimal
    charge: int
    number_of_dissociation_steps: int
    pka_values: tuple[Decimal, ...]
    conjugate_species_ids: tuple[str, ...]
    species_sequence: SpeciesSequence
    dissociation_steps: tuple[DissociationStep, ...]

    def __post_init__(self) -> None:
        """Validate all approved ES-007 chain invariants."""

        validate_step_number(self.number_of_dissociation_steps)
        if not isinstance(self.molecular_weight, Decimal) or not self.molecular_weight.is_finite():
            raise ValueError("molecular_weight must be a finite Decimal in g/mol.")
        if len(self.pka_values) != self.number_of_dissociation_steps:
            raise ValueError("pKa value count must equal number_of_dissociation_steps.")
        if any(validate_pka(value) is None for value in self.pka_values):
            raise ValueError("Invalid pKa values.")
        if any(left >= right for left, right in zip(self.pka_values, self.pka_values[1:])):
            raise ValueError("pKa values must be strictly ascending.")
        species = self.species_sequence.species
        if len(species) != self.number_of_dissociation_steps + 1:
            raise ValueError("Species sequence must contain one more species than dissociation steps.")
        ids = tuple(record.species_id for record in species)
        if len(set(ids)) != len(ids):
            raise ValueError("Species identifiers must be unique.")
        if tuple(self.conjugate_species_ids) != ids[1:]:
            raise ValueError("conjugate_species_ids must match the ordered sequence after the acid.")
        if len(self.dissociation_steps) != self.number_of_dissociation_steps:
            raise ValueError("Exactly one DissociationStep is required per dissociation.")
        for index, step in enumerate(self.dissociation_steps, start=1):
            if step.step_number != index or step.acid_species_id != ids[index - 1] or step.base_species_id != ids[index]:
                raise ValueError("Dissociation steps must be contiguous and match the species sequence.")
            if step.pka != self.pka_values[index - 1]:
                raise ValueError("Dissociation-step pKa values must match pka_values.")
            if species[index].charge != species[index - 1].charge - 1:
                raise ValueError("Each dissociation species charge must decrease by one.")
