import json
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"


def load_yaml(path):
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def assert_lang_string(value):
    assert isinstance(value, dict)
    assert isinstance(value.get("en"), str)
    assert value["en"].strip()


def assert_recipe_document(document, expected_type):
    assert document["schema"] == "https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml"
    assert document["version"] == "1.0"
    assert document["kind"] == "Recipe"
    recipe = document["recipe"]
    assert recipe["type"] == expected_type
    assert recipe["version"]
    assert recipe["metadata"]["id"].startswith("RCP-")
    assert_lang_string(recipe["metadata"]["name"])
    assert_lang_string(recipe["metadata"]["description"])
    assert recipe["steps"]


def assert_provider_document(document, expected_id):
    assert document["schema"] == "https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml"
    assert document["version"] == "1.0"
    assert document["kind"] == "RuntimeProfile"
    provider = document["runtimeProfile"]
    assert provider["provider"] == expected_id
    assert expected_id in provider["providers"]
    assert provider["providers"][expected_id]["type"]
    assert provider["providers"][expected_id]["model"]


def assert_recipe_catalog_document(document):
    assert document["schema"] == "https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml"
    assert document["version"] == "1.0"
    assert document["kind"] == "RecipeCatalog"
    catalog = document["recipeCatalog"]
    assert catalog["metadata"]["id"].startswith("RCP-CATALOG-")
    assert_lang_string(catalog["metadata"]["name"])
    assert catalog["version"]
    groups = catalog.get("groups", [])
    group_ids = []
    for group in groups:
        assert set(group).isdisjoint({"steps", "status", "runId", "logs", "plannedWrites"})
        assert group["id"]
        assert_lang_string(group["name"])
        group_ids.append(group["id"])
    assert len(group_ids) == len(set(group_ids))
    assert catalog["recipes"]
    for entry in catalog["recipes"]:
        assert set(entry).isdisjoint({"steps", "status", "runId", "logs", "plannedWrites"})
        assert entry["path"].endswith(".yaml")
        assert entry["id"].startswith("RCP-")
        assert_lang_string(entry["name"])
        if "groupRef" in entry:
            assert entry["groupRef"] in group_ids


def assert_data_product_recipe_document(document):
    assert document["schema"] == "https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml"
    assert document["version"] == "1.0"
    assert document["kind"] == "DataProductRecipe"
    data_product_recipe = document["dataProductRecipe"]
    assert data_product_recipe["version"] == "1.0.0"
    section_ids = {section["id"] for section in data_product_recipe["sections"]}
    assert section_ids == {
        "recipe-readme",
        "source-product-spec",
        "product-summary",
        "delivery-plan",
        "open-questions",
        "ai-agent-brief",
        "relationship-context",
    }
    assert isinstance(data_product_recipe["readiness"]["score"], int)
    assert 0 <= data_product_recipe["readiness"]["score"] <= 100


class AgentArtifactsTest(unittest.TestCase):
    def test_schema_uses_recipe_provider_and_catalog_roots(self):
        schema = load_yaml(SOURCE / "schema" / "odpr.yaml")
        json_schema = json.loads((SOURCE / "schema" / "odpr.json").read_text(encoding="utf-8"))

        self.assertEqual(schema["required"], ["schema", "version", "kind"])
        self.assertEqual(list(schema["properties"]), ["schema", "version", "kind", "recipe", "runtimeProfile", "recipeCatalog", "dataProductRecipe"])
        self.assertEqual(schema["properties"]["kind"]["enum"], ["Recipe", "RuntimeProfile", "RecipeCatalog", "DataProductRecipe"])
        self.assertIn("recipe", schema["properties"])
        self.assertIn("runtimeProfile", schema["properties"])
        self.assertIn("recipeCatalog", schema["properties"])
        self.assertIn("dataProductRecipe", schema["properties"])
        self.assertNotIn("RecipeRunPlan", schema["properties"]["kind"]["enum"])
        self.assertNotIn("RecipeRunManifest", schema["properties"]["kind"]["enum"])
        self.assertNotIn("RecipeInspection", schema["properties"]["kind"]["enum"])
        self.assertEqual(json_schema["required"], schema["required"])
        self.assertEqual(list(json_schema["properties"]), ["schema", "version", "kind", "recipe", "runtimeProfile", "recipeCatalog", "dataProductRecipe"])
        self.assertEqual(json_schema["properties"]["kind"]["enum"], ["Recipe", "RuntimeProfile", "RecipeCatalog", "DataProductRecipe"])

        recipe_ref = schema["properties"]["recipe"]["$ref"].split("/")[-1]
        recipe = schema["$defs"][recipe_ref]
        self.assertEqual(recipe["required"], ["metadata", "version", "type", "steps"])
        self.assertIn("version", recipe["properties"])
        scope_ref = recipe["properties"]["scope"]["$ref"].split("/")[-1]
        self.assertEqual(schema["$defs"][scope_ref]["enum"], ["data-product", "catalog", "graph", "portfolio"])
        self.assertIn("execution", recipe["properties"])
        self.assertIn("intent", recipe["properties"])
        self.assertIn("instructions", recipe["properties"])
        self.assertIn("groundingTo", recipe["properties"])
        self.assertIn("contextFormat", recipe["properties"])
        self.assertIn("trigger", recipe["properties"])
        self.assertIn("graphContext", recipe["properties"])
        self.assertIn("gates", recipe["properties"])
        self.assertIn("review", recipe["properties"])
        step = schema["$defs"]["Step"]
        self.assertIn("iterationLimit", step["properties"])
        self.assertIn("exitWhen", step["properties"])
        trigger = schema["$defs"]["GraphTrigger"]
        self.assertEqual(
            trigger["properties"]["event"]["enum"],
            [
                "node.added",
                "node.removed",
                "node.attributeChanged",
                "edge.added",
                "edge.removed",
                "edge.attributeChanged",
                "graph.conditionMatched",
            ],
        )
        node_type = schema["$defs"]["GraphNodeType"]
        self.assertIn("*", node_type["enum"])
        attribute = schema["$defs"]["GraphTriggerAttribute"]
        self.assertNotIn("*", attribute["properties"]["name"].get("enum", []))

        provider_ref = schema["properties"]["runtimeProfile"]["$ref"].split("/")[-1]
        provider = schema["$defs"][provider_ref]
        self.assertEqual(provider["required"], ["provider", "providers"])
        self.assertIn("model", provider["properties"])
        self.assertIn("portfolio", provider["properties"])
        self.assertIn("providers", provider["properties"])
        provider_profile = schema["$defs"]["RuntimeProviderProfile"]
        self.assertIn("apiKeyEnv", provider_profile["properties"])
        self.assertIn("maxTokens", provider_profile["properties"])

        catalog_ref = schema["properties"]["recipeCatalog"]["$ref"].split("/")[-1]
        catalog = schema["$defs"][catalog_ref]
        self.assertEqual(catalog["required"], ["metadata", "version", "recipes"])
        self.assertIn("version", catalog["properties"])
        self.assertIn("groups", catalog["properties"])
        self.assertIn("groupRef", schema["$defs"]["RecipeCatalogEntry"]["properties"])

        data_product_recipe_ref = schema["properties"]["dataProductRecipe"]["$ref"].split("/")[-1]
        data_product_recipe = schema["$defs"][data_product_recipe_ref]
        readiness_ref = data_product_recipe["properties"]["readiness"]["$ref"].split("/")[-1]
        readiness = schema["$defs"][readiness_ref]
        self.assertEqual(readiness["properties"]["score"]["minimum"], 0)
        self.assertEqual(readiness["properties"]["score"]["maximum"], 100)

    def test_examples_cover_minimal_ci_release_and_hybrid_recipes(self):
        expected = [
            "minimal.yaml",
            "ci-validate-generated-fragments.yaml",
            "release-portfolio-review.yaml",
            "portfolio-localization.yaml",
            "hybrid-graph-review.yaml",
            "data-product-delivery.yaml",
            "graph-triggered-impact-review.yaml",
        ]

        for filename in expected:
            self.assertTrue((SOURCE / "recipes" / "examples" / filename).is_file())

        assert_recipe_document(
            load_yaml(SOURCE / "recipes" / "examples" / "minimal.yaml"),
            "dev",
        )
        ci_recipe = load_yaml(
            SOURCE / "recipes" / "examples" / "ci-validate-generated-fragments.yaml"
        )
        release_recipe = load_yaml(
            SOURCE / "recipes" / "examples" / "release-portfolio-review.yaml"
        )
        hybrid_recipe = load_yaml(
            SOURCE / "recipes" / "examples" / "hybrid-graph-review.yaml"
        )

        assert_recipe_document(ci_recipe, "ci")
        assert_recipe_document(release_recipe, "release")
        assert_recipe_document(hybrid_recipe, "hybrid")

        self.assertNotIn("execution", ci_recipe["recipe"])
        self.assertNotIn("contextFormat", ci_recipe["recipe"])
        self.assertEqual(release_recipe["recipe"]["execution"]["mode"], "hosted")
        self.assertTrue(release_recipe["recipe"]["review"]["required"])
        self.assertEqual(hybrid_recipe["recipe"]["execution"]["mode"], "hybrid")

        localization_recipe = load_yaml(
            SOURCE / "recipes" / "examples" / "portfolio-localization.yaml"
        )
        assert_recipe_document(localization_recipe, "localization")
        languages = localization_recipe["recipe"]["steps"][0]["languages"]
        self.assertIsInstance(languages, list)

        data_product_recipe = load_yaml(
            SOURCE / "recipes" / "examples" / "data-product-delivery.yaml"
        )
        assert_recipe_document(data_product_recipe, "agent")
        self.assertEqual(data_product_recipe["recipe"]["scope"], "data-product")

        graph_triggered_recipe = load_yaml(
            SOURCE / "recipes" / "examples" / "graph-triggered-impact-review.yaml"
        )
        assert_recipe_document(graph_triggered_recipe, "agent")
        self.assertEqual(graph_triggered_recipe["recipe"]["scope"], "graph")
        self.assertEqual(
            graph_triggered_recipe["recipe"]["trigger"]["event"],
            "node.attributeChanged",
        )
        self.assertEqual(
            graph_triggered_recipe["recipe"]["trigger"]["subject"]["nodeType"],
            "*",
        )
        self.assertEqual(
            graph_triggered_recipe["recipe"]["trigger"]["subject"]["attribute"]["name"],
            "status",
        )
        self.assertEqual(
            graph_triggered_recipe["recipe"]["graphContext"]["start"],
            "trigger.subject",
        )
        self.assertEqual(graph_triggered_recipe["recipe"]["contextFormat"]["primary"], "gcf")
        self.assertIn("data-product", graph_triggered_recipe["recipe"]["groundingTo"])
        self.assertTrue(graph_triggered_recipe["recipe"]["intent"].strip())
        self.assertTrue(graph_triggered_recipe["recipe"]["instructions"].strip())
        graph_step = graph_triggered_recipe["recipe"]["steps"][0]
        self.assertEqual(graph_step["iterationLimit"], 3)
        self.assertTrue(graph_step["exitWhen"].strip())

    def test_examples_cover_recipe_catalog(self):
        document = load_yaml(SOURCE / "recipes" / "catalog.yaml")
        assert_recipe_catalog_document(document)

    def test_examples_cover_data_product_recipe(self):
        document = load_yaml(SOURCE / "recipes" / "examples" / "data-product-recipe.yaml")
        assert_data_product_recipe_document(document)

    def test_examples_cover_provider_profiles(self):
        expected = [
            "production-quality.yaml",
            "local-fast.yaml",
            "local-graph.yaml",
            "internal-secure.yaml",
        ]

        for filename in expected:
            self.assertTrue((SOURCE / "runtime-profiles" / "examples" / filename).is_file())

        assert_provider_document(
            load_yaml(SOURCE / "runtime-profiles" / "examples" / "production-quality.yaml"),
            "production-quality",
        )
        assert_provider_document(
            load_yaml(SOURCE / "runtime-profiles" / "examples" / "local-fast.yaml"),
            "local-fast",
        )
        assert_provider_document(
            load_yaml(SOURCE / "runtime-profiles" / "examples" / "local-graph.yaml"),
            "local-graph",
        )
        assert_provider_document(
            load_yaml(SOURCE / "runtime-profiles" / "examples" / "internal-secure.yaml"),
            "internal-secure",
        )

    def test_retrieval_jsonl_is_parseable_and_referenced(self):
        jsonl_path = SOURCE / "recipes" / "recipes.jsonl"
        self.assertTrue(jsonl_path.is_file())

        records = [
            json.loads(line)
            for line in jsonl_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

        ids = {record["id"] for record in records}
        self.assertEqual(ids, {"Recipe", "RuntimeProfile", "RecipeCatalog", "DataProductRecipe", "Step", "ExecutionPolicy", "ContextFormatPolicy", "GraphTrigger", "Gate"})

        for record in records:
            self.assertTrue(record["definition"])
            self.assertIsInstance(record["requiredFields"], list)
            self.assertTrue(record["doUseFor"])
            self.assertTrue(record["doNotUseFor"])

        llms = (SOURCE / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("/recipes/recipes.jsonl", llms)
        self.assertIn("/schema/odpr.yaml", llms)
        self.assertIn("/runtime-profiles/examples/production-quality.yaml", llms)
        self.assertIn("/recipes/examples/data-product-recipe.yaml", llms)
        self.assertIn("scripts/build_recipe_catalog.py", llms)

    def test_agent_guidance_has_current_recipe_contract_wording(self):
        llms = (SOURCE / "llms.txt").read_text(encoding="utf-8")
        llms_words = " ".join(llms.split())
        index = (SOURCE / "index.html.md").read_text(encoding="utf-8")
        library = (SOURCE / "includes" / "_recipe_library.md").read_text(encoding="utf-8")

        self.assertNotIn("6. Use provider references", llms)
        self.assertNotIn("metadata requires stable id, name, and description", llms_words)
        self.assertNotIn("define data products, catalogs, graphs", llms_words)
        self.assertIn("define data products, ODPC catalog object models, graphs", llms_words)
        self.assertIn("Data Product Recipe handoff document", llms_words)
        self.assertIn("Optional recipe references are provenance, not implementation dependencies", llms_words)
        self.assertIn("DataProductRecipe", llms_words)
        self.assertIn("Do not use `ProductRecipe`", llms_words)

        self.assertNotIn("provider reference or provider class", index)
        self.assertNotIn("operation against `generated/fragments/`", index)
        self.assertNotIn("operation against `generated/fragments/signal.yaml`", index)
        self.assertIn("data_product_recipe", index)
        self.assertIn("three composite flow contracts", index)
        self.assertIn("Read the three flow sections first", index)
        self.assertIn("validates `generated/fragments/signal.yaml`", library)


if __name__ == "__main__":
    unittest.main()
