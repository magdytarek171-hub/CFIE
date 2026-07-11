"""Safe JSON and YAML serialization for immutable formula models."""

import json
from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

import yaml

from backend.core.formulation.formula import Formula
from backend.core.formulation.ingredient_entry import IngredientEntry
from backend.core.formulation.phase import Phase


def formula_to_dict(formula: Formula) -> dict[str, Any]:
    """Convert a nested Formula object into JSON-compatible primitive values."""

    return {
        "formula_id": str(formula.formula_id), "name": formula.name,
        "product_type": formula.product_type, "description": formula.description,
        "version": formula.version, "created_at": formula.created_at.isoformat(),
        "modified_at": formula.modified_at.isoformat(), "author": formula.author,
        "status": formula.status, "notes": list(formula.notes),
        "phases": [{"name": phase.name, "order": phase.order,
                    "temperature": None if phase.temperature is None else str(phase.temperature),
                    "mixing_instructions": list(phase.mixing_instructions),
                    "ingredients": [{"ingredient_id": str(item.ingredient_id),
                                     "display_name": item.display_name, "percentage": str(item.percentage),
                                     "function": item.function, "processing_notes": list(item.processing_notes),
                                     "supplier_grade_id": None if item.supplier_grade_id is None else str(item.supplier_grade_id)}
                                    for item in phase.ingredients]}
                   for phase in formula.phases],
    }


def formula_from_dict(data: dict[str, Any]) -> Formula:
    """Reconstruct an immutable Formula from serialized primitive values."""

    phases = tuple(Phase(
        name=phase["name"], order=phase["order"],
        temperature=None if phase["temperature"] is None else Decimal(phase["temperature"]),
        mixing_instructions=tuple(phase["mixing_instructions"]),
        ingredients=tuple(IngredientEntry(UUID(item["ingredient_id"]), item["display_name"],
            Decimal(item["percentage"]), item["function"], tuple(item.get("processing_notes", [])),
            None if item.get("supplier_grade_id") is None else UUID(item["supplier_grade_id"]))
            for item in phase["ingredients"]),
    ) for phase in data["phases"])
    return Formula(UUID(data["formula_id"]), data["name"], data["product_type"], data.get("description"),
                   data["version"], datetime.fromisoformat(data["created_at"]),
                   datetime.fromisoformat(data["modified_at"]), data["author"], data["status"], phases,
                   tuple(data.get("notes", [])))


def to_json(formula: Formula) -> str:
    """Serialize a Formula to JSON without persistence."""

    return json.dumps(formula_to_dict(formula), ensure_ascii=False, sort_keys=True)


def from_json(serialized: str) -> Formula:
    """Deserialize JSON into a Formula."""

    return formula_from_dict(json.loads(serialized))


def to_yaml(formula: Formula) -> str:
    """Safely serialize a Formula to YAML."""

    return yaml.safe_dump(formula_to_dict(formula), allow_unicode=True, sort_keys=True)


def from_yaml(serialized: str) -> Formula:
    """Safely deserialize YAML into a Formula."""

    data = yaml.safe_load(serialized)
    if not isinstance(data, dict):
        raise ValueError("Formula YAML must contain a mapping.")
    return formula_from_dict(data)
