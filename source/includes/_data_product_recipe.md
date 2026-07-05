# Data Product Recipe

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

The data product recipe manifest indexes a reviewable set of files. Mandatory
core sections make every data product recipe understandable and validatable,
including the graph context for the product. Optional standardized sections add
detail only when the product needs them.


![Data Product Recipe manifest with mandatory core sections and optional standardized sections.](images/data-product-recipe.svg)






`DataProductRecipe` is the ODPR root object for the reviewable handoff artifact
used by developers and AI agents when planning and implementing one data
product.

The data product recipe manifest describes the handoff artifact. It does not
define implementation workflow execution, and it does not define the ODPS
product itself. Developers and AI agents may use their own repositories,
platforms, CI/CD systems, SDKs, and agent tools to implement the product. The
source product specification remains an ODPS file referenced by the data product
recipe.

## Manifest boundary

`data-product-recipe.yaml` is mostly structure and metadata. More precisely, it
is the manifest index for the handoff artifact. It answers these questions:

- What is this Data Product Recipe?
- What version, status, readiness, and review state does it have?
- Which required files are included?
- Where are those files?
- What format are they?
- Is there optional provenance, such as `recipeRef`?

The manifest MUST NOT contain the full plan content, product specification,
relationship graph, pricing details, implementation instructions, or AI-agent
operating brief. Those details belong in referenced files such as
`plans/delivery-plan.md`, `product-context/odps.yaml`, `context/odpg.yaml`,
optional plan sections, and `agent/ai-agent-brief.md`.

## Root structure

> Root shape example:

```yaml
schema: <ODPR schema URI>
version: "1.0"
kind: DataProductRecipe
dataProductRecipe:
  metadata:
    id: <data product recipe id>
    name: <localized data product recipe name>
    description: <localized data product recipe description>
  version: <data product recipe artifact version>
  status: draft
  sections: []
  readiness: {}
  review: {}
```

The data product recipe root uses the same ODPR document envelope as other ODPR
objects: `schema`, `version`, and `kind` identify the document, and
`dataProductRecipe` contains the manifest.

The manifest is intentionally an index, not the full delivery plan. It points to
the files that developers, reviewers, SDKs, CI checks, and AI agents should
inspect:

- `version` identifies the data product recipe artifact version, separate from
  the ODPR specification version.
- `recipeRef`, when present, identifies provenance or generation context for
  the data product recipe. It is not an instruction for developers or AI agents
  to execute an ODPR workflow recipe.
- `sections` lists the stable section IDs, paths, and formats. The source ODPS
  product specification and recipe README are referenced through mandatory
  section entries instead of duplicate top-level fields.
- `readiness.score` is a confidence value from `0` to `100`.
- `review.status` records whether the data product recipe is still pending,
  approved, or needs changes.

The YAML example shows the minimal valid data product recipe manifest. It
includes every schema-required field and every mandatory section ID, including
`relationship-context`, but omits optional metadata and optional sections such
as `pricing-plan`, `sla-plan`, and `relationship-plan`.

## Minimum folder structure

> Minimum folder structure example:

```text
customer-analytics-data-product-recipe/
├── data-product-recipe.yaml
├── README.md
├── product-context/
│   └── odps.yaml
├── context/
│   └── odpg.yaml
├── plans/
│   ├── product-summary.md
│   └── delivery-plan.md
├── governance/
│   └── open-questions.md
└── agent/
    └── ai-agent-brief.md
```

A minimum valid data product recipe is a small manifest-led folder. The root
contains the `data-product-recipe.yaml` manifest and the `README.md` entrypoint.
The remaining files are the mandatory core sections referenced from
`dataProductRecipe.sections`, including the source ODPS product specification,
relationship context, planning notes, governance questions, and AI-agent brief.

This folder structure is the recommended minimum convention. It keeps the
schema-required section IDs discoverable without making ODPR a filesystem
standard.

| Folder or file | Typical content |
|---|---|
| `data-product-recipe.yaml` | Root `DataProductRecipe` manifest. |
| `README.md` | `recipe-readme` section and first reader entrypoint. |
| `product-context/` | Source ODPS product specification. |
| `context/` | Mandatory ODPG graph or relationship context. |
| `plans/` | Mandatory product summary and delivery plan. |
| `governance/` | Mandatory open questions. |
| `agent/` | Mandatory AI agent brief and agent-facing handoff guidance. |

The schema validates the section IDs, paths, and formats declared in
`dataProductRecipe.sections`. It does not require every data product recipe to
use identical directory names, but using the minimum structure makes packages
predictable for humans, SDKs, CI checks, and AI agents.

## Full folder structure

> Full folder structure example:

```text
customer-analytics-data-product-recipe/
├── data-product-recipe.yaml
├── README.md
├── product-context/
│   └── odps.yaml
├── context/
│   └── odpg.yaml
├── plans/
│   ├── product-summary.md
│   ├── delivery-plan.md
│   ├── product-interface-plan.md
│   ├── access-plan.md
│   ├── contract-plan.yaml
│   ├── pricing-plan.md
│   ├── quality-plan.md
│   ├── sla-plan.md
│   ├── lifecycle-plan.md
│   ├── relationship-plan.md
│   ├── validation-plan.md
│   └── test-plan.md
├── readiness/
│   └── operational-readiness.md
├── governance/
│   ├── open-questions.md
│   ├── risk-register.md
│   └── developer-review-checklist.md
├── implementation/
│   ├── implementation-constraints.md
│   └── backlog-items.md
├── portfolio/
│   └── portfolio-context.md
└── agent/
    └── ai-agent-brief.md
```

The full structure shows one conventional placement for every standardized
optional section. It is an example for complete or highly governed data product
recipes, not the minimum required package.

Optional planning sections can live under `plans/` when they describe product
interfaces, access, contracts, pricing, quality, SLA, lifecycle, relationships,
validation, or tests. Readiness-specific material may use `readiness/`.
Governance material may use `governance/`. Implementation-oriented optional
sections may use `implementation/`, and portfolio context may use `portfolio/`.

The manifest remains the source of truth. A full folder is valid only when the
corresponding optional section IDs, paths, and formats are declared in
`dataProductRecipe.sections`. Files that are not declared in the manifest are
supporting material, not standardized Data Product Recipe sections.

## Mandatory data product recipe fields

| Element name | Type | Options | Description |
|---|---|---|---|
| `metadata` | object | - | Stable data product recipe identity and name. |
| `metadata.id` | string | - | Stable data product recipe identifier. |
| `metadata.name` | object | localized text object | Human-readable data product recipe name. |
| `metadata.description` | object | localized text object | Short data product recipe description for human readers. |
| `version` | string | semantic version | Version of this data product recipe artifact. This is separate from the top-level ODPR specification version. |
| `status` | string | `announcement`, `draft`, `development`, `testing`, `acceptance`, `production`, `sunset`, `retired` | Data product recipe lifecycle status aligned with ODPS status values. |
| `sections` | array | mandatory section IDs | Data product recipe section index with stable section IDs, paths, and formats. |
| `readiness.score` | number | `0`-`100` | Readiness confidence; `0` means no readiness confidence. |
| `readiness.status` | string | `missing`, `partial`, `ready` | Readiness status. |
| `review.required` | boolean | `true`, `false` | Whether human review is required before implementation, publication, automation, or agent-assisted code work. |
| `review.status` | string | `pending`, `approved`, `changes-requested` | Review status. |

## Optional data product recipe fields

| Element name | Type | Options | Description |
|---|---|---|---|
| `recipeRef` | relative path | - | Optional provenance or generation-context reference for the ODPR recipe that created or informed the data product recipe. This is not an implementation dependency for developers or AI agents. |

## Mandatory core section IDs

The following core section IDs define the minimum data product recipe that a
developer, reviewer, SDK, CI check, or AI agent can rely on. A valid
`DataProductRecipe` manifest MUST include each one in `dataProductRecipe.sections`.

![Mandatory Data Product Recipe core section files.](images/data-product-recipe-core.svg)

Each entry in `dataProductRecipe.sections` is an index record with a stable
`id`, a path relative to the data product recipe root, and a `format`. The
schema validates that the required IDs are present; tooling can then use the
paths and formats to locate the actual Markdown or YAML files.

The mandatory core is intentionally small. Markdown sections carry the human
delivery narrative, open decisions, and agent instructions. YAML sections carry
the machine-readable source product specification and relationship graph
context. Optional data product recipe sections may add more detail, but they do
not replace these core files.



### recipe-readme

> Recipe README example:

```markdown
## Recipe Status

Status: draft
Readiness score: 0
Review status: pending

## Read Order

1. product-context/odps.yaml
2. plans/product-summary.md
3. plans/delivery-plan.md
4. governance/open-questions.md
5. agent/ai-agent-brief.md
6. context/odpg.yaml

## Mandatory Sections

- recipe-readme
- source-product-spec
- product-summary
- delivery-plan
- open-questions
- ai-agent-brief
- relationship-context

## Optional Sections Present

- None

## Blocking Questions

- See governance/open-questions.md.

## Approval Gates

- Human review is required before implementation.

## Next Action

Resolve delivery-blocking questions.
```

`recipe-readme` is the required human and agent entrypoint for the data product
recipe. It summarizes data product recipe status, read order, mandatory
sections, optional sections present, blocking questions, approval gates, and the
next action.

Use this section to orient a reviewer before they inspect the data product
recipe details. The README should make the data product recipe state obvious
without requiring the reader to open every referenced file.

Expected content:

- Current `dataProductRecipe.status`, `readiness.score`, and `review.status`.
- Recommended read order for humans, developers, and agents.
- Core sections that are present and optional sections that were included.
- Blocking questions and approval gates.
- One concrete next action.

Do not use this section for the full delivery plan, backlog, risk register, or
implementation details. It should point to those sections when they exist.

Path: `README.md`

Format: `markdown`

### source-product-spec

> Source product specification example:

```yaml
# Abbreviated ODPS product specification.
# Use the current ODPS schema and required ODPS fields.
schema: <current ODPS schema URI>
version: <ODPS specification version>
kind: DataProduct
product:
  productId: customer-analytics
  name: Customer Analytics
```

`source-product-spec` is the source ODPS product specification included for
traceability. It is the product definition the data product recipe is about;
ODPR does not redefine the product model.

Use this section as the authoritative product input. Developers and agents
should treat it as the product contract and avoid inventing product facts that
are not present in the ODPS source or in approved data product recipe sections.

Expected content:

- A valid ODPS product specification.
- Stable product identity, name, owner/domain, consumers, and product metadata
  as defined by ODPS.
- Any product-level fields required by the ODPS version used by the data product
  recipe.

Do not convert the ODPS product spec into ODPR fields. Do not use this file for
delivery tasks, implementation notes, or agent instructions.

Path: `product-context/odps.yaml`

Format: `yaml`

### product-summary

> Product summary example:

```markdown
## Product Identity

Customer Analytics

## Purpose

Provide reusable customer analytics data for approved consumers.

## Owner And Domain

Customer domain, analytics owner.

## Consumers

- Customer success
- Marketing analytics

## Use Cases

- Segment customers
- Monitor lifecycle signals

## Signals And Outcomes

- Customer activity signals
- Retention and growth outcomes

## Product Boundary

This data product recipe covers one data product, not dashboards or downstream apps.
```

`product-summary` gives a concise human-readable summary of the product,
consumers, use cases, boundaries, and expected outcomes. It helps developers and
agents understand the product without reading every source field first.

Use this section to translate the source product specification into a short
reviewable narrative. The summary should help a developer understand what is
being built and what is outside the product boundary.

Expected content:

- Product identity and plain-language purpose.
- Owner, domain, expected consumers, and primary use cases.
- Signals, outcomes, or business/data objectives that define success.
- Product boundary, including what the data product recipe must not implement.

Do not introduce product facts that contradict the ODPS source. If the source is
ambiguous, record the ambiguity in `open-questions` instead of resolving it
silently.

Path: `plans/product-summary.md`

Format: `markdown`

### delivery-plan

> Delivery plan example:

```markdown
## Current Understanding

The source ODPS file defines one customer analytics data product.

## Decisions

- Use the source ODPS file as the product contract.
- Keep implementation changes human-reviewed.

## Missing Inputs

- Confirm target platform.
- Confirm consumer access path.

## Implementation Impact

Implementation requires product contract, access, and quality checks.

## Validation

Validate the data product recipe manifest, product spec, and generated implementation plan.
```

`delivery-plan` describes the developer-controlled implementation path. It
captures sequencing, dependencies, implementation impact, and validation
expectations without turning the data product recipe into an execution script.

Use this section to explain how the data product recipe can move from product
definition to implementation. It should be practical enough for a developer to
estimate the work and for an agent to understand the intended sequence.

Expected content:

- Current understanding of the delivery target.
- Decisions already made and inputs still missing.
- Implementation impact for product contract, access, quality, and validation.
- Validation expectations before implementation, publication, or automation.

Do not use this section for shell commands, deployment scripts, run logs, or
automatic ticket creation. ODPR recipes define workflow intent; implementation
execution belongs to tools and platforms.

Path: `plans/delivery-plan.md`

Format: `markdown`

### open-questions

> Open questions example:

```markdown
## Delivery-Blocking Questions

- Which platform owns implementation?
- Which consumers need first access?

## Non-Blocking Questions

- Should pricing be added later?

## Decision Owners

- Product owner
- Engineering owner

## Required Before Implementation

- Resolve delivery-blocking questions.
```

`open-questions` records missing or ambiguous decisions. It is mandatory because
draft packages are valid, but unresolved ambiguity must be visible.

Use this section to prevent false readiness. A data product recipe may be valid
while still being incomplete, but the missing decisions must be explicit and
assigned where possible.

Expected content:

- Delivery-blocking questions that must be answered before implementation.
- Non-blocking questions that can be resolved later.
- Decision owners or accountable roles.
- A clear list of questions required before implementation.

Do not hide unknowns in prose elsewhere. Do not let an AI agent infer answers
for delivery-blocking questions unless an authoritative data product recipe
input provides the answer.

Path: `governance/open-questions.md`

Format: `markdown`

### ai-agent-brief

> AI agent brief example:

```markdown
## Objective

Prepare implementation guidance for one data product recipe.

## Authoritative Inputs

- data-product-recipe.yaml
- product-context/odps.yaml
- plans/product-summary.md
- plans/delivery-plan.md
- governance/open-questions.md
- repository AGENTS.md or equivalent, when implementation code changes are requested

## Input Priority

1. data-product-recipe.yaml
2. product-context/odps.yaml
3. context/odpg.yaml
4. plans/*.md
5. governance/open-questions.md
6. repository agent instructions for code editing conventions only

## Allowed Work

- Read the data product recipe manifest first.
- Summarize implementation impact.
- Draft implementation guidance from referenced files.
- Inspect repository agent instructions before editing code.
- Preserve unrelated files.

## Prohibited Work

- Do not invent missing product facts.
- Do not create tickets or deploy automatically.
- Do not change source product or graph context unless asked.
- Do not copy tool-specific agent rules into the data product recipe.

## Ambiguity Handling

- Treat delivery-blocking questions as blockers.
- Record unresolved assumptions instead of silently resolving them.
- Prefer a short question over guessing when product facts conflict.

## Expected Outputs

- Implementation guidance.
- Validation notes.
- Open decisions that still require a human owner.
- Summary of files changed when implementation work is performed.

## Validation Expectations

- Check the Data Product Recipe manifest.
- Check referenced ODPS and ODPG files before implementation.
- Report validation commands, checks, or review evidence.

## Approval Gates

- Ask for review before implementation changes.

## Implementation Boundaries

- Work only from the referenced data product recipe files.
- Follow repository agent instructions when editing code.
```

`ai-agent-brief` is the handoff contract for AI-assisted work on the data
product recipe. It gives agents the objective, authoritative inputs, input
priority, allowed work, prohibited work, ambiguity handling, expected outputs,
validation expectations, approval gates, and implementation boundaries. It
derives common AGENTS.md practices into a product-specific brief: keep
instructions task-local, make input priority explicit, preserve unrelated files,
separate product facts from repository editing conventions, and require visible
validation evidence. It keeps agent guidance in a file instead of adding
agent-control fields to the manifest.

These practices are aligned with AGENTS.md research and industry guidance:
use a dedicated agent-readable guidance artifact for efficiency
([AGENTS.md efficiency study](https://arxiv.org/abs/2601.20404)), keep
instructions minimal and task-relevant to avoid reducing task success
([AGENTS.md evaluation study](https://arxiv.org/abs/2602.11988)), and avoid
context bloat, conflicting instructions, and leaked tool-specific rules
([AGENTS.md configuration-smell study](https://arxiv.org/abs/2606.15828)).

Use this section to make the data product recipe safe for AI-assisted work. It
should tell an agent what to read first, what it may produce, what it must not
do, how to handle missing information, which outputs are expected, and when
human approval is required.

Expected content:

- Objective for the agent in the context of this data product recipe.
- Authoritative input files and their priority.
- Allowed work and prohibited work.
- Ambiguity handling for blocking questions, assumptions, and missing inputs.
- Expected outputs from the agent.
- Validation expectations before implementation or publication.
- Approval gates and implementation boundaries.
- Repository agent instruction handling when implementation code changes are
  requested.

Do not put model-provider settings, credentials, hidden prompts, or broad
repository-wide agent rules here. Do not use this section to bypass unresolved
questions or human approval gates. Do not paste an implementation repository's
entire AGENTS.md into the data product recipe; reference repository instructions
only when implementation work will happen in that repository. Provider
configuration belongs to ODPR Provider objects or runtime configuration, and
repository guidance belongs in the repository's agent instruction files.

Path: `agent/ai-agent-brief.md`

Format: `markdown`

### relationship-context

> Relationship context example:

```yaml
schema: https://opendataproducts.org/odpg-v1.0/schema/odpg.yaml
version: 1.0
kind: Graph
graph:
  metadata:
    id: GRAPH-AVIATION-001
    name:
      en: Aviation Data Product Value Graph
    description:
      en: Graph for aviation data products, use cases, policies, agents, and objectives.
    domain:
      en: Aviation
    status: draft

  nodes:
    - id: UC-AVIATION-001
      type: UseCase
      $ref: ../usecases/predictive-maintenance-aircraft.yaml
    - id: OBJ-AVIATION-001
      type: BusinessObjective
      $ref: ../objectives/increase-fleet-availability.yaml
    - id: DP-AVIATION-001
      type: DataProduct
      $ref: ../products/aircraft-maintenance-history.yaml
    - id: DP-AVIATION-002
      type: DataProduct
      $ref: ../products/aircraft-sensor-events.yaml
    - id: AGENT-AVIATION-001
      type: Agent
      $ref: ../agents/maintenance-recommendation-agent.yaml

  edges:
    - from: UC-AVIATION-001
      to: DP-AVIATION-001
      type: uses
      confidence: high
    - from: UC-AVIATION-001
      to: DP-AVIATION-002
      type: uses
      confidence: high
    - from: UC-AVIATION-001
      to: OBJ-AVIATION-001
      type: supports
      confidence: high
    - from: AGENT-AVIATION-001
      to: DP-AVIATION-001
      type: uses
      confidence: high
```

`relationship-context` is the required graph context for the data product recipe. It
references the ODPG relationship view that places the product in context with
upstream products, downstream products, dependencies, shared signals, lineage,
or other graph relationships.

Use this section to make product context explicit for humans, developers, and AI
agents. A data product recipe may still describe relationship work in
`relationship-plan`, but the context graph itself MUST be available through
`relationship-context`.

Expected content:

- A valid ODPG graph or graph fragment.
- Relationship IDs or names that are relevant to this data product recipe.
- Source and target products for the relevant relationships.
- Relationship type, dependency direction, and any context decisions that affect
  implementation.

Do not use this section for free-form relationship notes. Use an ODPG artifact
or ODPG-compatible graph fragment so data product recipe context remains
machine-readable.

Path: `context/odpg.yaml`

Format: `yaml`

JSON Schema validates the manifest shape, the closed section ID enum, and the
presence of mandatory core section IDs. A repository checker SHOULD validate
the `recipe-readme` heading order because JSON Schema should not parse
Markdown bodies.

## Optional standardized section IDs

Optional standardized section IDs add detail only when the data product recipe
needs it. They are not required for a valid handoff artifact, but when present
they MUST use one of the standardized IDs below in `dataProductRecipe.sections`.
Each optional section entry still declares its own relative `path` and `format`
in the manifest.

### product-interface-plan

> Product interface plan example:

```markdown
## Interfaces

- REST API: customer segment lookup
- Table: analytics.customer_segments

## Consumers

- Customer success
- Marketing analytics

## Constraints

- No direct access to raw customer events.
```

`product-interface-plan` describes how consumers, platforms, tools, and agents
will interact with the data product. Use it when the data product recipe needs to clarify
interfaces beyond the product summary, such as APIs, files, events, query
endpoints, semantic layers, catalog entries, or AI-agent context surfaces.

Expected content includes the interface types, intended consumers, access
pattern for each interface, input/output expectations, and any interface-level
constraints that affect implementation.

### access-plan

> Access plan example:

```markdown
## Consumer Groups

- Customer success analysts

## Access Method

- Approved catalog request
- Read-only warehouse role

## Open Decisions

- Confirm external partner access.
```

`access-plan` describes how consumers get permission to use the product. Use it
when access decisions, approval flow, identity model, entitlement, onboarding,
or revocation must be understood before implementation.

Expected content includes consumer groups, authentication and authorization
expectations, approval owners, access request flow, onboarding notes, and any
access decisions that are still unresolved.

### contract-plan

> Contract plan example:

```yaml
# Abbreviated ODCS-compatible YAML data contract.
# Use Open Data Contract Standard v3.1.0 for the complete shape.
id: customer-analytics-contract
version: 1.0.0
name: Customer Analytics Contract
schema:
  - name: customer_id
    type: string
  - name: segment
    type: string
quality:
  - dimension: completeness
    rule: customer_id must be present
```

`contract-plan` is a YAML data contract aligned with the
[Open Data Contract Standard v3.1.0](https://bitol-io.github.io/open-data-contract-standard/v3.1.0/).
Use it when the data product recipe must clarify schemas, compatibility
expectations, versioning behavior, breaking-change handling, or commitments
between producers and consumers.

Expected content includes an ODCS-compatible contract structure, contract
scope, schema or payload expectations, consumer obligations, producer
obligations, compatibility policy, quality expectations when relevant, SLA or
support expectations when relevant, and the review path for contract changes.

The `contract-plan` section entry MUST use `format: yaml`.

### pricing-plan

> Pricing plan example:

```markdown
## Model

Internal showback by monthly active consumer team.

## Cost Drivers

- Storage
- Query volume
- Refresh frequency

## Review

Finance owner reviews quarterly.
```

`pricing-plan` describes the commercial, chargeback, or showback model for the
data product. Use it when the product has pricing, internal cost allocation,
entitlement tiers, cost drivers, or billing ownership that developers and
reviewers must understand.

Expected content includes pricing model, chargeback or showback approach,
entitlement tiers, measurable cost drivers, billing owner, review requirements,
and unresolved pricing decisions.

### quality-plan

> Quality plan example:

```markdown
## Dimensions

- Completeness: customer_id must be present
- Freshness: daily refresh before 08:00 UTC

## Blocking Checks

- Reject publish when required fields are missing.

## Warning Checks

- Warn when segment coverage drops below 95%.
```

`quality-plan` describes the quality expectations that implementation must
support. Use it when freshness, completeness, accuracy, validity, uniqueness,
or other quality dimensions need explicit checks.

Expected content includes quality dimensions, blocking validation rules,
warning-level checks, expected thresholds, data owner responsibilities, and how
quality failures should be surfaced.

### sla-plan

> SLA plan example:

```markdown
## Targets

- Availability: 99 percent monthly
- Refresh: daily

## Support

- Owner: analytics operations
- Escalation: data product owner

## Measurement

- Monitor refresh completion and access errors.
```

`sla-plan` describes operational commitments for the product. Use it when the
data product recipe needs to clarify availability, refresh timing, response expectations,
incident handling, support model, escalation, or measurement.

Expected content includes service targets, measurement method, support owner,
incident response expectations, escalation path, reporting cadence, and any SLA
assumptions that need approval.

### lifecycle-plan

> Lifecycle plan example:

```markdown
## Current State

development

## Transition Gates

- Contract approved
- Access reviewed
- Validation checks passing

## Change Process

Breaking changes require consumer review.
```

`lifecycle-plan` describes how the product moves through status changes over
time. Use it when development, testing, acceptance, production, sunset, retired
state, versioning, deprecation, or change process needs explicit guidance.

Expected content includes current lifecycle state, required transition gates,
release or publication expectations, versioning approach, deprecation process,
and owners for lifecycle decisions.

### relationship-plan

> Relationship plan example:

```markdown
## Upstream Products

- Customer master data

## Downstream Consumers

- Retention dashboard

## Delivery Impact

- Confirm upstream freshness before implementation.
```

`relationship-plan` describes product relationships that affect delivery. Use
it when upstream products, downstream consumers, shared objectives, shared
signals, dependencies, conflicts, or portfolio gaps change implementation
choices.

Expected content includes relevant upstream and downstream products, dependency
type, relationship impact, unresolved conflicts, and how the required
`relationship-context` should be interpreted during delivery.

### validation-plan

> Validation plan example:

```markdown
## Required Checks

- Validate Data Product Recipe manifest
- Validate ODPS source product specification
- Validate ODCS contract plan when present

## Pass Criteria

- No schema errors
- No unresolved blocking questions
```

`validation-plan` describes how the data product recipe and resulting implementation should
be checked before approval, publication, automation, or agent-assisted work.
Use it when validation goes beyond the core data product recipe manifest checks.

Expected content includes specification validation, contract validation,
quality validation, access validation, SLA validation, relationship validation,
documentation validation, readiness validation, and pass/fail expectations.

### test-plan

> Test plan example:

```markdown
## Test Scope

- Contract tests
- Quality checks
- Access checks

## Fixtures

- Approved sample customer segment records

## Acceptance

- Consumers can query approved fields only.
```

`test-plan` describes implementation-oriented tests derived from the data product recipe.
Use it when developers need to convert the product intent into repeatable
checks for code, pipelines, contracts, integrations, or consumer acceptance.

Expected content includes test scope, test levels, required fixtures, expected
assertions, acceptance tests, negative tests, and AI-agent context tests when
agent-assisted implementation is expected.

### operational-readiness

> Operational readiness example:

```markdown
## Readiness Score

60

## Missing Inputs

- Final access owner
- SLA approval

## Launch Blockers

- Contract not approved
```

`operational-readiness` describes whether the data product recipe is ready to move toward
production use. Use it when the readiness score needs supporting detail beyond
the numeric `readiness.score` field.

Expected content includes readiness dimensions, readiness score rationale,
missing inputs, launch blockers, required approvals, and the conditions needed
to move from partial readiness to ready.

### risk-register

> Risk register example:

```markdown
## Risks

- Risk: unclear external consumer access
  Impact: implementation delay
  Owner: product owner
  Status: open

## Blocking

- External access decision blocks launch.
```

`risk-register` records risks that could affect implementation or operation.
Use it when known product, access, contract, quality, SLA, lifecycle,
dependency, dashboard-confusion, or AI-agent-context risks need explicit
tracking.

Expected content includes risk description, impact, likelihood, owner,
mitigation, current status, and whether the risk blocks implementation.

### developer-review-checklist

> Developer review checklist example:

```markdown
## Checklist

- [ ] Mandatory sections are present
- [ ] ODPS source product is valid
- [ ] Open questions are reviewed
- [ ] Contract impact is understood
- [ ] Agent boundaries are clear
```

`developer-review-checklist` gives human developers a compact approval checklist
before implementation, publication, automation, or agent-assisted code work.
Use it when the data product recipe should support a repeatable engineering review.

Expected content includes checks for source product validity, mandatory data product recipe
sections, unresolved questions, contract impact, access impact, validation
expectations, implementation boundaries, and approval status.

### implementation-constraints

> Implementation constraints example:

```markdown
## Allowed

- Use existing warehouse platform
- Add read-only serving interface

## Prohibited

- Move raw customer events
- Change source product identity

## Assumptions

- Access is role-based.
```

`implementation-constraints` describes product-specific boundaries that affect
implementation. Use it when the data product recipe needs constraints that are more
specific than the general `ai-agent-brief`.

Expected content includes allowed platforms, prohibited changes, data movement
constraints, security or privacy boundaries, naming constraints, integration
limits, and assumptions that must not be changed without review.

### backlog-items

> Backlog items example:

```markdown
## Items

- Title: Create contract validation
  Priority: high
  Depends on: contract approval

- Title: Add access role
  Priority: medium
  Depends on: access owner decision
```

`backlog-items` lists reviewable work items without requiring ODPR to create
external tickets. Use it when the data product recipe should expose likely implementation
tasks while remaining independent of Jira, GitHub Issues, or another work
tracking system.

Expected content includes item title, short description, dependency, priority
or sequencing hint, owner when known, and acceptance notes. External ticket IDs
may be included as references but are not required.

### portfolio-context

> Portfolio context example:

```markdown
## Portfolio

Customer analytics portfolio

## Related Products

- Customer master data
- Customer engagement events

## Decision Impact

- Avoid duplicate customer segmentation products.
```

`portfolio-context` includes ODPC catalog or portfolio context when the product
belongs to a broader portfolio. Use it when portfolio placement, catalog entry,
ownership model, duplication risk, or portfolio-level governance affects the
data product recipe.

Expected content includes the referenced ODPC catalog or portfolio artifact,
portfolio identity, related products, ownership context, and any portfolio
decision that affects implementation.

## Practice alignment

The data product recipe model follows common CI/CD and agent practices without
importing their execution models into ODPR. Stable section IDs act like artifact
names. The data product recipe uses mandatory section entries for handoff files
such as the README, ODPS product specification, ODPG graph context, delivery
plan, open questions, and AI agent brief. Optional `recipeRef` may record
provenance or generation context, but it is not required for developers or AI
agents to execute an ODPR workflow recipe. Execution terms such as job, run, and
step stay out of `DataProductRecipe` because `Recipe.steps` already models
workflow steps elsewhere in ODPR.

The `ai-agent-brief` derives the portable parts of AGENTS.md practice without
turning ODPR into an agent configuration format. It should define the objective,
source-of-truth files, input priority, allowed work, prohibited work, ambiguity
handling, expected outputs, validation expectations, approval gates, and
implementation boundaries for this data product recipe. Repository-level
AGENTS.md or equivalent files remain the right place for coding conventions,
build commands, local test commands, and repository-specific tool rules.

The model is aligned with these non-normative practice references:

| Practice source | Applied ODPR practice |
|---|---|
| [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) | Keep execution terms such as workflow, job, run, and step distinct from data product recipe manifest terms. |
| [GitHub workflow artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data) | Treat generated outputs as named artifacts that can be archived, shared, downloaded, and validated. |
| [SLSA provenance v1.0](https://slsa.dev/spec/v1.0/provenance) | Separate what was produced from how it was produced and which inputs were used. |
| [Open Data Contract Standard v3.1.0](https://bitol-io.github.io/open-data-contract-standard/v3.1.0/) | Align `contract-plan` with a YAML data contract standard instead of inventing an ODPR-specific contract shape. |
| [Agentic AI Foundation and AGENTS.md](https://www.wired.com/story/openai-anthropic-and-block-are-teaming-up-on-ai-agent-standards) | Treat agent instructions as an interoperable guidance artifact, but keep ODPR's data product recipe brief product-specific and implementation-neutral. |
| [AGENTS.md efficiency study](https://arxiv.org/abs/2601.20404) | Provide agent-readable guidance as a dedicated data product recipe section. |
| [AGENTS.md evaluation study](https://arxiv.org/abs/2602.11988) | Keep agent instructions minimal and avoid broad, unnecessary requirements in the manifest. |
| [AGENTS.md configuration-smell study](https://arxiv.org/abs/2606.15828) | Avoid context bloat, conflicting instructions, and leaked tool-specific rules in the schema. |
