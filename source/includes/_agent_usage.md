# AI Agent Usage Patterns

ODPR is designed to be usable by AI agents, SDKs, CI/CD systems, and automation
tools. From an agent perspective, ODPR provides four composite flow contracts:
delivery flows, product handoff flows, agent discovery flows, and trigger-based
flows driven by graph changes. Recipes, RuntimeProfile generation configs, and
recipe catalogs support those flows as building blocks.

ODPS defines one data product. ODPC defines catalogs and reusable portfolio
objects. ODPG defines relationships between data product artifacts. ODPV
provides shared vocabulary terms. ODPR defines delivery work, handoff
manifests, and trigger-based flows around those artifacts.

<!-- AI_AGENT_USAGE_PATTERNS:
Use ODPR for delivery flows, product handoff flows, agent discovery flows, and trigger-based flows; do not use it for defining the data product, catalog, graph, or vocabulary model itself.
Use runtimeRef as a URI-reference to a RuntimeProfile document or profile under runtimeProfile.providers; provider execution and credential resolution belong to the SDK, CI system, or platform executing the recipe.
Use RecipeCatalog only for metadata-only discovery; load and validate the referenced Recipe before execution.
Use DataProductRecipe as a handoff manifest for one data product; do not treat it as a workflow execution script.
Prefer declarative steps and gates over arbitrary shell scripts.
Use contextFormat.primary to decide whether YAML, TOON, GCF, or automatic fallback should be used as prompt or review context.
Use recipe and step intent to understand why the work exists and what result the human recipe designer expects.
Use step discoveryType as the standardized discovery purpose for agent discovery steps. Agent discovery steps use discoveryType instead of command.
Use instructions for how the agent or tool should work, and groundingTo for the controlled graph node and edge types that should ground agent-assisted work.
Use step iterationLimit and exitWhen to bound in-step agent or LLM refinement when they are declared.
Use recipe.trigger and recipe.graphContext for graph-triggered recipes; treat triggers as graph change patterns, not graph queries or bindings to one graph node id.
-->

## Agent capabilities enabled by ODPR

Agents can use ODPR to:

* discover safe workflow recipes before running SDK tools
* read a `DataProductRecipe` to understand mandatory handoff files, readiness,
  review state, and agent instructions
* use a `RecipeCatalog` to find complete recipe files
* explain what a recipe will do before execution
* validate recipe files against `odpr.yaml` or `odpr.json`
* select a development, CI, release, localization, hybrid, or agent recipe
* inspect whether a workflow expects local, hosted, hybrid, or no model execution
* run bounded agent discovery over declared context to produce grounded answers
* inspect graph-triggered recipes whose ODPG graph change patterns make the
  recipe applicable
* recognize standardized agent discovery step types such as affected use case
  discovery, impact explanation, gap/risk identification, and final findings
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
| Agent discovery | Investigate bounded declared context and produce a grounded answer, finding, impact explanation, or review recommendation. |
| Graph-triggered workflow | Match an ODPG graph change to an ODPR recipe trigger, prepare declared graph context, and run the recipe steps. |
| Agent handoff | Inspect recipe steps and gates before invoking SDK tools. |

## Agent behavior constraints

Agents using ODPR should keep boundaries clear:

* Do not treat ODPR as a data product definition; use ODPS for product metadata.
* Do not treat ODPR as a catalog object model; use ODPC for catalogs and
  portfolio objects.
* Do not treat ODPR as a graph model; use ODPG for nodes, edges, and
  relationships.
* Do not attach recipe logic to one graph node id by default; graph-triggered
  recipes should use declared graph change patterns.
* Do not embed secrets or API keys in recipes.
* Do not put dry-run responses, run manifests, provider readiness results,
  planned writes, write-scope checks, run ids, or logs in ODPR documents.
* Do not use bare provider names as `runtimeRef`; use a URI-reference to a
  RuntimeProfile document or profile and let the executing SDK, CI system, or platform
  resolve it.
* Do not silently skip required gates or human review requirements.

## Example prompts ODPR enables

* "Validate this ODPR recipe and suggest schema-compliant repairs."
* "Create a CI recipe that generates signal fragments and validates them."
* "Create a release recipe that refreshes, localizes, and explains a portfolio."
* "Create a graph-triggered recipe that reacts when any graph node status changes to production."
* "Explain which steps this recipe will run and whether human review is required."
* "Convert this local development workflow into a hosted production recipe."
