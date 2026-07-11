"""Immutable formula aggregate model for CFIE."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Formula:
    """Represent one immutable cosmetic formula aggregate.

    This model intentionally provides no validation, serialization, versioning,
    calculations, or domain behavior. Those responsibilities are introduced by
    separate approved specifications.

    Args:
        formula_id: Stable UUID identifying the formula.
        name: Caller-supplied formula name.
        product_type: Caller-supplied product-type value.
        description: Optional descriptive text.
        version: Caller-supplied version label.
        created_at: Timezone-aware creation timestamp.
        modified_at: Timezone-aware modification timestamp.
        author: Caller-supplied author identifier.
        status: Caller-supplied formula-status value.
        phases: Immutable ordered phase collection.
        notes: Optional immutable notes collection.
    """

    formula_id: UUID
    name: str
    product_type: str
    description: str | None
    version: str
    created_at: datetime
    modified_at: datetime
    author: str
    status: str
    phases: tuple[Any, ...]
    notes: tuple[str, ...] = ()
