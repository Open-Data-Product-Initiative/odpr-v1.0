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


class AgentArtifactsTest(unittest.TestCase):
    def test_schema_uses_recipe_and_provider_roots(self):
        schema = load_yaml(SOURCE / "schema" / "odpr.yaml")
        json_schema = json.loads((SOURCE / "schema" / "odpr.json").read_text(encoding="utf-8"))

        self.assertEqual(schema["required"], ["schema", "version", "kind"])
        self.assertEqual(list(schema["properties"]), ["schema", "version", "kind", "recipe", "provider"])
        self.assertEqual(schema["properties"]["kind"]["enum"], ["Recipe", "Provider"])
        self.assertIn("recipe", schema["properties"])
        self.assertIn("provider", schema["properties"])
        self.assertNotIn("catalog", schema["properties"])
        self.assertEqual(json_schema["required"], schema["required"])
        self.assertEqual(list(json_schema["properties"]), ["schema", "version", "kind", "recipe", "provider"])
        self.assertEqual(json_schema["properties"]["kind"]["enum"], ["Recipe", "Provider"])

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

    def test_examples_cover_minimal_ci_release_and_hybrid_recipes(self):
        expected = [
            "minimal.yaml",
            "ci-validate-generated-fragments.yaml",
            "release-portfolio-review.yaml",
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
        self.assertEqual(ids, {"Recipe", "Provider", "Step", "ExecutionPolicy", "ContextPolicy", "Gate"})

        for record in records:
            self.assertTrue(record["definition"])
            self.assertIsInstance(record["requiredFields"], list)
            self.assertTrue(record["doUseFor"])
            self.assertTrue(record["doNotUseFor"])

        llms = (SOURCE / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("/recipes/recipes.jsonl", llms)
        self.assertIn("/schema/odpr.yaml", llms)
        self.assertIn("/providers/examples/production-quality.yaml", llms)


if __name__ == "__main__":
    unittest.main()
