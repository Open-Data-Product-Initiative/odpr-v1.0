# Recipe Toolkit

> Snippet of YAML version:

```yaml
schema: https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml
version: "1.0"
kind: Recipe
recipe:
  metadata:
    id: RCP-DEV-001
    name:
      en: Local Fragment Draft
    description:
      en: Generate draft ODPC fragments locally for fast iteration.
  type: dev
  execution:
    mode: local
    providerRef: local-fast
  steps:
    - id: generate-signals
      command: generate
      with:
        kind: signal
        input: source_docs/signals/
        output: generated/fragments/
```

ODPR is published in several forms for different users and tools. This
specification provides the human-readable documentation, while the schema,
recipe records, provider records, and example files provide machine-readable
resources for validation, workflow automation, AI retrieval, and agent use.

Use `odpr.yaml` or `odpr.json` to validate Recipe and Provider files,
`recipes.jsonl` for lightweight object selection and retrieval, and the
examples when generating or repairing ODPR YAML.

The [ODP Agent SDK](https://opendataproducts.org/sdk/) supports ODPR and is the
first reference implementation for validating and executing ODPR recipes. Use
it when building agents or automation across ODPS, ODPC, ODPG, and ODPV
workflows. ODPR recipes remain portable workflow contracts and can also be used
with other conforming SDKs, CI/CD systems, MCP servers, or platform
implementations.

<!-- AI_AGENT_GUIDANCE:
Use /schema/odpr.yaml or /schema/odpr.json to validate ODPR Recipe and Provider files.
Use /recipes/recipes.jsonl for retrieval, classification, ODPR object selection, and lightweight tool calls.
Use /recipes/examples/*.yaml when generating or repairing ODPR recipe content.
Use /providers/examples/*.yaml when generating or repairing ODPR Provider content.
Use the ODP Agent SDK as the first reference implementation for validating and executing ODPR recipes; do not treat it as the only possible ODPR implementation.
Keep recipes declarative. Do not turn ODPR into a shell scripting language or orchestration engine.
Keep Provider objects free of raw secrets and provider-specific API schemas.
-->

| Resource | Format | Purpose |
|---|---|---|
| [ODP Agent SDK](https://opendataproducts.org/sdk/) | SDK | First reference implementation for validating and executing ODPR recipes; ODPR can also be used with other conforming implementations |
| [`llms.txt`](/llms.txt) | Text | AI agent guidance for discovering and using ODPR resources |
| [`odpr.yaml`](/schema/odpr.yaml) | YAML Schema | YAML representation of the ODPR validation schema |
| [`odpr.json`](/schema/odpr.json) | JSON Schema | JSON representation of the ODPR validation schema |
| [`recipes.jsonl`](/recipes/recipes.jsonl) | JSONL | Agent-friendly one-recipe-per-line file for retrieval and lightweight tools |
| [`minimal.yaml`](/recipes/examples/minimal.yaml) | YAML | Minimal valid ODPR recipe example |
| [`ci-validate-generated-fragments.yaml`](/recipes/examples/ci-validate-generated-fragments.yaml) | YAML | CI recipe that generates and validates fragments |
| [`release-portfolio-review.yaml`](/recipes/examples/release-portfolio-review.yaml) | YAML | Release recipe for portfolio refresh, localization, and explanation |
| [`hybrid-graph-review.yaml`](/recipes/examples/hybrid-graph-review.yaml) | YAML | Hybrid recipe that mixes local and hosted execution |
| [`production-quality.yaml`](/providers/examples/production-quality.yaml) | YAML | Hosted Provider profile for production-quality generation |
| [`local-fast.yaml`](/providers/examples/local-fast.yaml) | YAML | Local Provider profile for fast development runs |
| [`local-graph.yaml`](/providers/examples/local-graph.yaml) | YAML | Local Provider profile for graph-building workflows |
| [`internal-secure.yaml`](/providers/examples/internal-secure.yaml) | YAML | Internal gateway Provider profile for controlled production use |

Agent-oriented helper scripts are available in the source repository for
maintaining and using recipe artifacts.

<!-- AI_AGENT_SCRIPT_GUIDANCE:
When working from the source repository, use scripts/search_recipes.py for repeatable local ODPR recipe lookup.
Use scripts/search_recipes.py --json when another tool or agent will consume the result.
Use scripts/validate_recipe.py to validate ODPR YAML or JSON Recipe or Provider files against source/schema/odpr.yaml and reject embedded secrets or API keys.
Use scripts/check_agent_artifacts.py in CI or review workflows to detect drift between schema, recipe artifacts, examples, and llms.txt.
Use scripts/generate_recipe_artifacts.py after editing source/schema/odpr.yaml to regenerate source/schema/odpr.json; use --check in CI or review workflows.
Install script dependencies with python -m pip install -r scripts/requirements-agent.txt.
Do not edit generated or derived artifacts without checking alignment across llms.txt, schema files, recipe artifacts, examples, and tests.
-->

| Script | Purpose |
|---|---|
| [`check_agent_artifacts.py`](https://github.com/Open-Data-Product-Initiative/odpr-v1.0/blob/main/scripts/check_agent_artifacts.py) | Checks schema alignment, example files, recipe JSONL records, and `llms.txt` references |
| [`generate_recipe_artifacts.py`](https://github.com/Open-Data-Product-Initiative/odpr-v1.0/blob/main/scripts/generate_recipe_artifacts.py) | Regenerates derived recipe artifacts such as `source/schema/odpr.json` from canonical source files; use `--check` to detect drift |
| [`search_recipes.py`](https://github.com/Open-Data-Product-Initiative/odpr-v1.0/blob/main/scripts/search_recipes.py) | Searches ODPR recipe records by keyword or exact recipe id; use `--json` for machine-readable results |
| [`validate_recipe.py`](https://github.com/Open-Data-Product-Initiative/odpr-v1.0/blob/main/scripts/validate_recipe.py) | Validates ODPR YAML or JSON Recipe or Provider files against the ODPR schema and rejects embedded secrets or API keys |

The Markdown tables in this specification are intended for human readers. The
schema, JSONL, and YAML example files are intended for programmable use,
automation, validation, AI retrieval, and recipe tooling.
