# Business Structure Designer

`business-structure-designer` is a reusable Codex skill for turning a rough business problem, spreadsheet, or Feishu table into a clean business data structure, Bitable template set, dashboard information architecture, and GitHub-ready design bundle.

## What It Produces

- `business-system.md`
- `data-structure-rationale.md`
- `source-mapping.md`
- `implementation-checklist.md`
- `current-state-inventory.md` when source material exists
- `legacy-to-new-mapping.md` when legacy sheets or tables exist
- `bitable/*.json` template files
- `dashboard/dashboard-ia.md`
- `manifest.json`

## Recommended Flow

1. Start from interview answers about goal, users, objects, stages, and data sources.
2. Add Excel paths, Feishu links, or existing docs as supporting evidence.
3. Generate the design bundle.
4. Export the bundle into a GitHub-readable directory.

## Commands

```bash
python3 scripts/materialize_business_design.py --input-file inputs/business-design.json --output-dir artifacts/design-bundle
```

```bash
python3 scripts/generate_bitable_templates.py --config inputs/business-design.json --output-dir artifacts/design-bundle/bitable
```

```bash
python3 scripts/export_design_bundle.py --source artifacts/design-bundle --output-dir artifacts/design-bundle-export
```

## Input Contract

The input file can be JSON or YAML and should cover:

- `business_name`
- `business_goal`
- `primary_users`
- `primary_objects`
- `stages`
- `service_lines`
- `data_sources`
- `dashboard_questions`

See [inputs/business-design.json](/Users/liming/Downloads/AI-COWORK/codex-dosometingnew/local-skills/business-structure-designer/inputs/business-design.json) for an example.
