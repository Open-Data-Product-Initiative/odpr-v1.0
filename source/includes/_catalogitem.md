# CatalogItem

The `CatalogItem` object defines an entry inside an ODPC catalog. It provides a common wrapper for reusable catalog objects such as product references, use cases, business objectives, KPIs, and signals.

In ODPC, catalog items make catalogs easier to manage, publish, filter, and govern. They allow different object types to be included in one catalog while preserving object-specific definitions separately.

A `CatalogItem` should identify the referenced object, describe its item type, provide catalog-level metadata, and support lifecycle, ownership, visibility, and priority management. It should not duplicate the full referenced object.

By defining catalog items as reusable wrappers, ODPC supports marketplace-style catalogs, enterprise catalogs, domain catalogs, AI-assisted catalog maintenance, and graph-based portfolio views.

## Attributes and options

> Example of CatalogItem object usage:

```yml
catalogItem:
  id: CI-001
  itemType: productReference
  ref: DP-001
  title:
    en: UrbanPulse Events Data Product
  summary:
    en: Catalog entry for a smart city events data product used in mobility and citizen service use cases.
  visibility: internal
  status: active
  priority: high
  owner:
    organization: Example Smart City Office
    role: Catalog Manager
  listedAt: 2026-01-15T08:00:00Z
  updatedAt: 2026-04-20T10:30:00Z
  tags:
    - events
    - mobility
    - smart-city
```

| Element | Type | Options | Description |
|---|---|---|---|
| **catalogItem** | object | required | Top-level object that defines an entry in an ODPC catalog. |
| **id** | string | required | Stable identifier for the catalog item. |
| **itemType** | string | `productReference`, `useCase`, `businessObjective`, `kpi`, `signal` | Type of catalog object referenced by the item. |
| **ref** | string | required | ID of the referenced ODPC object. |
| **title** | object | language-tagged strings | Catalog-level title for the item. |
| **summary** | object | language-tagged strings | Short catalog-level summary used in listings and previews. |
| **visibility** | string | e.g., `internal`, `partner`, `public`, `restricted`, `commercial` | Intended visibility of the catalog item. |
| **status** | string | e.g., `draft`, `active`, `hidden`, `deprecated`, `retired` | Lifecycle status of the catalog item. |
| **priority** | string | e.g., `low`, `medium`, `high`, `critical` | Priority used for catalog management and portfolio planning. |
| **owner** | object | optional | Ownership information for the catalog item. |
| **organization** | string | optional | Organization responsible for the catalog item. |
| **role** | string | optional | Responsible role, such as Catalog Manager. |
| **listedAt** | string | ISO 8601 datetime | Date and time when the item was first listed. |
| **updatedAt** | string | ISO 8601 datetime | Date and time when the item was last updated. |
| **tags** | array of strings | optional | Keywords used for search, grouping, filtering, and AI-assisted analysis. |
