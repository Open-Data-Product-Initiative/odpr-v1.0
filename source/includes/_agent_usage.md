# AI Agent Usage Patterns

ODPR is designed to be usable by AI agents, SDKs, CI/CD systems, and automation
tools. From an agent perspective, ODPR provides an inspectable workflow contract
before an action is run: it names the workflow, lists the steps, declares the
execution mode, points to context policy, and describes gates or review
expectations.

ODPS defines one data product. ODPC defines catalogs and reusable portfolio
objects. ODPG defines relationships between data product artifacts. ODPV
provides shared vocabulary terms. ODPR defines repeatable workflows around
those artifacts.

<!-- AI_AGENT_USAGE_PATTERNS:
Use ODPR for repeatable workflow recipes, not for defining the data product, catalog, graph, or vocabulary itself.
Use providerRef as an execution reference only; provider configuration belongs to the SDK, CI system, or platform executing the recipe.
Use RecipeCatalog only for metadata-only discovery; load and validate the referenced Recipe before execution.
Prefer declarative steps and gates over arbitrary shell scripts.
Use context.format to decide whether YAML, TOON, GCF, or automatic fallback should be used as prompt or review context.
-->

## Agent capabilities enabled by ODPR

Agents can use ODPR to:

* discover safe workflow recipes before running SDK tools
* use a `RecipeCatalog` to find complete recipe files
* explain what a recipe will do before execution
* validate recipe files against `odpr.yaml` or `odpr.json`
* select a development, CI, release, localization, hybrid, or agent recipe
* inspect whether a workflow expects local, hosted, hybrid, or no model execution
* follow declared gates and review requirements
* reuse a recipe in CI/CD or production automation
* preserve stable workflow intent while model providers vary by environment

## Common agent workflows

| Workflow | Agent behavior |
|---|---|
| Recipe validation | Validate ODPR recipe files and report schema-compliant repairs. |
| Recipe selection | Choose a recipe based on task type, execution mode, context format, or required review. |
| CI/CD preparation | Convert a repeatable SDK command sequence into a declared recipe. |
| Local development | Run draft recipes that use local providers for fast iteration. |
| Production review | Run release recipes that use hosted providers, validation gates, and review expectations. |
| Hybrid execution | Combine local generation or graph inference with hosted review or localization. |
| Agent handoff | Inspect recipe steps and gates before invoking SDK tools. |

## Agent behavior constraints

Agents using ODPR should keep boundaries clear:

* Do not treat ODPR as a data product definition; use ODPS for product metadata.
* Do not treat ODPR as a catalog object model; use ODPC for catalogs and
  portfolio objects.
* Do not treat ODPR as a graph model; use ODPG for nodes, edges, and
  relationships.
* Do not embed secrets or API keys in recipes.
* Do not put dry-run responses, run manifests, provider readiness results,
  planned writes, write-scope checks, run ids, or logs in ODPR documents.
* Do not assume `providerRef` is globally meaningful; it must be resolved by the
  executing SDK, CI system, or platform.
* Do not silently skip required gates or human review requirements.

## Example prompts ODPR enables

* "Validate this ODPR recipe and suggest schema-compliant repairs."
* "Create a CI recipe that generates signal fragments and validates them."
* "Create a release recipe that refreshes, localizes, and explains a portfolio."
* "Explain which steps this recipe will run and whether human review is required."
* "Convert this local development workflow into a hosted production recipe."
