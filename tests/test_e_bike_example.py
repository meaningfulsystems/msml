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
    "ElectricBike.BMS",
    "ElectricBike.BatteryPack.bms",
    "ElectricBike.CadenceSensor",
    "ElectricBike.WheelSpeedSensor",
    "ElectricBike.cadenceSensor",
    "ElectricBike.wheelSpeedSensor",
    "ElectricBike.walkAssistRequirement",
    "ElectricBike.continuousPowerRequirement",
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
    "ElectricBike.motorAssistCutoffRequirement",
    "ElectricBike.lightingRequirement",
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
    "ElectricBike.UC.adjustAssistUseCase",
)

REQUIRED_REL_IDS = (
    "allocateSafetyToBrakes",
    "allocateRangeToBattery",
    "allocateAssistToController",
    "allocateChargeToBms",
    "allocateSafetyToController",
    "allocateSafetyToBms",
    "allocateSafetyToSensors",
    "allocateAssistToWheelSpeed",
    "allocateWalkToController",
    "allocatePowerToHub",
    "ibd-ebike.batteryToBms",
    "ibd-ebike.cadenceToController",
    "ibd-ebike.wheelSpeedToController",
    "ibd-ebike.frameToBattery",
    "ibd-ebike.frameToMotor",
    "ibd-ebike.frameToInterface",
    "ibd-ebike.frameToBrakes",
    "ibd-ebike.batteryToController",
    "ibd-ebike.controllerToMotor",
    "ibd-ebike.interfaceToController",
    "ibd-ebike.brakesToController",
    "ibd-ebike.chargerToBattery",
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
    "stm-ebike.startWalk",
    "stm-ebike.stopWalk",
    "stm-ebike.brakeCutWalk",
    "stm-ebike.faultFromWalk",
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
    "ElectricBike.motorAssistCutoffRequirement": "REQ-009",
    "ElectricBike.lightingRequirement": "REQ-010",
    "ElectricBike.walkAssistRequirement": "REQ-011",
    "ElectricBike.continuousPowerRequirement": "REQ-012",
}


class EBikeExampleTests(unittest.TestCase):
    def test_project_files_exist(self):
        self.assertTrue((EBIKE / "e-bike-model.msml").exists())
        self.assertTrue((EBIKE / "architecture-summary.md").exists())
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
        for usage in (
            "batteryPack",
            "hubMotor",
            "humanInterface",
            "motorController",
            "brakeSystem",
            "cadenceSensor",
            "wheelSpeedSensor",
        ):
            self.assertTrue(
                any(usage in (EBIKE / f"{stem}.msmd").read_text() for stem in REQUIRED_VIEW_STEMS),
                usage,
            )
        self.assertEqual(defs["ElectricBike.cadenceSensor"]["type_ref"], "ElectricBike.CadenceSensor")
        self.assertEqual(defs["ElectricBike.wheelSpeedSensor"]["type_ref"], "ElectricBike.WheelSpeedSensor")
        self.assertIn("BatteryPack", usages)
        self.assertIn("HubMotor", usages)
        include = rels["uc-ebike.i-adjust-ride"]
        self.assertEqual(include["source"], "ElectricBike.UC.rideBikeUseCase")
        self.assertEqual(include["target"], "ElectricBike.UC.adjustAssistUseCase")
        charger_assoc = [
            rel
            for rel in rels.values()
            if rel.get("type") == "association"
            and rel.get("source") == "ElectricBike.Charger"
            and str(rel.get("target", "")).startswith("ElectricBike.UC.")
        ]
        self.assertEqual([rel["target"] for rel in charger_assoc], ["ElectricBike.UC.chargeBikeUseCase"])
        self.assertFalse(
            any(rel.get("target") == "ElectricBike.UC.adjustAssistUseCase" for rel in charger_assoc),
            "Charger must not associate with Adjust Assist",
        )
        ctx_text = (EBIKE / "e-bike-ctx.msmd").read_text(encoding="utf-8")
        self.assertNotIn("Wheel Torque", ctx_text)
        self.assertNotIn("WheelTorque", ctx_text)
        self.assertEqual(rels["stm-ebike.resetFault"]["source"], "ElectricBike.State.RideControl.fault")
        self.assertEqual(rels["stm-ebike.resetFault"]["target"], "ElectricBike.State.RideControl.off")
        self.assertEqual(rels["stm-ebike.plugIn"]["source"], "ElectricBike.State.RideControl.off")
        self.assertEqual(rels["stm-ebike.plugIn"]["target"], "ElectricBike.State.RideControl.charging")
        self.assertNotIn("stm-ebike.plugInStandby", rels)
        self.assertIn("from Off only", defs["ElectricBike.State.RideControl.charging"].get("do", ""))
        stm_text = (EBIKE / "e-bike-stm.msmd").read_text(encoding="utf-8")
        self.assertIn("from Off only", stm_text)
        self.assertNotIn("plugInStandby", stm_text)
        charging_view = next(
            el
            for el in read_json_file(EBIKE / "e-bike-stm.msmd")["diagram"]["elements"]
            if el.get("id") == "state-charging"
        )
        self.assertEqual(charging_view.get("display_name"), "charging")
        self.assertEqual(rels["stm-ebike.powerOff"]["source"], "ElectricBike.State.RideControl.standby")
        self.assertEqual(rels["stm-ebike.powerOff"]["target"], "ElectricBike.State.RideControl.off")
        self.assertEqual(defs["ElectricBike.State.RideControl.walk"]["name"], "walk")
        self.assertIn("6 km/h", defs["ElectricBike.State.RideControl.walk"].get("do", ""))
        self.assertEqual(rels["stm-ebike.startWalk"]["source"], "ElectricBike.State.RideControl.standby")
        self.assertEqual(rels["stm-ebike.startWalk"]["target"], "ElectricBike.State.RideControl.walk")
        self.assertEqual(rels["stm-ebike.stopWalk"]["target"], "ElectricBike.State.RideControl.standby")
        energy = defs["ElectricBike.PAR.energyBalance"]
        self.assertIn("energyPerKm", energy["expression"])
        self.assertIn("packEnergy", energy["expression"])
        self.assertNotIn("riderPower", energy["expression"])
        self.assertNotIn("riderPower", {p["name"] for p in energy["parameters"]})
        energy_bindings = [
            (rel["source"], rel["target"])
            for rel in rels.values()
            if rel.get("type") == "binding_connector"
            and "ElectricBike.PAR.energyBalance" in (rel.get("source"), rel.get("target"))
        ]
        self.assertIn(("ElectricBike.PAR.packEnergy", "ElectricBike.PAR.energyBalance"), energy_bindings)
        self.assertIn(("ElectricBike.PAR.energyPerKm", "ElectricBike.PAR.energyBalance"), energy_bindings)
        self.assertFalse(any("riderPower" in edge for pair in energy_bindings for edge in pair))
        ibd_connectors = [
            rel for rel in rels.values() if rel.get("id", "").startswith("ibd-ebike.") and rel.get("type") == "connector"
        ]
        for conn in ibd_connectors:
            owners = {defs[conn[end]].get("owner_ref") for end in ("source", "target")}
            if conn["id"] == "ibd-ebike.chargerToBattery":
                self.assertEqual(owners, {"ElectricBike", "ElectricBike.BMS"})
                continue
            self.assertNotIn(
                "ElectricBike",
                owners,
                f"{conn['id']} parked on ElectricBike",
            )
        self.assertNotIn("ibd-ebike.riderToInterface", rels)
        self.assertNotIn("ibd-ebike.roadToMotor", rels)
        self.assertEqual(rels["ibd-ebike.chargerToBattery"]["source"], "ElectricBike.Port.chargerIn")
        self.assertEqual(rels["ibd-ebike.chargerToBattery"]["target"], "ElectricBike.Port.bmsChargeIn")
        self.assertEqual(defs["ElectricBike.Port.bmsChargeIn"]["owner_ref"], "ElectricBike.BMS")
        self.assertEqual(rels["ibd-ebike.batteryToBms"]["source"], "ElectricBike.Port.bmsPackOut")
        self.assertEqual(rels["ibd-ebike.batteryToBms"]["target"], "ElectricBike.Port.packCellsIn")
        self.assertNotIn("ElectricBike.Port.chargeInputIn", defs)
        self.assertEqual(rels["sd-ebike.m1"]["name"], "powerOn")
        self.assertEqual(rels["sd-ebike.m3"]["name"], "phase")
        self.assertEqual(rels["sd-ebike.m4"]["name"], "lever")
        self.assertEqual(rels["req-ebike.d-override-safety"]["type"], "refine")
        self.assertNotIn("req-ebike.d-assist-range", rels)
        self.assertNotIn("req-ebike.d-display-range", rels)
        self.assertNotIn("ElectricBike.UC.lockBikeUseCase", defs)
        self.assertNotIn("ElectricBike.LockEcu", defs)
        self.assertEqual(defs["ElectricBike.BatteryPack.bms"]["name"], "bms")
        self.assertEqual(defs["ElectricBike.BatteryPack.bms"]["type_ref"], "ElectricBike.BMS")
        self.assertEqual(
            defs["ElectricBike.BatteryPack.bms"]["qualified_name"],
            "ElectricBike::BatteryPack::bms",
        )
        self.assertEqual(rels["allocateChargeToBms"]["target"], "ElectricBike.BatteryPack.bms")
        self.assertEqual(rels["allocateSafetyToController"]["target"], "ElectricBike.MotorController")
        self.assertEqual(rels["allocateSafetyToBms"]["target"], "ElectricBike.BatteryPack.bms")
        self.assertEqual(rels["allocateSafetyToSensors"]["target"], "ElectricBike.cadenceSensor")
        self.assertEqual(rels["allocateAssistToWheelSpeed"]["source"], "ElectricBike.assistLimitRequirement")
        self.assertEqual(rels["allocateAssistToWheelSpeed"]["target"], "ElectricBike.wheelSpeedSensor")
        self.assertEqual(rels["allocateWalkToController"]["target"], "ElectricBike.MotorController")
        self.assertEqual(rels["allocatePowerToHub"]["target"], "ElectricBike.HubMotor")
        self.assertNotIn("req-ebike.d-assist-walk", rels)
        self.assertNotIn("req-ebike.d-assist-power", rels)
        self.assertIn("bms : BMS", (EBIKE / "e-bike-ibd.msmd").read_text(encoding="utf-8"))
        range_text = defs["ElectricBike.rangeRequirement"]["text"]
        self.assertIn("Tour", range_text)
        self.assertIn("Not Eco / PAS-1", range_text)
        self.assertIn("8.3 Wh/km Tour", defs["ElectricBike.PAR.energyPerKm"]["name"])
        root_props = {p["name"]: p["type"] for p in defs["ElectricBike"]["compartments"]["properties"]}
        self.assertEqual(root_props["classification"], "EPAC / EN 15194")
        hub_props = {p["name"]: p["type"] for p in defs["ElectricBike.HubMotor"]["compartments"]["properties"]}
        self.assertEqual(hub_props["continuousAssist"], "250 W")
        self.assertEqual(hub_props["peakTorque"], "40 N·m")
        self.assertNotIn("peakPower", hub_props)
        self.assertNotIn("wheelTorque", hub_props)
        self.assertEqual(hub_props["location"], "rear geared hub")
        self.assertEqual(hub_props["regen"], "none")
        self.assertIn("StVZO / ISO 6742", defs["ElectricBike.lightingRequirement"]["text"])
        cutoff = defs["ElectricBike.motorAssistCutoffRequirement"]
        self.assertEqual(cutoff["name"], "motor-assist cut-off")
        self.assertIn("4.2.13", cutoff["text"])
        self.assertIn("Power management", cutoff["text"])
        self.assertIn("2 m", cutoff["text"])
        self.assertIn("5 m", cutoff["text"])
        self.assertIn("NOT vehicle brake distance", cutoff["text"])
        self.assertNotIn("Stopping Distance", cutoff["name"])
        self.assertNotIn("10×", cutoff["text"])
        self.assertNotIn("10x tighter", cutoff["text"])
        self.assertNotIn("ElectricBike.stoppingDistanceRequirement", defs)
        cutoff_targets = {
            r["target"]
            for r in rels.values()
            if r.get("type") == "allocate" and r.get("source") == "ElectricBike.motorAssistCutoffRequirement"
        }
        self.assertIn("ElectricBike.MotorController", cutoff_targets)
        self.assertIn("ElectricBike.cadenceSensor", cutoff_targets)
        self.assertIn("ElectricBike.wheelSpeedSensor", cutoff_targets)
        self.assertNotIn("ElectricBike.BrakeSystem", cutoff_targets)
        self.assertIn("electronic inhibit budget", defs["ElectricBike.brakeOverrideRequirement"]["text"])
        self.assertNotIn("10×", defs["ElectricBike.brakeOverrideRequirement"]["text"])
        self.assertNotIn("ECE R113", defs["ElectricBike.lightingRequirement"]["text"].replace("Not UN ECE R113", ""))
        act = (EBIKE / "e-bike-act.msmd").read_text(encoding="utf-8")
        self.assertIn("Pedal (EPAC)", act)
        self.assertNotIn("Pedal / Throttle", act)
        self.assertNotIn("Pedal (cadence)", act)
        int_text = (EBIKE / "e-bike-int.msmd").read_text(encoding="utf-8")
        self.assertIn("Rear Geared Hub", int_text)
        self.assertNotIn(":hubMotor", int_text)
        bdd_text = (EBIKE / "e-bike-bdd.msmd").read_text(encoding="utf-8")
        self.assertIn("Rear Geared Hub", bdd_text)
        self.assertIn("Wheel Speed Sensor", bdd_text)
        self.assertIn("Cadence Sensor", bdd_text)
        ibd_text = (EBIKE / "e-bike-ibd.msmd").read_text(encoding="utf-8")
        self.assertIn("Rear Geared Hub", ibd_text)
        self.assertIn("pack power", ibd_text)
        self.assertIn("phase drive", ibd_text)
        self.assertIn("wheelSpeedSensor", ibd_text)
        self.assertNotIn("rider : Rider", ibd_text)
        self.assertNotIn("charger : Charger", ibd_text)
        self.assertNotIn("road : Road", ibd_text)
        self.assertIn("ElectricBike.Port.chargerIn", ibd_text)
        self.assertIn("continuousAssist", ibd_text)
        self.assertIn("peakTorque", ibd_text)
        self.assertIn("250 W", ibd_text)
        self.assertIn("40 N", ibd_text)
        callout = defs["ElectricBike.Note.IbdCallout"]["text"]
        self.assertIn("continuous assist", callout)
        self.assertIn("peak torque", callout)
        self.assertIn("not peak", callout)
        self.assertIn("not continuous", callout)
        self.assertIn("usableWh: 500 Wh Tour", defs["ElectricBike.PAR.packEnergy"]["name"])
        self.assertIn("usableWh", defs["ElectricBike.rangeRequirement"]["text"])
        self.assertIn("6 km/h", defs["ElectricBike.walkAssistRequirement"]["text"])
        self.assertIn("250 W", defs["ElectricBike.continuousPowerRequirement"]["text"])
        self.assertIn("BMS inside the pack", defs["ElectricBike.batteryCutoffRequirement"]["text"])

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
