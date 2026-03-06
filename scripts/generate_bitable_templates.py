#!/usr/bin/env python3
"""Generate reusable Bitable templates for a business design."""

from __future__ import annotations

import argparse
from pathlib import Path

from business_structure_designer import customize_templates, load_input, write_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate business-specific Bitable templates.")
    parser.add_argument("--config", required=True, help="Structured interview input in JSON or YAML.")
    parser.add_argument("--output-dir", required=True, help="Directory for generated Bitable template files.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_input(Path(args.config).expanduser().resolve())
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    for filename, payload in customize_templates(config).items():
        write_json(output_dir / filename, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
