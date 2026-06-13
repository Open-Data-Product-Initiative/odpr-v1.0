#!/usr/bin/env python
import argparse
import json
import sys
from pathlib import Path

import yaml

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - friendly CLI message
    Draft202012Validator = None

from odpr_paths import SCHEMA_YAML


def load_data(path):
    with path.open(encoding="utf-8") as handle:
        if path.suffix.lower() == ".json":
            return json.load(handle)
        return yaml.safe_load(handle)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate an ODPR recipe file against the ODPR schema.",
    )
    parser.add_argument("recipe", help="Path to an ODPR YAML or JSON recipe file")
    args = parser.parse_args(argv)

    if Draft202012Validator is None:
        print(
            "jsonschema is required. Install dependencies with `python -m pip install -r scripts/requirements-agent.txt`.",
            file=sys.stderr,
        )
        return 2

    recipe_path = Path(args.recipe)
    try:
        schema = load_data(SCHEMA_YAML)
        recipe = load_data(recipe_path)
    except Exception as exc:
        print(f"Failed to read recipe or schema: {exc}", file=sys.stderr)
        return 1

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(recipe), key=lambda error: list(error.path))

    if errors:
        print(f"{recipe_path}: invalid ODPR recipe", file=sys.stderr)
        for error in errors:
            location = ".".join(str(part) for part in error.path) or "<root>"
            print(f"- {location}: {error.message}", file=sys.stderr)
        return 1

    print(f"{recipe_path}: valid ODPR recipe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
