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
| [`minimal.yaml`](/recipes/examples/minimal.yaml) | A developer wants the smallest valid local recipe for fast iteration. | The executor labels the run as `development`, prepares the local provider `local-fast`, runs one `generate` step for `signal` fragments, reads `source_docs/signals/`, writes draft fragments to `generated/fragments/`, and exposes that folder as `draft-fragments`. |
| [`ci-validate-generated-fragments.yaml`](/recipes/examples/ci-validate-generated-fragments.yaml) | CI must generate draft fragments and fail if the generated output is invalid. | The executor labels the run as `ci`, generates `signal` fragments, exposes `generated/fragments/` as `generated-fragments`, validates `generated/fragments/signal.yaml`, and enforces the required `fragments-valid` validation gate before the CI job can pass. |
| [`release-portfolio-review.yaml`](/recipes/examples/release-portfolio-review.yaml) | A release process must refresh, localize, explain, and review a portfolio before publication. | The executor labels the run as `production`, uses a hosted `production-quality` provider, refreshes `portfolio/`, localizes it to Finnish and Swedish, generates an explanation, exposes localized pages and explanation output paths, applies a release timeout, and requires human review before publishing. |
| [`portfolio-localization.yaml`](/recipes/examples/portfolio-localization.yaml) | A portfolio workspace must be localized into configured target languages. | The executor uses the hosted `production-quality` provider, localizes `portfolio/` to Finnish and Swedish using a YAML language list, exposes the localized HTML paths, and requires release-owner review. |
| [`hybrid-graph-review.yaml`](/recipes/examples/hybrid-graph-review.yaml) | A workflow should combine local graph work with hosted review or explanation. | The executor labels the run as `staging`, builds graph context locally from `generated/fragments/`, exposes `generated/graph.yaml` as `graph-context`, then uses a hosted `production-quality` provider to explain the portfolio, with both automated and human review expected. |

The library is intentionally small. Each example should demonstrate a distinct
workflow pattern rather than every possible command option. Local organizations
can extend these recipes with `x-` fields or implementation-specific command
bindings without changing ODPR semantics.

ODPR also publishes Provider examples under `/providers/examples/`. Use these
when a recipe references a provider profile such as `local-fast`,
`local-graph`, `production-quality`, or `internal-secure`.

| Provider | Use when | What it standardizes |
|---|---|---|
| [`local-fast.yaml`](/providers/examples/local-fast.yaml) | Local development should use a fast local model profile. | `providerRef: local-fast` resolves to an Ollama-backed local provider profile with a development environment label and low temperature. |
| [`local-graph.yaml`](/providers/examples/local-graph.yaml) | Graph-building steps should run locally without hosted model routing. | `providerRef: local-graph` resolves to a local graph-building provider profile with a deterministic temperature. |
| [`production-quality.yaml`](/providers/examples/production-quality.yaml) | Release, CI, or agent workflows need a hosted production-grade model profile. | `providerRef: production-quality` resolves to an OpenAI hosted provider profile with `gpt-4.1`, hosted provider class, production label, credentials reference, and `temperature: 0.2`. |
| [`internal-secure.yaml`](/providers/examples/internal-secure.yaml) | Enterprise workflows must route model calls through an approved internal gateway. | `providerRef: internal-secure` resolves to a gateway provider profile with endpoint and credentials references instead of raw secrets. |
