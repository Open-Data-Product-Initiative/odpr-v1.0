# Signal

The `Signal` object captures demand, risk, opportunity, quality, usage, feedback, or change signals related to a data product portfolio. Signals help organizations detect what needs attention and support portfolio decisions with evidence.

In ODPC, signals are reusable observation objects. They can indicate demand for a new product, increased use of an existing product, quality issues, policy changes, operational risks, stakeholder feedback, or market opportunities.

A `Signal` should describe what was observed, where it came from, how strong it is, and which catalog objects it may relate to. It should not define the full relationship graph. Relationship semantics belong to ODPG.

By defining signals as catalog objects, ODPC supports AI-assisted planning, backlog creation, governance monitoring, product improvement, and portfolio-level sensing.

## Attributes and options

> Example of Signal object usage:

```yml
signal:
  id: SIG-001
  name:
    en: Increased demand for real-time event data
  description:
    en: Multiple use case requests indicate demand for more frequent event data updates.
  type: demand
  source:
    system: Open Data Portal
    channel: search_queries
    reference: search-log-2026-04
  strength: high
  confidence: medium
  observedAt: 2026-04-18T09:30:00Z
  relatedObjects:
    productReferences:
      - DP-001
    useCases:
      - UC-001
    businessObjectives:
      - BO-001
  status: new
  recommendedAction:
    en: Review update frequency and assess feasibility of near real-time publication.
```

| Element | Type | Options | Description |
|---|---|---|---|
| **signal** | object | required | Top-level object that captures a reusable portfolio signal. |
| **id** | string | required | Stable identifier for the signal. |
| **name** | object | language-tagged strings | Human-readable signal name. |
| **description** | object | language-tagged strings | Explanation of the observation and why it matters. |
| **type** | string | e.g., `demand`, `risk`, `opportunity`, `quality`, `usage`, `feedback`, `change` | Signal category used for filtering and analysis. |
| **source** | object | optional | Source of the signal. |
| **system** | string | optional | System or platform where the signal was observed. |
| **channel** | string | optional | Channel, process, or data source that produced the signal. |
| **reference** | string | optional | Source reference, log identifier, ticket ID, document ID, or URL. |
| **strength** | string | e.g., `low`, `medium`, `high`, `critical` | Relative strength or urgency of the signal. |
| **confidence** | string | e.g., `low`, `medium`, `high` | Confidence level in the signal interpretation. |
| **observedAt** | string | ISO 8601 datetime | Time when the signal was observed. |
| **relatedObjects** | object | optional | Catalog object IDs that may be relevant to the signal. |
| **productReferences** | array of strings | optional | Related `ProductReference` IDs. |
| **useCases** | array of strings | optional | Related `UseCase` IDs. |
| **businessObjectives** | array of strings | optional | Related `BusinessObjective` IDs. |
| **status** | string | e.g., `new`, `reviewing`, `accepted`, `dismissed`, `resolved` | Lifecycle status of the signal. |
| **recommendedAction** | object | language-tagged strings | Suggested next action based on the signal. |
