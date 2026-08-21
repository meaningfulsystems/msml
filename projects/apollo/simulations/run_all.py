#!/usr/bin/env python3
"""Run the four educational estimate scripts with sourced inputs only."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from estimate_delta_v import main as delta_v_main  # noqa: E402
from estimate_rcs import main as rcs_main  # noqa: E402
from estimate_sps_load import main as sps_main  # noqa: E402
from estimate_stack_mass import main as stack_main  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    if argv:
        print("run_all.py takes no extra arguments; each script has its own flags.", file=sys.stderr)
        return 2
    sections = (
        ("change in velocity", delta_v_main),
        ("SPS propellant load", sps_main),
        ("RCS propellant", rcs_main),
        ("stack mass budget", stack_main),
    )
    for title, fn in sections:
        print()
        print("=" * 72)
        print(f"ESTIMATE section: {title}")
        print("=" * 72)
        code = fn([])
        if code:
            return code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
