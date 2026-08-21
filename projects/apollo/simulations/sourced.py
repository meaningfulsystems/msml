"""Pull published Apollo numbers from the model. Do not invent extras."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

MODEL_PATH = Path(__file__).resolve().parents[1] / "apollo-model.msml"

_LB = re.compile(r"([0-9][0-9,]*(?:\.[0-9]+)?)\s*lb\b", re.I)
_LBF = re.compile(r"([0-9][0-9,]*(?:\.[0-9]+)?)\s*lbf\b", re.I)


class UnknownOnModel(ValueError):
    """The model marks this value UNKNOWN — keep it a parameter."""


def load_model(path: Path | None = None) -> dict[str, Any]:
    return json.loads((path or MODEL_PATH).read_text(encoding="utf-8"))


def definitions(model: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    data = model if model is not None else load_model()
    return {item["id"]: item for item in data["model"]["definitions"]}


def prop_text(defs: dict[str, dict[str, Any]], block_id: str, name: str) -> str:
    block = defs[block_id]
    for item in block["compartments"]["properties"]:
        if item["name"] == name:
            return str(item.get("type") or "")
    raise KeyError(f"{block_id}.{name}")


def first_number(pattern: re.Pattern[str], text: str) -> float:
    match = pattern.search(text)
    if not match:
        raise ValueError(f"no number matching {pattern.pattern} in {text!r}")
    return float(match.group(1).replace(",", ""))


def sourced_lb(text: str, *, label: str) -> float:
    if "UNKNOWN" in text:
        raise UnknownOnModel(f"{label} is UNKNOWN on the model: {text}")
    return first_number(_LB, text)


def sourced_lbf(text: str, *, label: str) -> float:
    if "UNKNOWN" in text:
        raise UnknownOnModel(f"{label} is UNKNOWN on the model: {text}")
    return first_number(_LBF, text)


def is_unknown(text: str) -> bool:
    return "UNKNOWN" in text


def published_inputs(model: dict[str, Any] | None = None) -> dict[str, Any]:
    """Numbers the model already cites. Missing keys stay out of this dict."""
    defs = definitions(model)
    sic_fueled = sourced_lb(prop_text(defs, "Apollo.SIC", "fueled"), label="S-IC fueled")
    sic_dry = sourced_lb(prop_text(defs, "Apollo.SIC", "dry"), label="S-IC dry")
    sic_lox = sourced_lb(prop_text(defs, "Apollo.SIC", "lox"), label="S-IC LOX")
    sic_rp1 = sourced_lb(prop_text(defs, "Apollo.SIC", "rp1"), label="S-IC RP-1")
    sii_fueled = sourced_lb(prop_text(defs, "Apollo.SII", "fueled"), label="S-II fueled")
    sii_dry = sourced_lb(prop_text(defs, "Apollo.SII", "dry"), label="S-II dry")
    sii_lox = sourced_lb(prop_text(defs, "Apollo.SII", "lox"), label="S-II LOX")
    sii_lh2 = sourced_lb(prop_text(defs, "Apollo.SII", "lh2"), label="S-II LH2")
    sivb_fueled = sourced_lb(prop_text(defs, "Apollo.SIVB", "fueled"), label="S-IVB fueled")
    sivb_dry = sourced_lb(prop_text(defs, "Apollo.SIVB", "dry"), label="S-IVB dry")
    sivb_lox = sourced_lb(prop_text(defs, "Apollo.SIVB", "lox"), label="S-IVB LOX")
    sivb_lh2 = sourced_lb(prop_text(defs, "Apollo.SIVB", "lh2"), label="S-IVB LH2")
    return {
        "source_tank_rows": "A11 PK p.109 (model: Apollo.Note.TanksSourced)",
        "mass_budget_flag": prop_text(defs, "Apollo.SaturnV", "massBudget"),
        "ignition_lb": sourced_lb(prop_text(defs, "Apollo.SaturnV", "ignition"), label="ignition"),
        "first_motion_lb": sourced_lb(
            prop_text(defs, "Apollo.SaturnV", "firstMotion"), label="firstMotion"
        ),
        "delta_v_csm": prop_text(defs, "Apollo.SaturnV", "deltaV"),
        "sic": {
            "fueled_lb": sic_fueled,
            "dry_lb": sic_dry,
            "lox_lb": sic_lox,
            "rp1_lb": sic_rp1,
            "propellant_from_tanks_lb": sic_lox + sic_rp1,
            "propellant_from_fueled_minus_dry_lb": sic_fueled - sic_dry,
            "liftoff_thrust_lbf": sourced_lbf(
                prop_text(defs, "Apollo.SIC", "liftoffThrust"), label="S-IC liftoff"
            ),
            "source": prop_text(defs, "Apollo.SIC", "source"),
        },
        "sii": {
            "fueled_lb": sii_fueled,
            "dry_lb": sii_dry,
            "lox_lb": sii_lox,
            "lh2_lb": sii_lh2,
            "propellant_from_tanks_lb": sii_lox + sii_lh2,
            "propellant_from_fueled_minus_dry_lb": sii_fueled - sii_dry,
            "source": prop_text(defs, "Apollo.SII", "source"),
        },
        "sivb": {
            "fueled_lb": sivb_fueled,
            "dry_lb": sivb_dry,
            "lox_lb": sivb_lox,
            "lh2_lb": sivb_lh2,
            "propellant_from_tanks_lb": sivb_lox + sivb_lh2,
            "propellant_from_fueled_minus_dry_lb": sivb_fueled - sivb_dry,
            "source": prop_text(defs, "Apollo.SIVB", "source"),
        },
        "iu_lb": sourced_lb(prop_text(defs, "Apollo.IU", "mass"), label="IU"),
        "cm_launch_lb": sourced_lb(prop_text(defs, "Apollo.CM", "launch"), label="CM"),
        "sm_launch_lb": sourced_lb(prop_text(defs, "Apollo.SM", "launch"), label="SM"),
        "sm_sps_loaded": prop_text(defs, "Apollo.SM", "spsLoaded"),
        "lm_launch_lb": sourced_lb(prop_text(defs, "Apollo.LM", "launch"), label="LM"),
        "les_lb": sourced_lb(prop_text(defs, "Apollo.LES", "mass"), label="LES"),
        "dps_load_lb": sourced_lb(prop_text(defs, "Apollo.DPS", "load"), label="DPS load"),
        "aps_load_lb": sourced_lb(prop_text(defs, "Apollo.APS", "load"), label="APS load"),
        "lm_rcs_lb": sourced_lb(prop_text(defs, "Apollo.RCS_LM", "mass"), label="LM RCS"),
        "lm_rcs_thrust_lbf": sourced_lbf(
            prop_text(defs, "Apollo.RCS_LM", "thrust"), label="LM RCS thrust"
        ),
        "sm_rcs_thrust_lbf": sourced_lbf(
            prop_text(defs, "Apollo.RCS_SM", "thrust"), label="SM RCS thrust"
        ),
        "cm_rcs_thrust_lbf": sourced_lbf(
            prop_text(defs, "Apollo.RCS_CM", "thrust"), label="CM RCS thrust"
        ),
        "sm_rcs_loaded": prop_text(defs, "Apollo.RCS_SM", "loaded"),
        "cm_rcs_loaded": prop_text(defs, "Apollo.RCS_CM", "loaded"),
        "sps_loaded": prop_text(defs, "Apollo.SPS", "loaded"),
        "sps_of_ratio": prop_text(defs, "Apollo.SPS", "ofRatio"),
        "sps_thrust_pk_lbf": sourced_lbf(
            prop_text(defs, "Apollo.SPS", "thrustPk"), label="SPS PK thrust"
        ),
        "sps_thrust_tn_lbf": sourced_lbf(
            prop_text(defs, "Apollo.SPS", "thrustTn"), label="SPS TN thrust"
        ),
        "sps_thrust": prop_text(defs, "Apollo.SPS", "thrust"),
        "f1_thrust_lbf": sourced_lbf(prop_text(defs, "Apollo.F1", "thrust"), label="F-1"),
        "f1_source": prop_text(defs, "Apollo.F1", "source"),
        "sla_mass": None,
        "sla_serial": prop_text(defs, "Apollo.SLA", "serial"),
        "specific_impulse": None,
        "sa507_masses": None,
        "sp4029_masses": None,
    }
