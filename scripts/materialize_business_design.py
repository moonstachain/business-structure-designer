#!/usr/bin/env python3
"""Generate a business design bundle from structured interview input."""

from __future__ import annotations

import argparse
from pathlib import Path

from business_structure_designer import (
    copy_reference_dashboard,
    load_input,
    render_business_system,
    render_checklist,
    render_current_state,
    render_legacy_mapping,
    render_rationale,
    render_source_mapping,
    write_json,
    write_text,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a business design bundle.")
    parser.add_argument("--input-file", required=True, help="Structured interview input in JSON or YAML.")
    parser.add_argument("--output-dir", required=True, help="Directory for generated Markdown and metadata.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_input(Path(args.input_file).expanduser().resolve())
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    write_text(output_dir / "business-system.md", render_business_system(config))
    write_text(output_dir / "data-structure-rationale.md", render_rationale(config))
    write_text(output_dir / "source-mapping.md", render_source_mapping(config))
    write_text(output_dir / "implementation-checklist.md", render_checklist(config))

    if config["data_sources"]:
        write_text(output_dir / "current-state-inventory.md", render_current_state(config))
    if config["legacy_assets"] or config["data_sources"]:
        write_text(output_dir / "legacy-to-new-mapping.md", render_legacy_mapping(config))

    copy_reference_dashboard(output_dir)
    write_json(output_dir / "manifest.json", {"business_name": config["business_name"], "output_dir": str(output_dir)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
