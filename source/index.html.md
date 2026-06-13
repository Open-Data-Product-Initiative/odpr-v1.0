---
title: Open Data Product Recipe Specification (ODPR) version 1.0 | Linux Foundation

language_tabs:
- yaml

toc_footers:
  - License <a href='https://www.apache.org/licenses/LICENSE-2.0'>Apache 2.0</a>
  - <br/><a href='https://opendataproducts.org'>Specification home</a>
  - <br/>Linux Foundation</a>

includes:
- toolkit
- agent_usage
- recipe
- extensions
- contributors
- terms

search: true

code_clipboard: true

meta:
  - name: description
    content: Open Data Product Recipe Specification (ODPR) version 1.0 is a lightweight, vendor-neutral, machine-readable standard for reusable data product workflow recipes.
  - name: spec-version
    content: "1.0"
  - name: llms
    content: /llms.txt
  - name: ai-agent-guidance
    content: Use /llms.txt for agent guidance and /schema/odpr.yaml or /schema/odpr.json for validation.
---

# OPEN DATA PRODUCT RECIPE SPECIFICATION - The Linux Foundation

## Version DRAFT

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14
([RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119) and
[RFC 8174](https://datatracker.ietf.org/doc/html/rfc8174)) when, and only when,
they appear in all capitals, as shown here.

The specification is shared under <a href='https://www.apache.org/licenses/LICENSE-2.0'>Apache 2.0</a> license.
Development of the specification is under the umbrella of the Linux Foundation.

| Topic | Link | Description |
|---|---|---|
| Version source | <a href="https://github.com/Open-Data-Product-Initiative/odpr-v1.0">Data Product Recipe Specification on GitHub</a> | Official source repository for the ODPR specification |
| Knowledge Base | [Open Data Product Spec Family Knowledge Base](https://opendataproducts.org/howto/) | Practical examples, FAQs, and implementation guidance |
| Contribute | [Raise an issue in GitHub](https://github.com/Open-Data-Product-Initiative/odpr-v1.0/issues) | Submit issues or suggestions to the specification maintainers |

# Introduction

The Data Product Recipe Specification, ODPR, is a lightweight, vendor-neutral,
machine-readable recipe model for repeatable data product delivery workflows.

ODPR is part of the OpenDataProducts.org standards family. It complements the
Open Data Product Specification, ODPS, Open Data Product Catalogs, ODPC, Open
Data Product Graphs, ODPG, and Open Data Product Vocabulary, ODPV, by defining
how workflows around those artifacts can be declared and automated.

ODPR standardizes how data product work gets done, not only what the final
artifact looks like.

## Why ODPR is needed

Data product work often depends on manual command sequences, scripts, notebooks,
prompts, and local habits. That creates delivery variation, makes validation
and review steps easy to skip, hides model-provider choices, and forces CI/CD
automation and AI agents to guess the intended workflow.

ODPR solves this by turning repeatable data product work into declared recipes.
A recipe describes:

* what workflow runs
* which inputs it uses
* which outputs it creates
* which steps run
* which checks or gates apply
* which context format is preferred
* which execution mode is expected
* which provider reference or provider class is used
* whether human review is required

## Core design principle

A recipe is not a script.

A recipe is a portable, declarative workflow contract. Scripts tell one tool
what to do. Recipes tell teams, tools, agents, and automation systems how a data
product workflow should run.

## Relationship to the standards family

The OpenDataProducts.org standards family follows a separation of concerns:

* **ODPS defines the product.**
* **ODPC defines catalogs and reusable portfolio objects.**
* **ODPG defines relationships and graphs.**
* **ODPV defines shared vocabulary and terms.**
* **ODPR defines repeatable workflows for data product delivery.**

ODPR does not define the product, catalog, graph, or vocabulary model. It
defines the workflow contract around those artifacts.

## Example recipe

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
      en: Generate and validate draft ODPC fragments during CI.
  type: ci
  execution:
    mode: local
    providerRef: local-fast
  context:
    format: gcf
    fallback:
      - toon
      - yaml
  steps:
    - id: generate-signals
      command: generate
      with:
        kind: signal
        input: source_docs/signals/
        output: generated/fragments/
    - id: validate-fragments
      command: validate
      with:
        input: generated/fragments/
  gates:
    - id: fragments-valid
      type: validation
      required: true
  review:
    required: false
```

## Specification aims

ODPR aims to:

* make data product workflows portable, repeatable, inspectable, and
  automation-ready
* support standard development, CI, release, localization, hybrid, and
  agent-safe workflows
* let teams switch between local, hosted, and hybrid model execution
* keep provider execution configurable without making ODPR a provider registry
* support compact context policy such as YAML, TOON, GCF, or automatic fallback
* expose safe workflows to AI agents before they run tools

**Note!** In "Open Data Product" the focus is on the latter words and the
prefix "open" refers to the openness of the standard. Any connotations to open
data are not intentional, intended, or desirable.
