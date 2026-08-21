"""Apollo 11-class skeleton: public NASA architecture, in progress."""

from __future__ import annotations

import unittest
from pathlib import Path

from msml import validate, validate_all
from msml.io import read_json_file
from msml.render_all import render_all


ROOT = Path(__file__).resolve().parents[1]
APOLLO = ROOT / "projects/apollo"

REQUIRED_VIEW_STEMS = (
    "apollo-bdd",
    "apollo-ibd",
    "apollo-ctx",
    "apollo-stm",
    "apollo-act",
    "apollo-seq",
    "apollo-req",
    "apollo-pkg",
)

REQUIRED_DEF_IDS = (
    "Apollo",
    "Apollo.SaturnV",
    "Apollo.SIC",
    "Apollo.SII",
    "Apollo.SIVB",
    "Apollo.IU",
    "Apollo.LES",
    "Apollo.SLA",
    "Apollo.CSM",
    "Apollo.CM",
    "Apollo.SM",
    "Apollo.LM",
    "Apollo.LMDescent",
    "Apollo.LMAscent",
    "Apollo.Crew",
    "Apollo.ECLSS",
    "Apollo.AGC",
    "Apollo.LGC",
    "Apollo.AGS",
    "Apollo.IMU",
    "Apollo.DSKY",
    "Apollo.MCC",
    "Apollo.MSFN",
    "Apollo.USB",
    "Apollo.GroundComputer",
    "Apollo.Moon",
    "Apollo.Earth",
    "Apollo.LaunchVehicle",
    "Apollo.Spacecraft",
    "Apollo.CrewECLSS",
    "Apollo.GNC",
    "Apollo.Ground",
    "Apollo.Comms",
    "Apollo.Mission",
    "Apollo.crewSafetyRequirement",
    "Apollo.landingRequirement",
    "Apollo.commsContinuityRequirement",
)

REQUIRED_PHASES = (
    "Apollo.State.Mission.launch",
    "Apollo.State.Mission.tli",
    "Apollo.State.Mission.loi",
    "Apollo.State.Mission.landing",
    "Apollo.State.Mission.ascent",
    "Apollo.State.Mission.tei",
    "Apollo.State.Mission.entry",
)


class ApolloExampleTests(unittest.TestCase):
    def test_project_files_exist(self) -> None:
        self.assertTrue((APOLLO / "apollo-model.msml").exists())
        for stem in REQUIRED_VIEW_STEMS:
            self.assertTrue((APOLLO / f"{stem}.msmd").exists(), stem)

    def test_public_architecture_skeleton(self) -> None:
        model = read_json_file(APOLLO / "apollo-model.msml")["model"]
        self.assertEqual(model["namespace"], "Apollo")
        defs = {item["id"]: item for item in model["definitions"]}
        for did in REQUIRED_DEF_IDS + REQUIRED_PHASES:
            self.assertIn(did, defs, did)
        self.assertEqual(defs["Apollo.crewSafetyRequirement"]["req_id"], "REQ-001")
        self.assertEqual(defs["Apollo.landingRequirement"]["req_id"], "REQ-002")
        self.assertEqual(defs["Apollo.commsContinuityRequirement"]["req_id"], "REQ-003")

    def test_context_is_vehicle_crew_mcc_msfn_moon_earth(self) -> None:
        text = (APOLLO / "apollo-ctx.msmd").read_text(encoding="utf-8")
        for ref in (
            "Apollo",
            "Apollo.Crew",
            "Apollo.MCC",
            "Apollo.MSFN",
            "Apollo.Moon",
            "Apollo.Earth",
        ):
            self.assertIn(ref, text)
        self.assertNotIn("ElectricBike", text)

    def test_views_validate_strict(self) -> None:
        report = validate_all(APOLLO, strict=True)
        self.assertEqual(report.errors, 0)
        for stem in REQUIRED_VIEW_STEMS:
            report = validate(APOLLO / f"{stem}.msmd", strict=True)
            self.assertEqual(report.errors, 0, stem)

    def test_rendered_pngs(self) -> None:
        self.assertEqual(render_all(APOLLO), 0)
        for stem in REQUIRED_VIEW_STEMS:
            png = APOLLO / f"{stem}.png"
            self.assertTrue(png.exists(), png.name)
            self.assertGreater(png.stat().st_size, 1000, png.name)
