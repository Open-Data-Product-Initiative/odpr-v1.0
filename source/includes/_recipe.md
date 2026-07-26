# Recipe

The `Recipe` object is a supporting ODPR building block. It declares one
reusable workflow unit that delivery flows and trigger-based flows can use.

Recipes are intended to be readable by humans and executable by tools. A recipe
should be specific enough for an SDK, CI/CD system, MCP server, or agent to
understand the workflow before it runs, while staying portable enough to avoid
binding the standard to one implementation.

## Recipe design principle

A recipe is not a script. A recipe is a portable, declarative workflow
contract. Scripts tell one tool what to do. Recipes tell teams, tools, agents,
and automation systems how a data product workflow should run.

## Recipe structure

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

### Recipe fields

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
  scope: catalog
  steps:
    - id: validate-fragments
      command: validate
      document: generated/fragments/signal.yaml
  outputs:
    - id: generated-fragments
      path: generated/fragments/
```

| Element | Type | Required | Description |
|---|---|---|---|
| `metadata` | object | required | Stable recipe identity, name, optional description, owner, and tags. |
| `version` | string | required | Version of this recipe workflow. This is separate from the top-level ODPR specification version. |
| `type` | string | required | Recipe type such as `dev`, `ci`, `release`, `localization`, `hybrid`, or `agent`. |
| `scope` | string | optional | Standards-family target governed by the recipe. Allowed values are `data-product`, `catalog`, `graph`, and `portfolio`. |
| `steps` | array | required | Ordered workflow operations. |
| `inputs` | array | optional | Named workflow inputs. |
| `outputs` | array | optional | Named workflow outputs. |
| `intent` | string | optional | Human-authored reason for the recipe and the result the workflow should support. |
| `instructions` | string | optional | Human-authored guidance for how an agent or tool should work through the recipe. |
| `groundingTo` | object | optional | Controlled graph node and edge types that should ground agent-assisted work. |
| `contextFormat` | object | optional | Context serialization policy such as YAML, TOON, GCF, or automatic fallback. |
| `execution` | object | optional | Workflow intent such as local, hosted, hybrid, or model-free runtime/provider class. |
| `trigger` | object | optional | Graph change pattern that can make a graph-triggered recipe applicable. |
| `graphContext` | object | optional | Minimal ODPG graph context needed after a graph trigger matches. |
| `gates` | array | optional | Validation, quality, or review gates. |
| `review` | object | optional | Human or agent review expectations. |
| `environment` | string | optional | Environment label such as development, CI, staging, or production. |
| `runPolicy` | object | optional | Runtime limits such as timeout or retry guidance. |

### Step fields

Recipe steps are ordered operations or standardized agent discovery tasks. Each
step has a stable `id` and declares either a runnable `command` or a
standardized `discoveryType`.

| Element | Type | Required | Description |
|---|---|---|---|
| `id` | string | required | Stable step identifier inside the recipe. |
| `command` | string | optional | Operation the executor should run, such as `generate`, `validate`, `odpg.agent-context`, or `explain`. Use for executable workflow operations. Do not use on agent discovery steps that declare `discoveryType`. |
| `discoveryType` | enum string | optional | Controlled agent discovery step type. Allowed values:<br>`find-affected-use-cases`<br>`explain-use-case-impact`<br>`find-affected-data-products`<br>`explain-data-product-impact`<br>`find-affected-objectives`<br>`explain-objective-impact`<br>`identify-gaps-and-risks`<br>`produce-findings-and-recommendations` |
| `intent` | string | optional | Human-authored reason for the step and the result the step should support. |
| `instructions` | string | optional | Human-authored guidance for how an agent or tool should work through the step. |
| `iterationLimit` | integer | optional | Maximum number of agent or LLM work passes allowed inside the step. |
| `exitWhen` | string | optional | Human-authored stopping condition for bounded agent or LLM work inside the step. |
| `runtimeRef` | URI reference | optional | Step-level runtime profile override for LLM-backed steps. |
| `model` | string | optional | Step-level model override for LLM-backed steps. |
| `contextFormat` | object | optional | Step-level context serialization policy. |

### Recipe types

| Type | Purpose |
|---|---|
| `dev` | Local development, drafting, and fast iteration. |
| `ci` | Automated validation and build checks. |
| `release` | Production-grade review, refresh, localization, rendering, and publishing. |
| `localization` | Translation and multilingual portfolio or product work. |
| `hybrid` | Workflows that mix local and hosted execution. |
| `agent` | Agent-safe workflows that AI agents can inspect and run. |

### Recipe scopes

`recipe.scope` identifies the standards-family target the recipe primarily
governs. `recipe.type` describes the workflow category, while `recipe.scope`
describes what kind of artifact or standards-family area the recipe is for.

| Scope | Meaning |
|---|---|
| `data-product` | Workflow automation that generates, validates, or reviews Data Product Recipe handoff artifacts for one data product. |
| `catalog` | Catalog or portfolio catalog generation, validation, publication, synchronization, or review. |
| `graph` | Graph/context generation, relationship extraction, validation, rendering, or review. |
| `portfolio` | Portfolio assembly, refresh, localization, rendering, explanation, review, or release work. |

`recipe.scope: data-product` does not make the `Recipe` itself a Data Product
Recipe. A scoped recipe can generate, validate, or review a handoff artifact,
but the handoff artifact uses the `DataProductRecipe` root kind and
`dataProductRecipe` manifest object. ODPR does not define a separate
`ProductRecipe` root kind.

### Recipe patterns

ODPR uses one shared `Recipe` structure. Product delivery recipes use that
structure for delivery work and handoff support. Graph-triggered recipes use
that structure when a graph change should make the recipe applicable.

## Runtime behavior

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

### Context formats

`contextFormat` declares how retrieved or generated context should be serialized
for prompt, review, or handoff use. It does not define which graph context is
retrieved, why a step exists, or which evidence should ground an answer.

| Format | Meaning |
|---|---|
| `yaml` | Use canonical YAML context. |
| `toon` | Use TOON compact context when available. |
| `gcf` | Use GCF compact graph/catalog context when available. |
| `auto` | Let the executing tool choose the preferred available context. |

Use `contextFormat.primary` for the preferred format and
`contextFormat.fallback` for acceptable alternatives.

### Intent, instructions, and grounding

`intent` is a human-authored statement of why a recipe or step exists and what
kind of result is expected. It should capture the purpose and desired outcome,
not only a short label.

`instructions` tells an agent or tool how the recipe designer expects the work
to be performed or interpreted. It can be prompt-quality prose for LLM-backed or
agent-assisted work, but it remains part of the portable recipe contract rather
than a provider-specific prompt template.

`groundingTo` is a recipe-level graph grounding boundary for agent-assisted
work. It declares which retrieved graph node types and edge types may ground the
agent's answer, finding, impact explanation, or review recommendation. If
omitted, the full retrieved context may be used.

`groundingTo.nodeTypes` uses the same controlled values as graph trigger
`subject.nodeType`:

| Value | Meaning |
|---|---|
| `DataProduct` | Data product or product reference node. |
| `BusinessObjective` | Objective, KPI, or business outcome node. |
| `UseCase` | Use case node. |
| `Signal` | Signal, metric, event, or indicator node. |
| `Policy` | Policy, governance, privacy, consent, or compliance node. |
| `DataContract` | Data contract node. |
| `DataService` | Data service node. |
| `API` | API or endpoint node. |
| `Owner` | Owner, team, or accountable party node. |
| `System` | System or platform node. |
| `Agent` | Agent or AI-assisted worker node. |
| `Condition` | Matched condition or declared investigation condition node. |
| `*` | Any controlled graph node type. |

`groundingTo.edgeTypes` uses controlled graph relationship values:

| Value | Meaning |
|---|---|
| `uses` | Source node uses the target node. |
| `supports` | Source node supports the target objective, use case, product, or context. |
| `enables` | Source node enables the target node or outcome. |
| `dependsOn` | Source node depends on the target node. |

Agent discovery steps declare `discoveryType` so tools can recognize the
purpose of the step without parsing free-form instructions. A step that declares
`discoveryType` MUST NOT also declare `command`.

Allowed `discoveryType` values are:

| Value | Meaning |
|---|---|
| `find-affected-use-cases` | Find use cases affected by the condition, change, product, relationship, or previous finding. |
| `explain-use-case-impact` | Explain how identified use cases are affected. |
| `find-affected-data-products` | Find data products affected by the condition, change, use case, relationship, or previous finding. |
| `explain-data-product-impact` | Explain how identified data products are affected. |
| `find-affected-objectives` | Find business objectives or KPIs affected by the condition, change, product, use case, or previous finding. |
| `explain-objective-impact` | Explain how identified objectives or KPIs are affected. |
| `identify-gaps-and-risks` | Identify missing evidence, weak context, unresolved ownership, governance gaps, dependency risks, or conflicting relationships. |
| `produce-findings-and-recommendations` | Produce final grounded findings and recommended human actions. |

Step-level `intent` and `instructions` refine the recipe-level intent and
instructions for that operation or discovery task. They do not replace
discovery type, command parameters, inputs, outputs, gates, review policy, or
runtime policy.

Agent-assisted or LLM-backed steps MAY declare bounded in-step iteration with
`iterationLimit` and `exitWhen`.

`iterationLimit` is the maximum number of agent or LLM work passes allowed
inside that step. It is not the same as `runPolicy.maxRetries`: retries handle a
failed step execution, while `iterationLimit` bounds refinement or evidence
inspection inside one step.

`exitWhen` is a human-authored stopping condition. The runtime may stop earlier
when the condition is satisfied, but it MUST NOT exceed `iterationLimit` when
one is declared. ODPR v1 does not define loop traces, internal planning records,
or a general agent loop language.

### RuntimeProfile references

`runtimeRef` identifies an ODPR `RuntimeProfile` with a URI-reference. The
target points to a RuntimeProfile YAML document or runtime profile source. A
fragment selects the profile when the target contains or exposes more than one
profile, for example
`runtime-profiles/examples/production-quality.yaml#production-quality`.

The recipe does not embed runtime internals; it only references the runtime
profile that should be used.

A recipe can declare a default runtime profile in `execution.runtimeRef`. Individual
steps can override it with `step.runtimeRef` when one workflow mixes local and
hosted execution.

The referenced `RuntimeProfile` object defines SDK-compatible provider profiles,
model defaults, provider base URLs, API-key environment variable names, and safe
runtime generation defaults. Raw secrets MUST NOT be stored in recipes or
RuntimeProfile documents.

`execution.runtimeRef` is the default provider profile for LLM-backed steps.
Step-level `runtimeRef` overrides `execution.runtimeRef`. Step-level `model`
overrides the provider model for that step. Deterministic and report commands
MUST NOT use `runtimeRef` or `model`.

ODPR validation tools SHOULD reject embedded secrets or API keys in recipes.
Use `runtimeRef` in recipes and `apiKeyEnv` in RuntimeProfile provider profile entries
instead of fields such as `apiKey`, `token`, `password`, or inline secret
values.

### Recommended commands

ODPR keeps commands lightweight so recipes stay portable across implementations.
Implementations SHOULD support the recommended command names where the
underlying capability exists. Implementations MAY support additional commands.

| Command | Classification | Required step fields | Optional step fields |
|---|---|---|---|
| `generate` | `llm-backed` | `input`, `kind`, `output` | `config`, `prompts`, `profile`, `includeComponents`, `maxSourceChars`, `ollamaUrl` |
| `odpc.build` | `deterministic` | `input`, `output` | `html`, `toon`, `gcf`, `name`, `description`, `recursive`, `validate` |
| `odpg.build` | `llm-backed` | `input`, `output` | `toon`, `gcf`, `contextGraph`, `name`, `description`, `recursive`, `validate`, `config`, `prompts`, `ollamaUrl` |
| `odpg.agent-context` | `deterministic` | `graph`, `start`, `output` | `depth` |
| `odpg.render` | `deterministic` | `graph`, `output` | none |
| `portfolio.build` | `llm-backed` | at least one of `objectives`, `useCases`, `signals`, or `products`; and `output` | `title`, `config`, `prompts`, `ollamaUrl`, `strictValidation` |
| `portfolio.refresh` | `llm-backed` | none | `objectives`, `useCases`, `signals`, `products`, `title`, `config`, `allSources`, `prompts`, `ollamaUrl`, `strictValidation` |
| `portfolio.sync` | `deterministic` | none | `strictValidation` |
| `portfolio.localize` | `llm-backed` | `languages` | `defaultLanguage`, `config`, `prompts`, `ollamaUrl`, `strictValidation` |
| `portfolio.render` | `deterministic` | none | `output`, `strictValidation` |
| `portfolio.explain` | `report` | none | none |
| `validate` | `deterministic` | `document` | none |
| `explain` | `report` | `document` | none |

Command-specific parameters are written directly on the step. Shared durable
paths, such as a portfolio workspace used by several steps, belong in
recipe-level `inputs` or `outputs` instead of being repeated under every step.
`portfolio.localize.languages` SHOULD be written as a YAML list of BCP 47
language tags.

| Classification | Meaning |
|---|---|
| `deterministic` | No provider needed; repeatable from files and options. |
| `llm-backed` | Calls a configured provider and model. |
| `review` | Requires human or external approval. |
| `report` | Reads artifacts and produces summaries, diagnostics, or review material. |

### Outputs

Use `inputs` and `outputs` when a workflow uses or creates durable artifacts
that later steps, CI
jobs, reviewers, or agents should inspect. Outputs are named paths. They do not
replace a command-specific `output` field; they make expected durable
results visible at the recipe level.

Recipe-level paths should be project-relative. Recipes should not use absolute
paths or `..` traversal. ODPR states this safety expectation; SDKs and
platforms enforce write-scope policy.

### Gates, review, and runtime policy

Required gates SHOULD be evaluated or reported by the executing tool. Tools
SHOULD NOT silently skip required gates.

`review.required` declares whether a recipe expects review after automated
steps complete. `review.mode` can be `human`, `agent`, `both`, or `none`.

`runPolicy` gives lightweight runtime guidance such as timeout, stop-on-failure
behavior, and retry expectations. It is useful for CI jobs, local model calls,
portfolio localization, and hosted provider calls. ODPR v1 does not define
approval records, workflow pauses, run manifests, or gate status storage.

### Environment labels

Use `environment` to label the intended operating context, such as
`development`, `ci`, `staging`, or `production`. The value is a string so teams
can use local naming conventions while keeping common labels readable.

## Recipe example

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
    runtimeRef: runtime-profiles/examples/production-quality.yaml#production-quality
  inputs:
    - id: portfolio-workspace
      path: portfolio/
  steps:
    - id: refresh-portfolio
      command: portfolio.refresh
    - id: localize-portfolio
      command: portfolio.localize
      languages:
        - fi
        - sv
    - id: explain-portfolio
      command: portfolio.explain
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
```

This release recipe describes a portfolio review workflow. When an executor
runs it, the expected flow is:

1. Validate the recipe against the ODPR schema and confirm it is a `Recipe`.
2. Treat the workflow as a `release` recipe, which means it is intended for a
   publication or release-review process rather than local drafting.
3. Use hosted execution through the configured runtime reference
   `runtime-profiles/examples/production-quality.yaml#production-quality`. The
   matching ODPR `RuntimeProfile` object describes the
   runtime profile, while raw credentials and live endpoint resolution stay in
   the executing SDK or platform.
4. Treat `portfolio/` as the shared portfolio workspace input.
5. Run `portfolio.refresh`.
6. Run `portfolio.localize` and produce Finnish and
   Swedish localized outputs.
7. Run `portfolio.explain` so reviewers get generated explanation material for
   the refreshed portfolio.
8. Require human review before the release workflow is considered complete.
