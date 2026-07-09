# Recipe Library

ODPR publishes a small library of canonical recipes under
`/recipes/examples/`. These examples are not decorative snippets. They are
complete recipe files that can be copied, validated, adapted, and used by SDKs,
CI/CD systems, MCP servers, or other ODPR-aware platforms.

Agents and tools can also use `/recipes/recipes.jsonl` as a lightweight lookup
file for selecting the right recipe pattern before loading the full YAML
example.

Use `/recipes/catalog.yaml` when a tool needs metadata-only discovery of
available recipe files. Catalog entries point to complete recipes; they do not
embed step bodies or runtime output.

| Recipe | Use when | What happens |
|---|---|---|
| [`minimal.yaml`](/recipes/examples/minimal.yaml) | A developer wants the smallest valid local recipe for fast iteration. | The executor uses `runtime-profiles/examples/local-fast.yaml#local-fast`, runs one `generate` step for `signal` fragments, reads `source_docs/signals/`, writes draft fragments to `generated/fragments/`, and exposes that folder as `draft-fragments`. |
| [`ci-validate-generated-fragments.yaml`](/recipes/examples/ci-validate-generated-fragments.yaml) | CI must generate draft fragments and fail if the generated output is invalid. | The executor labels the run as `ci`, generates `signal` fragments, exposes `generated/fragments/` as `generated-fragments`, validates `generated/fragments/signal.yaml`, and enforces the required `fragments-valid` validation gate before the CI job can pass. |
| [`release-portfolio-review.yaml`](/recipes/examples/release-portfolio-review.yaml) | A release process must refresh, localize, explain, and review a portfolio before publication. | The executor uses `runtime-profiles/examples/production-quality.yaml#production-quality`, refreshes `portfolio/`, localizes it to Finnish and Swedish, generates an explanation, exposes localized pages and explanation output paths, and requires human review before publishing. |
| [`portfolio-localization.yaml`](/recipes/examples/portfolio-localization.yaml) | A portfolio workspace must be localized into configured target languages. | The executor uses `runtime-profiles/examples/production-quality.yaml#production-quality`, localizes `portfolio/` to Finnish and Swedish, exposes the localized HTML paths, and requires review. |
| [`hybrid-graph-review.yaml`](/recipes/examples/hybrid-graph-review.yaml) | A workflow should combine local graph work with hosted review or explanation. | The executor builds graph context locally with `runtime-profiles/examples/local-graph.yaml#local-graph`, exposes `generated/graph.yaml` as `graph-context`, then uses `runtime-profiles/examples/production-quality.yaml#production-quality` to generate review notes. |
| [`graph-triggered-impact-review.yaml`](/recipes/examples/graph-triggered-impact-review.yaml) | A graph change should activate a review recipe without binding the workflow to one node id. | The executor matches an ODPG node attribute transition, prepares declared graph context, materializes that context as GCF, then uses a hosted provider to generate impact notes for human review. |

The library is intentionally small. Each example should demonstrate a distinct
workflow pattern rather than every possible command option. Local organizations
can extend these recipes with `x-` fields or implementation-specific command
bindings without changing ODPR semantics.

ODPR also publishes RuntimeProfile examples under `/runtime-profiles/examples/`. Use these
when a recipe references a provider profile with a URI-reference such as
`runtime-profiles/examples/local-fast.yaml#local-fast`.

| RuntimeProfile | Use when | What it standardizes |
|---|---|---|
| [`local-fast.yaml`](/runtime-profiles/examples/local-fast.yaml) | Local development should use a fast local model profile. | `runtimeRef: runtime-profiles/examples/local-fast.yaml#local-fast` resolves to an Ollama-backed `runtimeProfile.providers.local-fast` profile. |
| [`local-graph.yaml`](/runtime-profiles/examples/local-graph.yaml) | Graph-building steps should run locally without hosted model routing. | `runtimeRef: runtime-profiles/examples/local-graph.yaml#local-graph` resolves to a local OpenAI-compatible `runtimeProfile.providers.local-graph` profile. |
| [`production-quality.yaml`](/runtime-profiles/examples/production-quality.yaml) | Release, CI, or agent workflows need a hosted production-grade model profile. | `runtimeRef: runtime-profiles/examples/production-quality.yaml#production-quality` resolves to an OpenAI `runtimeProfile.providers.production-quality` profile with `gpt-4.1` and `apiKeyEnv`. |
| [`internal-secure.yaml`](/runtime-profiles/examples/internal-secure.yaml) | Enterprise workflows must route model calls through an approved internal gateway. | `runtimeRef: runtime-profiles/examples/internal-secure.yaml#internal-secure` resolves to an OpenAI-compatible gateway profile with `apiKeyEnv` instead of raw secrets. |
