# CFIE Development Guide

## Repository layout

```
backend/
  cfie/
    api/         # Future HTTP interface adapters; no endpoints yet.
    chemistry/   # Future approved chemistry domain logic; no rules yet.
    database/    # Future persistence adapters and migrations.
    models/      # Future domain and transport data models.
    services/    # Future application orchestration services.
    utils/       # Shared, non-domain-specific utilities.
frontend/        # Reserved for the client application.
docs/            # Product, scientific, architectural, and operational documents.
tests/           # Automated tests, organized to mirror backend modules.
data/            # Local development data only; do not commit sensitive or licensed data.
scripts/         # Reproducible developer and maintenance scripts.
```

## Tooling

The Python project targets Python 3.12 and uses:

- `uv` for dependency and environment management
- FastAPI as the future backend web framework
- Pytest for automated tests
- Ruff for linting and formatting
- MyPy for static type checking

Install the development environment and run checks with:

```bash
uv sync --group dev
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy backend
```

## Implementation boundaries

- Do not introduce scientific formulas, ingredient limits, physical constants, compatibility claims, or regulatory conclusions without an approved specification.
- Keep domain logic independent from HTTP, database, and UI concerns.
- Place every approved scientific calculation in a focused module and add unit tests before it is considered complete.
- Document the specification source, expected units, input validation, output semantics, and known limits alongside each approved calculation.
- Prefer explicit types, small modules, and readable code over implicit behavior or clever abstractions.

## Data handling

The `data/` directory is intentionally ignored except for its placeholder. Store only non-sensitive, reproducible local development data there. Dataset provenance, licensing, version, and permitted use must be documented before any dataset is committed or used by CFIE.
