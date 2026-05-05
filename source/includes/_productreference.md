# ProductReference

The `ProductReference` object connects an ODPC catalog to the actual source definition of a data product. It does not redefine the full data product. It provides a stable catalog-level reference to a product described in ODPS, DPDS, an internal enterprise template, a vendor catalog, a marketplace definition, or another metadata source.

`ProductReference` is the bridge between the portfolio layer and the product definition layer. It allows catalogs, use cases, objectives, KPIs, and signals to point to data products without copying the full product metadata into ODPC.

A `ProductReference` should include enough information for discovery, ownership, lifecycle visibility, and system integration. The complete product details remain in the source model referenced by `uri`, `identifier`, or another system-specific reference.

By separating the catalog reference from the source product definition, ODPC supports mixed data product environments where products may be described using different standards, platforms, and internal models.

## Attributes and options

> Example of ProductReference object usage:

```yml
productReference:
  id: DP-001
  name:
    en: UrbanPulse Events Data Product
  description:
    en: Data product providing event information for urban analytics and citizen services.
  domain: smart-city
  owner:
    organization: Example Organization
    role: Data Product Owner
  productModel:
    standard: ODPS
    version: 4.1
    format: yaml
  uri: https://example.org/products/urbanpulse-events/odps.yaml
  status: active
  tags:
    - events
    - smart-city
    - mobility
```

| Element | Type | Options | Description |
|---|---|---|---|
| **productReference** | object | required | Top-level object that references a data product from an ODPC catalog. |
| **id** | string | required | Stable catalog-level identifier for the referenced data product. |
| **name** | object | language-tagged strings | Human-readable product name used in catalog views and portfolio analysis. |
| **description** | object | language-tagged strings | Short summary of the referenced data product. |
| **domain** | string | optional | Business, policy, or operational domain of the product. |
| **owner** | object | optional | Ownership information for the referenced product. |
| **organization** | string | optional | Organization responsible for the data product. |
| **role** | string | optional | Responsible role, such as Data Product Owner or Product Manager. |
| **productModel** | object | required | Describes the source product definition model. |
| **standard** | string | e.g., `ODPS`, `DPDS`, `internal`, `vendor`, `marketplace` | Standard or model used by the source product definition. |
| **version** | string | optional | Version of the source product model. |
| **format** | string | e.g., `yaml`, `json`, `api`, `html` | Format of the source product definition. |
| **uri** | string | URI | Link to the source product definition, product page, API endpoint, or repository location. |
| **status** | string | e.g., `planned`, `active`, `deprecated`, `retired` | Lifecycle status of the referenced product in the catalog. |
| **tags** | array of strings | optional | Keywords used for filtering, search, grouping, and AI-assisted portfolio analysis. |
