"""Apollo 11 / Block II full system + subsystem model."""

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
    "apollo-csm",
    "apollo-sat-bdd",
    "apollo-sat-ibd",
    "apollo-lm",
    "apollo-gnd",
    "apollo-gnd-bdd",
    "apollo-eclss",
    "apollo-eclss-par",
    "apollo-crew",
    "apollo-usb",
    "apollo-cmd",
)

REQUIRED_DEF_IDS = (
    "Apollo",
    "Apollo.SaturnV",
    "Apollo.SIC",
    "Apollo.SII",
    "Apollo.SIVB",
    "Apollo.IU",
    "Apollo.LVDC",
    "Apollo.LES",
    "Apollo.SLA",
    "Apollo.CSM",
    "Apollo.CM",
    "Apollo.SM",
    "Apollo.SCS",
    "Apollo.AGC_CM",
    "Apollo.IMU",
    "Apollo.DSKY",
    "Apollo.SPS",
    "Apollo.RCS_CM",
    "Apollo.ECLSS",
    "Apollo.LM",
    "Apollo.Descent",
    "Apollo.Ascent",
    "Apollo.PNGS",
    "Apollo.AGC_LM",
    "Apollo.AGS",
    "Apollo.DPS",
    "Apollo.APS",
    "Apollo.RCS_LM",
    "Apollo.LandingRadar",
    "Apollo.RendezvousRadar",
    "Apollo.Crew",
    "Apollo.CDR",
    "Apollo.CMP",
    "Apollo.LMP",
    "Apollo.A7L",
    "Apollo.PLSS",
    "Apollo.KSC_LCC",
    "Apollo.MCC",
    "Apollo.MCC_H",
    "Apollo.MOCR",
    "Apollo.FLIGHT",
    "Apollo.CAPCOM",
    "Apollo.EECOM",
    "Apollo.CCC",
    "Apollo.CCATS",
    "Apollo.P27",
    "Apollo.GSFC",
    "Apollo.NTTF",
    "Apollo.LC39",
    "Apollo.RSO",
    "Apollo.AFETR",
    "Apollo.Recovery",
    "Apollo.Hornet",
    "Apollo.AIS_Vanguard",
    "Apollo.AIS_Huntsville",
    "Apollo.AIS_Redstone",
    "Apollo.AIS_4th",
    "Apollo.ARIA",
    "Apollo.Goldstone210",
    "Apollo.Parkes",
    "Apollo.MSFN_30ft",
    "Apollo.HGA",
    "Apollo.Site642B",
    "Apollo.OPS",
    "Apollo.BioSensor",
    "Apollo.CrewComm",
    "Apollo.RTCC",
    "Apollo.MSFN",
    "Apollo.Goldstone",
    "Apollo.Madrid",
    "Apollo.Honeysuckle",
    "Apollo.NASCOM",
    "Apollo.USB",
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
    "Apollo.State.Mission.countdown",
    "Apollo.State.Mission.boost",
    "Apollo.State.Mission.earthOrbit",
    "Apollo.State.Mission.TLI",
    "Apollo.State.Mission.translunar",
    "Apollo.State.Mission.LOI",
    "Apollo.State.Mission.undock",
    "Apollo.State.Mission.DOI",
    "Apollo.State.Mission.descent",
    "Apollo.State.Mission.surfaceEVA",
    "Apollo.State.Mission.ascent",
    "Apollo.State.Mission.rendezvous",
    "Apollo.State.Mission.TEI",
    "Apollo.State.Mission.entry",
    "Apollo.State.Mission.recovery",
)

REQUIRED_ABORTS = (
    "Apollo.State.Abort.pad",
    "Apollo.State.Abort.I",
    "Apollo.State.Abort.II",
    "Apollo.State.Abort.III",
    "Apollo.State.Abort.IV",
    "Apollo.State.Abort.contingencyTLI",
    "Apollo.State.Abort.lunar",
    "Apollo.State.Abort.SPS",
)

FORBIDDEN_COLLAPSE = (
    "Apollo.AGC_CM",
    "Apollo.AGC_LM",
    "Apollo.DSKY",
    "Apollo.AGS",
    "Apollo.LVDC",
    "Apollo.USB",
)


class ApolloExampleTests(unittest.TestCase):
    def test_project_files_exist(self) -> None:
        self.assertTrue((APOLLO / "apollo-model.msml").exists())
        for stem in REQUIRED_VIEW_STEMS:
            self.assertTrue((APOLLO / f"{stem}.msmd").exists(), stem)
        self.assertFalse((APOLLO / "apollo-gnc.msmd").exists())

    def test_public_architecture_full_model(self) -> None:
        model = read_json_file(APOLLO / "apollo-model.msml")["model"]
        self.assertEqual(model["namespace"], "Apollo")
        defs = {item["id"]: item for item in model["definitions"]}
        for did in REQUIRED_DEF_IDS + REQUIRED_PHASES + REQUIRED_ABORTS:
            self.assertIn(did, defs, did)
        self.assertEqual(defs["Apollo.SIC"]["name"], "S-IC")
        self.assertEqual(defs["Apollo.SII"]["name"], "S-II")
        self.assertEqual(defs["Apollo.SIVB"]["name"], "S-IVB")
        self.assertEqual(defs["Apollo.AGC_CM"]["name"], "AGC_CM")
        self.assertEqual(defs["Apollo.AGC_LM"]["name"], "AGC_LM")
        self.assertEqual(defs["Apollo.Descent"]["name"], "descent")
        self.assertEqual(defs["Apollo.Ascent"]["name"], "ascent")
        self.assertEqual(defs["Apollo.LandingRadar"]["name"], "landingRadar")
        self.assertEqual(defs["Apollo.RendezvousRadar"]["name"], "rendezvousRadar")
        self.assertEqual(defs["Apollo.KSC_LCC"]["name"], "KSC_LCC")
        self.assertEqual(defs["Apollo.crewSafetyRequirement"]["req_id"], "REQ-001")
        self.assertEqual(defs["Apollo.landingRequirement"]["req_id"], "REQ-002")
        self.assertEqual(defs["Apollo.commsContinuityRequirement"]["req_id"], "REQ-003")
        props = {
            item["name"]: item.get("type")
            for item in defs["Apollo"]["compartments"]["properties"]
        }
        self.assertEqual(props["instance"], "Apollo 11 / Block II")
        self.assertEqual(props["stack"], "generic Saturn V + CSM + LM")

    def test_does_not_collapse_required_computers(self) -> None:
        model = read_json_file(APOLLO / "apollo-model.msml")["model"]
        defs = {item["id"]: item for item in model["definitions"]}
        for did in FORBIDDEN_COLLAPSE:
            self.assertIn(did, defs, did)
        self.assertNotEqual(defs["Apollo.AGC_CM"]["id"], defs["Apollo.AGC_LM"]["id"])
        names = {item["name"].lower() for item in model["definitions"]}
        self.assertIn("vanguard", names)
        self.assertIn("huntsville", names)
        self.assertIn("redstone", names)
        self.assertIn("UNKNOWN", defs["Apollo.AIS_4th"]["name"])
        for ship in ("mercury", "arco", "watertown"):
            self.assertNotIn(ship, names)
        thirty = {
            p["name"]: p["type"]
            for p in defs["Apollo.MSFN_30ft"]["compartments"]["properties"]
        }
        self.assertIn("do not merge", thirty["doNot"].lower())
        self.assertIn("the 14", thirty["doNot"])
        self.assertNotEqual(defs["Apollo.RSO"]["id"], defs["Apollo.FLIGHT"]["id"])
        self.assertNotEqual(defs["Apollo.P27"]["id"], defs["Apollo.CCATS"]["id"])
        p27 = {p["name"]: p["type"] for p in defs["Apollo.P27"]["compartments"]["properties"]}
        self.assertIn("V70–V73", p27["verbs"])
        rtcc = {p["name"]: p["type"] for p in defs["Apollo.RTCC"]["compartments"]["properties"]}
        self.assertEqual(rtcc["a11WhichIsWhich"], "UNKNOWN")
        usb = {p["name"]: p["type"] for p in defs["Apollo.USB"]["compartments"]["properties"]}
        self.assertEqual(usb["csmUplink"], "2106.40625 MHz")
        self.assertEqual(usb["csmPmDown"], "2287.5 MHz PM")
        self.assertEqual(usb["lmUplink"], "2101.802 MHz")
        self.assertIn("UNKNOWN", defs["Apollo.Note.UnknownFood"]["text"])
        self.assertIn("UNKNOWN", defs["Apollo.Note.UnknownBlackout"]["text"])
        # Vehicles + AGC research still incoming — do not invent AGC numbers.
        agc_cm = {p["name"]: p.get("type") for p in defs["Apollo.AGC_CM"]["compartments"]["properties"]}
        self.assertNotIn("memory", agc_cm)
        self.assertNotIn("cycleTime", agc_cm)

    def test_instance_is_apollo_11_block_ii(self) -> None:
        model = read_json_file(APOLLO / "apollo-model.msml")["model"]
        defs = {item["id"]: item for item in model["definitions"]}
        note = defs["Apollo.Note.Instance"]["text"]
        self.assertIn("Apollo 11 / Block II", note)
        self.assertIn("generic Saturn V + CSM + LM", note)
        atypical = defs["Apollo.Note.Atypical"]["text"]
        for mission in ("Apollo 7", "Apollo 8", "Apollo 10", "Apollo 13"):
            self.assertIn(mission, atypical)
        for extra in ("apollo-7", "apollo-8", "apollo-10", "apollo-13"):
            self.assertFalse((ROOT / "projects" / extra).exists(), extra)

    def test_context_is_vehicle_crew_mcc_msfn_moon_earth(self) -> None:
        text = (APOLLO / "apollo-ctx.msmd").read_text(encoding="utf-8")
        for ref in (
            "Apollo",
            "Apollo.Crew",
            "Apollo.MCC",
            "Apollo.MSFN",
            "Apollo.Moon",
            "Apollo.Earth",
            "Apollo.RTCC",
        ):
            self.assertIn(ref, text)
        self.assertIn("uplink", text)
        self.assertIn("downlink", text)
        self.assertIn("backup voice", text)
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
