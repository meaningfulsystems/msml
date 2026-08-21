#!/usr/bin/env python3
"""ESTIMATE Reaction Control System propellant sensitivity.

LM RCS 604 lb is sourced. SM and CM loaded pounds are UNKNOWN and stay parameters.
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
from rocket import delta_v_ft_per_s, delta_v_per_isp_s, range_pair, total_impulse_lbf_s  # noqa: E402
from sourced import published_inputs  # noqa: E402


def _fmt(value: float) -> str:
    return f"{value:,.4f}".rstrip("0").rstrip(".")


def _impulse_lines(name: str, load_lb: float, thrust_lbf: float, isps: list[float]) -> None:
    if not isps:
        parameter(f"{name}: pass --isp-s to turn {load_lb:g} lb into total impulse / Δv")
        return
    impulses = []
    for isp in isps:
        impulse = total_impulse_lbf_s(load_lb, isp)
        impulses.append(impulse)
        estimate(f"{name} load {load_lb:g} lb, Isp={isp:g} s → total impulse {_fmt(impulse)} lbf·s")
        estimate(
            f"{name} {thrust_lbf:g} lbf continuous (one engine) at Isp={isp:g} s → "
            f"ideal single-engine time {_fmt(impulse / thrust_lbf)} s"
        )
    lo, hi = range_pair(impulses)
    estimate(f"{name} total-impulse range {_fmt(lo)} … {_fmt(hi)} lbf·s")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="ESTIMATE RCS propellant sensitivity. Not a NASA fact."
    )
    parser.add_argument(
        "--sm-load-lb",
        type=float,
        action="append",
        default=[],
        help="SM RCS loaded propellant in lb (parameter). Repeat for a range.",
    )
    parser.add_argument(
        "--cm-load-lb",
        type=float,
        action="append",
        default=[],
        help="CM RCS loaded propellant in lb (parameter). Repeat for a range.",
    )
    parser.add_argument(
        "--isp-s",
        type=float,
        action="append",
        default=[],
        help="Specific impulse in seconds (parameter; not an Apollo citation).",
    )
    parser.add_argument(
        "--vehicle-lb",
        type=float,
        default=None,
        help="Vehicle mass for a Δv estimate (parameter; phase-dependent, not sourced).",
    )
    args = parser.parse_args(argv)

    banner()
    pub = published_inputs()
    sourced(f"LM RCS {pub['lm_rcs_lb']:,.0f} lb, {pub['lm_rcs_thrust_lbf']:g} lbf/engine (A11 PK p.93 / p.106)")
    sourced(f"SM RCS {pub['sm_rcs_thrust_lbf']:g} lbf/engine (A11 PK p.93 / p.106)")
    sourced(f"CM RCS {pub['cm_rcs_thrust_lbf']:g} lbf/engine (A11 PK p.93 / p.106)")
    sourced(f"SM RCS loaded on the model: {pub['sm_rcs_loaded']}")
    sourced(f"CM RCS loaded on the model: {pub['cm_rcs_loaded']}")
    parameter("Loaded SM RCS propellant mass stays unmarked.")
    parameter("Loaded CM RCS propellant mass stays unmarked.")
    parameter("RCS specific impulse is not on the model.")
    note("Thrust is sourced. Load × Isp → total impulse. Vehicle mass for Δv is a separate parameter.")

    _impulse_lines("LM RCS (sourced 604 lb)", pub["lm_rcs_lb"], pub["lm_rcs_thrust_lbf"], args.isp_s)

    if args.sm_load_lb:
        sm_lo, sm_hi = range_pair(args.sm_load_lb)
        parameter(f"Caller SM RCS load range {sm_lo:g} … {sm_hi:g} lb (not a sourced SM load)")
        for load in sorted(args.sm_load_lb):
            _impulse_lines("SM RCS (caller load)", load, pub["sm_rcs_thrust_lbf"], args.isp_s)
    else:
        parameter("Pass --sm-load-lb to sweep a caller SM RCS load. No Apollo SM load is assumed.")

    if args.cm_load_lb:
        cm_lo, cm_hi = range_pair(args.cm_load_lb)
        parameter(f"Caller CM RCS load range {cm_lo:g} … {cm_hi:g} lb (not a sourced CM load)")
        for load in sorted(args.cm_load_lb):
            _impulse_lines("CM RCS (caller load)", load, pub["cm_rcs_thrust_lbf"], args.isp_s)
    else:
        parameter("Pass --cm-load-lb to sweep a caller CM RCS load. No Apollo CM load is assumed.")

    if args.vehicle_lb is not None:
        parameter(f"Caller vehicle mass {args.vehicle_lb:g} lb (not a sourced RCS-phase mass)")
        loads: list[tuple[str, float]] = [("LM RCS sourced", pub["lm_rcs_lb"])]
        loads.extend(("SM RCS caller", load) for load in args.sm_load_lb)
        loads.extend(("CM RCS caller", load) for load in args.cm_load_lb)
        if args.isp_s:
            dvs: list[float] = []
            for name, load in loads:
                if load >= args.vehicle_lb:
                    estimate(f"{name} load {load:g} lb ≥ vehicle {args.vehicle_lb:g} lb — skipped")
                    continue
                coeff = delta_v_per_isp_s(args.vehicle_lb, args.vehicle_lb - load)
                estimate(f"{name} {load:g} lb on {args.vehicle_lb:g} lb → Δv/Isp = {_fmt(coeff)} (ft/s)/s")
                for isp in args.isp_s:
                    dv = delta_v_ft_per_s(args.vehicle_lb, args.vehicle_lb - load, isp)
                    dvs.append(dv)
                    estimate(f"{name} {load:g} lb, Isp={isp:g} s → Δv = {_fmt(dv)} ft/s")
            if dvs:
                lo, hi = range_pair(dvs)
                estimate(f"RCS Δv range {_fmt(lo)} … {_fmt(hi)} ft/s")
        else:
            parameter("Pass --isp-s with --vehicle-lb to print an RCS Δv range.")
    else:
        parameter("Pass --vehicle-lb if you want a Δv range. Phase mass is not on the model.")

    estimate("No SM/CM RCS loaded mass is printed as a fact. The teaching notes stay unmarked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
