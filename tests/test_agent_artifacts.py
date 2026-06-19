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
    assert document["kind"] == "Provider"
    provider = document["provider"]
    assert provider["id"] == expected_id
    assert provider["provider"]


def assert_recipe_catalog_document(document):
    assert document["schema"] == "https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml"
    assert document["version"] == "1.0"
    assert document["kind"] == "RecipeCatalog"
    catalog = document["recipeCatalog"]
    assert catalog["metadata"]["id"].startswith("RCP-CATALOG-")
    assert_lang_string(catalog["metadata"]["name"])
    assert catalog["recipes"]
    for entry in catalog["recipes"]:
        assert set(entry).isdisjoint({"steps", "status", "runId", "logs", "plannedWrites"})
        assert entry["path"].endswith(".yaml")
        assert entry["id"].startswith("RCP-")
        assert_lang_string(entry["name"])


class AgentArtifactsTest(unittest.TestCase):
    def test_schema_uses_recipe_provider_and_catalog_roots(self):
        schema = load_yaml(SOURCE / "schema" / "odpr.yaml")
        json_schema = json.loads((SOURCE / "schema" / "odpr.json").read_text(encoding="utf-8"))

        self.assertEqual(schema["required"], ["schema", "version", "kind"])
        self.assertEqual(list(schema["properties"]), ["schema", "version", "kind", "recipe", "provider", "recipeCatalog"])
        self.assertEqual(schema["properties"]["kind"]["enum"], ["Recipe", "Provider", "RecipeCatalog"])
        self.assertIn("recipe", schema["properties"])
        self.assertIn("provider", schema["properties"])
        self.assertIn("recipeCatalog", schema["properties"])
        self.assertNotIn("RecipeRunPlan", schema["properties"]["kind"]["enum"])
        self.assertNotIn("RecipeRunManifest", schema["properties"]["kind"]["enum"])
        self.assertNotIn("RecipeInspection", schema["properties"]["kind"]["enum"])
        self.assertEqual(json_schema["required"], schema["required"])
        self.assertEqual(list(json_schema["properties"]), ["schema", "version", "kind", "recipe", "provider", "recipeCatalog"])
        self.assertEqual(json_schema["properties"]["kind"]["enum"], ["Recipe", "Provider", "RecipeCatalog"])

        recipe_ref = schema["properties"]["recipe"]["$ref"].split("/")[-1]
        recipe = schema["$defs"][recipe_ref]
        self.assertEqual(recipe["required"], ["metadata", "version", "type", "steps"])
        self.assertIn("version", recipe["properties"])
        self.assertIn("execution", recipe["properties"])
        self.assertIn("context", recipe["properties"])
        self.assertIn("gates", recipe["properties"])
        self.assertIn("review", recipe["properties"])

        provider_ref = schema["properties"]["provider"]["$ref"].split("/")[-1]
        provider = schema["$defs"][provider_ref]
        self.assertEqual(provider["required"], ["id", "provider"])
        self.assertIn("model", provider["properties"])
        self.assertIn("credentialsRef", provider["properties"])
        self.assertIn("temperature", provider["properties"])

        catalog_ref = schema["properties"]["recipeCatalog"]["$ref"].split("/")[-1]
        catalog = schema["$defs"][catalog_ref]
        self.assertEqual(catalog["required"], ["metadata", "recipes"])

    def test_examples_cover_minimal_ci_release_and_hybrid_recipes(self):
        expected = [
            "minimal.yaml",
            "ci-validate-generated-fragments.yaml",
            "release-portfolio-review.yaml",
            "portfolio-localization.yaml",
            "hybrid-graph-review.yaml",
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

        self.assertEqual(ci_recipe["recipe"]["execution"]["mode"], "local")
        self.assertEqual(ci_recipe["recipe"]["context"]["format"], "gcf")
        self.assertEqual(release_recipe["recipe"]["execution"]["mode"], "hosted")
        self.assertTrue(release_recipe["recipe"]["review"]["required"])
        self.assertEqual(hybrid_recipe["recipe"]["execution"]["mode"], "hybrid")

        localization_recipe = load_yaml(
            SOURCE / "recipes" / "examples" / "portfolio-localization.yaml"
        )
        assert_recipe_document(localization_recipe, "localization")
        languages = localization_recipe["recipe"]["steps"][0]["with"]["languages"]
        self.assertIsInstance(languages, list)

    def test_examples_cover_recipe_catalog(self):
        document = load_yaml(SOURCE / "recipes" / "catalog.yaml")
        assert_recipe_catalog_document(document)

    def test_examples_cover_provider_profiles(self):
        expected = [
            "production-quality.yaml",
            "local-fast.yaml",
            "local-graph.yaml",
            "internal-secure.yaml",
        ]

        for filename in expected:
            self.assertTrue((SOURCE / "providers" / "examples" / filename).is_file())

        assert_provider_document(
            load_yaml(SOURCE / "providers" / "examples" / "production-quality.yaml"),
            "production-quality",
        )
        assert_provider_document(
            load_yaml(SOURCE / "providers" / "examples" / "local-fast.yaml"),
            "local-fast",
        )
        assert_provider_document(
            load_yaml(SOURCE / "providers" / "examples" / "local-graph.yaml"),
            "local-graph",
        )
        assert_provider_document(
            load_yaml(SOURCE / "providers" / "examples" / "internal-secure.yaml"),
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
        self.assertEqual(ids, {"Recipe", "Provider", "RecipeCatalog", "Step", "ExecutionPolicy", "ContextPolicy", "Gate"})

        for record in records:
            self.assertTrue(record["definition"])
            self.assertIsInstance(record["requiredFields"], list)
            self.assertTrue(record["doUseFor"])
            self.assertTrue(record["doNotUseFor"])

        llms = (SOURCE / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("/recipes/recipes.jsonl", llms)
        self.assertIn("/schema/odpr.yaml", llms)
        self.assertIn("/providers/examples/production-quality.yaml", llms)

    def test_agent_guidance_has_current_recipe_contract_wording(self):
        llms = (SOURCE / "llms.txt").read_text(encoding="utf-8")
        llms_words = " ".join(llms.split())
        index = (SOURCE / "index.html.md").read_text(encoding="utf-8")
        library = (SOURCE / "includes" / "_recipe_library.md").read_text(encoding="utf-8")

        self.assertNotIn("6. Use provider references", llms)
        self.assertNotIn("metadata requires stable id, name, and description", llms_words)
        self.assertNotIn("define data products, catalogs, graphs", llms_words)
        self.assertIn("define data products, ODPC catalog object models, graphs", llms_words)

        self.assertNotIn("provider reference or provider class", index)
        self.assertNotIn("operation against `generated/fragments/`", index)
        self.assertIn("operation against `generated/fragments/signal.yaml`", index)
        self.assertIn("validates `generated/fragments/signal.yaml`", library)


if __name__ == "__main__":
    unittest.main()
