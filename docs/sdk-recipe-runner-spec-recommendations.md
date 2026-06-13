# SDK Recipe Runner Spec Recommendations

This note lists recommended ODPR spec additions that would make recipes work
cleanly with the ODP Agent SDK recipe runner plan. These are proposed additions,
not current normative requirements.

## 1. Provider Resolution

ODPR should explain that `providerRef` points to a standardized ODPR Provider
object. The Provider object should define the portable profile shape, while the
executing implementation resolves live endpoints, credentials, and
provider-specific APIs.

Example:

```yaml
execution:
  mode: hosted
  providerRef: production-quality
```

Recommended wording:

> `providerRef` identifies an ODPR Provider profile by `provider.id`. Provider
> profiles standardize the named runtime profile while raw credentials,
> endpoint resolution, and provider-specific API behavior stay in the executing
> SDK, CI/CD system, agent runtime, or platform.

Example Provider:

```yaml
schema: https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml
version: "1.0"
kind: Provider
provider:
  id: production-quality
  provider: openai
  model: gpt-4.1
  providerClass: hosted
  temperature: 0.2
  credentialsRef: env:OPENAI_API_KEY
```

## 2. Initial Command Registry

ODPR should define a small recommended command vocabulary so recipes can be
portable across tools while still allowing implementations to add commands.

Recommended initial commands:

```text
generate
validate
odpc.build
odpg.build
portfolio.build
portfolio.refresh
portfolio.render
portfolio.localize
portfolio.explain
```

Recommended wording:

> Implementations SHOULD support the recommended command names where the
> underlying capability exists. Implementations MAY support additional commands.

## 3. Step Argument Semantics

ODPR should clarify that `step.with` contains command-specific arguments.

Example:

```yaml
steps:
  - id: localize-portfolio
    command: portfolio.localize
    with:
      workspace: portfolio/
      languages:
        - fi
        - sv
```

Recommended wording:

> `with` is an argument object for the selected command. ODPR standardizes where
> command arguments live, but v1.0 does not define the complete argument schema
> for every command.

## 4. Run Policy

ODPR should keep lightweight runtime guidance for practical SDK and CI usage.

Example:

```yaml
runPolicy:
  timeoutSeconds: 900
  retries: 1
```

This is useful for local LLMs, portfolio localization, and hosted provider
calls that may need different operational limits.

## 5. Gates

Gates should be first-class enough for CI/CD and release automation.

Example:

```yaml
gates:
  - id: schema-valid
    type: validation
    required: true
  - id: human-review
    type: review
    required: true
```

Recommended wording:

> A required gate SHOULD be evaluated or reported by the executing tool. Tools
> SHOULD NOT silently skip required gates.

## 6. Outputs

Canonical examples should include outputs where the workflow creates durable
artifacts. This helps CI jobs and agents know what to inspect after a run.

Example:

```yaml
outputs:
  - id: localized-portfolio-fi
    path: portfolio/index.fi.html
  - id: report
    path: portfolio/report.json
```

## 7. Review Policy

The `review` object should support human, agent, both, and none modes.

Example:

```yaml
review:
  required: true
  mode: human
  instructions: Review localized pages and generated reports before publishing.
```

This is especially useful for release recipes and generated ODPS/ODPC/ODPG
artifacts that should not be accepted without review.

## 8. Agent Safety

ODPR should provide a lightweight way to expose agent execution expectations.
This could be a separate `agent` object or be modeled through gates and review.

Possible shape:

```yaml
agent:
  safeToRun: true
  requiresConfirmation: false
```

Alternative:

```yaml
gates:
  - id: agent-confirmation
    type: approval
    required: true
```

Recommendation: keep v1.0 simple. Prefer gates/review unless a separate agent
object becomes necessary.

## 9. Environment

ODPR should support explicit environment labels so teams can distinguish local
development recipes from CI, staging, and production recipes.

Example:

```yaml
environment: production
```

Recommended values:

```text
development
ci
staging
production
```

## 10. Recipe Composition

Recipe composition is useful but should probably remain future scope.

Possible future shape:

```yaml
uses:
  - recipeRef: ci-validate-generated-fragments
```

Recommendation: do not add composition to the v1.0 core unless there is a clear
near-term executor design. Keep the first version focused on one recipe, its
steps, gates, context, execution, and review.

## Recommended Near-Term Spec Additions

The highest-value additions for SDK compatibility are:

1. Provider object and provider reference semantics.
2. Recommended command vocabulary.
3. Clear `step.with` argument semantics.
4. Outputs in examples.
5. Stronger gates and review guidance.
6. Run policy examples.
7. Environment labels.

Together, these additions let ODPR remain a lightweight standard while giving
the SDK enough structure to implement `recipe validate` and `recipe run`.
