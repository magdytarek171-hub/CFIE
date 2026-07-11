# ES-002: Scientific Unit & Quantity Engine

## Scope

The unit engine supplies a small, deterministic foundation for future CFIE scientific calculations. It has no cosmetic-domain rules, chemistry, buffer calculations, or external data.

`Quantity` is an immutable value object containing a finite `Decimal` value and one approved `Unit`. Its `to()` method creates a new quantity only when the source and target have the same approved dimension.

## Approved conversion boundaries

| Dimension | Units | Allowed conversions |
| --- | --- | --- |
| Mass | `g`, `kg`, `mg`, `µg` | Within mass |
| Volume | `mL`, `L` | Within volume |
| Amount of substance | `mol`, `mmol` | Within amount of substance |
| Amount concentration | `mol/L`, `mmol/L` | Within amount concentration |
| Mass fraction | `% w/w`, `ppm`, `ppb` | Within mass fraction |
| Mass-per-volume percentage | `% w/v` | Identity only |
| pH | `pH` | Identity only |
| pKa | `pKa` | Identity only |

Conversions across these dimensions are rejected with `IncompatibleUnitError`. In particular, no conversion infers density, molecular weight, hydration state, purity, temperature, or volume.

The approved mass-fraction relationships are:

- `1 % w/w = 10,000 ppm`
- `1 ppm = 1,000 ppb`

## Example

```python
from backend.core import Quantity
from backend.core.exceptions import IncompatibleUnitError

mass = Quantity("1.25", "g")
assert mass.to("mg").value == 1250

concentration = Quantity("2", "mmol/L")
assert concentration.to("mol/L").value == 0.002

try:
    Quantity("1", "g").to("mL")
except IncompatibleUnitError:
    # Density has not been supplied, so the conversion is rejected.
    pass
```
