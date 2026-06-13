#!/usr/bin/env python
import argparse
import json

from odpr_paths import RECIPES_JSONL


def load_records():
    records = []
    for line in RECIPES_JSONL.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def matches(record, query):
    haystack = " ".join(
        str(record.get(key, ""))
        for key in ["id", "definition", "requiredFields", "doUseFor", "doNotUseFor"]
    ).lower()
    return query.lower() in haystack


def render_text(records):
    if not records:
        return "No matching ODPR recipes found.\n"

    chunks = []
    for record in records:
        chunks.append(
            "\n".join(
                [
                    f"{record['id']}",
                    f"Definition: {record.get('definition', '')}",
                    f"Example: {record.get('exampleFile', '')}",
                ]
            )
        )
    return "\n\n".join(chunks) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Search ODPR recipe records.")
    parser.add_argument("query", nargs="?", help="Keyword query")
    parser.add_argument("--id", dest="record_id", help="Exact recipe concept id")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args(argv)

    records = load_records()
    if args.record_id:
        results = [record for record in records if record.get("id") == args.record_id]
    elif args.query:
        results = [record for record in records if matches(record, args.query)]
    else:
        results = records

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(render_text(results), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
