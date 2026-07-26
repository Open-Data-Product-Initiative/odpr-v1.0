# Agent Discovery Flows

> Root shape example:

```yaml
schema: https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml
version: "1.0"
kind: Recipe
recipe:
  metadata:
    id: RCP-DISCOVERY-001
    name:
      en: High-Value Customer Inactivity Discovery
  version: "1.0.0"
  type: agent
  scope: graph
  intent: |
    Explain why the matched high-value customer inactivity condition matters
    and what business review result the discovery should support.
  instructions: |
    Investigate bounded graph context only. Find visible evidence, affected
    use cases, owner context, objective impact, and the next human review
    decision. Do not add facts outside retrieved context.
  groundingTo:
    nodeTypes:
      - Condition
      - DataProduct
      - UseCase
      - BusinessObjective
      - Owner
    edgeTypes:
      - uses
      - supports
      - enables
      - dependsOn
  graphContext:
    startNodeId: nd_7f3a9c2e4b8d
    depth: 2
  contextFormat:
    primary: gcf
    fallback:
      - yaml
      - toon
  steps:
    - id: step-1
      discoveryType: find-affected-use-cases
      output: generated/discovery/affected-use-cases.md
      intent: |
        Find use cases affected by the matched inactivity condition.
      instructions: |
        Starting from the graph node identified by `graphContext.startNodeId`,
        inspect the bounded graph context that fits `groundingTo` and
        `graphContext.depth`. Preserve visible evidence that explains why the
        condition matters.
    - id: step-2
      discoveryType: identify-gaps-and-risks
      output: generated/discovery/gaps-and-risks.md
      intent: |
        Identify missing graph evidence, unresolved ownership, and dependency
        risks that affect the review.
      instructions: |
        Review the evidence found by previous discovery steps and the bounded
        graph context. Identify gaps, risks, and missing context that a human
        reviewer must resolve before accepting the findings.
    - id: step-3
      discoveryType: produce-findings-and-recommendations
      output: generated/discovery/high-value-customer-inactivity-answer.md
      intent: |
        Produce the final grounded summary and recommended human actions by
        synthesizing the evidence collected by previous discovery steps in this
        recipe.
      instructions: |
        Review the outputs and evidence produced by earlier discovery steps in
        this recipe. Explain affected use cases, evidence products, owner
        context, objective impact, gaps, risks, and the next human review
        action. Use only visible collected evidence and separate visible facts
        from missing context.
      iterationLimit: 3
      exitWhen: |
        Stop when the final findings are ready for review or when another pass
        over the collected evidence from previous discovery steps does not add
        materially new grounding.
  review:
    required: true
```

Agent discovery flows declare how an AI agent investigates bounded data product,
catalog, graph, or portfolio context to produce grounded answers, findings,
impact explanations, or review recommendations.

The workflow path remains deterministic: the recipe declares the graph context
boundary, ordered steps, outputs, gates, and review expectations. The agent gets
controlled freedom inside agent-assisted steps through human-authored `intent`,
`instructions`, `groundingTo`, `iterationLimit`, and `exitWhen`.

Agent discovery flows are guided step flows. The recipe declares the
deterministic path, context boundaries, grounding boundary, outputs, gates, and
review. Inside an agent-assisted step, an implementation may use iterative agent
techniques, including repeated inspection or refinement, but it must stay within
the declared instructions, `groundingTo` boundary, `iterationLimit`, and
`exitWhen` condition.

### Discovery flow boundaries

An agent discovery flow SHOULD answer six practical questions:

- What question, condition, or concern should the agent investigate?
- Which bounded context may the agent inspect?
- What kinds of evidence should ground the answer?
- Which ordered retrieval, inspection, explanation, or review steps run?
- When should bounded in-step investigation stop?
- Which answer, finding, or review recommendation should be produced?

An agent discovery flow MUST NOT define open-ended autonomous agents, hidden
prompts, chain-of-thought disclosure, persistent memory stores, unbounded tool
loops, runtime traces, or implementation-specific agent internals. It declares a
portable investigation contract, not an agent runtime.

### Discovery flow fields

| Element name | Type | Options | Description |
|---|---|---|---|
| `schema` | string | ODPR schema URI | URI of the ODPR schema used to validate the document. |
| `version` | string | ODPR specification version | Version of the ODPR specification used by the document. |
| `kind` | string | `Recipe` | ODPR root object type. Agent discovery flows are encoded as `Recipe` documents. |
| `recipe` | object | - | Top-level object that declares the discovery flow contract. |
| `recipe.metadata` | object | - | Stable discovery flow identity and name. |
| `recipe.version` | string | semantic version | Version of this discovery flow artifact. This is separate from the top-level ODPR specification version. |
| `recipe.type` | string | commonly `agent` | Discovery flows commonly use `agent` because the flow exists for agent-assisted investigation. |
| `recipe.scope` | string | `data-product`, `portfolio`, `graph`, `catalog` | Standards-family context being investigated. |
| `recipe.intent` | string | multiline text | Human-authored reason for the discovery and the result the investigation should support. |
| `recipe.instructions` | string | multiline text | Human-authored guidance for how the agent or tool should investigate and interpret the context. |
| `recipe.groundingTo` | object | node and edge type boundary | Controlled graph node and edge types that should ground the agent's answer. |
| `recipe.graphContext` | object | graph context request | Bounded graph context request for graph-scoped discovery flows. For human-initiated discovery, `startNodeId` is the opaque id of the starting graph node selected before the run, and `depth` limits neighborhood expansion. |
| `recipe.contextFormat` | object | context format policy | Preferred serialization format for retrieved context. |
| `recipe.steps` | array | ordered step objects | Ordered retrieval, inspection, explanation, validation, or review tasks. |
| `step.id` | string | stable local identifier | Stable identifier for this step instance inside the recipe. It does not need to duplicate `discoveryType`. |
| `step.discoveryType` | enum string | `find-affected-use-cases`<br>`explain-use-case-impact`<br>`find-affected-data-products`<br>`explain-data-product-impact`<br>`find-affected-objectives`<br>`explain-objective-impact`<br>`identify-gaps-and-risks`<br>`produce-findings-and-recommendations` | Standardized discovery purpose fulfilled by the step. It tells tools and reviewers what kind of answer the step is trying to produce. |
| `step.intent` | string | multiline text | Human-authored reason for the step and the result the step should support. |
| `step.instructions` | string | multiline text | Human-authored guidance for how the agent or tool should work inside the step. |
| `step.iterationLimit` | integer | positive integer | Maximum number of agent or LLM work passes allowed inside the step. |
| `step.exitWhen` | string | multiline text | Human-authored stopping condition for bounded agent or LLM work inside the step. |
| `recipe.outputs` | array | output objects | Durable answers, findings, context files, or review notes expected after the run. |
| `recipe.gates` | array | gate objects | Grounding, quality, validation, or review conditions. |
| `recipe.review.required` | boolean | `true`, `false` | Whether human review is required before accepting the discovery result. |

## Discovery flow model

Agent discovery flows are useful when the task is not mainly to create or
publish an artifact, but to investigate declared context and answer a question.
They can be human-initiated, trigger-initiated, or embedded in a larger delivery
workflow.

Every agent discovery flow SHOULD make these parts visible:

| Part | Purpose |
|---|---|
| Discovery intent | The question, condition, or concern being investigated and the expected answer or review result. |
| Grounding boundary | The graph node types and edge types that may ground the answer. |
| Retrieval path | Deterministic steps that inspect or materialize bounded context from the declared starting node and graph limits. |
| Agent instructions | Human-authored instructions for interpreting context and producing findings. |
| Bounded iteration | Step-level `iterationLimit` and `exitWhen` controls that stop in-step agent or LLM refinement. |
| Durable result | The answer, finding, impact explanation, or review recommendation produced from the collected discovery evidence. |
| Review | Human or agent review expectations before the result is accepted or reused. |

### Discovery step types

Agent discovery steps declare `discoveryType` instead of `command`. The value
standardizes the kind of discovery work the step performs without replacing
`intent`, `instructions`, inputs, outputs, gates, or review policy.

| Value | Purpose |
|---|---|
| `find-affected-use-cases` | Find use cases affected by the condition, change, product, relationship, or previous finding. |
| `explain-use-case-impact` | Explain how identified use cases are affected. |
| `find-affected-data-products` | Find data products affected by the condition, change, use case, relationship, or previous finding. |
| `explain-data-product-impact` | Explain how identified data products are affected. |
| `find-affected-objectives` | Find business objectives or KPIs affected by the condition, change, product, use case, or previous finding. |
| `explain-objective-impact` | Explain how identified objectives or KPIs are affected. |
| `identify-gaps-and-risks` | Identify missing evidence, weak context, unresolved ownership, governance gaps, dependency risks, or conflicting relationships. |
| `produce-findings-and-recommendations` | Produce final grounded findings and recommended human actions from the collected discovery evidence. |

Agent discovery flows can use graph triggers, but they are not the same as
trigger-based flows. A trigger-based flow declares when work becomes applicable.
An agent discovery flow declares how an AI agent investigates bounded context
and produces a grounded result.
