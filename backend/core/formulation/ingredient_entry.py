"""Immutable formula ingredient-entry model for CFIE."""

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True, slots=True)
class IngredientEntry:
    """Represent one ingredient entry contained by a formula phase.

    Args:
        ingredient_id: UUID linked to the future ingredient knowledge record.
        display_name: Caller-supplied formula display name.
        percentage: Explicit formula percentage without calculation behavior.
        function: Caller-supplied formulation-function value.
        processing_notes: Optional immutable processing notes.
        supplier_grade_id: Optional UUID linked to a future supplier-grade record.
    """

    ingredient_id: UUID
    display_name: str
    percentage: Decimal
    function: str
    processing_notes: tuple[str, ...] = ()
    supplier_grade_id: UUID | None = None
