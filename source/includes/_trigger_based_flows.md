# Trigger-Based Flows

> Root shape example:

```yaml
schema: https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml
version: "1.0"
kind: Recipe
recipe:
  metadata:
    id: RCP-GRAPH-001
    name:
      en: Graph Triggered Impact Review
  version: "1.0.0"
  type: agent
  scope: graph
  intent: |
    Explain why the matched graph condition matters and what business result
    the review should support.
  instructions: |
    Use retrieved graph context only. Separate visible graph facts from missing
    context, and do not treat the traversal as business approval.
  groundingTo:
    nodeTypes:
      - DataProduct
      - UseCase
      - BusinessObjective
      - Owner
    edgeTypes:
      - uses
      - supports
      - enables
      - dependsOn
  trigger:
    source: odpg
    event: node.attributeChanged
    subject:
      nodeType: "*"
      attribute:
        name: status
        to: production
  graphContext:
    graphRef: graphs/portfolio.odpg.yaml
    start: trigger.subject
    depth: 2
  contextFormat:
    primary: gcf
    fallback:
      - yaml
      - toon
  steps:
    - id: explain-impact
      discoveryType: produce-findings-and-recommendations
      kind: graph
      input: generated/graph-context.gcf
      output: generated/graph-impact.md
      intent: |
        Explain the visible impact of the changed graph node.
      instructions: |
        Use the connected graph neighborhood to identify affected context,
        likely review concerns, and the next human decision.
      iterationLimit: 3
      exitWhen: |
        Stop when the generated result is ready for review or when another pass
        over the retrieved graph context does not add materially new grounding.
  review:
    required: true
```

Trigger-based flows are composite flows that become applicable when a graph
change matches a declared trigger. They use `Recipe` as the reusable workflow
unit, with `trigger` for the graph change and optional `graphContext` for the
graph context the steps need.

ODPG owns graph structure and state. The runtime owns observation, execution,
and run evidence. ODPR only declares the recipe contract.

### Trigger flow boundaries

A trigger-based flow SHOULD answer five practical questions:

- Which graph source is observed?
- Which graph change can make the flow applicable?
- Which node, edge, attribute, or named condition must match?
- Which graph context is needed after the match?
- Which delivery or review operations should run?

A trigger-based flow MUST NOT redefine ODPG graph structure, store observed
graph state, embed graph queries as workflow logic, bind ordinary flow logic to
one node id by default, or activate simply because a signal was observed. It
declares the boundary where a graph change should make action applicable.

### Trigger flow fields

| Element name | Type | Options | Description |
|---|---|---|---|
| `schema` | string | ODPR schema URI | URI of the ODPR schema used to validate the document. |
| `version` | string | ODPR specification version | Version of the ODPR specification used by the document. |
| `kind` | string | `Recipe` | ODPR root object type. Trigger-based flows are encoded as `Recipe` documents. |
| `recipe` | object | - | Top-level object that declares the trigger-based flow contract. |
| `recipe.metadata` | object | - | Stable trigger-based flow identity and name. |
| `recipe.metadata.id` | string | - | Stable trigger-based flow identifier. |
| `recipe.metadata.name` | object | localized text object | Human-readable trigger-based flow name. |
| `recipe.version` | string | semantic version | Version of this trigger-based flow artifact. This is separate from the top-level ODPR specification version. |
| `recipe.type` | string | `development`, `ci`, `release`, `agent`, `custom` | Flow intent. Trigger-based flows commonly use `agent` or `release`. |
| `recipe.scope` | string | `data-product`, `portfolio`, `graph`, `catalog`, `fragment`, `custom` | Artifact or graph area affected by the trigger-based flow. |
| `recipe.intent` | string | multiline text | Human-authored reason for the flow and result the review should support. |
| `recipe.instructions` | string | multiline text | Human-authored guidance for how an agent or tool should perform or interpret the flow. |
| `recipe.groundingTo` | object | node and edge type boundary | Controlled graph node and edge types that should ground agent-assisted work. |
| `recipe.trigger` | object | graph trigger object | Graph change boundary that can make the flow applicable. |
| `recipe.trigger.source` | string | `odpg` | Graph source observed by the runtime. |
| `recipe.trigger.event` | string | `node.added`, `node.removed`, `node.attributeChanged`, `edge.added`, `edge.removed`, `edge.attributeChanged`, `graph.conditionMatched` | Graph change category that can activate the flow. |
| `recipe.trigger.subject` | object | node or edge subject | Node, edge, endpoint, and attribute boundary that must match the observed graph change. |
| `recipe.trigger.subject.nodeType` | string | controlled node type, `*` | Node type boundary for node triggers. `*` allows any controlled node type. |
| `recipe.trigger.subject.edgeType` | string | controlled edge type | Relationship type boundary for edge triggers. |
| `recipe.trigger.subject.attribute.name` | string | explicit attribute name | Attribute that must change. Attribute names are not wildcards. |
| `recipe.trigger.subject.attribute.to` | string | target value | Target attribute value that makes action applicable. |
| `recipe.graphContext` | object | graph context request | Minimal ODPG context needed after a trigger matches. |
| `recipe.graphContext.graphRef` | string | graph file or graph reference | ODPG graph source used to materialize context. |
| `recipe.graphContext.start` | string | `trigger.subject`, graph reference | Starting point for context collection. |
| `recipe.graphContext.depth` | integer | positive integer | Default graph neighborhood depth requested after the trigger match. A graph-context step may override this with `step.depth`. |
| `recipe.contextFormat` | object | context format policy | Preferred serialization format for retrieved graph context, with optional fallback formats. |
| `recipe.steps` | array | ordered step objects | Ordered delivery, impact review, explanation, validation, or review operations that run after the trigger matches. |
| `step.iterationLimit` | integer | positive integer | Maximum number of agent or LLM work passes allowed inside the step. |
| `step.exitWhen` | string | multiline text | Human-authored stopping condition for bounded agent or LLM work inside the step. |
| `recipe.outputs` | array | output objects | Durable graph context, impact notes, reports, rendered artifacts, or review notes expected after the run. |
| `recipe.review.required` | boolean | `true`, `false` | Whether human review is required before accepting the trigger-based flow result. |

## Trigger flow model

A trigger-based flow declares when a graph change should make follow-up work
applicable. The trigger is the boundary: it names the observed graph source, the
change event, and the subject pattern that must match. The flow then declares
the graph context and operations needed after the match.

A trigger-based flow SHOULD make these field groups visible:

| Part | Purpose |
|---|---|
| `trigger.source` | Graph source observed by the runtime. In v1 this is `odpg`. |
| `trigger.event` | Graph change category, such as node added, edge removed, or attribute changed. |
| `trigger.subject` | Node or edge boundary that must match, including controlled node type, controlled edge type, endpoint pattern, and explicit attribute condition when needed. |
| `graphContext` | Minimal graph neighborhood or context artifact needed by the follow-up steps. |
| `intent`, `instructions`, `groundingTo` | Human-authored purpose, working guidance, and grounding boundary for agent-assisted interpretation. |
| `contextFormat` | Serialization policy for retrieved or generated context. |
| `steps` | Ordered delivery, impact review, explanation, validation, or review operations that should run after the trigger matches. |
| `outputs`, `gates`, `review` | Durable results and acceptance expectations for the triggered run. |

The runtime observes graph changes and decides whether they match the trigger.
ODPR declares the portable contract for that match and the work that follows.

## Trigger events

ODPR v1 supports graph-change triggers on nodes and edges. These events are
intentionally small so a trigger can be evaluated without turning ODPR into a
graph query language.

| Event | Use when | Required boundary |
|---|---|---|
| `node.added` | A new graph node appears and should cause delivery or review work. | `subject.nodeType`. |
| `node.removed` | A graph node is removed and impact should be reviewed or artifacts refreshed. | `subject.nodeType`. |
| `node.attributeChanged` | A node attribute crosses a declared boundary, such as `status` changing to `production`. | `subject.nodeType` and `subject.attribute.name`; the attribute condition SHOULD name `from`, `to`, or both when relevant. |
| `edge.added` | A new relationship appears and should cause downstream delivery or review work. | `subject.edgeType`; endpoint patterns SHOULD be declared when the flow depends on which node types are connected. |
| `edge.removed` | A relationship is removed and impact should be reviewed or artifacts refreshed. | `subject.edgeType`; endpoint patterns SHOULD be declared when relationship direction matters. |
| `edge.attributeChanged` | A relationship attribute crosses a declared boundary. | `subject.edgeType` and `subject.attribute.name`; the attribute condition SHOULD name `from`, `to`, or both when relevant. |
| `graph.conditionMatched` | A named graph condition becomes true and should make a flow applicable. | `condition.name`. |

`subject.nodeType` MAY be a controlled node type or `*`.
`subject.edgeType` MUST use a controlled edge type. Attribute names are not
wildcards; attribute-change triggers MUST name the attribute explicitly.

## Trigger patterns

Trigger-based flows are intended for graph changes that create a need for
action, not for every observation in the graph. A trigger SHOULD represent a
meaningful boundary such as:

| Pattern | Example use |
|---|---|
| New node | A data product, objective, signal, or policy node is added and related artifacts should be prepared or reviewed. |
| Removed node | A graph node is removed and dependent artifacts or reviews need impact analysis. |
| Node state transition | A data product, objective, signal, or other graph node changes status and review work should start. |
| New relationship | A dependency, ownership, enablement, or lineage edge is added and generated artifacts should be refreshed. |
| Removed relationship | A dependency or ownership edge is removed and impact notes should be generated. |
| Relationship state transition | An edge-level attribute changes and connected artifacts need validation or review. |
| Named graph condition | A graph-level condition such as objective enablement or portfolio readiness is detected by the runtime. |

The runtime decides whether an observed graph change matches the trigger and
when to execute the recipe. ODPR does not define scheduler behavior, event
delivery, retry policy, run logs, or approval records.

## Trigger flow examples

Canonical examples live in `/recipes/examples/`. They are complete ODPR files
that demonstrate trigger-based flow patterns without making this section a YAML
reference manual.

| Example | Demonstrates |
|---|---|
| [`graph-triggered-impact-review.yaml`](/recipes/examples/graph-triggered-impact-review.yaml) | A node attribute transition where any node type can match if `status` changes to `production`, graph context is collected, and impact notes require human review. |

### Trigger shape examples

The examples below show only the `recipe.trigger` shape. They are intended to
show matching boundaries, not complete runnable recipes.

Node added:

```yaml
trigger:
  source: odpg
  event: node.added
  subject:
    nodeType: DataProduct
```

Node state transition:

```yaml
trigger:
  source: odpg
  event: node.attributeChanged
  subject:
    nodeType: DataProduct
    attribute:
      name: status
      from: acceptance
      to: production
```

Edge added:

```yaml
trigger:
  source: odpg
  event: edge.added
  subject:
    edgeType: enables
    fromNodeType: DataProduct
    toNodeType: BusinessObjective
```

Edge removed:

```yaml
trigger:
  source: odpg
  event: edge.removed
  subject:
    edgeType: dependsOn
    fromNodeType: "*"
    toNodeType: DataProduct
```

Edge state transition:

```yaml
trigger:
  source: odpg
  event: edge.attributeChanged
  subject:
    edgeType: dependsOn
    attribute:
      name: status
      to: deprecated
```

Named graph condition:

```yaml
trigger:
  source: odpg
  event: graph.conditionMatched
  condition:
    name: business-objective-enabled
```
