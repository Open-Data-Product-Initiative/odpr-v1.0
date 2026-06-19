# Terms used

ODPR uses the [Open Data Product Vocabulary, ODPV](https://opendataproducts.org/odpv-v1.0/), as the shared vocabulary for the OpenDataProducts.org standards family. Use ODPV for common terms, stable ids, labels, definitions, aliases, and relationship names across ODPS, ODPC, ODPG, ODPR, and related tools.

The terms below explain ODPR-specific usage where this specification gives a
shared vocabulary term a concrete recipe meaning or modeling constraint.

## Shared terms from ODPV

| Term | ODPR usage |
|---|---|
| Recipe | A portable, declarative workflow contract for repeatable data product work. |
| Workflow | A sequence of steps that creates, validates, reviews, localizes, publishes, or refreshes data product artifacts. |
| Step | One declared operation in a recipe. |
| Gate | A required validation, quality, publication, or review condition. |
| Context | The artifact or compact sidecar format used as prompt, review, or execution context. |
| Provider | A named ODPR runtime profile that recipes can reference with `providerRef`. |
| Recipe catalog | Metadata-only discovery list for available recipe files. |
| Review | A human or agent review expectation declared by the recipe. |

## ODPR-specific usage notes

| Term | Description |
|---|---|
| `Recipe` | The ODPR root object that declares one repeatable data product workflow. |
| `Provider` | The ODPR root object that declares one named provider profile. |
| `RecipeCatalog` | The ODPR root object that lists recipe metadata and paths to full recipe files. |
| `providerRef` | A reference from a recipe to `Provider.provider.id`. |
| `context.format` | The preferred context format for a recipe, such as `yaml`, `toon`, `gcf`, or `auto`. |
| `execution.mode` | Runtime/provider class such as local, hosted, hybrid, or none; not SDK invocation mode. |
| `runPolicy` | Runtime guidance such as timeout or retry expectations. |
| `Extension property` | A local or implementation-specific field whose name begins with `x-`. |

ODPR should stay focused on workflow contracts. Product metadata belongs to
ODPS. Catalog and portfolio objects belong to ODPC. Graph structures and
relationships belong to ODPG. Shared vocabulary belongs to ODPV.
