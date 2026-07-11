# CFIE

Cosmetic Formulation Intelligence Engine

## Engineering foundation

CFIE is a scientific software platform for cosmetic formulation work. This repository is currently the engineering foundation only; it contains no chemistry rules, scientific equations, calculations, or working API endpoints.

## Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/)

## Quick start

```bash
uv sync --group dev
uv run pytest
uv run ruff check .
uv run mypy backend
```

See [DEVELOPMENT.md](DEVELOPMENT.md) for the repository layout and development conventions.

The approved unit engine and its conversion boundaries are documented in
[ES-002: Scientific Unit & Quantity Engine](docs/es-002-scientific-unit-quantity-engine.md).

The immutable scientific data models are documented in
[ES-003: Chemical Species & Compound Data Model](docs/es-003-chemical-species-compound-data-model.md).

The formula model architecture is documented in
[Formula Data Model](docs/formulation/formula-data-model.md).

## Scientific implementation policy

Scientific functionality is introduced only from an approved specification. Each approved calculation must have documented inputs, units, assumptions, validation criteria, traceability to its source, and unit tests.
