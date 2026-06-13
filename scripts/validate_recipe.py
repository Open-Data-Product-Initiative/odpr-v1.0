#!/usr/bin/env python
import argparse
import json
import re
import sys
from pathlib import Path

import yaml

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - friendly CLI message
    Draft202012Validator = None

from odpr_paths import SCHEMA_YAML


SECRET_KEY_MARKERS = (
    "apikey",
    "secret",
    "token",
    "password",
    "authorization",
    "bearer",
    "privatekey",
)

SECRET_VALUE_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{8,}\b"),
)


def load_data(path):
    with path.open(encoding="utf-8") as handle:
        if path.suffix.lower() == ".json":
            return json.load(handle)
        return yaml.safe_load(handle)


def format_path(parts):
    if not parts:
        return "<root>"

    formatted = str(parts[0])
    for part in parts[1:]:
        if isinstance(part, int):
            formatted += f"[{part}]"
        else:
            formatted += f".{part}"
    return formatted


def is_secret_key(key):
    normalized = re.sub(r"[^a-z0-9]", "", str(key).lower())
    if normalized.endswith("ref"):
        return False
    return any(marker in normalized for marker in SECRET_KEY_MARKERS)


def contains_secret_value(value):
    if not isinstance(value, str):
        return False
    return any(pattern.search(value) for pattern in SECRET_VALUE_PATTERNS)


def find_embedded_secrets(value, path=None):
    path = path or []
    findings = []

    if isinstance(value, dict):
        for key, child in value.items():
            child_path = path + [key]
            if is_secret_key(key):
                findings.append((format_path(child_path), "secret-like field name"))
            findings.extend(find_embedded_secrets(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(find_embedded_secrets(child, path + [index]))
    elif contains_secret_value(value):
        findings.append((format_path(path), "secret-like value"))

    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate an ODPR Recipe or Provider file against the ODPR schema.",
    )
    parser.add_argument("recipe", help="Path to an ODPR YAML or JSON file")
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
    secret_findings = find_embedded_secrets(recipe)

    if errors or secret_findings:
        print(f"{recipe_path}: invalid ODPR document", file=sys.stderr)
        for error in errors:
            location = ".".join(str(part) for part in error.path) or "<root>"
            print(f"- {location}: {error.message}", file=sys.stderr)
        for location, reason in secret_findings:
            print(
                f"- {location}: embedded secret or API key is not allowed ({reason})",
                file=sys.stderr,
            )
        return 1

    print(f"{recipe_path}: valid ODPR document")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
