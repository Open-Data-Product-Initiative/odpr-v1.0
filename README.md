# Data Product Recipe Specification (ODPR)

The Data Product Recipe Specification, ODPR, is a lightweight, vendor-neutral,
machine-readable standard for reusable data product workflow recipes, named
provider profiles, and metadata-only recipe catalogs.

ODPR describes how repeatable data product work gets done: which steps run,
which inputs and outputs are used, which checks or gates apply, which context
format is preferred, which execution mode is expected, and which standardized
provider profile should be used.

The Open Data Product SDK is intended to be the first reference implementation
for validating and executing ODPR recipes.

# What ODPR Defines

ODPR defines portable recipes for workflows such as:

* local development and fast drafting
* CI validation and build checks
* release review packages
* portfolio refresh, rendering, and localization
* hybrid local and hosted LLM execution
* agent-safe data product automation

Recipes are declarative workflow contracts. They are not scripts and they are
not tied to one SDK, CI/CD system, model provider, or orchestration engine.

ODPR also defines portable Provider profiles so `providerRef` values resolve to
a consistent object shape instead of implementation-specific provider
configuration. Provider profiles standardize names, provider family, model,
provider class, endpoint reference, credentials reference, and safe defaults
such as temperature. They do not store raw secrets.

ODPR also defines `RecipeCatalog` documents for discovery. Catalogs list recipe
metadata and paths to complete recipe files; they do not contain full step
bodies, runtime status, planned writes, run ids, logs, or readiness results.

Validation should reject embedded secrets or API keys in Recipe, Provider, and
RecipeCatalog documents. Use `providerRef` and `credentialsRef` instead of raw
keys, tokens, passwords, or inline secret values.

# Relationship To The Standards Family

ODPR is part of the OpenDataProducts.org standards family.

* ODPS describes one data product.
* ODPC describes catalogs, portfolios, product references, use cases,
  objectives, and signals.
* ODPG describes relationships and graphs between data product artifacts.
* ODPV describes shared vocabulary and terms.
* ODPR describes repeatable workflows for data product delivery.

ODPR does not replace ODPS, ODPC, ODPG, or ODPV. It defines how workflows around
those artifacts can be declared, inspected, validated, automated, and reused.

# Specification Aims

* Make data product workflows portable, repeatable, inspectable, and
  automation-ready.
* Support local development, CI/CD, release, localization, hybrid, and
  agent-safe workflows.
* Let workflows stay stable while model runtimes vary by environment, task, or
  deployment stage.
* Support compact context policy such as YAML, TOON, GCF, or automatic fallback.
* Standardize provider profile shape without storing raw secrets or defining
  provider-specific APIs.
* Give AI agents a safe recipe contract they can inspect before running tools.

# Found a Bug?

Found a bug, question, or improvement idea?

Submit an issue or propose changes with a pull request.

# Contributors

Data Product Recipe Specification is part of the OpenDataProducts.org standards
family under the Open Data Product Initiative.
