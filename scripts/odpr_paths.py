from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source"
SCHEMA_YAML = SOURCE / "schema" / "odpr.yaml"
SCHEMA_JSON = SOURCE / "schema" / "odpr.json"
RECIPES_DIR = SOURCE / "recipes"
RECIPES_JSONL = RECIPES_DIR / "recipes.jsonl"
LLMS_TXT = SOURCE / "llms.txt"
EXAMPLES_DIR = RECIPES_DIR / "examples"
