#!/usr/bin/env python3
"""Render all .msmd diagram files in a directory tree."""
import sys
from pathlib import Path
from render_msml import render

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
files = sorted(root.rglob("*.msmd"))
if not files:
    print(f"No .msmd files found under {root}")
    sys.exit(1)
print(f"Rendering {len(files)} diagram(s):")
errors = []
for f in files:
    try:
        render(f)
    except Exception as e:
        print(f"  ERROR {f.name}: {e}")
        errors.append(f)
print(f"\nDone. {len(files)-len(errors)} succeeded, {len(errors)} failed.")
if errors:
    sys.exit(1)
