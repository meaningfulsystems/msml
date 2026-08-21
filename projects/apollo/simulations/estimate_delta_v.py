#!/usr/bin/env python3
"""ESTIMATE mission / stage change in velocity from published masses.

Specific impulse is not on the model. It stays a parameter.
Simulation output is not a NASA fact.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from report import banner, estimate, note, parameter, sourced  # noqa: E402
from rocket import delta_v_ft_per_s, delta_v_per_isp_s, range_pair  # noqa: E402
from sourced import published_inputs  # noqa: E402


def _fmt(value: float) -> str:
    return f"{value:,.4f}".rstrip("0").rstrip(".")


def _print_stage(name: str, fueled_lb: float, prop_a: float, prop_b: float) -> None:
    props = sorted({prop_a, prop_b})
    note(
        f"{name}: stage-alone mass ratio uses stage fueled/dry only. "
        "That is not flight Δv — payload is a parameter."
    )
    for prop_lb in props:
        mf = fueled_lb - prop_lb
        coeff = delta_v_per_isp_s(fueled_lb, mf)
        estimate(
            f"{name} stage-alone Δv/Isp = {_fmt(coeff)} (ft/s) per second of Isp "
            f"(m0={_fmt(fueled_lb)} lb, mp={_fmt(prop_lb)} lb, mf={_fmt(mf)} lb)"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="ESTIMATE change-in-velocity sensitivity. Not a NASA fact."
    )
    parser.add_argument(
        "--isp-s",
        type=float,
        action="append",
        default=[],
        help="Specific impulse in seconds (parameter; not an Apollo citation). Repeat for a range.",
    )
    parser.add_argument(
        "--payload-lb",
        type=float,
        default=None,
        help="Optional payload on top of a stage (parameter). Used with S-IC ignition/first-motion only if omitted.",
    )
    args = parser.parse_args(argv)

    banner()
    pub = published_inputs()
    sourced(f"Tank rows: {pub['source_tank_rows']}")
    sourced(f"Mass-budget flag: {pub['mass_budget_flag']}")
    sourced(f"CSM lunar Δv on the model: {pub['delta_v_csm']}")
    parameter("Official CSM lunar Δv table stays unmarked. This script does not fill it.")
    parameter("Specific impulse is not on the model.")
    note("Δv = Isp * g0 * ln(m0/mf). g0=32.174 ft/s² is a unit convention, not an Apollo figure.")

    sic = pub["sic"]
    sii = pub["sii"]
    sivb = pub["sivb"]
    sourced(
        f"S-IC fueled {sic['fueled_lb']:,.0f} lb, dry {sic['dry_lb']:,.0f} lb, "
        f"LOX+RP-1 {sic['propellant_from_tanks_lb']:,.0f} lb ({sic['source']})"
    )
    sourced(
        f"S-II fueled {sii['fueled_lb']:,.0f} lb, dry {sii['dry_lb']:,.0f} lb, "
        f"LOX+LH2 {sii['propellant_from_tanks_lb']:,.0f} lb ({sii['source']})"
    )
    sourced(
        f"S-IVB fueled {sivb['fueled_lb']:,.0f} lb, dry {sivb['dry_lb']:,.0f} lb, "
        f"LOX+LH2 {sivb['propellant_from_tanks_lb']:,.0f} lb ({sivb['source']})"
    )

    sii_mismatch = sii["propellant_from_fueled_minus_dry_lb"] - sii["propellant_from_tanks_lb"]
    estimate(
        f"S-II tank sum vs fueled−dry differs by {sii_mismatch:,.0f} lb "
        "(UNRECONCILED inside Press Kit rows; both stay in the range)"
    )

    _print_stage(
        "S-IC",
        sic["fueled_lb"],
        sic["propellant_from_tanks_lb"],
        sic["propellant_from_fueled_minus_dry_lb"],
    )
    _print_stage(
        "S-II",
        sii["fueled_lb"],
        sii["propellant_from_tanks_lb"],
        sii["propellant_from_fueled_minus_dry_lb"],
    )
    _print_stage(
        "S-IVB",
        sivb["fueled_lb"],
        sivb["propellant_from_tanks_lb"],
        sivb["propellant_from_fueled_minus_dry_lb"],
    )

    sourced(f"Stack ignition {pub['ignition_lb']:,.0f} lb (A11 PK p.109)")
    sourced(f"Stack first motion {pub['first_motion_lb']:,.0f} lb (A11 PK p.109)")
    note(
        "S-IC with published stack m0 (ignition vs first motion) still needs Isp. "
        "Do not treat the residual against the stage-row sum as a missing payload."
    )
    sic_props = sorted(
        {
            sic["propellant_from_tanks_lb"],
            sic["propellant_from_fueled_minus_dry_lb"],
        }
    )
    stack_m0s = [pub["ignition_lb"], pub["first_motion_lb"]]
    coeffs: list[float] = []
    for m0 in stack_m0s:
        for mp in sic_props:
            mf = m0 - mp
            coeff = delta_v_per_isp_s(m0, mf)
            coeffs.append(coeff)
            estimate(
                f"S-IC + published stack m0={_fmt(m0)} lb, mp={_fmt(mp)} lb → "
                f"Δv/Isp = {_fmt(coeff)} (ft/s)/s"
            )
    lo, hi = range_pair(coeffs)
    estimate(f"S-IC published-m0 Δv/Isp range {_fmt(lo)} … {_fmt(hi)} (ft/s) per second of Isp")

    if args.payload_lb is not None:
        parameter(f"Caller payload {args.payload_lb:,.4f} lb (not a sourced stack mass)")
        for name, stage in ("S-II", sii), ("S-IVB", sivb):
            for mp in sorted(
                {
                    stage["propellant_from_tanks_lb"],
                    stage["propellant_from_fueled_minus_dry_lb"],
                }
            ):
                m0 = stage["fueled_lb"] + args.payload_lb
                mf = m0 - mp
                estimate(
                    f"{name} + caller payload: Δv/Isp = {_fmt(delta_v_per_isp_s(m0, mf))} "
                    f"(ft/s)/s (m0={_fmt(m0)} lb)"
                )
    else:
        parameter("Upper-stage flight payload is not a closed number on the model.")

    if args.isp_s:
        isp_lo, isp_hi = range_pair(args.isp_s)
        parameter(f"Caller Isp range {isp_lo:g} … {isp_hi:g} s (not an Apollo citation)")
        dvs = [isp * c for isp in args.isp_s for c in coeffs]
        dv_lo, dv_hi = range_pair(dvs)
        estimate(
            f"S-IC + published stack m0, caller Isp → Δv {_fmt(dv_lo)} … {_fmt(dv_hi)} ft/s"
        )
        for isp in sorted(set(args.isp_s)):
            for m0 in stack_m0s:
                for mp in sic_props:
                    mf = m0 - mp
                    estimate(
                        f"Isp={isp:g} s, m0={_fmt(m0)} lb, mp={_fmt(mp)} lb → "
                        f"Δv = {_fmt(delta_v_ft_per_s(m0, mf, isp))} ft/s"
                    )
    else:
        parameter("Pass --isp-s (repeatable) to multiply the Δv/Isp range by a caller Isp.")

    estimate("No single mission Δv is printed. The official CSM lunar Δv table stays unmarked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
