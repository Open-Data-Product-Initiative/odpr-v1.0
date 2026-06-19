#!/usr/bin/env python
import argparse
import json
import sys
from pathlib import Path

import yaml

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - optional validation dependency
    Draft202012Validator = None

from odpr_paths import EXAMPLES_DIR, RECIPES_DIR, SCHEMA_YAML
from validate_recipe import load_data


SCHEMA_URI = "https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml"
DEFAULT_METADATA = {
    "id": "RCP-CATALOG-001",
    "name": {"en": "ODPR Example Recipe Catalog"},
    "description": {"en": "Metadata-only discovery catalog for canonical ODPR recipe examples."},
}
DEFAULT_EXAMPLE_ORDER = [
    "minimal.yaml",
    "ci-validate-generated-fragments.yaml",
    "release-portfolio-review.yaml",
    "portfolio-localization.yaml",
    "hybrid-graph-review.yaml",
]


class IndentedSafeDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


def load_document(path):
    with path.open(encoding="utf-8") as handle:
        if path.suffix.lower() == ".json":
            return json.load(handle)
        return yaml.safe_load(handle)


def iter_recipe_files(input_dir):
    patterns = ("*.yaml", "*.yml", "*.json")
    paths = []
    for pattern in patterns:
        paths.extend(input_dir.glob(pattern))
    order = {name: index for index, name in enumerate(DEFAULT_EXAMPLE_ORDER)}
    return sorted(
        (path for path in paths if path.is_file()),
        key=lambda path: (order.get(path.name, len(order)), path.name),
    )


def relative_recipe_path(path):
    return path.relative_to(RECIPES_DIR.parent).as_posix()


def extract_entry(path):
    document = load_document(path)
    if not isinstance(document, dict) or document.get("kind") != "Recipe":
        raise ValueError(f"{path}: expected an ODPR Recipe document")

    recipe = document.get("recipe")
    if not isinstance(recipe, dict):
        raise ValueError(f"{path}: missing recipe object")

    metadata = recipe.get("metadata", {})
    execution = recipe.get("execution", {})
    context = recipe.get("context", {})
    review = recipe.get("review", {})
    steps = recipe.get("steps", [])

    entry = {
        "path": relative_recipe_path(path),
        "id": metadata.get("id"),
        "version": recipe.get("version"),
        "type": recipe.get("type"),
        "name": metadata.get("name"),
    }

    optional_fields = [
        ("description", metadata.get("description")),
        ("tags", metadata.get("tags")),
        ("environment", recipe.get("environment")),
        ("executionMode", execution.get("mode") if isinstance(execution, dict) else None),
        ("providerRef", execution.get("providerRef") if isinstance(execution, dict) else None),
        ("contextFormat", context.get("format") if isinstance(context, dict) else None),
        ("requiresReview", review.get("required") if isinstance(review, dict) else None),
        (
            "commands",
            [
                step.get("command")
                for step in steps
                if isinstance(step, dict) and step.get("command")
            ],
        ),
    ]

    for key, value in optional_fields:
        if value is not None and value != []:
            entry[key] = value

    return entry


def build_catalog(input_dir):
    entries = [extract_entry(path) for path in iter_recipe_files(input_dir)]
    return {
        "schema": SCHEMA_URI,
        "version": "1.0",
        "kind": "RecipeCatalog",
        "recipeCatalog": {
            "metadata": DEFAULT_METADATA,
            "recipes": entries,
        },
    }


def validate_catalog(document):
    if Draft202012Validator is None:
        return []

    schema = load_data(SCHEMA_YAML)
    validator = Draft202012Validator(schema)
    return sorted(validator.iter_errors(document), key=lambda error: list(error.path))


def render_yaml(document):
    return yaml.dump(
        document,
        Dumper=IndentedSafeDumper,
        sort_keys=False,
        allow_unicode=False,
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build the ODPR metadata-only RecipeCatalog from canonical recipe examples.",
    )
    parser.add_argument(
        "--input-dir",
        default=str(EXAMPLES_DIR),
        help="Folder containing canonical ODPR Recipe YAML or JSON files.",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=str(RECIPES_DIR / "catalog.yaml"),
        help="Output RecipeCatalog YAML path.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check whether the RecipeCatalog is up to date without writing files.",
    )
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip optional schema validation of the generated RecipeCatalog.",
    )
    args = parser.parse_args(argv)

    input_dir = Path(args.input_dir)
    output = Path(args.output)

    if not input_dir.is_dir():
        print(f"Input folder not found: {input_dir}", file=sys.stderr)
        return 1

    try:
        document = build_catalog(input_dir)
        if not args.no_validate:
            errors = validate_catalog(document)
            if errors:
                print("Generated RecipeCatalog is invalid:", file=sys.stderr)
                for error in errors:
                    location = ".".join(str(part) for part in error.path) or "<root>"
                    print(f"- {location}: {error.message}", file=sys.stderr)
                return 1
        expected = render_yaml(document)
    except (json.JSONDecodeError, yaml.YAMLError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1

    if args.check:
        current = output.read_text(encoding="utf-8") if output.exists() else ""
        if current != expected:
            print(
                f"{output}: out of date. Run `python3 scripts/build_recipe_catalog.py`.",
                file=sys.stderr,
            )
            return 1
        print("OK: recipe catalog is up to date.")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(expected, encoding="utf-8")
    print(f"Generated {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
