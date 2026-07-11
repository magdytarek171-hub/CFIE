"""Approved scale relationships for ES-002 units.

The named values in this module are limited to the exact SI-prefix and
mass-fraction relationships approved in ES-002. They are not cosmetic data.
"""

from decimal import Decimal
from typing import Final

BASE_SCALE: Final = Decimal("1")
GRAMS_PER_KILOGRAM: Final = Decimal("1000")
MILLIGRAMS_PER_GRAM: Final = Decimal("1000")
MICROGRAMS_PER_GRAM: Final = Decimal("1000000")
MILLILITRES_PER_LITRE: Final = Decimal("1000")
MILLIMOLES_PER_MOLE: Final = Decimal("1000")
PARTS_PER_MILLION_PER_PERCENT_W_W: Final = Decimal("10000")
PARTS_PER_BILLION_PER_PART_PER_MILLION: Final = Decimal("1000")
PARTS_PER_BILLION_PER_PERCENT_W_W: Final = (
    PARTS_PER_MILLION_PER_PERCENT_W_W * PARTS_PER_BILLION_PER_PART_PER_MILLION
)
