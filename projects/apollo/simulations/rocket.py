"""Rocket-equation helpers. g0 is a unit convention, not an Apollo number."""

from __future__ import annotations

import math

# Standard gravity used with English-unit specific impulse (seconds).
# Not an Apollo measurement and not a sourced vehicle figure.
G0_FT_PER_S2 = 32.174


def require_positive(name: str, value: float) -> float:
    if value <= 0:
        raise ValueError(f"{name} must be > 0, got {value}")
    return value


def mass_ratio(m0_lb: float, mf_lb: float) -> float:
    require_positive("m0_lb", m0_lb)
    require_positive("mf_lb", mf_lb)
    if mf_lb >= m0_lb:
        raise ValueError(f"mf_lb ({mf_lb}) must be < m0_lb ({m0_lb})")
    return m0_lb / mf_lb


def ln_mass_ratio(m0_lb: float, mf_lb: float) -> float:
    return math.log(mass_ratio(m0_lb, mf_lb))


def delta_v_per_isp_s(m0_lb: float, mf_lb: float) -> float:
    """ft/s of Δv per second of specific impulse. ESTIMATE coefficient."""
    return G0_FT_PER_S2 * ln_mass_ratio(m0_lb, mf_lb)


def delta_v_ft_per_s(m0_lb: float, mf_lb: float, isp_s: float) -> float:
    require_positive("isp_s", isp_s)
    return isp_s * delta_v_per_isp_s(m0_lb, mf_lb)


def burn_time_s(propellant_lb: float, thrust_lbf: float, isp_s: float) -> float:
    """Constant-thrust estimate. In lbf/lbm units, mdot (lbm/s) = F_lbf / Isp."""
    require_positive("propellant_lb", propellant_lb)
    require_positive("thrust_lbf", thrust_lbf)
    require_positive("isp_s", isp_s)
    return propellant_lb / (thrust_lbf / isp_s)


def total_impulse_lbf_s(propellant_lb: float, isp_s: float) -> float:
    require_positive("propellant_lb", propellant_lb)
    require_positive("isp_s", isp_s)
    return propellant_lb * isp_s


def range_pair(values: list[float]) -> tuple[float, float]:
    if not values:
        raise ValueError("need at least one value")
    return min(values), max(values)
