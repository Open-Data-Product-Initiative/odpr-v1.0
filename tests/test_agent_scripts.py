import json
import subprocess
import sys
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


if __name__ == "__main__":
    unittest.main()
