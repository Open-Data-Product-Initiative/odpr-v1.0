# Recipe Catalog Builder Design

## Scope

Add maintenance-only Python tooling for ODPR recipe catalog generation.

The tool keeps `source/recipes/catalog.yaml` aligned with canonical recipe
examples in `source/recipes/examples/`. It does not execute recipes, explain
recipes, resolve providers, or define SDK behavior.

## Behavior

- Read ODPR `Recipe` YAML or JSON files from an input directory.
- Generate one metadata-only `RecipeCatalog` document.
- Extract only fields allowed for `RecipeCatalogEntry`:
  - `path`
  - `id`
  - `version`
  - `type`
  - `name`
  - `description`
  - `tags`
  - `environment`
  - `executionMode`
  - `providerRef`
  - `contextFormat`
  - `requiresReview`
  - `commands`
- Never copy full `steps`, runtime state, logs, run ids, planned writes,
  provider internals, or SDK execution details into catalog entries.
- Support `--check` so CI and review workflows can detect drift without
  rewriting files.
- Support `--output` for alternate output paths while defaulting to
  `source/recipes/catalog.yaml`.

## Interfaces

Primary command:

```bash
python3 scripts/build_recipe_catalog.py
```

Check mode:

```bash
python3 scripts/build_recipe_catalog.py --check
```

Alternate output:

```bash
python3 scripts/build_recipe_catalog.py --output /tmp/catalog.yaml
```

## Validation

The generated catalog should be validated against `source/schema/odpr.yaml`
when `jsonschema` is installed. If the dependency is not available, generation
can still proceed, matching the existing optional-dependency behavior used by
the validation script tests.

## Documentation

Update `source/includes/_toolkit.md` and `source/llms.txt` so agents and
maintainers discover the new script alongside the existing artifact,
validation, search, and consistency scripts.
