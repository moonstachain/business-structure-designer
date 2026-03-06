---
name: business-structure-designer
description: 当用户要设计业务系统、飞书多维表结构、业务主表、阶段表、机制表、证据表，或把粗糙 Excel 和现有表重构成业务系统时触发。
---

# Business Structure Designer

Use this skill to turn a rough business idea, spreadsheet, Feishu table, or mixed operational archive into a reusable business data structure, Bitable template set, implementation bundle, and GitHub-ready knowledge package.

## When To Use

Use when the user wants to:

- design a business system from scratch
- restructure an existing Excel or Feishu setup
- split a business into main table, stage table, mechanism table, and evidence table
- design dashboard information architecture
- produce reusable Bitable templates and a GitHub-readable design bundle

## Workflow

1. Start with business interview answers.
   Collect goal, audience, core object, stages, service layers, data sources, and dashboard questions.
2. Pull in existing evidence only as support.
   Excel files, Feishu links, and old docs are supplemental inputs, not the primary modeling method.
3. Generate the design bundle.
   Use `scripts/materialize_business_design.py` to produce business-system, rationale, source-mapping, checklist, and optional current-state docs.
4. Generate Bitable templates.
   Use `scripts/generate_bitable_templates.py` to output reusable main, stage, mechanism, and evidence table JSON.
5. Export for GitHub or handoff.
   Use `scripts/export_design_bundle.py` to package Markdown and JSON outputs into a GitHub-readable bundle.

## Entry Commands

```bash
python3 scripts/materialize_business_design.py --input-file inputs/business-design.json --output-dir artifacts/design-bundle
```

```bash
python3 scripts/generate_bitable_templates.py --config inputs/business-design.json --output-dir artifacts/design-bundle/bitable
```

```bash
python3 scripts/export_design_bundle.py --source artifacts/design-bundle --output-dir artifacts/design-bundle-export
```

## Constraints

- Keep interview-first behavior. Existing sheets and tables inform the design but do not replace business modeling.
- Output must include methodology, rationale, templates, dashboard guidance, and implementation checklist together.
- Main tables hold decision objects only, not raw full text, attachment JSON, or heavy teaching material.
- Do not store secrets, browser state, or runtime artifacts in the repository.

## References

- `references/business-structure-method.md`
- `references/crm-vs-strategy-library.md`
- `references/new-business-modeling-checklist.md`
- `references/templates-overview.md`
- `references/dashboard-ia.md`

## Expected Outputs

- A reusable business design bundle with Markdown docs and JSON templates.
- A clean handoff package suitable for GitHub review and reuse.
- A repeatable skill that can be reused across other businesses and future Feishu modeling work.
