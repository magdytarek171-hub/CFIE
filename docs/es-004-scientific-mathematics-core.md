# ES-004: Scientific Mathematics Core

ES-004 provides reusable Decimal mathematics only. Its explicit global policy is 50 significant digits with `ROUND_HALF_EVEN`. It contains no chemistry, equilibrium, buffer, pH equation, or cosmetic calculation.

```python
from decimal import Decimal
from backend.core.math import log10_decimal, pow10_decimal

assert log10_decimal(Decimal("100")) == Decimal("2")
assert pow10_decimal(Decimal("2")) == Decimal("100")
```
