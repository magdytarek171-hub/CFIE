"""Immutable formula-phase model for CFIE."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass(frozen=True, slots=True)
class Phase:
    """Represent one ordered formula phase without processing behavior.

    Args:
        name: Caller-supplied phase name.
        order: Caller-supplied phase order.
        temperature: Optional explicit process temperature in degrees Celsius.
        mixing_instructions: Optional immutable mixing instructions.
        ingredients: Immutable ingredient-entry collection contained by this phase.
    """

    name: str
    order: int
    temperature: Decimal | None
    mixing_instructions: tuple[str, ...]
    ingredients: tuple[Any, ...]
