#!/usr/bin/env python
import json
import sys

import yaml

from odpr_paths import (
    EXAMPLES_DIR,
    LLMS_TXT,
    PROVIDER_EXAMPLES_DIR,
    RECIPES_JSONL,
    SCHEMA_JSON,
    SCHEMA_YAML,
    SOURCE,
)


EXPECTED_EXAMPLES = [
    "minimal.yaml",
    "ci-validate-generated-fragments.yaml",
    "release-portfolio-review.yaml",
    "hybrid-graph-review.yaml",
]

EXPECTED_PROVIDER_EXAMPLES = [
    "production-quality.yaml",
    "local-fast.yaml",
    "local-graph.yaml",
    "internal-secure.yaml",
]

EXPECTED_RECORD_IDS = {"Recipe", "Provider", "Step", "ExecutionPolicy", "ContextPolicy", "Gate"}


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


def assert_recipe_document(document, expected_type):
    assert document["schema"] == "https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml"
    assert document["version"] == "1.0"
    assert document["kind"] == "Recipe"
    recipe = document["recipe"]
    assert recipe["type"] == expected_type
    assert isinstance(recipe.get("version"), str) and recipe["version"].strip()
    assert isinstance(recipe["metadata"].get("id"), str) and recipe["metadata"]["id"].startswith("RCP-")
    assert_lang_string(recipe["metadata"].get("name"), "recipe.metadata.name")
    assert_lang_string(recipe["metadata"].get("description"), "recipe.metadata.description")
    assert recipe["steps"], "recipe.steps must not be empty"


def assert_provider_document(document, expected_id):
    assert document["schema"] == "https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml"
    assert document["version"] == "1.0"
    assert document["kind"] == "Provider"
    provider = document["provider"]
    assert provider["id"] == expected_id
    assert isinstance(provider["provider"], str) and provider["provider"].strip()


def check_schema():
    schema = load_yaml(SCHEMA_YAML)
    json_schema = load_json(SCHEMA_JSON)

    assert schema["required"] == ["schema", "version", "kind"], "YAML schema root requirements changed"
    assert json_schema["required"] == schema["required"], "JSON schema root requirements must match YAML schema"
    assert list(schema["properties"]) == ["schema", "version", "kind", "recipe", "provider"], "YAML schema root property order changed"
    assert list(json_schema["properties"]) == ["schema", "version", "kind", "recipe", "provider"], "JSON schema root property order changed"
    assert schema["properties"]["kind"]["enum"] == ["Recipe", "Provider"], "YAML schema root kind must support Recipe and Provider"
    assert json_schema["properties"]["kind"]["enum"] == ["Recipe", "Provider"], "JSON schema root kind must support Recipe and Provider"
    assert "recipe" in schema["properties"], "YAML schema must define recipe property"
    assert "provider" in schema["properties"], "YAML schema must define provider property"
    assert "catalog" not in schema["properties"], "YAML schema must not use catalog root"

    recipe = schema["$defs"][schema["properties"]["recipe"]["$ref"].split("/")[-1]]
    assert recipe["required"] == ["metadata", "version", "type", "steps"], "Recipe required fields changed unexpectedly"
    assert "version" in recipe["properties"], "Recipe must define recipe version"
    assert "execution" in recipe["properties"], "Recipe must define execution policy"
    assert "context" in recipe["properties"], "Recipe must define context policy"
    assert "gates" in recipe["properties"], "Recipe must define gates"
    assert "review" in recipe["properties"], "Recipe must define review"

    provider = schema["$defs"][schema["properties"]["provider"]["$ref"].split("/")[-1]]
    assert provider["required"] == ["id", "provider"], "Provider required fields changed unexpectedly"
    assert "model" in provider["properties"], "Provider must define model"
    assert "credentialsRef" in provider["properties"], "Provider must define credentialsRef"
    assert "temperature" in provider["properties"], "Provider must define temperature"


def check_examples():
    for filename in EXPECTED_EXAMPLES:
        path = EXAMPLES_DIR / filename
        assert path.is_file(), f"Missing example: {path.relative_to(SOURCE)}"
        load_yaml(path)

    assert_recipe_document(load_yaml(EXAMPLES_DIR / "minimal.yaml"), "dev")
    assert_recipe_document(load_yaml(EXAMPLES_DIR / "ci-validate-generated-fragments.yaml"), "ci")
    assert_recipe_document(load_yaml(EXAMPLES_DIR / "release-portfolio-review.yaml"), "release")
    assert_recipe_document(load_yaml(EXAMPLES_DIR / "hybrid-graph-review.yaml"), "hybrid")

    for filename in EXPECTED_PROVIDER_EXAMPLES:
        path = PROVIDER_EXAMPLES_DIR / filename
        assert path.is_file(), f"Missing provider example: {path.relative_to(SOURCE)}"
        load_yaml(path)

    assert_provider_document(load_yaml(PROVIDER_EXAMPLES_DIR / "production-quality.yaml"), "production-quality")
    assert_provider_document(load_yaml(PROVIDER_EXAMPLES_DIR / "local-fast.yaml"), "local-fast")
    assert_provider_document(load_yaml(PROVIDER_EXAMPLES_DIR / "local-graph.yaml"), "local-graph")
    assert_provider_document(load_yaml(PROVIDER_EXAMPLES_DIR / "internal-secure.yaml"), "internal-secure")

    ci_recipe = load_yaml(EXAMPLES_DIR / "ci-validate-generated-fragments.yaml")["recipe"]
    assert ci_recipe["execution"]["mode"] == "local"
    assert ci_recipe["context"]["format"] == "gcf"
    assert ci_recipe["gates"][0]["type"] == "validation"

    release_recipe = load_yaml(EXAMPLES_DIR / "release-portfolio-review.yaml")["recipe"]
    assert release_recipe["execution"]["mode"] == "hosted"
    assert release_recipe["review"]["required"] is True

    hybrid_recipe = load_yaml(EXAMPLES_DIR / "hybrid-graph-review.yaml")["recipe"]
    assert hybrid_recipe["execution"]["mode"] == "hybrid"
    assert hybrid_recipe["steps"][0]["providerRef"] == "local-graph"
    assert hybrid_recipe["steps"][1]["providerRef"] == "production-quality"


def check_recipes_and_llms():
    records = load_jsonl(RECIPES_JSONL)
    ids = {record["id"] for record in records}
    assert ids == EXPECTED_RECORD_IDS, f"Unexpected recipe record ids: {sorted(ids)}"

    for record in records:
        for key in ["definition", "requiredFields", "doUseFor", "doNotUseFor", "exampleFile"]:
            assert key in record, f"{record.get('id', '<unknown>')} missing {key}"
        assert isinstance(record["requiredFields"], list), f"{record['id']}.requiredFields must be a list"

    llms = LLMS_TXT.read_text(encoding="utf-8")
    for fragment in [
        "/recipes/recipes.jsonl",
        "/recipes/examples/minimal.yaml",
        "/recipes/examples/ci-validate-generated-fragments.yaml",
        "/providers/examples/production-quality.yaml",
        "/schema/odpr.yaml",
        "/schema/odpr.json",
    ]:
        assert fragment in llms, f"llms.txt missing {fragment}"


def main():
    checks = [check_schema, check_examples, check_recipes_and_llms]
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

    print("OK: ODPR agent artifacts are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
