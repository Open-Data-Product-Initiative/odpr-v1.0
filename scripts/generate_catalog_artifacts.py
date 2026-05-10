#!/usr/bin/env python3
import argparse
import json
import sys

import yaml

from odpc_paths import SCHEMA_JSON, SCHEMA_YAML


def load_schema_yaml():
    with SCHEMA_YAML.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def render_schema_json():
    return json.dumps(load_schema_yaml(), indent=2) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate derived ODPC catalog artifacts from canonical sources.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check whether generated artifacts are up to date without writing files.",
    )
    args = parser.parse_args(argv)

    expected = render_schema_json()
    current = SCHEMA_JSON.read_text(encoding="utf-8") if SCHEMA_JSON.exists() else ""

    if args.check:
        if current != expected:
            print(f"{SCHEMA_JSON}: out of date. Run `python3 scripts/generate_catalog_artifacts.py`.", file=sys.stderr)
            return 1
        print("OK: catalog artifacts are up to date.")
        return 0

    SCHEMA_JSON.write_text(expected, encoding="utf-8")
    print(f"Generated {SCHEMA_JSON.relative_to(SCHEMA_JSON.parents[2])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

