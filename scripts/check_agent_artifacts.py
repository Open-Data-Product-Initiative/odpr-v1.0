#!/usr/bin/env python
import json
import sys

import yaml

from odpc_paths import EXAMPLES_DIR, LLMS_TXT, OBJECTS_JSONL, SCHEMA_JSON, SCHEMA_YAML, SOURCE


EXPECTED_EXAMPLES = [
    "minimal.yaml",
    "full.yaml",
    "product-reference.yaml",
    "use-case.yaml",
    "business-objective-with-kpis.yaml",
    "signal.yaml",
]

EXPECTED_OBJECT_IDS = {"Catalog", "ProductReference", "UseCase", "BusinessObjective", "KPI", "Signal"}


def load_yaml(path):
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path):
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
    return records


def assert_lang_string(value, label):
    assert isinstance(value, dict), f"{label} must be an object"
    assert isinstance(value.get("en"), str) and value["en"].strip(), f"{label}.en must be a non-empty string"


def assert_named_object(value, prefix, label):
    assert isinstance(value.get("id"), str) and value["id"].startswith(prefix), f"{label}.id must start with {prefix}"
    assert_lang_string(value.get("name"), f"{label}.name")
    assert_lang_string(value.get("description"), f"{label}.description")


def check_schema():
    schema = load_yaml(SCHEMA_YAML)
    json_schema = load_json(SCHEMA_JSON)

    assert schema["required"] == ["schema", "version", "kind", "catalog"], "YAML schema root must require kind and catalog"
    assert json_schema["required"] == schema["required"], "JSON schema root requirements must match YAML schema"
    assert list(schema["properties"]) == ["schema", "version", "kind", "catalog"], "YAML schema root property order changed"
    assert list(json_schema["properties"]) == ["schema", "version", "kind", "catalog"], "JSON schema root property order changed"
    assert schema["properties"]["kind"]["const"] == "Catalog", "YAML schema root kind must be Catalog"
    assert json_schema["properties"]["kind"]["const"] == "Catalog", "JSON schema root kind must be Catalog"
    assert "catalog" in schema["properties"], "YAML schema must define catalog property"
    assert "catalog" in json_schema["properties"], "JSON schema must define catalog property"
    assert "product" not in schema["properties"], "YAML schema must not use product root"
    assert "product" not in json_schema["properties"], "JSON schema must not use product root"

    catalog = schema["$defs"][schema["properties"]["catalog"]["$ref"].split("/")[-1]]
    assert catalog["required"] == ["metadata"], "Catalog must require metadata"
    assert "metadata" in catalog["properties"], "Catalog must define metadata"
    assert "meta" not in catalog["properties"], "Catalog must not define meta"
    metadata = schema["$defs"][catalog["properties"]["metadata"]["$ref"].split("/")[-1]]
    assert metadata["required"] == ["id", "name", "description"], "Catalog metadata required fields changed unexpectedly"
    assert "tags" in metadata["properties"], "Catalog tags must be defined in metadata"
    assert "tags" not in catalog["properties"], "Catalog tags must not be defined at catalog root"
    graph_reference = schema["$defs"]["GraphReference"]
    assert graph_reference["required"] == ["standard", "version", "$ref"], "GraphReference must require $ref"
    assert "$ref" in graph_reference["properties"], "GraphReference must define $ref"
    assert "uri" not in graph_reference["properties"], "GraphReference must not define uri"
    for collection in ["productReferences", "useCases", "businessObjectives", "signals"]:
        assert collection in catalog["properties"], f"Catalog missing {collection}"


def check_examples():
    for filename in EXPECTED_EXAMPLES:
        path = EXAMPLES_DIR / filename
        assert path.is_file(), f"Missing example: {path.relative_to(SOURCE)}"
        load_yaml(path)

    minimal = load_yaml(EXAMPLES_DIR / "minimal.yaml")
    assert minimal["schema"] == "https://opendataproducts.org/odpc-v1.0/schema/odpc.yaml"
    assert minimal["version"] == "1.0"
    assert minimal["kind"] == "Catalog", "minimal catalog example must set kind to Catalog"
    assert_named_object(minimal["catalog"]["metadata"], "CAT-", "catalog.metadata")
    assert "meta" not in minimal["catalog"], "minimal catalog example must not use catalog.meta"

    full_document = load_yaml(EXAMPLES_DIR / "full.yaml")
    assert full_document["kind"] == "Catalog", "full catalog example must set kind to Catalog"
    full = full_document["catalog"]
    assert_named_object(full["metadata"], "CAT-", "catalog.metadata")
    assert "tags" in full["metadata"], "full catalog example must put tags in catalog.metadata"
    assert "meta" not in full, "full catalog example must not use catalog.meta"
    assert "tags" not in full, "full catalog example must not put tags at catalog root"
    assert "$ref" in full["metadata"]["graph"], "full catalog example graph must use $ref"
    assert "uri" not in full["metadata"]["graph"], "full catalog example graph must not use uri"
    assert_named_object(full["productReferences"][0], "DP-", "productReferences[0]")
    assert_named_object(full["useCases"][0], "UC-", "useCases[0]")
    assert_named_object(full["businessObjectives"][0], "BO-", "businessObjectives[0]")
    assert_named_object(full["signals"][0], "SIG-", "signals[0]")


def check_objects_and_llms():
    records = load_jsonl(OBJECTS_JSONL)
    ids = {record["id"] for record in records}
    assert ids == EXPECTED_OBJECT_IDS, f"Unexpected object ids: {sorted(ids)}"

    for record in records:
        for key in ["definition", "requiredFields", "doUseFor", "doNotUseFor", "exampleFile"]:
            assert key in record, f"{record.get('id', '<unknown>')} missing {key}"
        assert isinstance(record["requiredFields"], list), f"{record['id']}.requiredFields must be a list"

    llms = LLMS_TXT.read_text(encoding="utf-8")
    for fragment in [
        "/catalog/objects.jsonl",
        "/catalog/examples/minimal.yaml",
        "/catalog/examples/full.yaml",
        "/schema/odpc.yaml",
        "/schema/odpc.json",
    ]:
        assert fragment in llms, f"llms.txt missing {fragment}"


def main():
    checks = [check_schema, check_examples, check_objects_and_llms]
    failures = []
    for check in checks:
        try:
            check()
        except Exception as exc:
            failures.append(f"{check.__name__}: {exc}")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1

    print("OK: ODPC agent artifacts are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
