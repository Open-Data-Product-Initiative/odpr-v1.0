# RuntimeProfile

The `RuntimeProfile` object is a supporting ODPR object. It standardizes the runtime
generation configuration that recipes use when a step needs an LLM or another
model-backed execution provider.

ODPR uses the same provider-map shape as the Open Data Product SDK generation
config. This keeps recipes, SDK execution, CI runners, MCP servers, and agent
runtimes aligned around one provider configuration model instead of mixing a
standard reference with SDK-only provider fields.

RuntimeProfile documents MUST NOT contain raw secrets. Use `apiKeyEnv` to name the
environment variable that contains an API key. ODPR validation tools SHOULD
reject embedded secrets or API keys, including fields such as `apiKey`, `token`,
`password`, or raw secret-looking values.

## RuntimeProfile structure

```yaml
schema: https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml
version: "1.0"
kind: RuntimeProfile
runtimeProfile:
  provider: production-quality
  model: gpt-4.1
  input: open_data_products/generation/source_docs/
  output: open_data_products/generation/fragments/
  prompts: prompts/
  portfolio:
    sourceBudget:
      maxSourceChars: 2000
      maxPromptChars: 32000
    privacy:
      obfuscatePersonalData: true
  providers:
    production-quality:
      type: openai
      model: gpt-4.1
      baseUrl: https://api.openai.com/v1
      apiKeyEnv: OPENAI_API_KEY
      maxTokens: 8192
```

| Element | Type | Required | Description |
|---|---|---|---|
| `schema` | string | required | URI of the ODPR schema used to validate the provider file. |
| `version` | string | required | Version of the ODPR specification used by the provider file. |
| `kind` | string | required | ODPR root object type. RuntimeProfile files MUST use `RuntimeProfile`. |
| `runtimeProfile` | object | required | Top-level runtime generation configuration object. |

### RuntimeProfile fields

| Element | Type | Required | Description |
|---|---|---|---|
| `runtimeProfile.provider` | string | required | Default provider profile name selected from `runtimeProfile.providers`. |
| `runtimeProfile.model` | string | optional | Default model override used when the selected provider profile does not define a model. |
| `runtimeProfile.input` | string | optional | Default input path for generation-oriented runs. |
| `runtimeProfile.output` | string | optional | Default output path for generated artifacts. |
| `runtimeProfile.prompts` | string | optional | Default prompt directory. |
| `runtimeProfile.baseUrl` | string | optional | Default base URL override used by compatible provider clients. |
| `runtimeProfile.version` | string | optional | API version or provider client version hint. |
| `runtimeProfile.maxTokens` | integer | optional | Default maximum output token budget. |
| `runtimeProfile.modelPath` | string | optional | Local model path for embedded runtimes such as llama.cpp. |
| `runtimeProfile.contextWindow` | integer | optional | Context window size for local or embedded runtimes. |
| `runtimeProfile.gpuLayers` | integer | optional | GPU layer count for local or embedded runtimes. |
| `runtimeProfile.portfolio` | object | optional | Portfolio intake budget and privacy policy used by generation workflows. |
| `runtimeProfile.providers` | object | required | Map of named provider profiles. `runtimeRef` fragments resolve to keys in this map. |

### Provider profile fields

```yaml
runtimeProfile:
  provider: openai
  providers:
    openai:
      type: openai
      model: gpt-4.1-mini
      baseUrl: https://api.openai.com/v1
      apiKeyEnv: OPENAI_API_KEY
      maxTokens: 8192
```

| Element | Type | Required | Description |
|---|---|---|---|
| `type` | string | optional | Provider client type: `anthropic`, `llama-cpp`, `ollama`, `openai`, or `openai-chat`. |
| `model` | string | optional | Model name or runtime model identifier. |
| `baseUrl` | string | optional | Provider API base URL or local runtime URL. |
| `apiKeyEnv` | string | optional | Environment variable name that contains the API key. The value is a name, not the secret itself. |
| `version` | string | optional | API version or provider-specific version hint. |
| `maxTokens` | integer | optional | Maximum output token budget for this profile. |
| `modelPath` | string | optional | Local model path for embedded runtimes. |
| `contextWindow` | integer | optional | Context window size for local or embedded runtimes. |
| `gpuLayers` | integer | optional | GPU layer count for local or embedded runtimes. |

### Portfolio policy fields

| Element | Type | Required | Description |
|---|---|---|---|
| `portfolio.sourceBudget.maxSourceChars` | integer | optional | Maximum extracted source characters considered per source chunk. |
| `portfolio.sourceBudget.maxPromptChars` | integer | optional | Maximum prompt character budget for portfolio intake. |
| `portfolio.privacy.obfuscatePersonalData` | boolean | optional | Whether personal data masking should run before model-backed portfolio intake. |

### RuntimeProfile references

A recipe uses `runtimeRef` to point to a RuntimeProfile document and, normally, one
profile inside its `runtimeProfile.providers` map. The value is a URI-reference, so it
may point to a local file, a published URL, or the same document with a
fragment. The fragment selects the provider profile key:

```yaml
execution:
  mode: hosted
  runtimeRef: runtime-profiles/examples/production-quality.yaml#production-quality
```

The executor resolves the file or URL, validates the ODPR `RuntimeProfile` document,
then resolves `#production-quality` to:

```yaml
runtimeProfile:
  providers:
    production-quality:
      type: openai
      model: gpt-4.1
```

If `runtimeRef` does not include a fragment, the executor SHOULD use
`runtimeProfile.provider` as the selected profile. If the referenced RuntimeProfile source
contains several profiles, a fragment is recommended so the recipe contract is
unambiguous.

## RuntimeProfile examples

```yaml
schema: https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml
version: "1.0"
kind: RuntimeProfile
runtimeProfile:
  provider: local-fast
  model: gemma
  providers:
    local-fast:
      type: ollama
      model: gemma
      baseUrl: http://localhost:11434
```

`local-fast` is intended for development and fast CI-style checks. A recipe
that uses `runtimeRef: runtime-profiles/examples/local-fast.yaml#local-fast` asks the
executor to use the `local-fast` profile from the referenced RuntimeProfile document.

```yaml
schema: https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml
version: "1.0"
kind: RuntimeProfile
runtimeProfile:
  provider: internal-secure
  model: approved-llm
  providers:
    internal-secure:
      type: openai-chat
      model: approved-llm
      baseUrl: https://gateway.example.org/v1
      apiKeyEnv: ODP_INTERNAL_GATEWAY_API_KEY
      maxTokens: 8192
```

`internal-secure` is intended for controlled production or enterprise
environments. A recipe that uses
`runtimeRef: runtime-profiles/examples/internal-secure.yaml#internal-secure` asks the
executor to route model calls through the referenced gateway profile. The
profile names the API key environment variable but does not embed the actual
credential or API key.
