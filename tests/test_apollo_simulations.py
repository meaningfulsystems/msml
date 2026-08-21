"""Educational Apollo estimate scripts — they must not become requirements."""

from __future__ import annotations

import math
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APOLLO = ROOT / "projects/apollo"
SIM = APOLLO / "simulations"
NOTE = APOLLO / "architecture-summary.md"
README = SIM / "README.md"
HOS_NOTE = ROOT / "projects/humanity-optimization/architecture-summary.md"

SCRIPTS = (
    SIM / "estimate_delta_v.py",
    SIM / "estimate_sps_load.py",
    SIM / "estimate_rcs.py",
    SIM / "estimate_stack_mass.py",
    SIM / "run_all.py",
)


def _run(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        check=True,
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )


class ApolloSimulationTests(unittest.TestCase):
    def test_folder_and_readme_exist(self) -> None:
        self.assertTrue(SIM.is_dir())
        self.assertTrue(README.is_file())
        for script in SCRIPTS:
            self.assertTrue(script.is_file(), script.name)

    def test_readme_forbids_promoting_estimates_into_shalls(self) -> None:
        text = README.read_text(encoding="utf-8")
        lowered = text.lower()
        self.assertIn("not a nasa fact", lowered)
        self.assertIn("educational", lowered)
        self.assertIn("shall", lowered)
        self.assertIn("architecture-summary", lowered)
        self.assertIn("never copy", lowered)
        self.assertIn("never turn an estimate into a *shall*", lowered)
        self.assertIn("do not promote", lowered)
        self.assertIn("unmarked", lowered)
        self.assertIn("parameter", lowered)
        self.assertIn("unreconciled", lowered)
        for phrase in (
            "official csm lunar",
            "service propulsion",
            "reaction control",
        ):
            self.assertIn(phrase, lowered)

    def test_scripts_run_and_label_estimate(self) -> None:
        for script in SCRIPTS:
            result = _run(script)
            self.assertEqual(result.returncode, 0, script.name)
            out = result.stdout
            self.assertIn("ESTIMATE", out, script.name)
            self.assertIn("not a NASA fact", out, script.name)
            self.assertIn("shall", out.lower(), script.name)
            self.assertNotIn("NASA fact:", out)

    def test_delta_v_keeps_isp_as_parameter_and_prints_a_range(self) -> None:
        bare = _run(SIM / "estimate_delta_v.py")
        self.assertIn("PARAMETER", bare.stdout)
        self.assertIn("Specific impulse", bare.stdout)
        self.assertIn("UNRECONCILED", bare.stdout)
        self.assertIn("Δv/Isp", bare.stdout)
        self.assertIn("range", bare.stdout.lower())
        self.assertNotIn("NASA Isp", bare.stdout)

        swept = _run(SIM / "estimate_delta_v.py", "--isp-s", "260", "--isp-s", "305")
        self.assertIn("ESTIMATE", swept.stdout)
        self.assertIn("Caller Isp", swept.stdout)
        self.assertIn("not an Apollo citation", swept.stdout)
        self.assertIn("…", swept.stdout)
        self.assertIn("unmarked", swept.stdout.lower())

    def test_sps_and_rcs_unknowns_stay_parameters(self) -> None:
        sps = _run(SIM / "estimate_sps_load.py")
        self.assertIn("UNKNOWN", sps.stdout)
        self.assertIn("CSM-107", sps.stdout)
        self.assertIn("PARAMETER", sps.stdout)
        self.assertIn("20,500", sps.stdout)
        self.assertIn("21,500", sps.stdout)
        self.assertIn("1.6", sps.stdout)
        self.assertIn("unmarked", sps.stdout.lower())

        sps_range = _run(
            SIM / "estimate_sps_load.py",
            "--sps-load-lb",
            "20000",
            "--sps-load-lb",
            "40000",
            "--isp-s",
            "300",
            "--isp-s",
            "314",
        )
        self.assertIn("ESTIMATE", sps_range.stdout)
        self.assertIn("Δv range", sps_range.stdout)
        self.assertIn("not a sourced CSM-107 load", sps_range.stdout)

        rcs = _run(SIM / "estimate_rcs.py")
        self.assertIn("604", rcs.stdout)
        self.assertIn("UNKNOWN", rcs.stdout)
        self.assertIn("SM RCS", rcs.stdout)
        self.assertIn("CM RCS", rcs.stdout)
        self.assertIn("PARAMETER", rcs.stdout)
        self.assertIn("unmarked", rcs.stdout.lower())

    def test_stack_budget_does_not_close_or_invent_sa507_sp4029(self) -> None:
        out = _run(SIM / "estimate_stack_mass.py").stdout
        self.assertIn("UNRECONCILED", out)
        self.assertIn("not a sourced SLA mass", out)
        self.assertIn("SA-507", out)
        self.assertIn("SP-4029", out)
        self.assertIn("not on this model", out)
        self.assertIn("must not be forced", out.lower())
        self.assertIn("ESTIMATE", out)
        self.assertNotIn("NASA SP-4029 p.", out)

    def test_rocket_equation_matches_known_identity(self) -> None:
        sys.path.insert(0, str(SIM))
        import rocket  # type: ignore

        e = math.e
        self.assertAlmostEqual(rocket.delta_v_ft_per_s(e, 1.0, 1.0), rocket.G0_FT_PER_S2)
        self.assertAlmostEqual(rocket.delta_v_per_isp_s(e, 1.0), rocket.G0_FT_PER_S2)
        self.assertAlmostEqual(rocket.burn_time_s(314.0, 314.0, 1.0), 1.0)
        self.assertAlmostEqual(rocket.total_impulse_lbf_s(10.0, 280.0), 2800.0)

    def test_architecture_notes_stay_unmarked_and_have_no_estimates(self) -> None:
        note = NOTE.read_text(encoding="utf-8")
        self.assertIn("Official CSM lunar Δv table", note)
        self.assertIn("CSM-107 SPS loaded mass", note)
        self.assertIn("Loaded SM RCS propellant mass", note)
        self.assertIn("Loaded CM RCS propellant mass", note)
        self.assertIn("Do **not** invent", note)
        self.assertNotIn("ESTIMATE", note)
        self.assertNotIn("simulations/", note)
        self.assertNotIn("Δv/Isp", note)
        self.assertNotIn("ft/s)/s", note)

    def test_get_lock_untouched(self) -> None:
        note = NOTE.read_text(encoding="utf-8")
        model = (APOLLO / "apollo-model.msml").read_text(encoding="utf-8")
        for text in (note, model):
            self.assertIn("75:54:28", text)
            self.assertIn("A11-FP", text)
            self.assertIn("~075:49:50", text)
            self.assertIn("PAD/MR", text)
            self.assertNotIn("075:49:49.65", text)
            self.assertNotIn("A11-FP / Press Kit", text)
        self.assertIn("A11-FP **planned**", note)
        self.assertNotIn("do not cite Press Kit as the LOI-1 source", note)

    def test_hos_untouched_by_this_folder(self) -> None:
        self.assertTrue(HOS_NOTE.exists())
        hos = HOS_NOTE.read_text(encoding="utf-8")
        self.assertNotIn("projects/apollo/simulations", hos)
        self.assertNotIn("ESTIMATE — educational only", hos)
