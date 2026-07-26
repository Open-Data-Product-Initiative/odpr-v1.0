#!/usr/bin/env python
import json
import sys

import yaml

from odpr_paths import (
    EXAMPLES_DIR,
    LLMS_TXT,
    RUNTIME_PROFILE_EXAMPLES_DIR,
    RECIPES_DIR,
    RECIPES_JSONL,
    SCHEMA_JSON,
    SCHEMA_YAML,
    SOURCE,
)


EXPECTED_EXAMPLES = [
    "minimal.yaml",
    "ci-validate-generated-fragments.yaml",
    "release-portfolio-review.yaml",
    "portfolio-localization.yaml",
    "hybrid-graph-review.yaml",
    "data-product-delivery.yaml",
    "graph-triggered-impact-review.yaml",
    "data-product-recipe.yaml",
]

EXPECTED_RUNTIME_PROFILE_EXAMPLES = [
    "production-quality.yaml",
    "local-fast.yaml",
    "local-graph.yaml",
    "internal-secure.yaml",
]

EXPECTED_RECORD_IDS = {"Recipe", "RuntimeProfile", "RecipeCatalog", "DataProductRecipe", "AgentDiscoveryFlow", "Step", "ExecutionPolicy", "ContextFormatPolicy", "GraphTrigger", "Gate"}


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
    assert document["kind"] == "RuntimeProfile"
    provider = document["runtimeProfile"]
    assert provider["provider"] == expected_id
    assert expected_id in provider["providers"]
    profile = provider["providers"][expected_id]
    assert isinstance(profile["type"], str) and profile["type"].strip()
    assert isinstance(profile["model"], str) and profile["model"].strip()


def assert_recipe_catalog_document(document):
    assert document["schema"] == "https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml"
    assert document["version"] == "1.0"
    assert document["kind"] == "RecipeCatalog"
    catalog = document["recipeCatalog"]
    assert isinstance(catalog["metadata"].get("id"), str) and catalog["metadata"]["id"].startswith("RCP-CATALOG-")
    assert_lang_string(catalog["metadata"].get("name"), "recipeCatalog.metadata.name")
    assert isinstance(catalog.get("version"), str) and catalog["version"].strip(), "recipeCatalog.version must be set"
    groups = catalog.get("groups", [])
    group_ids = []
    for index, group in enumerate(groups):
        forbidden = {"steps", "status", "runId", "logs", "plannedWrites"}
        assert forbidden.isdisjoint(group), f"recipeCatalog.groups[{index}] contains runtime or full-step fields"
        assert isinstance(group.get("id"), str) and group["id"].strip(), f"recipeCatalog.groups[{index}].id must be set"
        assert_lang_string(group.get("name"), f"recipeCatalog.groups[{index}].name")
        group_ids.append(group["id"])
    assert len(group_ids) == len(set(group_ids)), "recipeCatalog.groups ids must be unique"
    assert catalog["recipes"], "recipeCatalog.recipes must not be empty"
    for index, entry in enumerate(catalog["recipes"]):
        forbidden = {"steps", "status", "runId", "logs", "plannedWrites"}
        assert forbidden.isdisjoint(entry), f"recipeCatalog.recipes[{index}] contains runtime or full-step fields"
        assert entry["path"].endswith(".yaml"), f"recipeCatalog.recipes[{index}].path must point to YAML"
        if "commands" in entry:
            assert isinstance(entry["commands"], list), f"recipeCatalog.recipes[{index}].commands must be a list"
        if "groupRef" in entry:
            assert entry["groupRef"] in group_ids, f"recipeCatalog.recipes[{index}].groupRef must reference a declared group"


def assert_data_product_recipe_document(document):
    assert document["schema"] == "https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml"
    assert document["version"] == "1.0"
    assert document["kind"] == "DataProductRecipe"
    data_product_recipe = document["dataProductRecipe"]
    section_ids = {section["id"] for section in data_product_recipe["sections"]}
    assert "source-product-spec" in section_ids
    assert "ai-agent-brief" in section_ids
    assert "relationship-context" in section_ids
    assert 0 <= data_product_recipe["readiness"]["score"] <= 100


def check_schema():
    schema = load_yaml(SCHEMA_YAML)
    json_schema = load_json(SCHEMA_JSON)

    assert schema["required"] == ["schema", "version", "kind"], "YAML schema root requirements changed"
    assert json_schema["required"] == schema["required"], "JSON schema root requirements must match YAML schema"
    assert list(schema["properties"]) == ["schema", "version", "kind", "recipe", "runtimeProfile", "recipeCatalog", "dataProductRecipe"], "YAML schema root property order changed"
    assert list(json_schema["properties"]) == ["schema", "version", "kind", "recipe", "runtimeProfile", "recipeCatalog", "dataProductRecipe"], "JSON schema root property order changed"
    assert schema["properties"]["kind"]["enum"] == ["Recipe", "RuntimeProfile", "RecipeCatalog", "DataProductRecipe"], "YAML schema root kind must support Recipe, RuntimeProfile, RecipeCatalog, and DataProductRecipe"
    assert json_schema["properties"]["kind"]["enum"] == ["Recipe", "RuntimeProfile", "RecipeCatalog", "DataProductRecipe"], "JSON schema root kind must support Recipe, RuntimeProfile, RecipeCatalog, and DataProductRecipe"
    assert "recipe" in schema["properties"], "YAML schema must define recipe property"
    assert "runtimeProfile" in schema["properties"], "YAML schema must define runtimeProfile property"
    assert "recipeCatalog" in schema["properties"], "YAML schema must define recipeCatalog property"
    for runtime_kind in ["RecipeRunPlan", "RecipeRunManifest", "RecipeInspection"]:
        assert runtime_kind not in schema["properties"]["kind"]["enum"], f"{runtime_kind} must remain outside ODPR v1 roots"

    recipe = schema["$defs"][schema["properties"]["recipe"]["$ref"].split("/")[-1]]
    assert recipe["required"] == ["metadata", "version", "type", "steps"], "Recipe required fields changed unexpectedly"
    assert "version" in recipe["properties"], "Recipe must define recipe version"
    assert recipe["properties"]["scope"]["$ref"] == "#/$defs/RecipeScope", "Recipe must define optional scope"
    assert "execution" in recipe["properties"], "Recipe must define execution policy"
    assert "intent" in recipe["properties"], "Recipe must define optional intent"
    assert "instructions" in recipe["properties"], "Recipe must define optional instructions"
    assert "groundingTo" in recipe["properties"], "Recipe must define optional grounding"
    assert recipe["properties"]["groundingTo"]["$ref"] == "#/$defs/GroundingTarget", "groundingTo must use controlled graph grounding"
    grounding = schema["$defs"]["GroundingTarget"]
    assert grounding["properties"]["nodeTypes"]["items"]["$ref"] == "#/$defs/GraphNodeType", "groundingTo.nodeTypes must use GraphNodeType"
    assert grounding["properties"]["edgeTypes"]["items"]["$ref"] == "#/$defs/GraphEdgeType", "groundingTo.edgeTypes must use GraphEdgeType"
    assert schema["$defs"]["GraphEdgeType"]["enum"] == [
        "uses",
        "supports",
        "enables",
        "dependsOn",
    ], "GraphEdgeType enum changed unexpectedly"
    step = schema["$defs"]["Step"]
    assert step["required"] == ["id"], "Step must require id only"
    assert {"required": ["command"]} in step["anyOf"], "Step must allow executable command steps"
    assert {"required": ["discoveryType"]} in step["anyOf"], "Step must allow command-free discovery steps"
    assert any(
        branch.get("if", {}).get("required") == ["discoveryType"]
        and branch.get("then", {}).get("not", {}).get("required") == ["command"]
        for branch in step["allOf"]
    ), "Step.discoveryType must be mutually exclusive with command"
    assert schema["$defs"]["Step"]["properties"]["discoveryType"]["$ref"] == "#/$defs/DiscoveryStepType", "Step.discoveryType must use controlled discovery type"
    assert schema["$defs"]["DiscoveryStepType"]["enum"] == [
        "find-affected-use-cases",
        "explain-use-case-impact",
        "find-affected-data-products",
        "explain-data-product-impact",
        "find-affected-objectives",
        "explain-objective-impact",
        "identify-gaps-and-risks",
        "produce-findings-and-recommendations",
    ], "DiscoveryStepType enum changed unexpectedly"
    assert "contextFormat" in recipe["properties"], "Recipe must define context format policy"
    assert "trigger" in recipe["properties"], "Recipe must define optional graph trigger"
    assert "graphContext" in recipe["properties"], "Recipe must define optional graph context"
    assert "gates" in recipe["properties"], "Recipe must define gates"
    assert "review" in recipe["properties"], "Recipe must define review"
    trigger = schema["$defs"]["GraphTrigger"]
    assert trigger["properties"]["event"]["enum"] == [
        "node.added",
        "node.removed",
        "node.attributeChanged",
        "edge.added",
        "edge.removed",
        "edge.attributeChanged",
        "graph.conditionMatched",
    ], "GraphTrigger event enum changed unexpectedly"
    assert "*" in schema["$defs"]["GraphNodeType"]["enum"], "GraphNodeType must allow wildcard node type"

    provider = schema["$defs"][schema["properties"]["runtimeProfile"]["$ref"].split("/")[-1]]
    assert provider["required"] == ["provider", "providers"], "RuntimeProfile required fields changed unexpectedly"
    assert "model" in provider["properties"], "RuntimeProfile must define model"
    assert "portfolio" in provider["properties"], "RuntimeProfile must define portfolio policy"
    assert "providers" in provider["properties"], "RuntimeProfile must define providers map"
    provider_profile = schema["$defs"]["RuntimeProviderProfile"]
    assert "apiKeyEnv" in provider_profile["properties"], "RuntimeProviderProfile must define apiKeyEnv"
    assert "maxTokens" in provider_profile["properties"], "RuntimeProviderProfile must define maxTokens"

    catalog = schema["$defs"][schema["properties"]["recipeCatalog"]["$ref"].split("/")[-1]]
    assert catalog["required"] == ["metadata", "version", "recipes"], "RecipeCatalog required fields changed unexpectedly"
    assert "version" in catalog["properties"], "RecipeCatalog must define catalog version"
    assert "groups" in catalog["properties"], "RecipeCatalog must define optional groups"
    entry = schema["$defs"]["RecipeCatalogEntry"]
    assert "groupRef" in entry["properties"], "RecipeCatalogEntry must define optional groupRef"

    data_product_recipe = schema["$defs"][schema["properties"]["dataProductRecipe"]["$ref"].split("/")[-1]]
    assert data_product_recipe["properties"]["readiness"]["$ref"] == "#/$defs/DataProductRecipeReadiness", "DataProductRecipe must define readiness"


def check_examples():
    for filename in EXPECTED_EXAMPLES:
        path = EXAMPLES_DIR / filename
        assert path.is_file(), f"Missing example: {path.relative_to(SOURCE)}"
        load_yaml(path)

    assert_recipe_document(load_yaml(EXAMPLES_DIR / "minimal.yaml"), "dev")
    assert_recipe_document(load_yaml(EXAMPLES_DIR / "ci-validate-generated-fragments.yaml"), "ci")
    assert_recipe_document(load_yaml(EXAMPLES_DIR / "release-portfolio-review.yaml"), "release")
    assert_recipe_document(load_yaml(EXAMPLES_DIR / "portfolio-localization.yaml"), "localization")
    assert_recipe_document(load_yaml(EXAMPLES_DIR / "hybrid-graph-review.yaml"), "hybrid")
    data_product_recipe = load_yaml(EXAMPLES_DIR / "data-product-delivery.yaml")
    assert_recipe_document(data_product_recipe, "agent")
    assert data_product_recipe["recipe"]["scope"] == "data-product"
    graph_triggered_recipe = load_yaml(EXAMPLES_DIR / "graph-triggered-impact-review.yaml")
    assert_recipe_document(graph_triggered_recipe, "agent")
    assert graph_triggered_recipe["recipe"]["scope"] == "graph"
    assert graph_triggered_recipe["recipe"]["trigger"]["source"] == "odpg"
    assert graph_triggered_recipe["recipe"]["trigger"]["event"] == "node.attributeChanged"
    assert graph_triggered_recipe["recipe"]["trigger"]["subject"]["nodeType"] == "*"
    assert graph_triggered_recipe["recipe"]["trigger"]["subject"]["attribute"]["name"] == "status"
    assert graph_triggered_recipe["recipe"]["graphContext"]["start"] == "trigger.subject"
    assert graph_triggered_recipe["recipe"]["contextFormat"]["primary"] == "gcf"
    assert "DataProduct" in graph_triggered_recipe["recipe"]["groundingTo"]["nodeTypes"]
    assert "dependsOn" in graph_triggered_recipe["recipe"]["groundingTo"]["edgeTypes"]
    assert graph_triggered_recipe["recipe"]["intent"].strip()
    assert graph_triggered_recipe["recipe"]["instructions"].strip()
    graph_step = graph_triggered_recipe["recipe"]["steps"][0]
    assert graph_step["discoveryType"] == "produce-findings-and-recommendations"
    assert "command" not in graph_step
    assert graph_step["iterationLimit"] == 3
    assert graph_step["exitWhen"].strip()
    assert_data_product_recipe_document(load_yaml(EXAMPLES_DIR / "data-product-recipe.yaml"))
    assert_recipe_catalog_document(load_yaml(RECIPES_DIR / "catalog.yaml"))

    for filename in EXPECTED_RUNTIME_PROFILE_EXAMPLES:
        path = RUNTIME_PROFILE_EXAMPLES_DIR / filename
        assert path.is_file(), f"Missing provider example: {path.relative_to(SOURCE)}"
        load_yaml(path)

    assert_provider_document(load_yaml(RUNTIME_PROFILE_EXAMPLES_DIR / "production-quality.yaml"), "production-quality")
    assert_provider_document(load_yaml(RUNTIME_PROFILE_EXAMPLES_DIR / "local-fast.yaml"), "local-fast")
    assert_provider_document(load_yaml(RUNTIME_PROFILE_EXAMPLES_DIR / "local-graph.yaml"), "local-graph")
    assert_provider_document(load_yaml(RUNTIME_PROFILE_EXAMPLES_DIR / "internal-secure.yaml"), "internal-secure")

    ci_recipe = load_yaml(EXAMPLES_DIR / "ci-validate-generated-fragments.yaml")["recipe"]
    assert "execution" not in ci_recipe
    assert "contextFormat" not in ci_recipe
    assert ci_recipe["gates"][0]["type"] == "validation"

    release_recipe = load_yaml(EXAMPLES_DIR / "release-portfolio-review.yaml")["recipe"]
    assert release_recipe["execution"]["mode"] == "hosted"
    assert release_recipe["review"]["required"] is True

    hybrid_recipe = load_yaml(EXAMPLES_DIR / "hybrid-graph-review.yaml")["recipe"]
    assert hybrid_recipe["execution"]["mode"] == "hybrid"
    assert (
        hybrid_recipe["steps"][0]["runtimeRef"]
        == "runtime-profiles/examples/local-graph.yaml#local-graph"
    )
    assert (
        hybrid_recipe["steps"][1]["runtimeRef"]
        == "runtime-profiles/examples/production-quality.yaml#production-quality"
    )

    localization_recipe = load_yaml(EXAMPLES_DIR / "portfolio-localization.yaml")["recipe"]
    assert isinstance(localization_recipe["steps"][0]["languages"], list)


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
        "/recipes/examples/portfolio-localization.yaml",
        "/recipes/examples/data-product-delivery.yaml",
        "/recipes/examples/graph-triggered-impact-review.yaml",
        "/recipes/examples/data-product-recipe.yaml",
        "/recipes/catalog.yaml",
        "/runtime-profiles/examples/production-quality.yaml",
        "/schema/odpr.yaml",
        "/schema/odpr.json",
        "scripts/build_recipe_catalog.py",
        "agent discovery flows",
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
