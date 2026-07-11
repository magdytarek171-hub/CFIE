"""Immutable dissociation-species records."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SpeciesRecord:
    """One species in an ordered polyprotic dissociation chain.

    Args:
        species_id: Stable unique identifier.
        formula: Explicit formula supplied by an approved source.
        charge: Formal charge for this dissociation state.
        dissociation_state: Zero-based state within the chain.
    """

    species_id: str
    formula: str
    charge: int
    dissociation_state: int


@dataclass(frozen=True, slots=True)
class SpeciesSequence:
    """Immutable ordered species chain for a polyprotic acid.

    Args:
        species: Species from fully protonated state through final conjugate base.
    """

    species: tuple[SpeciesRecord, ...]
