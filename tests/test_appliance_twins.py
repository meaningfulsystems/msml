import json
import unittest
from pathlib import Path

from msml import validate, validate_all
from msml.io import read_json_file

ROOT = Path(__file__).resolve().parents[1]
TOASTER = ROOT / "projects/appliances/toaster"
BLENDER = ROOT / "projects/appliances/blender"

TOASTER_REQ_IDS = {
    "Toaster.toastSafetyRequirement": "REQ-001",
    "Toaster.electricalSafetyRequirement": "REQ-002",
    "Toaster.browningRequirement": "REQ-003",
    "Toaster.timingRequirement": "REQ-004",
    "Toaster.userInterfaceRequirement": "REQ-005",
    "Toaster.cleanabilityRequirement": "REQ-006",
    "Toaster.serviceabilityRequirement": "REQ-007",
    "Toaster.powerRatingRequirement": "REQ-008",
    "Toaster.surfaceTemperatureRequirement": "REQ-009",
    "Toaster.thermalCutoffRequirement": "REQ-010",
    "Toaster.browningLevelsRequirement": "REQ-011",
    "Toaster.carriageReleaseRequirement": "REQ-012",
    "Toaster.crumbTrayForceRequirement": "REQ-013",
    "Toaster.cycleLifeRequirement": "REQ-014",
}

DROPPED_TOASTER_IDS = (
    "Toaster.REQ-001.1",
    "Toaster.REQ-001.2",
    "Toaster.REQ-002.1",
    "Toaster.REQ-001",
    "Toaster.REQ-001.3",
    "Toaster.REQ-001.4",
    "Toaster.REQ-002",
    "Toaster.REQ-002.2",
    "Toaster.REQ-003",
    "Toaster.REQ-003.1",
)

BLENDER_REQ_IDS = {
    "Blender.lidInterlockRequirement": "REQ-001",
    "Blender.motorControlRequirement": "REQ-002",
    "Blender.smoothnessDetectionRequirement": "REQ-003",
    "Blender.powerRequirement": "REQ-004",
    "Blender.userControlsRequirement": "REQ-005",
    "Blender.cleaningRequirement": "REQ-006",
    "Blender.serviceRequirement": "REQ-007",
    "Blender.motorSpeedRequirement": "REQ-008",
    "Blender.interlockLatencyRequirement": "REQ-009",
    "Blender.overcurrentProtectionRequirement": "REQ-010",
    "Blender.smoothnessThresholdRequirement": "REQ-011",
    "Blender.noiseRequirement": "REQ-012",
    "Blender.containerSeatRequirement": "REQ-013",
}

INVENTED_APPLIANCE_NUMBERS = (
    "900–1200",
    "900-1200",
    "20,000 rpm",
    "100 ms",
    "250 ms",
    "5–15 N",
)


def _defs(model_path: Path) -> dict:
    model = read_json_file(model_path)["model"]
    return {item["id"]: item for item in model["definitions"]}


def _rels(model_path: Path) -> dict:
    model = read_json_file(model_path)["model"]
    return {item["id"]: item for item in model["relationships"]}


class ApplianceTwinTests(unittest.TestCase):
    def test_toaster_sysml2d_requirements(self):
        defs = _defs(TOASTER / "toaster-model.msml")
        for did, req_id in TOASTER_REQ_IDS.items():
            self.assertIn(did, defs, did)
            self.assertEqual(defs[did]["req_id"], req_id)
            self.assertEqual(defs[did]["type"], "requirement")
        for dropped in DROPPED_TOASTER_IDS:
            self.assertNotIn(dropped, defs, dropped)

        levels = defs["Toaster.browningLevelsRequirement"]["text"]
        self.assertIn("at least three", levels)
        force = defs["Toaster.crumbTrayForceRequirement"]["text"]
        self.assertIn("10 N", force)
        life = defs["Toaster.cycleLifeRequirement"]["text"]
        self.assertIn("10,000", life)
        timing = defs["Toaster.timingRequirement"]["text"]
        self.assertIn("±5%", timing)
        self.assertIn("selected setting", timing)
        self.assertNotIn("energy variance", timing.lower())

        cutoff = defs["Toaster.thermalCutoffRequirement"]["text"]
        self.assertIn("safe threshold", cutoff)
        self.assertNotIn("300", cutoff)
        power = defs["Toaster.powerRatingRequirement"]["text"]
        self.assertIn("rated power", power.lower())

        self.assertIn("Toaster.CrumbTray", defs)
        self.assertIn("Toaster.Chassis", defs)

    def test_toaster_forbids_dropped_sysml1_numbers(self):
        blob = (TOASTER / "toaster-model.msml").read_text(encoding="utf-8")
        note = (TOASTER / "architecture-summary.md").read_text(encoding="utf-8")
        for text in (blob, note):
            self.assertNotIn("30s", text)
            self.assertNotIn("30 s", text)
            self.assertNotIn("1–5 min", text)
            self.assertNotIn("1-5 min", text)
            self.assertNotIn("300°C", text)
            self.assertNotIn("300 °C", text)
            for invented in INVENTED_APPLIANCE_NUMBERS:
                self.assertNotIn(invented, text)
        self.assertNotIn("start(90s)", blob)
        self.assertIn("≥3", note)
        self.assertIn("10 N", note)
        self.assertIn("10,000", note)
        self.assertIn("±5%", note)

    def test_toaster_allocations_and_parts(self):
        rels = _rels(TOASTER / "toaster-model.msml")
        expected = {
            "sat-toaster.levels": ("Toaster.BrowningControl", "Toaster.browningLevelsRequirement"),
            "sat-toaster.crumb-force": ("Toaster.CrumbTray", "Toaster.crumbTrayForceRequirement"),
            "sat-toaster.cycle": ("Toaster", "Toaster.cycleLifeRequirement"),
            "sat-toaster.timing": ("Toaster.Timer", "Toaster.timingRequirement"),
            "sat-toaster.cutoff": ("Toaster.ThermalCutoff", "Toaster.thermalCutoffRequirement"),
            "sat-toaster.surface": ("Toaster.Chassis", "Toaster.surfaceTemperatureRequirement"),
            "sat-toaster.clean": ("Toaster.CrumbTray", "Toaster.cleanabilityRequirement"),
            "sat-toaster.carriage": ("Toaster.Carriage", "Toaster.carriageReleaseRequirement"),
        }
        for rid, (source, target) in expected.items():
            self.assertIn(rid, rels, rid)
            self.assertEqual(rels[rid]["source"], source)
            self.assertEqual(rels[rid]["target"], target)
        self.assertEqual(rels["bdd-toaster.c-toaster-crumb"]["target"], "Toaster.CrumbTray")
        self.assertEqual(rels["bdd-toaster.c-toaster-chassis"]["target"], "Toaster.Chassis")
        for rid in rels:
            self.assertFalse(rid.startswith("req-toaster.r"), rid)
            self.assertFalse(rid.startswith("req-toaster.d"), rid)

    def test_toaster_views_bind_new_ids(self):
        req = json.loads((TOASTER / "toaster-req.msmd").read_text(encoding="utf-8"))
        refs = {el["model_ref"] for el in req["diagram"]["elements"]}
        self.assertEqual(refs, set(TOASTER_REQ_IDS))
        self.assertEqual(req["diagram"]["relationships"], [])
        reqt = json.loads((TOASTER / "toaster-reqt.msmd").read_text(encoding="utf-8"))
        table_refs = {el["model_ref"] for el in reqt["diagram"]["elements"]}
        self.assertEqual(table_refs, set(TOASTER_REQ_IDS))
        bdd = (TOASTER / "toaster-bdd.msmd").read_text(encoding="utf-8")
        self.assertIn("Toaster.CrumbTray", bdd)
        self.assertIn("Toaster.Chassis", bdd)

    def test_blender_sysml2d_requirements(self):
        defs = _defs(BLENDER / "blender-model.msml")
        self.assertEqual(
            {did for did, item in defs.items() if item.get("type") == "requirement"},
            set(BLENDER_REQ_IDS),
        )
        for did, req_id in BLENDER_REQ_IDS.items():
            self.assertEqual(defs[did]["req_id"], req_id)
        interlock = defs["Blender.interlockLatencyRequirement"]["text"]
        self.assertIn("50 ms", interlock)
        speed = defs["Blender.motorSpeedRequirement"]["text"]
        self.assertIn("±10%", speed)
        noise = defs["Blender.noiseRequirement"]["text"]
        self.assertIn("85 dB(A)", noise)
        overcurrent = defs["Blender.overcurrentProtectionRequirement"]["text"]
        self.assertIn("overcurrent", overcurrent.lower())
        self.assertIn("before motor damage", overcurrent)
        control = defs["Blender.motorControlRequirement"]["text"]
        self.assertIn("200 ms", control)
        threshold = defs["Blender.smoothnessThresholdRequirement"]["text"]
        self.assertIn("at least three", threshold)

    def test_blender_allocations(self):
        rels = _rels(BLENDER / "blender-model.msml")
        expected = {
            "allocateInterlockToControlPanel": (
                "Blender.lidInterlockRequirement",
                "Blender.ControlPanel",
            ),
            "allocateTorqueToMotor": ("Blender.motorControlRequirement", "Blender.Motor"),
            "allocateSmoothnessToSensor": (
                "Blender.smoothnessDetectionRequirement",
                "Blender.SmoothieCompleteSensor",
            ),
            "allocateCleaningToContainer": ("Blender.cleaningRequirement", "Blender.Container"),
            "allocateProtectionToMotorBase": (
                "Blender.overcurrentProtectionRequirement",
                "Blender.MotorBase",
            ),
            "allocateInterfaceToControlPanel": (
                "Blender.userControlsRequirement",
                "Blender.ControlPanel",
            ),
            "sat-blender.speed": ("Blender.Motor", "Blender.motorSpeedRequirement"),
            "sat-blender.interlock-latency": (
                "Blender.ControlPanel",
                "Blender.interlockLatencyRequirement",
            ),
            "sat-blender.noise": ("Blender.Motor", "Blender.noiseRequirement"),
        }
        for rid, (source, target) in expected.items():
            self.assertIn(rid, rels, rid)
            self.assertEqual(rels[rid]["source"], source)
            self.assertEqual(rels[rid]["target"], target)

    def test_blender_forbids_invented_numbers(self):
        blob = (BLENDER / "blender-model.msml").read_text(encoding="utf-8")
        note = (BLENDER / "architecture-summary.md").read_text(encoding="utf-8")
        for text in (blob, note):
            for invented in INVENTED_APPLIANCE_NUMBERS:
                self.assertNotIn(invented, text)
            self.assertNotIn("20,000", text)
        self.assertIn("50 ms", note)
        self.assertIn("±10%", note)
        self.assertIn("85 dB(A)", note)
        self.assertIn("overcurrent", note.lower())

    def test_appliance_views_validate(self):
        toaster = validate_all(TOASTER, strict=True)
        self.assertEqual(toaster.errors, 0, toaster)
        blender = validate_all(BLENDER, strict=True)
        self.assertEqual(blender.errors, 0, blender)
        for name in ("blender-req.msmd", "blender-reqt.msmd"):
            report = validate(BLENDER / name, strict=True)
            self.assertEqual(report.errors, 0, name)


if __name__ == "__main__":
    unittest.main()
