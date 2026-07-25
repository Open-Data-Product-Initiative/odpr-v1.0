# Terms used

ODPR uses the [Open Data Product Vocabulary, ODPV](https://opendataproducts.org/odpv-v1.0/), as the shared vocabulary for the OpenDataProducts.org standards family. Use ODPV for common terms, stable ids, labels, definitions, aliases, and relationship names across ODPS, ODPC, ODPG, ODPR, and related tools.

The terms below explain ODPR-specific usage where this specification gives a
shared vocabulary term a concrete recipe meaning or modeling constraint.

## Shared terms from ODPV

| Term | ODPR usage |
|---|---|
| Delivery flow | A composite ODPR flow for repeatable delivery work such as portfolio building, validation, localization, publishing, or release review. |
| Recipe | A supporting portable workflow unit used inside delivery flows and trigger-based flows. |
| Product Delivery Recipe | A recipe pattern or handoff agreement for delivering or changing one data product. In ODPR v1, the handoff manifest is the `DataProductRecipe` root object. |
| Data Product Recipe | A reviewable handoff artifact for delivery planning, readiness, validation, implementation guidance, AI-agent guidance, and review around one data product. |
| Trigger-based flow | A workflow made applicable by a declared graph change. |
| Workflow | A sequence of steps that creates, validates, reviews, localizes, publishes, or refreshes data product artifacts. |
| Step | One declared operation in a recipe. |
| Gate | A required validation, quality, publication, or review condition. |
| Context | The artifact or compact sidecar format used as prompt, review, or execution context. |
| RuntimeProfile | A supporting runtime generation configuration document that recipes can reference with `runtimeRef`. |
| Recipe catalog | Supporting metadata-only discovery list for available recipe files. |
| Review | A human or agent review expectation declared by the recipe. |
| Graph trigger | A small recipe trigger pattern that makes a normal ODPR Recipe applicable when an ODPG graph change matches. |

## ODPR-specific usage notes

| Term | Description |
|---|---|
| `Recipe` | Supporting ODPR object that declares one reusable workflow unit. |
| `RuntimeProfile` | Supporting ODPR object that declares SDK-compatible provider profile maps and generation defaults. |
| `RecipeCatalog` | Supporting ODPR object that lists recipe metadata and paths to full recipe files. |
| `DataProductRecipe` | The ODPR root object that indexes the reviewable handoff files for one Data Product Recipe. |
| `recipeRef` | Optional provenance or generation-context reference; not an implementation dependency for developers or AI agents. |
| `contract-plan` | Optional standardized section ID for a YAML data contract aligned with the Open Data Contract Standard. |
| `runtimeRef` | A URI-reference from a recipe to a RuntimeProfile document or provider profile fragment under `runtimeProfile.providers`. |
| `contextFormat.primary` | The preferred context serialization format for a recipe or step, such as `yaml`, `toon`, `gcf`, or `auto`. |
| `intent` | Human-authored reason and expected result for a recipe or step. |
| `instructions` | Human-authored working guidance for an agent or tool executing a recipe or step. |
| `iterationLimit` | Step-level maximum number of agent or LLM work passes allowed inside one step. |
| `exitWhen` | Human-authored stopping condition for bounded agent or LLM work inside one step. |
| `groundingTo` | Recipe-level list of graph node types, artifact types, or context categories that should ground agent-assisted work. |
| `trigger` | Optional Recipe field that declares which ODPG graph change can make the recipe applicable. |
| `graphContext` | Optional Recipe field that requests minimal ODPG context after a trigger match. |
| `execution.mode` | Runtime/provider class such as local, hosted, hybrid, or none; not SDK invocation mode. |
| `runPolicy` | Runtime guidance such as timeout or retry expectations. |
| `Extension property` | A local or implementation-specific field whose name begins with `x-`. |

ODPR should stay focused on workflow contracts. Product metadata belongs to
ODPS. Catalog and portfolio objects belong to ODPC. Graph structures and
relationships belong to ODPG. Shared vocabulary belongs to ODPV.
