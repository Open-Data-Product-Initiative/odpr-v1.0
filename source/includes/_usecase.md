# UseCase

The `UseCase` object describes a business, operational, analytical, or policy use case that needs data products. It captures why data is needed, who needs it, what decision or process it supports, and what outcome is expected.

In ODPC, a use case is a demand-side portfolio object. It helps organizations understand where data products create value and which products support real business needs.

A `UseCase` can reference one or more data products through `productReferences`. It can also connect to business objectives and KPIs through catalog-level relationships or graph definitions. The object should remain focused on the use case itself, not on detailed relationship semantics. Relationship modeling belongs to ODPG.

By defining use cases as reusable catalog objects, ODPC enables discovery, prioritization, gap analysis, reuse analysis, and AI-assisted planning across data product portfolios.

## Attributes and options

> Example of UseCase object usage:

```yml
useCase:
  id: UC-001
  name:
    en: Predictive Maintenance for Aircraft Fleet
  description:
    en: Predict maintenance needs earlier by combining aircraft usage, schedules, and maintenance history.
  domain: aviation
  stakeholders:
    - Fleet Operations Manager
    - Maintenance Planning Team
    - Safety and Compliance Team
  decision:
    en: Schedule aircraft maintenance proactively based on usage patterns.
  expectedOutcome:
    en: Reduce maintenance costs and increase aircraft availability.
  dataNeeds:
    - flight schedules
    - aircraft usage
    - maintenance history
  productReferences:
    - DP-001
    - DP-002
    - DP-003
  status: active
  priority: high
  tags:
    - maintenance
    - aviation
    - operations
```

| Element | Type | Options | Description |
|---|---|---|---|
| **useCase** | object | required | Top-level object that describes a reusable data product use case. |
| **id** | string | required | Stable identifier for the use case. |
| **name** | object | language-tagged strings | Human-readable use case name. |
| **description** | object | language-tagged strings | Short explanation of the business or operational challenge. |
| **domain** | string | optional | Business, policy, or operational domain of the use case. |
| **stakeholders** | array of strings | optional | Roles, teams, or groups that benefit from or own the use case. |
| **decision** | object | language-tagged strings | Decision, process, or action the use case supports. |
| **expectedOutcome** | object | language-tagged strings | Business, operational, or policy outcome expected from the use case. |
| **dataNeeds** | array of strings | optional | Data needs expressed in business language. |
| **productReferences** | array of strings | optional | IDs of `ProductReference` objects expected to support the use case. |
| **status** | string | e.g., `proposed`, `active`, `at_risk`, `completed`, `cancelled` | Lifecycle status of the use case. |
| **priority** | string | e.g., `low`, `medium`, `high`, `critical` | Priority used for portfolio planning and backlog decisions. |
| **tags** | array of strings | optional | Keywords used for search, grouping, and AI-assisted analysis. |
