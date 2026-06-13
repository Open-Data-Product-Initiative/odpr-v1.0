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
    assert recipe["metadata"]["id"].startswith("RCP-")
    assert_lang_string(recipe["metadata"]["name"])
    assert_lang_string(recipe["metadata"]["description"])
    assert recipe["steps"]


class AgentArtifactsTest(unittest.TestCase):
    def test_schema_uses_recipe_root(self):
        schema = load_yaml(SOURCE / "schema" / "odpr.yaml")
        json_schema = json.loads((SOURCE / "schema" / "odpr.json").read_text(encoding="utf-8"))

        self.assertEqual(schema["required"], ["schema", "version", "kind", "recipe"])
        self.assertEqual(list(schema["properties"]), ["schema", "version", "kind", "recipe"])
        self.assertEqual(schema["properties"]["kind"]["const"], "Recipe")
        self.assertIn("recipe", schema["properties"])
        self.assertNotIn("catalog", schema["properties"])
        self.assertEqual(json_schema["required"], schema["required"])
        self.assertEqual(list(json_schema["properties"]), ["schema", "version", "kind", "recipe"])
        self.assertEqual(json_schema["properties"]["kind"]["const"], "Recipe")

        recipe_ref = schema["properties"]["recipe"]["$ref"].split("/")[-1]
        recipe = schema["$defs"][recipe_ref]
        self.assertEqual(recipe["required"], ["metadata", "type", "steps"])
        self.assertIn("execution", recipe["properties"])
        self.assertIn("context", recipe["properties"])
        self.assertIn("gates", recipe["properties"])
        self.assertIn("review", recipe["properties"])

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

    def test_retrieval_jsonl_is_parseable_and_referenced(self):
        jsonl_path = SOURCE / "recipes" / "recipes.jsonl"
        self.assertTrue(jsonl_path.is_file())

        records = [
            json.loads(line)
            for line in jsonl_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

        ids = {record["id"] for record in records}
        self.assertEqual(ids, {"Recipe", "Step", "ExecutionPolicy", "ContextPolicy", "Gate"})

        for record in records:
            self.assertTrue(record["definition"])
            self.assertIsInstance(record["requiredFields"], list)
            self.assertTrue(record["doUseFor"])
            self.assertTrue(record["doNotUseFor"])

        llms = (SOURCE / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("/recipes/recipes.jsonl", llms)
        self.assertIn("/schema/odpr.yaml", llms)


if __name__ == "__main__":
    unittest.main()
