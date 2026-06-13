# ODPR Provider

The `Provider` object is the second ODPR root object. It defines a named
runtime provider profile that recipes can reference with `providerRef`.

Providers standardize the shape of LLM and execution-provider configuration
without putting provider details inside workflow recipes. A recipe stays focused
on what should happen. A provider profile declares how a named runtime profile
resolves to a provider family, model, endpoint reference, credentials reference,
and model settings.

Provider profiles MUST NOT contain raw secrets. Use `credentialsRef` or
implementation-specific secret references instead.
ODPR validation tools SHOULD reject embedded secrets or API keys, including
fields such as `apiKey`, `token`, `password`, or raw secret-looking values.

## Root structure

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
```

| Element | Type | Required | Description |
|---|---|---|---|
| `schema` | string | required | URI of the ODPR schema used to validate the provider file. |
| `version` | string | required | Version of the ODPR specification used by the provider file. |
| `kind` | string | required | ODPR root object type. Provider files MUST use `Provider`. |
| `provider` | object | required | Top-level object that defines one named provider profile. |

## Provider fields

```yaml
provider:
  id: production-quality
  provider: openai
  model: gpt-4.1
  providerClass: hosted
  endpointRef: platform:openai
  credentialsRef: env:OPENAI_API_KEY
  temperature: 0.2
  settings:
    maxOutputTokens: 4000
```

| Element | Type | Required | Description |
|---|---|---|---|
| `id` | string | required | Stable profile name referenced by `execution.providerRef` or `step.providerRef`. |
| `provider` | string | required | Provider family or runtime adapter, such as `openai`, `ollama`, `lmstudio`, `openrouter`, or `gateway`. |
| `model` | string | optional | Model name or runtime model identifier. |
| `providerClass` | string | optional | Provider class such as `local`, `hosted`, `hybrid`, or `none`. |
| `endpointRef` | string | optional | Reference to a platform, gateway, or runtime endpoint. |
| `credentialsRef` | string | optional | Reference to credentials managed outside the provider document. |
| `temperature` | number | optional | Default generation temperature for this provider profile. |
| `settings` | object | optional | Additional provider settings that are safe to share and do not contain secrets. |
| `description` | string | optional | Human-readable purpose of the provider profile. |
| `environment` | string | optional | Environment label such as development, CI, staging, or production. |

## Provider references

A recipe uses `providerRef` to select a Provider profile by `provider.id`:

```yaml
execution:
  mode: hosted
  providerRef: production-quality
```

The Provider object with `id: production-quality` defines the runtime profile:

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

This keeps the recipe portable while avoiding a provider wild west. Recipes
standardize workflow intent. Providers standardize named runtime profiles.
Executing SDKs, CI/CD systems, MCP servers, agent runtimes, and platforms then
resolve `endpointRef`, `credentialsRef`, and any implementation-specific
settings during execution.

## Example profiles

```yaml
schema: https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml
version: "1.0"
kind: Provider
provider:
  id: local-fast
  provider: ollama
  model: gemma
  providerClass: local
  temperature: 0.1
  environment: development
```

These examples show how Provider profiles turn recipe-level `providerRef`
names into standardized runtime profiles.

`local-fast` is intended for development and fast CI-style checks. A recipe
that uses `providerRef: local-fast` asks the executor to use a local provider
profile backed by Ollama and the `gemma` model. The low temperature keeps local
drafting runs predictable while avoiding any hosted model dependency.

```yaml
schema: https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml
version: "1.0"
kind: Provider
provider:
  id: internal-secure
  provider: gateway
  model: approved-llm
  providerClass: hosted
  endpointRef: platform:internal-gateway
  credentialsRef: vault:odp-agent-runtime
  temperature: 0.0
  environment: production
```

`internal-secure` is intended for controlled production or enterprise
environments. A recipe that uses `providerRef: internal-secure` asks the
executor to route model calls through an approved internal gateway. The profile
names the gateway endpoint and credential reference, but it does not embed the
actual credential or API key.


