"""Supported unit definitions for ES-002.

Conversions are permitted only between units that share the same dimension.
Each dimension intentionally prevents chemistry-dependent inferences such as
mass-to-volume conversion without an explicitly supplied density.
"""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from types import MappingProxyType
from typing import Final, Mapping

from backend.core.constants import (
    BASE_SCALE,
    GRAMS_PER_KILOGRAM,
    MICROGRAMS_PER_GRAM,
    MILLIGRAMS_PER_GRAM,
    MILLILITRES_PER_LITRE,
    MILLIMOLES_PER_MOLE,
    PARTS_PER_BILLION_PER_PERCENT_W_W,
    PARTS_PER_MILLION_PER_PERCENT_W_W,
)
from backend.core.exceptions import InvalidUnitError


class Dimension(str, Enum):
    """Dimensions supported by the ES-002 unit engine."""

    MASS = "mass"
    VOLUME = "volume"
    AMOUNT_OF_SUBSTANCE = "amount_of_substance"
    AMOUNT_CONCENTRATION = "amount_concentration"
    MASS_FRACTION = "mass_fraction"
    MASS_PER_VOLUME_PERCENT = "mass_per_volume_percent"
    PH = "pH"
    PKA = "pKa"


class Unit(str, Enum):
    """Units approved for use by ES-002."""

    GRAM = "g"
    KILOGRAM = "kg"
    MILLIGRAM = "mg"
    MICROGRAM = "µg"
    MILLILITRE = "mL"
    LITRE = "L"
    MOLE = "mol"
    MILLIMOLE = "mmol"
    MOLE_PER_LITRE = "mol/L"
    MILLIMOLE_PER_LITRE = "mmol/L"
    PERCENT_W_W = "% w/w"
    PERCENT_W_V = "% w/v"
    PARTS_PER_MILLION = "ppm"
    PARTS_PER_BILLION = "ppb"
    PH = "pH"
    PKA = "pKa"


@dataclass(frozen=True, slots=True)
class UnitDefinition:
    """Describes a supported unit and its conversion scale.

    Args:
        dimension: Physical or approved scientific dimension of the unit.
        scale_to_base: Multiplier that converts one unit to its dimension's base unit.
    """

    dimension: Dimension
    scale_to_base: Decimal


UNIT_DEFINITIONS: Final[Mapping[Unit, UnitDefinition]] = MappingProxyType(
    {
        Unit.GRAM: UnitDefinition(Dimension.MASS, BASE_SCALE),
        Unit.KILOGRAM: UnitDefinition(Dimension.MASS, GRAMS_PER_KILOGRAM),
        Unit.MILLIGRAM: UnitDefinition(Dimension.MASS, BASE_SCALE / MILLIGRAMS_PER_GRAM),
        Unit.MICROGRAM: UnitDefinition(Dimension.MASS, BASE_SCALE / MICROGRAMS_PER_GRAM),
        Unit.MILLILITRE: UnitDefinition(Dimension.VOLUME, BASE_SCALE / MILLILITRES_PER_LITRE),
        Unit.LITRE: UnitDefinition(Dimension.VOLUME, BASE_SCALE),
        Unit.MOLE: UnitDefinition(Dimension.AMOUNT_OF_SUBSTANCE, BASE_SCALE),
        Unit.MILLIMOLE: UnitDefinition(
            Dimension.AMOUNT_OF_SUBSTANCE, BASE_SCALE / MILLIMOLES_PER_MOLE
        ),
        Unit.MOLE_PER_LITRE: UnitDefinition(Dimension.AMOUNT_CONCENTRATION, BASE_SCALE),
        Unit.MILLIMOLE_PER_LITRE: UnitDefinition(
            Dimension.AMOUNT_CONCENTRATION, BASE_SCALE / MILLIMOLES_PER_MOLE
        ),
        Unit.PERCENT_W_W: UnitDefinition(
            Dimension.MASS_FRACTION, BASE_SCALE / Decimal("100")
        ),
        Unit.PARTS_PER_MILLION: UnitDefinition(
            Dimension.MASS_FRACTION, BASE_SCALE / PARTS_PER_MILLION_PER_PERCENT_W_W / Decimal("100")
        ),
        Unit.PARTS_PER_BILLION: UnitDefinition(
            Dimension.MASS_FRACTION, BASE_SCALE / PARTS_PER_BILLION_PER_PERCENT_W_W / Decimal("100")
        ),
        Unit.PERCENT_W_V: UnitDefinition(Dimension.MASS_PER_VOLUME_PERCENT, BASE_SCALE),
        Unit.PH: UnitDefinition(Dimension.PH, BASE_SCALE),
        Unit.PKA: UnitDefinition(Dimension.PKA, BASE_SCALE),
    }
)


def get_unit_definition(unit: Unit) -> UnitDefinition:
    """Return the approved definition for a supported unit.

    Args:
        unit: Supported unit to look up.

    Returns:
        The immutable definition for ``unit``.
    """

    return UNIT_DEFINITIONS[unit]


def parse_unit(unit: Unit | str) -> Unit:
    """Validate and normalize a unit supplied to the public API.

    Args:
        unit: Approved ``Unit`` member or its exact textual representation.

    Returns:
        A validated ``Unit`` member.

    Raises:
        InvalidUnitError: If ``unit`` is not an approved unit representation.
    """

    if isinstance(unit, Unit):
        return unit
    if not isinstance(unit, str):
        raise InvalidUnitError(unit)
    try:
        return Unit(unit)
    except ValueError as error:
        raise InvalidUnitError(unit) from error
