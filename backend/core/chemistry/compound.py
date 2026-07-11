"""Immutable compound data models for ES-003."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class DensityMeasurement:
    """A supplier or reference density measurement in g/mL.

    Args:
        value: Density value in g/mL.
        temperature_celsius: Optional measurement temperature in degrees Celsius.
    """

    value: Decimal
    temperature_celsius: Decimal | None = None

    def __post_init__(self) -> None:
        """Validate explicitly supplied density metadata."""

        _require_finite_decimal("value", self.value)
        if self.temperature_celsius is not None:
            _require_finite_decimal("temperature_celsius", self.temperature_celsius)


@dataclass(frozen=True, slots=True)
class Compound:
    """An immutable, traceable representation of one chemical compound form.

    ``molecular_weight`` is expressed in g/mol and describes exactly the form
    named by ``hydration_state``. ``purity`` is a Decimal fraction on the
    inclusive 0–1 basis. The model does not infer any scientific property.

    Args:
        common_name: Common compound name from an approved source.
        inci_name: INCI name from an approved source.
        chemical_formula: Formula for the specified chemical form.
        cas_number: CAS Registry Number supplied by the source.
        molecular_weight: Molecular weight in g/mol for ``hydration_state``.
        purity: Decimal purity fraction on the inclusive 0–1 basis.
        hydration_state: Explicit hydration-state description.
        charge: Integer chemical charge.
        pka_values: Ordered pKa values by dissociation sequence.
        aliases: Immutable alternative names.
        references: Immutable source references for traceability.
        density: Optional density measurement in g/mL.
        supplier_name: Optional supplier name associated with this record.
    """

    common_name: str
    inci_name: str
    chemical_formula: str
    cas_number: str
    molecular_weight: Decimal
    purity: Decimal
    hydration_state: str
    charge: int
    pka_values: tuple[Decimal, ...]
    aliases: tuple[str, ...]
    references: tuple[str, ...]
    density: DensityMeasurement | None = None
    supplier_name: str | None = None

    def __post_init__(self) -> None:
        """Validate type-preserving, explicitly provided scientific metadata."""

        _require_finite_decimal("molecular_weight", self.molecular_weight)
        _require_finite_decimal("purity", self.purity)
        if not Decimal("0") <= self.purity <= Decimal("1"):
            raise ValueError("purity must be a Decimal fraction in the inclusive range 0 to 1.")
        if isinstance(self.charge, bool) or not isinstance(self.charge, int):
            raise TypeError("charge must be an integer.")
        _require_decimal_tuple("pka_values", self.pka_values)
        _require_string_tuple("aliases", self.aliases)
        _require_string_tuple("references", self.references)
        if self.density is not None and not isinstance(self.density, DensityMeasurement):
            raise TypeError("density must be a DensityMeasurement or None.")
        if self.supplier_name is not None and not isinstance(self.supplier_name, str):
            raise TypeError("supplier_name must be a string or None.")


def _require_finite_decimal(field_name: str, value: Decimal) -> None:
    """Ensure a scientific numeric field is a finite Decimal.

    Args:
        field_name: Model field being validated.
        value: Field value to validate.
    """

    if not isinstance(value, Decimal):
        raise TypeError(f"{field_name} must be a Decimal.")
    if not value.is_finite():
        raise ValueError(f"{field_name} must be finite.")


def _require_decimal_tuple(field_name: str, values: tuple[Decimal, ...]) -> None:
    """Ensure a collection is an immutable tuple of finite Decimals.

    Args:
        field_name: Model field being validated.
        values: Collection to validate.
    """

    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be an immutable tuple.")
    for value in values:
        _require_finite_decimal(field_name, value)


def _require_string_tuple(field_name: str, values: tuple[str, ...]) -> None:
    """Ensure a collection is an immutable tuple of strings.

    Args:
        field_name: Model field being validated.
        values: Collection to validate.
    """

    if not isinstance(values, tuple) or not all(isinstance(value, str) for value in values):
        raise TypeError(f"{field_name} must be an immutable tuple of strings.")
