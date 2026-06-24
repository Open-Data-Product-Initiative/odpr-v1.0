import pytest
import yaml
from jsonschema import Draft202012Validator


SCHEMA_URI = "https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml"


@pytest.fixture(scope="module")
def validator():
    with open("source/schema/odpr.yaml", encoding="utf-8") as handle:
        schema = yaml.safe_load(handle)
    return Draft202012Validator(schema)


def assert_valid(validator, document):
    errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
    assert errors == []


def assert_invalid(validator, document):
    errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
    assert errors
    return errors


def recipe_with_step(step):
    return {
        "schema": SCHEMA_URI,
        "version": "1.0",
        "kind": "Recipe",
        "recipe": {
            "metadata": {
                "id": "RCP-TEST-001",
                "name": {"en": "Test Recipe"},
                "description": {"en": "Schema validation fixture."},
            },
            "version": "1.0.0",
            "type": "dev",
            "steps": [step],
        },
    }


def test_recipe_catalog_validates_and_stays_metadata_only(validator):
    catalog = {
        "schema": SCHEMA_URI,
        "version": "1.0",
        "kind": "RecipeCatalog",
        "recipeCatalog": {
            "metadata": {
                "id": "RCP-CATALOG-001",
                "name": {"en": "SDK Recipe Catalog"},
            },
            "version": "1.0.0",
            "groups": [
                {
                    "id": "examples",
                    "name": {"en": "Example Recipes"},
                    "description": {"en": "Complete learning and demonstration recipes."},
                }
            ],
            "recipes": [
                {
                    "path": "recipes/release-portfolio-review.yaml",
                    "id": "RCP-RELEASE-001",
                    "groupRef": "examples",
                    "version": "1.0.0",
                    "type": "release",
                    "name": {"en": "Release Portfolio Review"},
                    "commands": ["portfolio.refresh", "portfolio.localize"],
                    "requiresReview": True,
                }
            ],
        },
    }

    assert_valid(validator, catalog)

    catalog["recipeCatalog"]["recipes"][0]["steps"] = [
        {"id": "refresh", "command": "portfolio.refresh"}
    ]
    assert_invalid(validator, catalog)


def test_recipe_catalog_group_requires_id_and_name(validator):
    catalog = {
        "schema": SCHEMA_URI,
        "version": "1.0",
        "kind": "RecipeCatalog",
        "recipeCatalog": {
            "metadata": {
                "id": "RCP-CATALOG-001",
                "name": {"en": "SDK Recipe Catalog"},
            },
            "version": "1.0.0",
            "groups": [{"id": "examples"}],
            "recipes": [
                {
                    "path": "recipes/release-portfolio-review.yaml",
                    "id": "RCP-RELEASE-001",
                    "version": "1.0.0",
                    "type": "release",
                    "name": {"en": "Release Portfolio Review"},
                }
            ],
        },
    }

    assert_invalid(validator, catalog)


@pytest.mark.parametrize("kind", ["RecipeRunPlan", "RecipeRunManifest", "RecipeInspection"])
def test_runtime_root_kinds_are_not_v1_documents(validator, kind):
    document = {"schema": SCHEMA_URI, "version": "1.0", "kind": kind}

    assert_invalid(validator, document)


def test_recipe_must_have_at_least_one_step(validator):
    document = recipe_with_step({"id": "generate", "command": "generate"})
    document["recipe"]["steps"] = []

    assert_invalid(validator, document)


def test_deterministic_commands_reject_provider_ref_and_model(validator):
    document = recipe_with_step(
        {
            "id": "validate",
            "command": "validate",
            "providerRef": "production-quality",
            "model": "gpt-4.1",
            "with": {"document": "generated/fragments/signal.yaml"},
        }
    )

    assert_invalid(validator, document)


def test_llm_backed_generate_accepts_provider_ref_and_required_parameters(validator):
    document = recipe_with_step(
        {
            "id": "generate",
            "command": "generate",
            "providerRef": "local-fast",
            "model": "gemma",
            "with": {
                "input": "source_docs/signals/",
                "kind": "signal",
                "output": "generated/fragments/",
            },
        }
    )

    assert_valid(validator, document)


def test_portfolio_localize_requires_languages_list(validator):
    document = recipe_with_step(
        {
            "id": "localize",
            "command": "portfolio.localize",
            "with": {"workspace": "portfolio/", "languages": ["fi", "sv"]},
        }
    )
    assert_valid(validator, document)

    document["recipe"]["steps"][0]["with"]["languages"] = "fi,sv"
    assert_invalid(validator, document)


def test_portfolio_build_accepts_output_and_workspace_together(validator):
    document = recipe_with_step(
        {
            "id": "build-portfolio",
            "command": "portfolio.build",
            "with": {
                "signals": ["source_docs/signals/"],
                "output": "portfolio/index.html",
                "workspace": "portfolio/",
            },
        }
    )

    assert_valid(validator, document)
