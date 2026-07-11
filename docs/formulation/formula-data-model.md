# Formula Data Model

## Architecture

The formula foundation is an immutable aggregate: `Formula` contains ordered `Phase` objects, and each phase contains immutable `IngredientEntry` objects. An entry links to an ingredient by UUID and may link to a supplier grade by UUID. The model contains no chemistry, manufacturing, compatibility, or recommendation behavior.

## Object relationships

```text
Formula → Phase → IngredientEntry → Ingredient UUID
```

Containment defines an ingredient's phase membership; an ingredient entry does not duplicate a phase identifier.

## Validation rules

Structural validation requires at least one phase and one ingredient, unique phase orders, unique ingredient UUIDs, approved product/status/function enum values, ingredient percentages from 0 to 100 inclusive, and a total exactly equal to `100.000000`.

## Versioning philosophy

Formula objects are frozen. Future edits create new Formula objects and immutable complete-version snapshots; no in-place mutation is permitted. Version history is therefore reconstructable without changing prior records.

## Serialization format

The serializer converts nested Formula, Phase, and IngredientEntry objects to primitive JSON-compatible values. JSON uses the standard library. YAML uses only PyYAML `safe_dump()` and `safe_load()`. Serialization does not persist data.

## Future extension points

Future approved modules may add FormulaVersion snapshots, controlled metadata, batch and manufacturing models, validated ingredient registry links, and reporting adapters. Such extensions must preserve immutable historical formula data.
