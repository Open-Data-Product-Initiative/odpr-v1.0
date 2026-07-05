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


@pytest.mark.parametrize("scope", ["data-product", "catalog", "graph", "portfolio"])
def test_recipe_scope_accepts_standard_scope_values(validator, scope):
    document = recipe_with_step({"id": "explain", "command": "explain", "with": {"document": "README.md"}})
    document["recipe"]["type"] = "agent"
    document["recipe"]["scope"] = scope

    assert_valid(validator, document)


def test_recipe_scope_rejects_unknown_values(validator):
    document = recipe_with_step({"id": "explain", "command": "explain", "with": {"document": "README.md"}})
    document["recipe"]["scope"] = "dashboard"

    assert_invalid(validator, document)


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
            "recipes": [
                {
                    "path": "recipes/release-portfolio-review.yaml",
                    "id": "RCP-RELEASE-001",
                    "version": "1.0.0",
                    "type": "release",
                    "scope": "portfolio",
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


def minimal_data_product_recipe():
    return {
        "schema": SCHEMA_URI,
        "version": "1.0",
        "kind": "DataProductRecipe",
        "dataProductRecipe": {
            "metadata": {
                "id": "DPR-001",
                "name": {"en": "Customer Analytics Data Product Recipe"},
                "description": {"en": "Reviewable recipe for delivering the Customer Analytics data product."},
            },
            "version": "1.0.0",
            "recipeRef": "recipe.yaml",
            "status": "draft",
            "sections": [
                {"id": "recipe-readme", "path": "README.md", "format": "markdown"},
                {"id": "source-product-spec", "path": "product-context/odps.yaml", "format": "yaml"},
                {"id": "product-summary", "path": "plans/product-summary.md", "format": "markdown"},
                {"id": "delivery-plan", "path": "plans/delivery-plan.md", "format": "markdown"},
                {"id": "open-questions", "path": "governance/open-questions.md", "format": "markdown"},
                {"id": "ai-agent-brief", "path": "agent/ai-agent-brief.md", "format": "markdown"},
                {"id": "relationship-context", "path": "context/odpg.yaml", "format": "yaml"},
            ],
            "readiness": {"score": 0, "status": "missing"},
            "review": {"required": True, "status": "pending"},
        },
    }


def test_data_product_recipe_minimal_manifest_validates(validator):
    assert_valid(validator, minimal_data_product_recipe())


@pytest.mark.parametrize("version", ["1.0.0", "1.2.3", "2.0.0-beta.1"])
def test_data_product_recipe_accepts_artifact_version(validator, version):
    document = minimal_data_product_recipe()
    document["dataProductRecipe"]["version"] = version

    assert_valid(validator, document)


def test_data_product_recipe_requires_artifact_version(validator):
    document = minimal_data_product_recipe()
    del document["dataProductRecipe"]["version"]

    assert_invalid(validator, document)


def test_data_product_recipe_requires_metadata_description(validator):
    document = minimal_data_product_recipe()
    del document["dataProductRecipe"]["metadata"]["description"]

    assert_invalid(validator, document)


def test_data_product_recipe_rejects_invalid_artifact_version(validator):
    document = minimal_data_product_recipe()
    document["dataProductRecipe"]["version"] = "v1"

    assert_invalid(validator, document)


@pytest.mark.parametrize(
    "status",
    ["announcement", "draft", "development", "testing", "acceptance", "production", "sunset", "retired"],
)
def test_data_product_recipe_accepts_odps_status_values(validator, status):
    document = minimal_data_product_recipe()
    document["dataProductRecipe"]["status"] = status

    assert_valid(validator, document)


def test_data_product_recipe_rejects_non_odps_status_values(validator):
    document = minimal_data_product_recipe()
    document["dataProductRecipe"]["status"] = "ready-for-review"

    assert_invalid(validator, document)


@pytest.mark.parametrize(
    "section_id",
    [
        "recipe-readme",
        "source-product-spec",
        "product-summary",
        "delivery-plan",
        "open-questions",
        "ai-agent-brief",
        "relationship-context",
    ],
)
def test_data_product_recipe_requires_core_sections(validator, section_id):
    document = minimal_data_product_recipe()
    document["dataProductRecipe"]["sections"] = [
        section for section in document["dataProductRecipe"]["sections"] if section["id"] != section_id
    ]

    assert_invalid(validator, document)


def test_data_product_recipe_rejects_unknown_section_id(validator):
    document = minimal_data_product_recipe()
    document["dataProductRecipe"]["sections"].append(
        {"id": "dashboard-plan", "path": "plans/dashboard-plan.md", "format": "markdown"}
    )

    assert_invalid(validator, document)


@pytest.mark.parametrize("score", [-1, 101])
def test_data_product_recipe_readiness_score_is_zero_to_one_hundred(validator, score):
    document = minimal_data_product_recipe()
    document["dataProductRecipe"]["readiness"]["score"] = score

    assert_invalid(validator, document)


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
