import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_script(*args):
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class AgentScriptsTest(unittest.TestCase):
    def test_check_agent_artifacts_script_passes(self):
        result = run_script("scripts/check_agent_artifacts.py")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("OK", result.stdout)

    def test_search_recipes_returns_json_results(self):
        result = run_script("scripts/search_recipes.py", "context", "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        records = json.loads(result.stdout)
        ids = {record["id"] for record in records}
        self.assertIn("ContextPolicy", ids)

    def test_search_recipes_can_show_one_record(self):
        result = run_script("scripts/search_recipes.py", "--id", "Recipe")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Recipe", result.stdout)
        self.assertIn("workflow", result.stdout)

    def test_validate_recipe_accepts_minimal_example_or_reports_missing_dependency(self):
        result = run_script("scripts/validate_recipe.py", "source/recipes/examples/minimal.yaml")

        if result.returncode == 2:
            self.assertIn("jsonschema", result.stderr)
        else:
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("valid", result.stdout.lower())

    def test_generate_recipe_artifacts_check_passes(self):
        result = run_script("scripts/generate_recipe_artifacts.py", "--check")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("up to date", result.stdout.lower())

    def test_build_recipe_catalog_generates_metadata_only_catalog(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "catalog.yaml"
            result = run_script("scripts/build_recipe_catalog.py", "--output", str(output))

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            document = __import__("yaml").safe_load(output.read_text(encoding="utf-8"))

        self.assertEqual(document["kind"], "RecipeCatalog")
        groups = document["recipeCatalog"]["groups"]
        self.assertEqual(groups[0]["id"], "examples")
        self.assertEqual(groups[0]["name"], {"en": "Example Recipes"})
        recipes = document["recipeCatalog"]["recipes"]
        self.assertGreaterEqual(len(recipes), 5)

        ci_entry = next(entry for entry in recipes if entry["id"] == "RCP-CI-001")
        self.assertEqual(ci_entry["path"], "recipes/examples/ci-validate-generated-fragments.yaml")
        self.assertEqual(ci_entry["groupRef"], "examples")
        self.assertEqual(ci_entry["executionMode"], "local")
        self.assertEqual(ci_entry["providerRef"], "local-fast")
        self.assertEqual(ci_entry["contextFormat"], "gcf")
        self.assertFalse(ci_entry["requiresReview"])
        self.assertEqual(ci_entry["commands"], ["generate", "validate"])
        self.assertNotIn("steps", ci_entry)
        self.assertNotIn("runId", ci_entry)
        self.assertNotIn("logs", ci_entry)

    def test_build_recipe_catalog_check_passes_for_current_catalog(self):
        result = run_script("scripts/build_recipe_catalog.py", "--check")

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("up to date", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
