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
  steps: []
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
        input: generated/fragments/
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
| `metadata` | object | required | Stable recipe identity, name, description, owner, and tags. |
| `version` | string | required | Version of this recipe workflow. This is separate from the top-level ODPR specification version. |
| `type` | string | required | Recipe type such as `dev`, `ci`, `release`, `localization`, `hybrid`, or `agent`. |
| `steps` | array | required | Ordered workflow operations. |
| `inputs` | array | optional | Named workflow inputs. |
| `outputs` | array | optional | Named workflow outputs. |
| `context` | object | optional | Context format policy such as YAML, TOON, GCF, or automatic fallback. |
| `execution` | object | optional | Execution policy such as local, hosted, hybrid, or model-free. |
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

ODPR validation tools SHOULD reject embedded secrets or API keys in recipes.
Use `providerRef` in recipes and `credentialsRef` in Provider documents instead
of fields such as `apiKey`, `token`, `password`, or inline secret values.

## Recommended commands

ODPR keeps commands lightweight so recipes stay portable across implementations.
Implementations SHOULD support the recommended command names where the
underlying capability exists. Implementations MAY support additional commands.

| Command | Typical use |
|---|---|
| `generate` | Generate draft data product, catalog, graph, or vocabulary fragments. |
| `validate` | Validate generated or source artifacts against a schema or rule set. |
| `odpc.build` | Build catalog or portfolio objects. |
| `odpg.build` | Build graph context or graph artifacts. |
| `portfolio.build` | Build a portfolio package or site. |
| `portfolio.refresh` | Refresh portfolio source material or generated fragments. |
| `portfolio.render` | Render portfolio output. |
| `portfolio.localize` | Localize portfolio content into target languages. |
| `portfolio.explain` | Generate explanation or review material for a portfolio. |

`with` is the argument object for the selected command. ODPR standardizes where
command arguments live, but v1.0 does not define the complete argument schema
for every command.

## Outputs

Use `outputs` when a workflow creates durable artifacts that later steps, CI
jobs, reviewers, or agents should inspect. Outputs are named paths. They do not
replace the command-specific `with.output` argument; they make expected durable
results visible at the recipe level.

## Gates, review, and runtime policy

Required gates SHOULD be evaluated or reported by the executing tool. Tools
SHOULD NOT silently skip required gates.

`review.required` declares whether a recipe expects review after automated
steps complete. `review.mode` can be `human`, `agent`, `both`, or `none`.

`runPolicy` gives lightweight runtime guidance such as timeout and retry
expectations. It is useful for CI jobs, local model calls, portfolio
localization, and hosted provider calls.

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
