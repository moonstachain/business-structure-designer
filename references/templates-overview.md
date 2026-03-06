# Templates Overview

This skill ships with four base Bitable templates:

1. `business-master.json`
   The decision-entry table for the main business object.
2. `stage-map.json`
   The navigation table for stages or scenes.
3. `mechanism-map.json`
   The implementation-mechanism table for automation, rules, scripts, or platform capabilities.
4. `evidence-table.json`
   The evidence and case table for screenshots, SOPs, transcripts, and examples.

## Template Rules

- The main table should hold decision objects only.
- Stage tables provide navigation and summary axes.
- Mechanism tables separate "how it works" from "what is being managed".
- Evidence tables keep teaching and verification material out of the main table.
- Stable IDs should be explicit in every generated template.

## Dashboard Reference

Use `dashboard-ia.md` with these templates to design:

- overview cards
- diagnosis cards
- action cards
