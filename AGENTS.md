# AGENTS.md

Instruction file for AI coding agents working in this repository.

## Project

This repository is the source of truth for ODPR, the Data Product Recipe
Specification. ODPR is part of the OpenDataProducts.org standards family.

ODPR defines portable, declarative workflow recipes for repeatable data product
delivery. It does not define data product metadata, catalog objects, graph
relationships, vocabulary terms, SDK internals, CI/CD engines, or model
providers.

## Source Of Truth

- Human-readable specification: `source/index.html.md`
- Agent routing: `source/llms.txt`
- Canonical schema: `source/schema/odpr.yaml`
- Derived JSON schema: `source/schema/odpr.json`
- Agent retrieval records: `source/recipes/recipes.jsonl`
- Canonical examples: `source/recipes/examples/`

Keep these surfaces aligned when changing recipe semantics.

## SDK Relationship

The ODP Agent SDK is the first reference implementation for validating and
executing ODPR recipes. The SDK consumes ODPR semantics; it does not define
them.

When SDK behavior and ODPR semantics diverge, update the ODPR source first,
then update SDK fixtures, docs, and release notes to match the supported ODPR
version.

## Style

- Keep ODPR lightweight and implementation-neutral.
- Use `providerRef` for provider references; do not define provider internals in
  ODPR.
- Keep recipes declarative. Do not turn ODPR into a shell scripting language.
- Use extension fields beginning with `x-` for local implementation details.
- Preserve the ODPS family separation of concerns:
  - ODPS defines products.
  - ODPC defines catalogs and portfolio objects.
  - ODPG defines graphs and relationships.
  - ODPV defines shared vocabulary.
  - ODPR defines repeatable workflows.

## Verification

Before marking source changes complete, run:

1. `python3 scripts/generate_recipe_artifacts.py --check`
2. `python3 scripts/check_agent_artifacts.py`
3. `python3 -m pytest -q`
4. `git diff --check`

If Ruby/Middleman dependencies are available, also run the existing site build
workflow for the Slate docs.
