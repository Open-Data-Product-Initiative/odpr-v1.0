# ODPR RecipeCatalog

The `RecipeCatalog` object is the ODPR root object for recipe discovery. It
lists available recipes and points to their complete `Recipe` files.

A catalog is metadata-only. It MUST NOT contain full recipe step bodies,
credentials, provider readiness results, runtime status, planned writes, run
ids, or logs. Catalog entries should be treated as stale until the referenced
recipe file is loaded and validated.

## Root structure

```yaml
schema: https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml
version: "1.0"
kind: RecipeCatalog
recipeCatalog:
  metadata:
    id: RCP-CATALOG-001
    name:
      en: ODPR Example Recipe Catalog
  version: "1.0.0"
  groups:
    - id: examples
      name:
        en: Example Recipes
      description:
        en: Complete learning and demonstration recipes.
  recipes:
    - path: recipes/examples/release-portfolio-review.yaml
      id: RCP-RELEASE-001
      groupRef: examples
      version: "1.0.0"
      type: release
      name:
        en: Release Portfolio Review
      description:
        en: Refresh, localize, explain, and review a portfolio before release.
      tags:
        - portfolio
        - release
      environment: production
      executionMode: hosted
      providerRef: production-quality
      contextFormat: gcf
      requiresReview: true
      commands:
        - portfolio.refresh
        - portfolio.localize
        - portfolio.explain
```

| Element | Type | Required | Description |
|---|---|---|---|
| `schema` | string | required | URI of the ODPR schema used to validate the catalog file. |
| `version` | string | required | Version of the ODPR specification used by the catalog file. |
| `kind` | string | required | ODPR root object type. Catalog files MUST use `RecipeCatalog`. |
| `recipeCatalog` | object | required | Top-level object that defines recipe discovery metadata. |

## RecipeCatalog fields

| Element | Type | Required | Description |
|---|---|---|---|
| `metadata.id` | string | required | Stable catalog id. |
| `metadata.name` | language map | required | Human-readable catalog name. |
| `version` | string | required | Catalog artifact version. This is separate from the root ODPR specification `version`. |
| `groups` | array | optional | Metadata-only group definitions for organizing catalog entries. |
| `recipes` | array | required | Metadata entries pointing to complete recipe files. |

## Catalog group fields

| Element | Type | Required | Description |
|---|---|---|---|
| `id` | string | required | Stable group id, unique within the catalog. |
| `name` | language map | required | Human-readable group name. |
| `description` | language map | optional | Short group description. |

## Catalog entry fields

| Element | Type | Required | Description |
|---|---|---|---|
| `path` | string | required | Project-relative path to the complete `Recipe` file. |
| `id` | string | required | Recipe id copied from the referenced recipe metadata. |
| `groupRef` | string | optional | Reference to a declared catalog group id. Entries without `groupRef` are ungrouped. |
| `version` | string | required | Recipe version copied from the referenced recipe. |
| `type` | string | required | Recipe type such as `dev`, `ci`, `release`, `localization`, `hybrid`, or `agent`. |
| `name` | language map | required | Human-readable recipe name. |
| `description` | language map | optional | Short recipe description. |
| `tags` | array | optional | Discovery tags. |
| `environment` | string | optional | Intended environment label. |
| `executionMode` | string | optional | Expected runtime/provider class: `local`, `hosted`, `hybrid`, or `none`. |
| `providerRef` | string | optional | Default provider profile reference for LLM-backed steps. |
| `contextFormat` | string | optional | Preferred context format: `yaml`, `toon`, `gcf`, or `auto`. |
| `requiresReview` | boolean | optional | Whether the referenced recipe declares required review. |
| `commands` | array | optional | Command names used by the referenced recipe. |
