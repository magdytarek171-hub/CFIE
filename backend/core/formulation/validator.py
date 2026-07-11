"""Structural validation for immutable CFIE formula models."""

from decimal import Decimal

from backend.core.formulation.enums import FormulaStatus, IngredientFunction, ProductType
from backend.core.formulation.formula import Formula
from backend.core.formulation.ingredient_entry import IngredientEntry
from backend.core.formulation.phase import Phase

TOTAL_PERCENTAGE = Decimal("100.000000")


def validate_formula(formula: Formula) -> Formula:
    """Validate formula structure without performing scientific calculations.

    Args:
        formula: Immutable formula aggregate to validate.

    Returns:
        The unchanged validated formula.

    Raises:
        ValueError: If required formula structure or approved enum values fail.
    """

    if not formula.phases:
        raise ValueError("Formula must contain at least one phase.")
    try:
        ProductType(formula.product_type)
        FormulaStatus(formula.status)
    except ValueError as error:
        raise ValueError("Formula product_type or status is not an approved enum value.") from error

    orders: list[int] = []
    ingredient_ids = []
    percentages: list[Decimal] = []
    for phase in formula.phases:
        if not isinstance(phase, Phase):
            raise ValueError("Formula phases must contain Phase objects.")
        orders.append(phase.order)
        for entry in phase.ingredients:
            if not isinstance(entry, IngredientEntry):
                raise ValueError("Phase ingredients must contain IngredientEntry objects.")
            try:
                IngredientFunction(entry.function)
            except ValueError as error:
                raise ValueError("Ingredient function is not an approved enum value.") from error
            if not Decimal("0") <= entry.percentage <= Decimal("100"):
                raise ValueError("Ingredient percentage must be between 0 and 100 inclusive.")
            ingredient_ids.append(entry.ingredient_id)
            percentages.append(entry.percentage)
    if not percentages:
        raise ValueError("Formula must contain at least one ingredient.")
    if len(set(orders)) != len(orders):
        raise ValueError("Phase order values must be unique.")
    if len(set(ingredient_ids)) != len(ingredient_ids):
        raise ValueError("Ingredient UUIDs must be unique.")
    if sum(percentages, Decimal("0")) != TOTAL_PERCENTAGE:
        raise ValueError("Formula total percentage must equal exactly 100.000000.")
    return formula
