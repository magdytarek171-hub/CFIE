# ES-003: Chemical Species & Compound Data Model

ES-003 provides immutable, descriptive scientific records only. It performs no chemistry, equations, calculations, persistence, or API operations.

`Compound.molecular_weight` is a `Decimal` in g/mol for the exact supplied `hydration_state`. `purity` is a `Decimal` fraction from 0 to 1. `DensityMeasurement.value` is in g/mL; its optional `temperature_celsius` is metadata only and is never corrected or converted.

`AcidBasePair` records explicit acid/base compounds, an approved `Decimal` pKa value, and an integer dissociation step. `BufferSystem` records an `AcidBasePair`, inclusive `(lower, upper)` Decimal pH ranges, and source-reference tuples.

## Example objects

The values below are structural placeholders, not chemical data. Replace each with approved, referenced source data.

```python
from decimal import Decimal
from backend.core.chemistry import AcidBasePair, BufferSystem, Compound, DensityMeasurement

acid = Compound(
    common_name="Approved acid name", inci_name="Approved INCI name",
    chemical_formula="Approved formula", cas_number="Approved CAS number",
    molecular_weight=Decimal("100.000"), purity=Decimal("0.980"),
    hydration_state="Approved hydration state", charge=0,
    pka_values=(Decimal("4.000"),), aliases=(), references=("Approved reference",),
    density=DensityMeasurement(Decimal("1.000"), Decimal("20")),
)
base = Compound(
    common_name="Approved base name", inci_name="Approved base INCI name",
    chemical_formula="Approved base formula", cas_number="Approved base CAS number",
    molecular_weight=Decimal("99.000"), purity=Decimal("1.000"),
    hydration_state="Approved hydration state", charge=-1,
    pka_values=(), aliases=(), references=("Approved reference",),
)
pair = AcidBasePair(acid, base, Decimal("4.000"), 1)
system = BufferSystem(
    "Approved buffer-system name", pair, (Decimal("3"), Decimal("5")),
    (Decimal("3.5"), Decimal("4.5")), ("Approved reference",),
)
```
