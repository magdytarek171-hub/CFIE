"""Approved global Decimal policy for ES-004."""

from decimal import ROUND_HALF_EVEN
from typing import Final

DECIMAL_PRECISION: Final = 50
DECIMAL_ROUNDING: Final = ROUND_HALF_EVEN
