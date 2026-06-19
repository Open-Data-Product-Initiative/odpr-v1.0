# ODPR Recipe

The `Recipe` object is the root ODPR object. It declares one repeatable workflow
for data product delivery, validation, review, localization, publishing, or
automation.

Recipes are intended to be readable by humans and executable by tools. A recipe
should be specific enough for an SDK, CI/CD system, MCP server, or agent to
understand the workflow before it runs, while staying portable enough to avoid
binding the standard to one implementation.

## Root structure

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
      en: Generate draft fragments locally.
  version: "1.0.0"
  type: dev
  steps:
    - id: generate-signals
      command: generate
      with:
        kind: signal
        input: source_docs/signals/
        output: generated/fragments/
```

| Element | Type | Required | Description |
|---|---|---|---|
| `schema` | string | required | URI of the ODPR schema used to validate the recipe file. |
| `version` | string | required | Version of the ODPR specification used by the recipe file. |
| `kind` | string | required | ODPR root object type. Recipe files MUST use `Recipe`. |
| `recipe` | object | required | Top-level object that defines the workflow recipe. |

## Recipe fields

```yaml
recipe:
  metadata:
    id: RCP-CI-001
    name:
      en: CI Validate Generated Fragments
    description:
      en: Generate and validate fragments.
  version: "1.0.0"
  type: ci
  environment: ci
  execution:
    mode: local
    providerRef: local-fast
  context:
    format: gcf
    fallback:
      - toon
      - yaml
  steps:
    - id: validate-fragments
      command: validate
      with:
        document: generated/fragments/signal.yaml
  outputs:
    - id: generated-fragments
      path: generated/fragments/
  gates:
    - id: fragments-valid
      type: validation
      required: true
  review:
    required: false
  runPolicy:
    timeoutSeconds: 300
```

| Element | Type | Required | Description |
|---|---|---|---|
| `metadata` | object | required | Stable recipe identity, name, optional description, owner, and tags. |
| `version` | string | required | Version of this recipe workflow. This is separate from the top-level ODPR specification version. |
| `type` | string | required | Recipe type such as `dev`, `ci`, `release`, `localization`, `hybrid`, or `agent`. |
| `steps` | array | required | Ordered workflow operations. |
| `inputs` | array | optional | Named workflow inputs. |
| `outputs` | array | optional | Named workflow outputs. |
| `context` | object | optional | Context format policy such as YAML, TOON, GCF, or automatic fallback. |
| `execution` | object | optional | Workflow intent such as local, hosted, hybrid, or model-free runtime/provider class. |
| `gates` | array | optional | Validation, quality, or review gates. |
| `review` | object | optional | Human or agent review expectations. |
| `environment` | string | optional | Environment label such as development, CI, staging, or production. |
| `runPolicy` | object | optional | Runtime limits such as timeout or retry guidance. |

## Recipe types

| Type | Purpose |
|---|---|
| `dev` | Local development, drafting, and fast iteration. |
| `ci` | Automated validation and build checks. |
| `release` | Production-grade review, refresh, localization, rendering, and publishing. |
| `localization` | Translation and multilingual portfolio or product work. |
| `hybrid` | Workflows that mix local and hosted execution. |
| `agent` | Agent-safe workflows that AI agents can inspect and run. |

## Execution modes

A `Recipe` is the portable workflow contract. The same recipe document can be
validated, dry-run, executed, or resumed by an SDK or platform. ODPR does not
store invocation mode in the recipe body. Invocation mode belongs to the
executing tool, for example an SDK command using `--dry-run` or `--execute`.
`recipe.execution.mode` describes runtime/provider class such as local, hosted,
hybrid, or none.

| Mode | Meaning |
|---|---|
| `local` | Runs with local model or local tooling. |
| `hosted` | Runs with hosted model or hosted service. |
| `hybrid` | Uses local and hosted execution in the same recipe. |
| `none` | Does not require model execution. |

## Context formats

| Format | Meaning |
|---|---|
| `yaml` | Use canonical YAML context. |
| `toon` | Use TOON compact context when available. |
| `gcf` | Use GCF compact graph/catalog context when available. |
| `auto` | Let the executing tool choose the preferred available context. |

## Provider references

`providerRef` identifies a standardized ODPR `Provider` profile by
`provider.id`. The recipe does not embed provider internals; it only names the
profile that should be used.

A recipe can declare a default provider in `execution.providerRef`. Individual
steps can override it with `step.providerRef` when one workflow mixes local and
hosted execution.

The referenced `Provider` object defines the provider family, model, provider
class, endpoint reference, credentials reference, and safe runtime defaults.
Raw secrets MUST NOT be stored in recipes or provider documents.

`execution.providerRef` is the default provider profile for LLM-backed steps.
Step-level `providerRef` overrides `execution.providerRef`. Step-level `model`
overrides the provider model for that step. Deterministic and report commands
MUST NOT use `providerRef` or `model`.

ODPR validation tools SHOULD reject embedded secrets or API keys in recipes.
Use `providerRef` in recipes and `credentialsRef` in Provider documents instead
of fields such as `apiKey`, `token`, `password`, or inline secret values.

## Recommended commands

ODPR keeps commands lightweight so recipes stay portable across implementations.
Implementations SHOULD support the recommended command names where the
underlying capability exists. Implementations MAY support additional commands.

| Command | Classification | Required `with` | Optional `with` |
|---|---|---|---|
| `generate` | `llm-backed` | `input`, `kind`, `output` | `config`, `prompts`, `profile`, `includeComponents`, `maxSourceChars`, `ollamaUrl` |
| `odpc.build` | `deterministic` | `input`, `output` | `html`, `toon`, `gcf`, `id`, `name`, `description`, `recursive`, `validate` |
| `odpg.build` | `llm-backed` | `input`, `output` | `toon`, `gcf`, `contextGraph`, `id`, `name`, `description`, `recursive`, `validate`, `config`, `prompts`, `ollamaUrl` |
| `odpg.render` | `deterministic` | `graph`, `output` | none |
| `portfolio.build` | `llm-backed` | at least one of `objectives`, `useCases`, `signals`, or `products`; and `output`, `workspace`, or both | `title`, `config`, `prompts`, `ollamaUrl`, `strictValidation` |
| `portfolio.refresh` | `llm-backed` | `workspace` | `objectives`, `useCases`, `signals`, `products`, `title`, `config`, `allSources`, `prompts`, `ollamaUrl`, `strictValidation` |
| `portfolio.sync` | `deterministic` | `workspace` | `strictValidation` |
| `portfolio.localize` | `llm-backed` | `workspace`, `languages` | `defaultLanguage`, `config`, `prompts`, `ollamaUrl`, `strictValidation` |
| `portfolio.render` | `deterministic` | `workspace` | `output`, `strictValidation` |
| `portfolio.explain` | `report` | `workspace` | none |
| `validate` | `deterministic` | `document` | none |
| `explain` | `report` | `document` | none |

`with` is the argument object for the selected command. `providerRef` and
`model` stay beside `command`; they do not belong inside `with`.
`portfolio.localize.with.languages` SHOULD be written as a YAML list of BCP 47
language tags.

| Classification | Meaning |
|---|---|
| `deterministic` | No provider needed; repeatable from files and options. |
| `llm-backed` | Calls a configured provider and model. |
| `review` | Requires human or external approval. |
| `report` | Reads artifacts and produces summaries, diagnostics, or review material. |

## Outputs

Use `inputs` and `outputs` when a workflow uses or creates durable artifacts
that later steps, CI
jobs, reviewers, or agents should inspect. Outputs are named paths. They do not
replace the command-specific `with.output` argument; they make expected durable
results visible at the recipe level.

Recipe-level paths should be project-relative. Recipes should not use absolute
paths or `..` traversal. ODPR states this safety expectation; SDKs and
platforms enforce write-scope policy.

## Gates, review, and runtime policy

Required gates SHOULD be evaluated or reported by the executing tool. Tools
SHOULD NOT silently skip required gates.

`review.required` declares whether a recipe expects review after automated
steps complete. `review.mode` can be `human`, `agent`, `both`, or `none`.

`runPolicy` gives lightweight runtime guidance such as timeout, stop-on-failure
behavior, and retry expectations. It is useful for CI jobs, local model calls,
portfolio localization, and hosted provider calls. ODPR v1 does not define
approval records, workflow pauses, run manifests, or gate status storage.

## Environment labels

Use `environment` to label the intended operating context, such as
`development`, `ci`, `staging`, or `production`. The value is a string so teams
can use local naming conventions while keeping common labels readable.

## Example

```yaml
schema: https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml
version: "1.0"
kind: Recipe
recipe:
  metadata:
    id: RCP-RELEASE-001
    name:
      en: Release Portfolio Review
    description:
      en: Refresh, localize, and explain a portfolio for release review.
  version: "1.0.0"
  type: release
  execution:
    mode: hosted
    providerRef: production-quality
  environment: production
  context:
    format: gcf
    fallback:
      - toon
      - yaml
  runPolicy:
    timeoutSeconds: 900
  steps:
    - id: refresh-portfolio
      command: portfolio.refresh
      with:
        workspace: portfolio/
    - id: localize-portfolio
      command: portfolio.localize
      with:
        workspace: portfolio/
        languages:
          - fi
          - sv
    - id: explain-portfolio
      command: portfolio.explain
      with:
        workspace: portfolio/
  outputs:
    - id: localized-portfolio-fi
      path: portfolio/index.fi.html
    - id: localized-portfolio-sv
      path: portfolio/index.sv.html
    - id: release-explanation
      path: portfolio/explanation.md
  gates:
    - id: human-review
      type: review
      required: true
  review:
    required: true
    mode: human
    instructions: Review localized pages and generated reports before publishing.
```

This release recipe describes a portfolio review workflow. When an executor
runs it, the expected flow is:

1. Validate the recipe against the ODPR schema and confirm it is a `Recipe`.
2. Treat the workflow as a `release` recipe, which means it is intended for a
   publication or release-review process rather than local drafting.
3. Use hosted execution through the configured provider reference
   `production-quality`. The matching ODPR `Provider` object describes the
   runtime profile, while raw credentials and live endpoint resolution stay in
   the executing SDK or platform.
4. Prepare compact context in GCF format, with TOON and YAML as fallback
   formats.
5. Run `portfolio.refresh` for the `portfolio/` workspace.
6. Run `portfolio.localize` for the same workspace and produce Finnish and
   Swedish localized outputs.
7. Run `portfolio.explain` so reviewers get generated explanation material for
   the refreshed portfolio.
8. Require human review before the release workflow is considered complete.
