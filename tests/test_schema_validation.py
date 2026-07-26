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


def provider_document(provider):
    return {
        "schema": SCHEMA_URI,
        "version": "1.0",
        "kind": "RuntimeProfile",
        "runtimeProfile": provider,
    }


def test_provider_accepts_sdk_generation_config_shape(validator):
    document = provider_document(
        {
            "provider": "openai",
            "model": "gpt-4.1-mini",
            "input": "open_data_products/generation/source_docs/",
            "output": "open_data_products/generation/fragments/",
            "prompts": "prompts/",
            "portfolio": {
                "sourceBudget": {
                    "maxSourceChars": 2000,
                    "maxPromptChars": 32000,
                },
                "privacy": {
                    "obfuscatePersonalData": True,
                },
            },
            "providers": {
                "openai": {
                    "type": "openai",
                    "model": "gpt-4.1-mini",
                    "baseUrl": "https://api.openai.com/v1",
                    "apiKeyEnv": "OPENAI_API_KEY",
                    "maxTokens": 8192,
                },
                "llamacpp-embedded": {
                    "type": "llama-cpp",
                    "model": "local-gguf",
                    "modelPath": "models/qwen2.5-7b-instruct-q4_k_m.gguf",
                    "contextWindow": 8192,
                    "gpuLayers": -1,
                },
            },
        }
    )

    assert_valid(validator, document)


def test_provider_rejects_unknown_profile_fields(validator):
    document = provider_document(
        {
            "provider": "openai",
            "providers": {
                "openai": {
                    "type": "openai",
                    "model": "gpt-4.1-mini",
                    "secretValue": "not-allowed",
                }
            },
        }
    )

    assert_invalid(validator, document)


@pytest.mark.parametrize("scope", ["data-product", "catalog", "graph", "portfolio"])
def test_recipe_scope_accepts_standard_scope_values(validator, scope):
    document = recipe_with_step({"id": "explain", "command": "explain", "document": "README.md"})
    document["recipe"]["type"] = "agent"
    document["recipe"]["scope"] = scope

    assert_valid(validator, document)


def test_recipe_scope_rejects_unknown_values(validator):
    document = recipe_with_step({"id": "explain", "command": "explain", "document": "README.md"})
    document["recipe"]["scope"] = "dashboard"

    assert_invalid(validator, document)


def test_graph_trigger_accepts_node_attribute_change_for_any_node_type(validator):
    document = recipe_with_step(
        {
            "id": "explain-impact",
            "kind": "graph",
            "input": "generated/graph-context.gcf",
            "output": "generated/graph-impact.md",
        }
    )
    document["recipe"]["type"] = "agent"
    document["recipe"]["scope"] = "graph"
    document["recipe"]["trigger"] = {
        "source": "odpg",
        "event": "node.attributeChanged",
        "subject": {
            "nodeType": "*",
            "attribute": {
                "name": "status",
                "to": "production",
            },
        },
    }
    document["recipe"]["graphContext"] = {
        "depth": 2,
    }
    document["recipe"]["intent"] = "Explain why the changed graph node matters."
    document["recipe"]["instructions"] = "Use retrieved graph context only."
    document["recipe"]["groundingTo"] = {
        "nodeTypes": ["DataProduct", "UseCase", "BusinessObjective", "Owner"],
        "edgeTypes": ["uses", "supports", "enables", "dependsOn"],
    }
    document["recipe"]["contextFormat"] = {"primary": "gcf", "fallback": ["yaml", "toon"]}
    document["recipe"]["steps"][0]["discoveryType"] = "produce-findings-and-recommendations"
    document["recipe"]["steps"][0]["intent"] = "Explain visible graph impact."
    document["recipe"]["steps"][0]["instructions"] = "Separate visible facts from missing context."
    document["recipe"]["steps"][0]["iterationLimit"] = 3
    document["recipe"]["steps"][0]["exitWhen"] = (
        "Stop when the generated result is ready for review or no new grounding is found."
    )

    assert_valid(validator, document)


@pytest.mark.parametrize(
    "node_type",
    ["DataProduct", "BusinessObjective", "UseCase", "Signal", "Policy", "DataContract", "DataService", "API", "Owner", "System", "Agent", "Condition", "*"],
)
def test_recipe_grounding_to_accepts_controlled_node_types(validator, node_type):
    document = recipe_with_step({"id": "explain", "command": "explain", "document": "README.md"})
    document["recipe"]["groundingTo"] = {"nodeTypes": [node_type]}

    assert_valid(validator, document)


@pytest.mark.parametrize("edge_type", ["uses", "supports", "enables", "dependsOn"])
def test_recipe_grounding_to_accepts_controlled_edge_types(validator, edge_type):
    document = recipe_with_step({"id": "explain", "command": "explain", "document": "README.md"})
    document["recipe"]["groundingTo"] = {"edgeTypes": [edge_type]}

    assert_valid(validator, document)


def test_recipe_grounding_to_rejects_unknown_node_types(validator):
    document = recipe_with_step({"id": "explain", "command": "explain", "document": "README.md"})
    document["recipe"]["groundingTo"] = {"nodeTypes": ["CustomerSegment"]}

    assert_invalid(validator, document)


def test_recipe_grounding_to_rejects_unknown_edge_types(validator):
    document = recipe_with_step({"id": "explain", "command": "explain", "document": "README.md"})
    document["recipe"]["groundingTo"] = {"edgeTypes": ["influences"]}

    assert_invalid(validator, document)


@pytest.mark.parametrize(
    "discovery_type",
    [
        "find-affected-use-cases",
        "explain-use-case-impact",
        "find-affected-data-products",
        "explain-data-product-impact",
        "find-affected-objectives",
        "explain-objective-impact",
        "identify-gaps-and-risks",
        "produce-findings-and-recommendations",
    ],
)
def test_step_discovery_type_accepts_controlled_values(validator, discovery_type):
    document = recipe_with_step(
        {
            "id": "discover",
            "document": "generated/context.gcf",
            "discoveryType": discovery_type,
        }
    )

    assert_valid(validator, document)


def test_step_discovery_type_rejects_unknown_values(validator):
    document = recipe_with_step(
        {
            "id": "discover",
            "command": "explain",
            "document": "generated/context.gcf",
            "discoveryType": "find-random-things",
        }
    )

    assert_invalid(validator, document)


def test_step_discovery_type_rejects_command(validator):
    document = recipe_with_step(
        {
            "id": "discover",
            "command": "explain",
            "document": "generated/context.gcf",
            "discoveryType": "produce-findings-and-recommendations",
        }
    )

    assert_invalid(validator, document)


def test_step_requires_command_or_discovery_type(validator):
    document = recipe_with_step({"id": "empty-step"})

    assert_invalid(validator, document)


def test_graph_context_accepts_human_start_node_id(validator):
    document = recipe_with_step(
        {
            "id": "discover",
            "discoveryType": "find-affected-use-cases",
        }
    )
    document["recipe"]["graphContext"] = {
        "startNodeId": "nd_7f3a9c2e4b8d",
        "depth": 2,
    }

    assert_valid(validator, document)


def test_graph_context_rejects_obsolete_start_field(validator):
    document = recipe_with_step(
        {
            "id": "discover",
            "discoveryType": "find-affected-use-cases",
        }
    )
    document["recipe"]["graphContext"] = {
        "start": "condition:high-value-customer-inactivity",
        "depth": 2,
    }

    assert_invalid(validator, document)


def test_recipe_rejects_legacy_context_format_field(validator):
    document = recipe_with_step({"id": "explain", "command": "explain", "document": "README.md"})
    document["recipe"]["context"] = {"format": "gcf", "fallback": ["yaml"]}

    assert_invalid(validator, document)


def test_context_format_requires_primary_format(validator):
    document = recipe_with_step({"id": "explain", "command": "explain", "document": "README.md"})
    document["recipe"]["contextFormat"] = {"fallback": ["yaml"]}

    assert_invalid(validator, document)


def test_step_iteration_limit_must_be_positive(validator):
    document = recipe_with_step(
        {
            "id": "explain",
            "command": "explain",
            "document": "README.md",
            "iterationLimit": 0,
            "exitWhen": "Stop when the generated result is ready for review.",
        }
    )

    assert_invalid(validator, document)


def test_graph_trigger_rejects_wildcard_attribute_names(validator):
    document = recipe_with_step({"id": "explain", "command": "explain", "document": "README.md"})
    document["recipe"]["trigger"] = {
        "source": "odpg",
        "event": "node.attributeChanged",
        "subject": {
            "nodeType": "DataProduct",
            "attribute": {
                "name": "*",
                "to": "production",
            },
        },
    }

    assert_invalid(validator, document)


def test_graph_trigger_accepts_edge_removal_with_endpoint_patterns(validator):
    document = recipe_with_step({"id": "explain", "command": "explain", "document": "README.md"})
    document["recipe"]["trigger"] = {
        "source": "odpg",
        "event": "edge.removed",
        "subject": {
            "edgeType": "dependsOn",
            "fromNodeType": "*",
            "toNodeType": "DataProduct",
        },
    }

    assert_valid(validator, document)


def test_graph_trigger_rejects_unknown_edge_type(validator):
    document = recipe_with_step({"id": "explain", "command": "explain", "document": "README.md"})
    document["recipe"]["trigger"] = {
        "source": "odpg",
        "event": "edge.added",
        "subject": {
            "edgeType": "influences",
        },
    }

    assert_invalid(validator, document)


def test_graph_condition_trigger_requires_condition_name(validator):
    document = recipe_with_step({"id": "explain", "command": "explain", "document": "README.md"})
    document["recipe"]["trigger"] = {
        "source": "odpg",
        "event": "graph.conditionMatched",
        "condition": {
            "name": "business-objective-enabled",
        },
    }

    assert_valid(validator, document)

    del document["recipe"]["trigger"]["condition"]["name"]
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


def test_data_product_recipe_accepts_optional_recipe_ref(validator):
    document = minimal_data_product_recipe()
    document["dataProductRecipe"]["recipeRef"] = "provenance/data-product-delivery-recipe.yaml"

    assert_valid(validator, document)


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


def test_data_product_recipe_contract_plan_requires_yaml_format(validator):
    document = minimal_data_product_recipe()
    document["dataProductRecipe"]["sections"].append(
        {"id": "contract-plan", "path": "plans/contract-plan.yaml", "format": "yaml"}
    )
    assert_valid(validator, document)

    document["dataProductRecipe"]["sections"][-1]["format"] = "markdown"
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
            "runtimeRef": "runtime-profiles/examples/production-quality.yaml#production-quality",
            "model": "gpt-4.1",
            "document": "generated/fragments/signal.yaml",
        }
    )

    assert_invalid(validator, document)


def test_llm_backed_generate_accepts_provider_ref_and_required_parameters(validator):
    document = recipe_with_step(
        {
            "id": "generate",
            "command": "generate",
            "runtimeRef": "runtime-profiles/examples/local-fast.yaml#local-fast",
            "model": "gemma",
            "input": "source_docs/signals/",
            "kind": "signal",
            "output": "generated/fragments/",
        }
    )

    assert_valid(validator, document)


def test_provider_ref_rejects_bare_profile_name(validator):
    document = recipe_with_step(
        {
            "id": "generate",
            "command": "generate",
            "runtimeRef": "local-fast",
            "input": "source_docs/signals/",
            "kind": "signal",
            "output": "generated/fragments/",
        }
    )

    assert_invalid(validator, document)


def test_portfolio_localize_requires_languages_list(validator):
    document = recipe_with_step(
        {
            "id": "localize",
            "command": "portfolio.localize",
            "languages": ["fi", "sv"],
        }
    )
    assert_valid(validator, document)

    document["recipe"]["steps"][0]["languages"] = "fi,sv"
    assert_invalid(validator, document)


def test_portfolio_build_accepts_declared_output_without_workspace_argument(validator):
    document = recipe_with_step(
        {
            "id": "build-portfolio",
            "command": "portfolio.build",
            "signals": ["source_docs/signals/"],
            "output": "portfolio/index.html",
        }
    )

    assert_valid(validator, document)


def test_portfolio_commands_reject_workspace_argument(validator):
    document = recipe_with_step(
        {
            "id": "refresh",
            "command": "portfolio.refresh",
            "workspace": "portfolio/",
        }
    )

    assert_invalid(validator, document)
