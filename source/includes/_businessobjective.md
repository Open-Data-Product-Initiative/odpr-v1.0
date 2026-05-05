# BusinessObjective

The `BusinessObjective` object defines a higher-level business, operational, policy, or strategic objective that data products and use cases contribute to. It captures the outcome the organization wants to achieve and provides the portfolio-level anchor for value management.

In ODPC, business objectives help move data product management from asset lists to outcome-driven portfolios. They make it possible to understand which data products support strategic goals, which use cases contribute to measurable outcomes, and where gaps exist.

A `BusinessObjective` can be measured by one or more KPIs. It can also be referenced by use cases, catalog items, or graph relationships. The objective should remain reusable and stable across products and use cases.

By defining objectives as catalog objects, ODPC supports prioritization, investment decisions, governance reviews, AI-assisted portfolio analysis, and reporting on business value.

## Attributes and options

> Example of BusinessObjective object usage:

```yml
businessObjective:
  id: BO-001
  name:
    en: Improve Urban Mobility Efficiency
  description:
    en: Reduce travel delays and improve movement across the city through better data-driven planning and operations.
  strategicAlignment:
    - en: Smart City Vision 2030
    - en: Transport Digital Transformation Program
  owner:
    organization: Example Transport Authority
    role: Strategy Lead
  kpis:
    - KPI-001
    - KPI-002
  timeframe:
    startDate: 2026-01-01
    endDate: 2026-12-31
  status: active
  priority: high
```

| Element | Type | Options | Description |
|---|---|---|---|
| **businessObjective** | object | required | Top-level object that describes a reusable business objective. |
| **id** | string | required | Stable identifier for the business objective. |
| **name** | object | language-tagged strings | Human-readable objective name. |
| **description** | object | language-tagged strings | Natural-language explanation of the intended outcome. |
| **strategicAlignment** | array of objects | language-tagged strings | Strategies, programs, policies, or plans the objective supports. |
| **owner** | object | optional | Ownership information for the objective. |
| **organization** | string | optional | Organization responsible for the objective. |
| **role** | string | optional | Responsible role, such as Strategy Lead or Business Owner. |
| **kpis** | array of strings | optional | IDs of KPI objects used to measure progress toward the objective. |
| **timeframe** | object | optional | Start and end dates for the objective. |
| **startDate** | string | ISO 8601 date (YYYY-MM-DD) | Date when the objective becomes active. |
| **endDate** | string | ISO 8601 date (YYYY-MM-DD) | Date when the objective ends or is planned to end. |
| **status** | string | e.g., `planned`, `active`, `at_risk`, `achieved`, `cancelled`, `expired` | Lifecycle status of the business objective. |
| **priority** | string | e.g., `low`, `medium`, `high`, `critical` | Priority used for portfolio and investment decisions. |
