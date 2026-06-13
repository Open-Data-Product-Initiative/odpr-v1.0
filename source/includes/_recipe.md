# ODPR Recipe

The `Recipe` object is the root ODPR object. It declares one repeatable workflow
for data product delivery, validation, review, localization, publishing, or
automation.

Recipes are intended to be readable by humans and executable by tools. A recipe
should be specific enough for an SDK, CI/CD system, MCP server, or agent to
understand the workflow before it runs, while staying portable enough to avoid
binding the standard to one implementation.

## Root structure

| Element | Type | Required | Description |
|---|---|---|---|
| `schema` | string | required | URI of the ODPR schema used to validate the recipe file. |
| `version` | string | required | Version of the ODPR specification used by the recipe file. |
| `kind` | string | required | ODPR root object type. Recipe files MUST use `Recipe`. |
| `recipe` | object | required | Top-level object that defines the workflow recipe. |

## Recipe fields

| Element | Type | Required | Description |
|---|---|---|---|
| `metadata` | object | required | Stable recipe identity, name, description, owner, and tags. |
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
  type: release
  execution:
    mode: hosted
    providerRef: production-quality
  context:
    format: gcf
    fallback:
      - toon
      - yaml
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
  review:
    required: true
```
