"""Exceptions raised by ES-004 mathematical utilities."""


class MathematicalDomainError(ValueError):
    """Raised when an input is outside a mathematical function's domain."""


class PrecisionError(ArithmeticError):
    """Raised when a result cannot be produced under the precision policy."""


class ValidationError(ValueError):
    """Raised when a scientific numeric value fails validation."""
