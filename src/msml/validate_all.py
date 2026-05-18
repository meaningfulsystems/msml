"""Validate all MSML model and diagram files in a directory tree."""

import argparse
import sys
from pathlib import Path

from .validate import validate_all


def main():
    parser = argparse.ArgumentParser(description="Validate all MSML model (.msml) and diagram (.msmd) files under a directory.")
    parser.add_argument("root", nargs="?", default=".", help="Directory to search. Defaults to current directory.")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--lint", action="store_true")
    args = parser.parse_args()

    reporter = validate_all(Path(args.root), strict=args.strict, lint=args.lint)
    print(f"{reporter.errors} errors, {reporter.warnings} warnings.")
    sys.exit(1 if reporter.errors else 0)


if __name__ == "__main__":
    main()
