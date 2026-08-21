#!/usr/bin/env python3
"""ESTIMATE whether published mass/tank figures close a stack budget.

They should not be forced to agree. Simulation output is not a NASA fact.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from report import banner, estimate, note, parameter, sourced  # noqa: E402
from sourced import published_inputs  # noqa: E402


def _fmt(value: float) -> str:
    return f"{value:,.4f}".rstrip("0").rstrip(".")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="ESTIMATE stack-mass residual. Not a NASA fact. Do not force sources to agree."
    )
    parser.add_argument(
        "--sa507-ignition-lb",
        type=float,
        default=None,
        help="Caller SA-507 stack mass (parameter). Not on this model.",
    )
    parser.add_argument(
        "--sp4029-ignition-lb",
        type=float,
        default=None,
        help="Caller SP-4029 stack mass (parameter). Not on this model.",
    )
    parser.add_argument(
        "--sla-lb",
        type=float,
        default=None,
        help="Caller SLA mass (parameter). SLA mass is not on the model.",
    )
    args = parser.parse_args(argv)

    banner()
    pub = published_inputs()
    sourced(f"Tank rows: {pub['source_tank_rows']}")
    sourced(f"Mass-budget flag: {pub['mass_budget_flag']}")
    sourced(f"Ignition {pub['ignition_lb']:,.0f} lb (A11 PK p.109)")
    sourced(f"First motion {pub['first_motion_lb']:,.0f} lb (A11 PK p.109)")
    sourced(f"F-1 {pub['f1_thrust_lbf']:,.0f} lbf is a {pub['f1_source']} citation, not an AS-506 mass")
    parameter("SA-507 tank/mass figures are not on this model (only the F-1 thrust citation).")
    parameter("SP-4029 tank/mass figures are not on this model. No page or number is invented.")
    parameter(f"SLA mass is not on the model (serial {pub['sla_serial']} only).")

    rows = [
        ("S-IC fueled", pub["sic"]["fueled_lb"]),
        ("S-II fueled", pub["sii"]["fueled_lb"]),
        ("S-IVB fueled", pub["sivb"]["fueled_lb"]),
        ("IU", pub["iu_lb"]),
        ("CM launch", pub["cm_launch_lb"]),
        ("SM launch", pub["sm_launch_lb"]),
        ("LM-5 launch", pub["lm_launch_lb"]),
        ("LES", pub["les_lb"]),
    ]
    total = 0.0
    for name, value in rows:
        sourced(f"{name} {value:,.0f} lb")
        total += value
    estimate(f"Sum of those Press Kit rows = {_fmt(total)} lb")

    sic = pub["sic"]
    sii = pub["sii"]
    sivb = pub["sivb"]
    estimate(
        f"S-IC dry+LOX+RP-1 = {_fmt(sic['dry_lb'] + sic['lox_lb'] + sic['rp1_lb'])} lb "
        f"vs fueled {sic['fueled_lb']:,.0f} lb "
        f"(delta {_fmt(sic['fueled_lb'] - (sic['dry_lb'] + sic['lox_lb'] + sic['rp1_lb']))} lb)"
    )
    sii_parts = sii["dry_lb"] + sii["lox_lb"] + sii["lh2_lb"]
    estimate(
        f"S-II dry+LOX+LH2 = {_fmt(sii_parts)} lb vs fueled {sii['fueled_lb']:,.0f} lb "
        f"(delta {_fmt(sii['fueled_lb'] - sii_parts)} lb) — UNRECONCILED inside the same table"
    )
    estimate(
        f"S-IVB dry+LOX+LH2 = {_fmt(sivb['dry_lb'] + sivb['lox_lb'] + sivb['lh2_lb'])} lb "
        f"vs fueled {sivb['fueled_lb']:,.0f} lb "
        f"(delta {_fmt(sivb['fueled_lb'] - (sivb['dry_lb'] + sivb['lox_lb'] + sivb['lh2_lb']))} lb)"
    )

    vs_ignition = pub["ignition_lb"] - total
    vs_first = pub["first_motion_lb"] - total
    estimate(f"Ignition − row sum = {_fmt(vs_ignition)} lb")
    estimate(f"First motion − row sum = {_fmt(vs_first)} lb")
    note(
        "Those residuals are not a sourced SLA mass and not a missing tank load. "
        "Do not assign the leftover to SLA or to SPS."
    )
    if args.sla_lb is not None:
        parameter(f"Caller SLA {args.sla_lb:g} lb (not on the model)")
        with_sla = total + args.sla_lb
        estimate(f"Row sum + caller SLA = {_fmt(with_sla)} lb")
        estimate(f"Ignition − (row sum + caller SLA) = {_fmt(pub['ignition_lb'] - with_sla)} lb")
        note("Even with a caller SLA, do not call the budget closed.")

    columns = [("A11 PK p.109 ignition", pub["ignition_lb"]), ("A11 PK p.109 first motion", pub["first_motion_lb"])]
    if args.sa507_ignition_lb is not None:
        parameter(f"Caller SA-507 mass {args.sa507_ignition_lb:g} lb (not on this model)")
        columns.append(("caller SA-507", args.sa507_ignition_lb))
    else:
        parameter("Pass --sa507-ignition-lb only if you have a sourced SA-507 extract. Nothing is invented here.")
    if args.sp4029_ignition_lb is not None:
        parameter(f"Caller SP-4029 mass {args.sp4029_ignition_lb:g} lb (not on this model)")
        columns.append(("caller SP-4029", args.sp4029_ignition_lb))
    else:
        parameter("Pass --sp4029-ignition-lb only if you have a sourced SP-4029 extract. Nothing is invented here.")

    note("Independent source columns — do not pick a winner and do not force them to agree.")
    for name, value in columns:
        estimate(f"{name} = {_fmt(value)} lb vs Press Kit row sum {_fmt(total)} lb → residual {_fmt(value - total)} lb")

    distinct = {round(value, 3) for _, value in columns}
    if len(distinct) > 1:
        estimate("Sources differ. Budget stays UNRECONCILED.")
    else:
        estimate(
            "Caller numbers happened to match one published mass. "
            "Still do not promote a closed stack budget — the model flag stays UNRECONCILED."
        )

    estimate("Press Kit vs SA-507 vs SP-4029 must not be forced to close. No silent winner.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
