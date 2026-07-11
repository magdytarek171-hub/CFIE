"""Immutable quantity value object for approved ES-002 units."""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import TypeAlias

from backend.core.exceptions import IncompatibleUnitError
from backend.core.units import Unit, get_unit_definition
from backend.core.units.definitions import parse_unit

QuantityValue: TypeAlias = Decimal | int | str


@dataclass(frozen=True, slots=True, init=False)
class Quantity:
    """A numeric value associated with one approved unit.

    Values are represented as ``Decimal`` to preserve decimal conversion
    precision. Floating-point input is deliberately rejected because its
    binary representation is not an exact decimal scientific value.

    Args:
        value: Decimal, integer, or decimal string value.
        unit: Approved unit or its exact text representation.

    Raises:
        TypeError: If ``value`` is not a supported exact numeric representation.
        ValueError: If ``value`` is not a valid finite decimal value.
        InvalidUnitError: If ``unit`` is not a supported unit.
    """

    value: Decimal
    unit: Unit

    def __init__(self, value: QuantityValue, unit: Unit | str) -> None:
        """Normalize an exact numeric value and validate its unit.

        Args:
            value: Decimal, integer, or decimal string value.
            unit: Approved unit or its exact text representation.
        """

        object.__setattr__(self, "value", _to_decimal(value))
        object.__setattr__(self, "unit", parse_unit(unit))

    def to(self, target_unit: Unit | str) -> "Quantity":
        """Convert this quantity to a compatible approved unit.

        Args:
            target_unit: Unit requested for the converted quantity.

        Returns:
            A new quantity in ``target_unit``.

        Raises:
            InvalidUnitError: If ``target_unit`` is not supported.
            IncompatibleUnitError: If conversion needs missing scientific
                information, such as density or volume, or targets a different
                approved dimension.
        """

        validated_target = parse_unit(target_unit)
        source_definition = get_unit_definition(self.unit)
        target_definition = get_unit_definition(validated_target)

        if source_definition.dimension is not target_definition.dimension:
            raise IncompatibleUnitError(
                self.unit.value,
                validated_target.value,
                "No density, volume, molecular weight, hydration state, purity, or temperature "
                "has been supplied for an inferred conversion.",
            )

        converted_value = (
            self.value * source_definition.scale_to_base / target_definition.scale_to_base
        )
        return Quantity(value=converted_value, unit=validated_target)


def _to_decimal(value: QuantityValue) -> Decimal:
    """Convert an exact supported numeric input to a finite ``Decimal``.

    Args:
        value: Decimal, integer, or decimal string to validate.

    Returns:
        The equivalent finite decimal.

    Raises:
        TypeError: If a float or another unsupported type is supplied.
        ValueError: If the supplied numeric text is invalid or non-finite.
    """

    if isinstance(value, bool) or not isinstance(value, (Decimal, int, str)):
        raise TypeError(
            "Quantity value must be a Decimal, int, or decimal string; floats are not accepted."
        )
    try:
        decimal_value = Decimal(value)
    except (InvalidOperation, ValueError) as error:
        raise ValueError(f"Quantity value must be a valid decimal: {value!r}.") from error
    if not decimal_value.is_finite():
        raise ValueError("Quantity value must be finite.")
    return decimal_value
