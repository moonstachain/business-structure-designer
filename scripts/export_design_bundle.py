#!/usr/bin/env python3
"""Export a generated design bundle into a GitHub-readable directory."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from business_structure_designer import load_input, render_export_readme, write_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export a business design bundle for GitHub or handoff.")
    parser.add_argument("--source", required=True, help="Generated design bundle directory.")
    parser.add_argument("--output-dir", required=True, help="Export directory.")
    parser.add_argument("--input-file", help="Optional original interview input for README rendering.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    source = Path(args.source).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()

    output_dir.mkdir(parents=True, exist_ok=True)
    for child in source.iterdir():
        target = output_dir / child.name
        if child.is_dir():
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(child, target)
        else:
            shutil.copy2(child, target)

    if args.input_file:
        config = load_input(Path(args.input_file).expanduser().resolve())
        write_text(output_dir / "README.md", render_export_readme(config, output_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
