# Delivery Flows

> Root shape example:

```yaml
schema: https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml
version: "1.0"
kind: Recipe
recipe:
  metadata:
    id: RCP-DELIVERY-001
    name:
      en: Portfolio Delivery Flow
  version: "1.0.0"
  type: release
  scope: portfolio
  execution:
    mode: hosted
    providerRef: production-quality
  steps: []
  outputs: []
  gates: []
  review:
    required: true
```

Delivery flows declare repeatable work around data product artifacts. They
cover work such as portfolio building, validation, localization, publishing,
release review, and other delivery operations that teams want to make portable
across tools and environments.

Delivery flows coordinate a sequence of delivery operations. A delivery flow
can generate or refresh artifacts, validate them, render outputs, localize
content, explain results, and require review before release.

### Delivery flow boundaries

A delivery flow SHOULD answer five practical questions before any tool runs:

- What delivery work is being performed?
- Which artifact area is affected?
- Which ordered operations run?
- Which durable outputs should exist afterwards?
- Which gates or review expectations apply?

A delivery flow MUST NOT redefine ODPS product metadata, ODPC catalog structure,
ODPG graph semantics, ODPV vocabulary terms, SDK internals, provider internals,
or CI/CD engine behavior. It may reference those standards as inputs, context,
or outputs of the delivery work.

### Delivery flow fields

| Element name | Type | Options | Description |
|---|---|---|---|
| `schema` | string | ODPR schema URI | URI of the ODPR schema used to validate the document. |
| `version` | string | ODPR specification version | Version of the ODPR specification used by the document. |
| `kind` | string | `Recipe` | ODPR root object type. Delivery flows are encoded as `Recipe` documents. |
| `recipe` | object | - | Top-level object that declares the delivery flow contract. |
| `recipe.metadata` | object | - | Stable delivery flow identity and name. |
| `recipe.metadata.id` | string | - | Stable delivery flow identifier. |
| `recipe.metadata.name` | object | localized text object | Human-readable delivery flow name. |
| `recipe.version` | string | semantic version | Version of this delivery flow artifact. This is separate from the top-level ODPR specification version. |
| `recipe.type` | string | `development`, `ci`, `release`, `agent`, `custom` | Delivery flow intent. Use `development` for draft generation or working artifacts, `ci` for automated validation, `release` for portfolio preparation or publication review, `agent` for agent-assisted delivery work, and `custom` only when the standard intents do not fit. |
| `recipe.scope` | string | `data-product`, `portfolio`, `graph`, `catalog`, `fragment`, `custom` | Artifact area affected by the delivery flow. |
| `recipe.execution.mode` | string | `local`, `hosted`, `hybrid`, `none` | Runtime expectation for the delivery flow. |
| `recipe.execution.providerRef` | string | provider reference | Named provider profile used by model-backed steps. |
| `recipe.steps` | array | ordered step objects | Ordered delivery operations that run. |
| `recipe.outputs` | array | output objects | Durable files, folders, reports, rendered pages, or review notes expected after the run. |
| `recipe.gates` | array | gate objects | Validation, quality, publication, or release conditions. |
| `recipe.review.required` | boolean | `true`, `false` | Whether human review is required before accepting the delivery flow result. |

## Delivery flow model

```yaml
recipe:
  type: release
  scope: portfolio
  execution:
    mode: hosted
    providerRef: production-quality
  steps:
    - id: refresh-portfolio
      command: portfolio.refresh
      with:
        workspace: portfolio/
    - id: explain-portfolio
      command: portfolio.explain
      with:
        workspace: portfolio/
  outputs:
    - id: release-explanation
      path: portfolio/explanation.md
  gates:
    - id: human-review
      type: review
      required: true
  review:
    required: true
```

A delivery flow is the portable operating contract for a repeatable delivery
activity. It is not the artifact being produced and it is not the runtime that
executes the work. It declares the work in a form that a developer, CI runner,
SDK executor, MCP server, or AI agent can inspect before the run starts.

![Delivery flow contract model.](images/delivery-flow-model.svg)

Every delivery flow SHOULD make these parts visible:

| Part | Purpose |
|---|---|
| Work intent | The delivery activity being performed, such as draft generation, validation, portfolio refresh, localization, release review, or publishing preparation. |
| Scope | The artifact area affected by the work, such as one product workspace, generated fragments, graph context, catalog input, or portfolio output. |
| Operations | The ordered delivery operations that run, including the command names and the minimal inputs needed by each operation. |
| Runtime expectation | Whether the flow expects local, hosted, hybrid, or model-free execution, and which provider reference is used when model-backed work is required. |
| Durable outputs | The files, folders, rendered pages, reports, or review notes that should exist after the run. |
| Gates and review | The validation checks, quality checks, human review, or release ownership expectations that determine whether the result can be accepted. |

The supporting `Recipe` building block carries the structured fields for these
parts. The delivery flow section defines why the flow exists and what contract
it represents; the `Recipe` section defines the reusable YAML shape.

## Delivery flow examples

Canonical examples live in `/recipes/examples/`. They are complete ODPR files
that demonstrate delivery flow patterns without making this section a YAML
reference manual.

| Example | Demonstrates |
|---|---|
| [`minimal.yaml`](/recipes/examples/minimal.yaml) | A smallest valid delivery flow for local draft generation. |
| [`ci-validate-generated-fragments.yaml`](/recipes/examples/ci-validate-generated-fragments.yaml) | A CI delivery flow that generates fragments, validates them, and fails when a required gate fails. |
| [`release-portfolio-review.yaml`](/recipes/examples/release-portfolio-review.yaml) | A production delivery flow that refreshes, localizes, explains, and requires review before release. |
| [`portfolio-localization.yaml`](/recipes/examples/portfolio-localization.yaml) | A localization delivery flow that turns portfolio input into configured language outputs. |
| [`hybrid-graph-review.yaml`](/recipes/examples/hybrid-graph-review.yaml) | A hybrid delivery flow where local graph context is prepared before hosted explanation or review. |
