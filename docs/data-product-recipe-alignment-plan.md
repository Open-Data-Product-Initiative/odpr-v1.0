# Data Product Recipe alignment plan

This plan records the current ODPR draft decision: the data-product-specific
result object is named **Data Product Recipe**.

## Naming decision

Use `DataProductRecipe` as the ODPR root kind for the reviewable handoff
artifact used by developers and AI agents when planning and implementing one
data product.

Do not use a separate `ProductRecipe` kind. Do not use Data Product Recipe
Package as the concept name in specification materials.

## Contract shape

A valid Data Product Recipe document uses the ODPR envelope:

```yaml
schema: https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml
version: "1.0"
kind: DataProductRecipe
dataProductRecipe:
  metadata:
    id: DPR-001
    name:
      en: Customer Analytics Data Product Recipe
    description:
      en: Reviewable recipe for delivering the Customer Analytics data product.
  version: "1.0.0"
  status: draft
  sections:
    - id: recipe-readme
      path: README.md
      format: markdown
    - id: source-product-spec
      path: product-context/odps.yaml
      format: yaml
    - id: product-summary
      path: plans/product-summary.md
      format: markdown
    - id: delivery-plan
      path: plans/delivery-plan.md
      format: markdown
    - id: open-questions
      path: governance/open-questions.md
      format: markdown
    - id: ai-agent-brief
      path: agent/ai-agent-brief.md
      format: markdown
    - id: relationship-context
      path: context/odpg.yaml
      format: yaml
  readiness:
    score: 0
    status: missing
  review:
    required: true
    status: pending
```

## Mandatory core

The mandatory core section IDs are:

| ID | Format | Purpose |
|---|---|---|
| `recipe-readme` | markdown | Human and agent entrypoint with status, read order, questions, gates, and next action. |
| `source-product-spec` | yaml | Source ODPS product specification. |
| `product-summary` | markdown | Plain-language product summary and boundary. |
| `delivery-plan` | markdown | Developer-controlled implementation path. |
| `open-questions` | markdown | Missing decisions and blockers. |
| `ai-agent-brief` | markdown | Agent handoff contract derived from AGENTS.md practices: objective, input priority, allowed work, prohibited work, ambiguity handling, expected outputs, validation evidence, gates, boundaries, and repository instruction handling. |
| `relationship-context` | yaml | ODPG graph context for the product. |

## Surfaces to keep aligned

- `source/schema/odpr.yaml`
- `source/schema/odpr.json`
- `source/includes/_data_product_recipe.md`
- `source/recipes/examples/data-product-recipe.yaml`
- `source/recipes/recipes.jsonl`
- `source/llms.txt`
- `source/images/data-product-recipe.svg`
- `source/images/data-product-recipe-core.svg`
- Tests and agent artifact checks

## Practice alignment

The Data Product Recipe keeps execution terms out of the handoff object.
`Recipe` continues to own reusable workflow steps elsewhere in ODPR.
`DataProductRecipe` indexes reviewable files, readiness, and review state for
one data product delivery effort. Optional `recipeRef` may record provenance or
generation context, but it is not required for developers or AI agents to
implement the product.
