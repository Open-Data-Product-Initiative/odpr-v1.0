# Recipe Catalog Builder Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Python maintenance script that regenerates the ODPR metadata-only recipe catalog from canonical recipe examples.

**Architecture:** The script follows the existing `scripts/` pattern: local path constants from `odpr_paths.py`, YAML/JSON loading with PyYAML, deterministic output via `yaml.safe_dump`, and optional JSON Schema validation when `jsonschema` is installed. The script is intentionally catalog-maintenance tooling, not recipe execution or SDK behavior.

**Tech Stack:** Python 3, PyYAML, optional `jsonschema`, existing `unittest` script tests.

---

### Task 1: Add Tests First

**Files:**
- Modify: `tests/test_agent_scripts.py`

- [ ] **Step 1: Write failing tests for generated catalog output and check mode**

Add tests that call `scripts/build_recipe_catalog.py` with a temporary output
path and with `--check`. The tests should assert that generated entries include
metadata and commands, and exclude full recipe step bodies.

- [ ] **Step 2: Run targeted tests to verify failure**

Run:

```bash
python3 -m pytest tests/test_agent_scripts.py -q
```

Expected before implementation: failures because `scripts/build_recipe_catalog.py`
does not exist.

### Task 2: Implement Catalog Builder

**Files:**
- Create: `scripts/build_recipe_catalog.py`
- Modify: `scripts/odpr_paths.py` only if extra path constants are needed

- [ ] **Step 1: Create helper functions**

Implement document loading, language-map handling, recipe extraction, command
collection, catalog rendering, optional validation, YAML writing, and check
comparison.

- [ ] **Step 2: Add CLI**

Support:

```bash
python3 scripts/build_recipe_catalog.py
python3 scripts/build_recipe_catalog.py --check
python3 scripts/build_recipe_catalog.py --output /tmp/catalog.yaml
python3 scripts/build_recipe_catalog.py --input-dir source/recipes/examples
```

- [ ] **Step 3: Run targeted tests**

Run:

```bash
python3 -m pytest tests/test_agent_scripts.py -q
```

Expected after implementation: all tests in `tests/test_agent_scripts.py` pass.

### Task 3: Update Documentation And Checks

**Files:**
- Modify: `source/includes/_toolkit.md`
- Modify: `source/llms.txt`
- Modify: `scripts/check_agent_artifacts.py`
- Modify: `tests/test_agent_artifacts.py` if existing guidance assertions need to include the new script

- [ ] **Step 1: Add script guidance**

Document `build_recipe_catalog.py` as the maintenance script for regenerating
`source/recipes/catalog.yaml` from canonical recipe examples.

- [ ] **Step 2: Keep agent checks aligned**

Extend consistency checks so `llms.txt` references `scripts/build_recipe_catalog.py`.

- [ ] **Step 3: Run required verification**

Run:

```bash
python3 scripts/generate_recipe_artifacts.py --check
python3 scripts/check_agent_artifacts.py
python3 -m pytest -q
git diff --check
```

Expected: all commands exit 0.
