import unittest
from pathlib import Path

from msml import validate, validate_all
from msml.io import read_json_file
from msml.render_all import render_all

ROOT = Path(__file__).resolve().parents[1]
EBIKE = ROOT / "projects/e-bike"

REQUIRED_VIEW_STEMS = (
    "e-bike-bdd",
    "e-bike-ibd",
    "e-bike-stm",
    "e-bike-act",
    "e-bike-int",
    "e-bike-uc",
    "e-bike-pkg",
    "e-bike-req",
    "e-bike-par",
    "e-bike-ctx",
    "e-bike-reqt",
    "e-bike-alloc",
    "e-bike-amx",
)

REQUIRED_DEF_IDS = (
    "ElectricBike",
    "ElectricBike.Frame",
    "ElectricBike.BatteryPack",
    "ElectricBike.MotorController",
    "ElectricBike.HubMotor",
    "ElectricBike.HumanInterface",
    "ElectricBike.BrakeSystem",
    "ElectricBike.Rider",
    "ElectricBike.Charger",
    "ElectricBike.Road",
    "ElectricBike.BikeModel",
    "ElectricBike.BikeStructure",
    "ElectricBike.BikeBehavior",
    "ElectricBike.BikeRequirements",
    "ElectricBike.BikeAnalysis",
    "ElectricBike.BikeVerification",
    "ElectricBike.RideControl",
    "ElectricBike.rideSafetyRequirement",
    "ElectricBike.rangeRequirement",
    "ElectricBike.assistLimitRequirement",
    "ElectricBike.chargeSafetyRequirement",
    "ElectricBike.brakeOverrideRequirement",
    "ElectricBike.batteryCutoffRequirement",
    "ElectricBike.displayRequirement",
    "ElectricBike.structuralRequirement",
    "ElectricBike.PAR.energyBalance",
    "ElectricBike.PAR.rangeEstimate",
    "ElectricBike.PAR.assistPowerLimit",
    "ElectricBike.PAR.brakeLatencyLimit",
    "ElectricBike.rangeAnalysis",
    "ElectricBike.brakeLatencyAnalysis",
    "ElectricBike.verifyRange",
    "ElectricBike.verifyBrakeCutoff",
    "ElectricBike.verifyChargeSafety",
    "ElectricBike.verifyAssistLimit",
    "ElectricBike.startRideInteraction",
    "ElectricBike.UC.rideBikeUseCase",
    "ElectricBike.UC.chargeBikeUseCase",
    "ElectricBike.UC.lockBikeUseCase",
    "ElectricBike.UC.adjustAssistUseCase",
)

REQUIRED_REL_IDS = (
    "allocateSafetyToBrakes",
    "allocateRangeToBattery",
    "allocateAssistToController",
    "allocateChargeToBms",
    "ibd-ebike.frameToBattery",
    "ibd-ebike.frameToMotor",
    "ibd-ebike.frameToInterface",
    "ibd-ebike.frameToBrakes",
    "ibd-ebike.batteryToController",
    "ibd-ebike.controllerToMotor",
    "ibd-ebike.interfaceToController",
    "ibd-ebike.brakesToController",
    "ibd-ebike.riderToInterface",
    "ibd-ebike.chargerToBattery",
    "ibd-ebike.roadToMotor",
    "stm-ebike.powerOn",
    "stm-ebike.startAssist",
    "stm-ebike.stopAssist",
    "stm-ebike.brakeCut",
    "stm-ebike.plugIn",
    "stm-ebike.chargeComplete",
    "stm-ebike.unplug",
    "stm-ebike.powerOff",
    "stm-ebike.faultFromAssist",
    "stm-ebike.resetFault",
)

REQUIRED_ACTIONS = (
    "powerOnBike",
    "selectAssist",
    "pedalAndThrottle",
    "applyBrake",
    "inhibitMotor",
    "deliverTorque",
    "plugInCharger",
    "stopCharge",
)

REQUIRED_REQ_IDS = {
    "ElectricBike.rideSafetyRequirement": "REQ-001",
    "ElectricBike.rangeRequirement": "REQ-002",
    "ElectricBike.assistLimitRequirement": "REQ-003",
    "ElectricBike.chargeSafetyRequirement": "REQ-004",
    "ElectricBike.brakeOverrideRequirement": "REQ-005",
    "ElectricBike.batteryCutoffRequirement": "REQ-006",
    "ElectricBike.displayRequirement": "REQ-007",
    "ElectricBike.structuralRequirement": "REQ-008",
}


class EBikeExampleTests(unittest.TestCase):
    def test_project_files_exist(self):
        self.assertTrue((EBIKE / "e-bike-model.msml").exists())
        for stem in REQUIRED_VIEW_STEMS:
            self.assertTrue((EBIKE / f"{stem}.msmd").exists(), stem)

    def test_model_names_and_requirement_ids(self):
        model = read_json_file(EBIKE / "e-bike-model.msml")["model"]
        self.assertEqual(model["namespace"], "ElectricBike")
        defs = {item["id"]: item for item in model["definitions"]}
        rels = {item["id"]: item for item in model["relationships"]}
        for did in REQUIRED_DEF_IDS:
            self.assertIn(did, defs, did)
        for rid in REQUIRED_REL_IDS:
            self.assertIn(rid, rels, rid)
        for action in REQUIRED_ACTIONS:
            self.assertIn(f"ElectricBike.Action.{action}", defs, action)
        for did, req_id in REQUIRED_REQ_IDS.items():
            self.assertEqual(defs[did]["req_id"], req_id)
        usages = {item["name"] for item in defs.values() if item.get("name")}
        for usage in ("batteryPack", "hubMotor", "humanInterface", "motorController", "brakeSystem"):
            self.assertTrue(
                any(usage in (EBIKE / f"{stem}.msmd").read_text() for stem in REQUIRED_VIEW_STEMS),
                usage,
            )
        self.assertIn("BatteryPack", usages)
        self.assertIn("HubMotor", usages)
        include = rels["uc-ebike.i-adjust-ride"]
        self.assertEqual(include["source"], "ElectricBike.UC.rideBikeUseCase")
        self.assertEqual(include["target"], "ElectricBike.UC.adjustAssistUseCase")
        self.assertEqual(rels["stm-ebike.resetFault"]["target"], "ElectricBike.State.RideControl.off")
        self.assertEqual(rels["ibd-ebike.riderToInterface"]["target"], "ElectricBike.Port.riderInputIn")
        self.assertEqual(rels["ibd-ebike.chargerToBattery"]["target"], "ElectricBike.Port.chargeInputIn")
        self.assertEqual(rels["ibd-ebike.roadToMotor"]["source"], "ElectricBike.Port.wheelLoadIn")
        self.assertEqual(rels["sd-ebike.m1"]["name"], "powerOn")
        self.assertEqual(rels["sd-ebike.m3"]["name"], "phase")
        self.assertEqual(rels["sd-ebike.m4"]["name"], "lever")
        self.assertEqual(rels["req-ebike.d-override-safety"]["type"], "refine")
        self.assertNotIn("req-ebike.d-assist-range", rels)
        self.assertNotIn("req-ebike.d-display-range", rels)

    def test_views_validate_strict(self):
        report = validate_all(EBIKE, strict=True)
        self.assertEqual(report.errors, 0)
        for stem in REQUIRED_VIEW_STEMS:
            report = validate(EBIKE / f"{stem}.msmd", strict=True)
            self.assertEqual(report.errors, 0, stem)

    def test_rendered_pngs(self):
        self.assertEqual(render_all(EBIKE), 0)
        for stem in REQUIRED_VIEW_STEMS:
            png = EBIKE / f"{stem}.png"
            self.assertTrue(png.exists(), f"missing {png.name}")
            self.assertGreater(png.stat().st_size, 1000, f"empty {png.name}")


if __name__ == "__main__":
    unittest.main()
