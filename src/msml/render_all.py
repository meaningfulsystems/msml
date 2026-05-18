"""Render all MSML diagram (.msmd) files in a directory tree."""

import argparse
import sys
from pathlib import Path

from .render import render


def render_all(root: Path) -> int:
    files = sorted(root.rglob("*.msmd"))
    if not files:
        print(f"No .msmd files found under {root}")
        return 1

    print(f"Rendering {len(files)} diagram(s):")
    errors = []
    for diagram_file in files:
        try:
            render(diagram_file)
        except Exception as exc:
            print(f"  ERROR {diagram_file.name}: {exc}")
            errors.append(diagram_file)

    print(f"\nDone. {len(files) - len(errors)} succeeded, {len(errors)} failed.")
    return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(description="Render all MSML diagram (.msmd) files under a directory.")
    parser.add_argument("root", nargs="?", default=".", help="Directory to search. Defaults to current directory.")
    args = parser.parse_args()
    sys.exit(render_all(Path(args.root)))


if __name__ == "__main__":
    main()
