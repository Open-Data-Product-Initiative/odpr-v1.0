import subprocess
import sys


def run_validator(path):
    return subprocess.run(
        [sys.executable, "scripts/validate_recipe.py", str(path)],
        check=False,
        text=True,
        capture_output=True,
    )


def test_validator_rejects_embedded_api_key_in_recipe(tmp_path):
    recipe = tmp_path / "embedded-secret.yaml"
    recipe.write_text(
        """schema: https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml
version: "1.0"
kind: Recipe
recipe:
  metadata:
    id: RCP-SECRET-001
    name:
      en: Secret Example
    description:
      en: Demonstrates an invalid embedded API key.
  version: "1.0.0"
  type: dev
  steps:
    - id: generate
      command: generate
      with:
        apiKey: sk-test-should-not-be-here
""",
        encoding="utf-8",
    )

    result = run_validator(recipe)

    assert result.returncode == 1
    assert "embedded secret" in result.stderr
    assert "recipe.steps[0].with.apiKey" in result.stderr


def test_validator_allows_credentials_ref_in_provider(tmp_path):
    provider = tmp_path / "provider-ref.yaml"
    provider.write_text(
        """schema: https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml
version: "1.0"
kind: Provider
provider:
  id: production-quality
  provider: openai
  model: gpt-4.1
  credentialsRef: env:OPENAI_API_KEY
""",
        encoding="utf-8",
    )

    result = run_validator(provider)

    assert result.returncode == 0
