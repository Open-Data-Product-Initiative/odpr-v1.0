# KPI

The `KPI` object defines a measurable indicator used to track business objectives, use case performance, catalog performance, or data product portfolio impact. It provides a reusable measurement object that can be referenced across ODPC catalogs.

In ODPC, KPIs create the measurement layer for portfolio management. They help organizations connect data product activity to expected outcomes and track progress using consistent definitions.

A `KPI` should describe what is measured, how it is measured, the target value, the desired direction of movement, and the measurement cadence. It can represent business-level KPIs, product-level KPIs, operational KPIs, or catalog-level KPIs.

By defining KPIs as reusable catalog objects, ODPC supports consistent reporting, objective tracking, AI-assisted analysis, and comparison across use cases, products, and business units.

## Attributes and options

> Example of KPI object usage:

```yml
kpi:
  id: KPI-001
  name:
    en: Average Emergency Response Time
  description:
    en: Average minutes from incident reporting to first responder arrival.
  type: business
  unit: minutes
  target: 5
  direction: at_most
  timeframe: by Q4 2026
  frequency: monthly
  calculation: average(first_responder_arrival_time - incident_report_time)
  owner:
    organization: Example Emergency Services Authority
    role: Performance Manager
  status: active
```

| Element | Type | Options | Description |
|---|---|---|---|
| **kpi** | object | required | Top-level object that defines a reusable key performance indicator. |
| **id** | string | required | Stable identifier for the KPI. |
| **name** | object | language-tagged strings | Human-readable KPI name. |
| **description** | object | language-tagged strings | Explanation of what the KPI measures. |
| **type** | string | e.g., `business`, `product`, `operational`, `catalog`, `quality` | KPI category used for analysis and reporting. |
| **unit** | string | e.g., `percentage`, `minutes`, `count`, `AED`, `score` | Unit of measurement. |
| **target** | number or string | optional | Target value or target expression. |
| **direction** | string | `increase`, `decrease`, `at_least`, `at_most`, `equals` | Desired movement or target condition. |
| **timeframe** | string | optional | Time period for reaching or evaluating the target. |
| **frequency** | string | e.g., `hourly`, `daily`, `weekly`, `monthly`, `quarterly` | Measurement cadence. |
| **calculation** | string | optional | Human-readable formula or measurement method. |
| **owner** | object | optional | Ownership information for KPI definition and reporting. |
| **organization** | string | optional | Organization responsible for KPI reporting. |
| **role** | string | optional | Responsible role, such as Performance Manager or Product Owner. |
| **status** | string | e.g., `draft`, `active`, `deprecated`, `retired` | Lifecycle status of the KPI definition. |
