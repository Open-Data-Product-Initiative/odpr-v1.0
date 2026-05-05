# Catalog

The `Catalog` object defines a managed collection of ODPC portfolio objects. It provides the container for product references, use cases, business objectives, KPIs, signals, and catalog items.

In ODPC, a catalog is the portfolio-level structure that allows organizations to organize, publish, govern, and exchange reusable catalog objects. A catalog may represent an enterprise data product catalog, a government portfolio catalog, a domain catalog, a marketplace catalog, or a project-specific catalog.

A `Catalog` should provide identity, ownership, scope, lifecycle status, and references to the objects included in the catalog. The catalog does not define relationship semantics between the objects. That belongs to ODPG.

By defining catalogs as machine-readable objects, ODPC supports interoperability between tools, platforms, marketplaces, AI workflows, and graph-based portfolio analysis.

## Attributes and options

> Example of Catalog object usage:

```yml
catalog:
  id: CAT-001
  name:
    en: Smart City Data Product Portfolio Catalog
  description:
    en: Catalog of reusable data product portfolio objects for smart city planning and operations.
  owner:
    organization: Example Smart City Office
    role: Data Product Portfolio Manager
  scope:
    domain: smart-city
    geography: Example City
    audience:
      - internal
      - partner
  version: 1.0.0
  status: active
  catalogItems:
    - CI-001
    - CI-002
    - CI-003
  tags:
    - smart-city
    - portfolio
    - data-products
```

| Element | Type | Options | Description |
|---|---|---|---|
| **catalog** | object | required | Top-level object that defines an ODPC catalog. |
| **id** | string | required | Stable identifier for the catalog. |
| **name** | object | language-tagged strings | Human-readable catalog name. |
| **description** | object | language-tagged strings | Short explanation of the catalog purpose and scope. |
| **owner** | object | optional | Ownership information for the catalog. |
| **organization** | string | optional | Organization responsible for the catalog. |
| **role** | string | optional | Responsible role, such as Data Product Portfolio Manager. |
| **scope** | object | optional | Defines the business, organizational, geographic, or audience scope of the catalog. |
| **domain** | string | optional | Domain covered by the catalog. |
| **geography** | string | optional | Geographic scope of the catalog, if relevant. |
| **audience** | array of strings | e.g., `internal`, `partner`, `public`, `commercial` | Intended audience for catalog use. |
| **version** | string | optional | Catalog version. |
| **status** | string | e.g., `draft`, `active`, `deprecated`, `retired` | Lifecycle status of the catalog. |
| **catalogItems** | array of strings | optional | IDs of `CatalogItem` objects included in the catalog. |
| **tags** | array of strings | optional | Keywords used for search, grouping, and portfolio analysis. |
