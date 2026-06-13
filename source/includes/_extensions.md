# Specification extensions

While ODPR defines the core recipe object and attributes, organizations may need
to add implementation-specific metadata for local tools, CI/CD systems,
governance workflows, or platform-specific requirements.

Extension properties are patterned fields prefixed with `x-`. These fields may
appear inside recipe objects where the schema allows extension properties.

Extensions are not part of the official ODPR object model unless they are later
adopted into the specification. Tooling may ignore extension fields unless
explicit support has been added.

Extensions should not redefine core ODPR semantics. They should be used only
for additional metadata that does not fit standard attributes.

Useful and widely adopted extensions may become candidates for future versions
of the standard. To propose useful extensions, raise an issue in GitHub:

[Open Data Product Initiative GitHub issues](https://github.com/Open-Data-Product-Initiative/odpr-v1.0/issues)

> Example of extension usage:

```yaml
schema: https://opendataproducts.org/odpr-v1.0/schema/odpr.yaml
version: "1.0"
kind: Recipe
recipe:
  metadata:
    id: RCP-CI-001
    name:
      en: CI Validate Generated Fragments
    description:
      en: Generate and validate fragments during CI.
    x-internal-owner-group: data-product-platform
  type: ci
  steps:
    - id: validate-fragments
      command: validate
      with:
        input: generated/fragments/
      x-ci-job-name: validate-generated-fragments
```

| <div style="width:150px">Element name</div> | Type | Options | Description |
|---|---|---|---|
| **^x-** | any | | Allows extensions to the ODPR schema. The field name MUST begin with x-, for example, x-ci-job-name. The value can be null, a primitive, an array, or an object. |
