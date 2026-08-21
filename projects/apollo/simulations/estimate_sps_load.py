#!/usr/bin/env python3
"""ESTIMATE Service Propulsion System propellant-load sensitivity.

CSM-107 SPS loaded pounds are UNKNOWN on the model and stay a parameter.
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
from rocket import burn_time_s, delta_v_ft_per_s, delta_v_per_isp_s, range_pair  # noqa: E402
from sourced import published_inputs  # noqa: E402


def _fmt(value: float) -> str:
    return f"{value:,.4f}".rstrip("0").rstrip(".")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="ESTIMATE SPS load sensitivity. Not a NASA fact."
    )
    parser.add_argument(
        "--sps-load-lb",
        type=float,
        action="append",
        default=[],
        help="SPS loaded propellant in lb (parameter). Repeat for a range.",
    )
    parser.add_argument(
        "--isp-s",
        type=float,
        action="append",
        default=[],
        help="Specific impulse in seconds (parameter; not an Apollo citation).",
    )
    parser.add_argument(
        "--wet-lb",
        type=float,
        default=None,
        help="Optional wet mass before the burn (parameter). Default: CM+SM launch sum.",
    )
    args = parser.parse_args(argv)

    banner()
    pub = published_inputs()
    sourced(f"CM launch {pub['cm_launch_lb']:,.0f} lb (A11 PK p.109)")
    sourced(f"SM launch {pub['sm_launch_lb']:,.0f} lb (A11 PK p.109)")
    sourced(f"SPS thrust: {pub['sps_thrust']}")
    sourced(f"SPS O/F: {pub['sps_of_ratio']}")
    sourced(f"SPS loaded on the model: {pub['sps_loaded']}")
    parameter("CSM-107 SPS loaded lb stays unmarked. This script does not fill it.")
    parameter("SPS specific impulse is not on the model.")

    cm_sm = pub["cm_launch_lb"] + pub["sm_launch_lb"]
    note(
        f"CM+SM launch sum {cm_sm:,.0f} lb is two Press Kit rows added. "
        "That sum is not a sourced CSM wet-mass requirement."
    )
    wet = args.wet_lb if args.wet_lb is not None else cm_sm
    if args.wet_lb is not None:
        parameter(f"Caller wet mass {wet:,.4f} lb")
    else:
        estimate(f"Default wet mass for the sensitivity = CM+SM sum {_fmt(wet)} lb")

    thrusts = sorted({pub["sps_thrust_pk_lbf"], pub["sps_thrust_tn_lbf"]})
    sourced(
        f"SPS thrust citations {thrusts[0]:,.0f} lbf (PK) and {thrusts[-1]:,.0f} lbf vac (TN D-7375) — cite both"
    )

    of_ratio = 1.6
    note("O/F 1.6 is a mixture ratio, not a load. If a load is supplied, oxidizer = 1.6/2.6 of the load.")

    if not args.sps_load_lb:
        parameter("Pass --sps-load-lb (repeatable) to sweep a caller load. No Apollo load is assumed.")
    if not args.isp_s:
        parameter("Pass --isp-s (repeatable) to print Δv. No Apollo Isp is assumed.")

    if args.sps_load_lb:
        load_lo, load_hi = range_pair(args.sps_load_lb)
        parameter(f"Caller SPS load range {load_lo:g} … {load_hi:g} lb (not a sourced CSM-107 load)")
        for load in sorted(args.sps_load_lb):
            if load >= wet:
                estimate(f"Load {load:g} lb ≥ wet {wet:g} lb — skipped (would invent a burn-out mass)")
                continue
            ox = load * of_ratio / (1.0 + of_ratio)
            fuel = load - ox
            estimate(f"Load {load:g} lb → oxidizer {_fmt(ox)} lb, fuel {_fmt(fuel)} lb (O/F 1.6 split)")
            coeff = delta_v_per_isp_s(wet, wet - load)
            estimate(f"Load {load:g} lb, wet {_fmt(wet)} lb → Δv/Isp = {_fmt(coeff)} (ft/s)/s")

        if args.isp_s:
            isp_lo, isp_hi = range_pair(args.isp_s)
            parameter(f"Caller Isp range {isp_lo:g} … {isp_hi:g} s (not an Apollo citation)")
            dvs: list[float] = []
            times: list[float] = []
            for load in args.sps_load_lb:
                if load >= wet:
                    continue
                for isp in args.isp_s:
                    dv = delta_v_ft_per_s(wet, wet - load, isp)
                    dvs.append(dv)
                    estimate(f"Load {load:g} lb, Isp={isp:g} s → Δv = {_fmt(dv)} ft/s")
                    for thrust in thrusts:
                        t_s = burn_time_s(load, thrust, isp)
                        times.append(t_s)
                        estimate(
                            f"Load {load:g} lb, Isp={isp:g} s, thrust {thrust:,.0f} lbf → "
                            f"burn time {_fmt(t_s)} s"
                        )
            if dvs:
                dv_lo, dv_hi = range_pair(dvs)
                estimate(f"SPS Δv range {_fmt(dv_lo)} … {_fmt(dv_hi)} ft/s")
            if times:
                t_lo, t_hi = range_pair(times)
                estimate(f"SPS constant-thrust burn-time range {_fmt(t_lo)} … {_fmt(t_hi)} s")

    estimate("No CSM-107 SPS loaded mass is printed as a fact. The teaching note stays unmarked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
