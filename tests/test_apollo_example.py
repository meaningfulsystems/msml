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
    "apollo-csm-bdd",
    "apollo-lm-bdd",
    "apollo-gnc-pkg",
    "apollo-abort",
    "apollo-eps",
    "apollo-ags-bdd",
    "apollo-dock",
    "apollo-rcs",
    "apollo-cmc-stm",
    "apollo-lgc-stm",
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
    "Apollo.DSKY2",
    "Apollo.DSKY_LM",
    "Apollo.EMS",
    "Apollo.F1",
    "Apollo.J2_SII",
    "Apollo.J2_SIVB",
    "Apollo.ST124",
    "Apollo.FCC",
    "Apollo.AEA",
    "Apollo.ASA",
    "Apollo.DEDA",
    "Apollo.AgZn_CM",
    "Apollo.Charger",
    "Apollo.PyroBatt",
    "Apollo.AgZn_Des",
    "Apollo.AgZn_Asc",
    "Apollo.ECA",
    "Apollo.DCBus_LM",
    "Apollo.Inverter",
    "Apollo.RCS_SM",
    "Apollo.Quad",
    "Apollo.Probe",
    "Apollo.Drogue",
    "Apollo.Latch",
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
    "Apollo.State.Mission.dockEject",
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
    "Apollo.State.Abort.P70",
    "Apollo.State.Abort.P71",
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
        self.assertTrue((APOLLO / "apollo-gnc-pkg.msmd").exists())

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
        self.assertEqual(props["vehicle"], "AS-506")
        self.assertEqual(defs["Apollo.F1"]["name"], "F-1")
        self.assertEqual(defs["Apollo.J2_SII"]["name"], "J-2")
        self.assertEqual(defs["Apollo.J2_SIVB"]["name"], "J-2")
        self.assertEqual(defs["Apollo.DSKY2"]["name"], "DSKY")
        self.assertEqual(defs["Apollo.DSKY_LM"]["name"], "DSKY")
        self.assertEqual(defs["Apollo.State.Mission.dockEject"]["name"], "dock/eject")
        self.assertIn("CMP", defs["Apollo.State.Mission.dockEject"].get("do", ""))
        self.assertIn("SM RCS", defs["Apollo.State.Mission.dockEject"].get("do", ""))
        self.assertIn("probe-drogue", defs["Apollo.State.Mission.dockEject"].get("do", ""))
        self.assertIn("03:20", defs["Apollo.State.Mission.dockEject"].get("entry", ""))
        self.assertIn("04:09", defs["Apollo.State.Mission.dockEject"].get("entry", ""))
        self.assertIn("02:44:15", defs["Apollo.State.Mission.TLI"].get("do", ""))
        self.assertIn("75:54:28", defs["Apollo.State.Mission.LOI"].get("do", ""))
        rels = {item["id"]: item for item in model["relationships"]}
        self.assertEqual(rels["stm-apollo.TLI-dockEject"]["source"], "Apollo.State.Mission.TLI")
        self.assertEqual(rels["stm-apollo.TLI-dockEject"]["target"], "Apollo.State.Mission.dockEject")
        self.assertEqual(rels["stm-apollo.dockEject-translunar"]["source"], "Apollo.State.Mission.dockEject")
        self.assertEqual(rels["stm-apollo.dockEject-translunar"]["target"], "Apollo.State.Mission.translunar")
        self.assertEqual(rels["stm-apollo.translunar-LOI"]["source"], "Apollo.State.Mission.translunar")
        self.assertEqual(rels["stm-apollo.translunar-LOI"]["target"], "Apollo.State.Mission.LOI")
        self.assertNotIn("stm-apollo.dockEject-LOI", rels)
        self.assertNotIn("stm-apollo.TLI-translunar", rels)
        self.assertEqual(rels["act-apollo.f4"]["target"], "Apollo.Action.dockEject")
        self.assertEqual(rels["act-apollo.f5a"]["source"], "Apollo.Action.dockEject")
        self.assertEqual(rels["act-apollo.f5b"]["source"], "Apollo.Action.translunar")
        self.assertEqual(rels["act-apollo.f5b"]["target"], "Apollo.Action.loi")
        self.assertEqual(defs["Apollo.State.Abort.pad"]["name"], "pad/LES")
        self.assertEqual(defs["Apollo.State.Abort.P70"]["name"], "P70 DPS")
        self.assertEqual(defs["Apollo.State.Abort.P71"]["name"], "P71 APS")

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
        agc_cm = {p["name"]: p.get("type") for p in defs["Apollo.AGC_CM"]["compartments"]["properties"]}
        self.assertEqual(agc_cm["word"], "16-bit")
        self.assertEqual(agc_cm["erasable"], "2048 E")
        self.assertEqual(agc_cm["fixed"], "36864 F")
        self.assertEqual(agc_cm["clock"], "1.024 MHz")
        self.assertEqual(agc_cm["mct"], "11.7 μs")
        self.assertIn("Colossus", agc_cm["software"])
        self.assertEqual(agc_cm["rope"], "Comanche 055")
        self.assertEqual(agc_cm["dsky"], "2")
        self.assertEqual(agc_cm["pipa"], "5.85 cm/s/pulse")
        self.assertIn("NOT abort", agc_cm["alarm1201"])
        self.assertIn("no digital to LVDC", agc_cm["lvdc"])
        agc_lm = {p["name"]: p.get("type") for p in defs["Apollo.AGC_LM"]["compartments"]["properties"]}
        self.assertIn("Luminary", agc_lm["software"])
        self.assertEqual(agc_lm["rope"], "LMY99 rev 001")
        self.assertEqual(agc_lm["dsky"], "1")
        self.assertEqual(agc_lm["pipa"], "1.0 cm/s/pulse")
        self.assertIn("P66 ROD", agc_lm["descent"])
        self.assertIn("P63–P68", agc_lm["landing"])
        self.assertNotIn("P68", agc_lm["abort"])
        ags = {p["name"]: p.get("type") for p in defs["Apollo.AGS"]["compartments"]["properties"]}
        self.assertIn("AEA + ASA + DEDA", ags["parts"])
        self.assertIn("R47", ags["init"])
        self.assertIn("not a landing computer", ags["not"])
        aea = {p["name"]: p.get("type") for p in defs["Apollo.AEA"]["compartments"]["properties"]}
        self.assertEqual(aea["memory"], "4096 × 18-bit words")
        self.assertEqual(aea["cycle"], "5 μs")
        self.assertEqual(aea["mass"], "14.8 kg (32.7 lb)")
        self.assertEqual(defs["Apollo.DEDA"]["name"], "DEDA")
        self.assertNotEqual(defs["Apollo.DEDA"]["id"], defs["Apollo.DSKY"]["id"])
        self.assertNotEqual(defs["Apollo.DEDA"]["id"], defs["Apollo.DSKY_LM"]["id"])
        fc = {p["name"]: p.get("type") for p in defs["Apollo.FuelCell"]["compartments"]["properties"]}
        self.assertEqual(fc["count"], "3")
        self.assertEqual(fc["reactants"], "H2 / O2")
        self.assertEqual(fc["watts"], "press kit does not state")
        self.assertIn("0.77", fc["water"])
        sm_rcs = {p["name"]: p.get("type") for p in defs["Apollo.RCS_SM"]["compartments"]["properties"]}
        self.assertEqual(sm_rcs["thrust"], "100 lbf each engine")
        self.assertIn("UNKNOWN", sm_rcs["loaded"])
        cm_rcs = {p["name"]: p.get("type") for p in defs["Apollo.RCS_CM"]["compartments"]["properties"]}
        self.assertEqual(cm_rcs["thrust"], "93 lbf each engine")
        self.assertIn("UNKNOWN", cm_rcs["loaded"])
        lm_rcs = {p["name"]: p.get("type") for p in defs["Apollo.RCS_LM"]["compartments"]["properties"]}
        self.assertEqual(lm_rcs["thrust"], "100 lbf each engine")
        self.assertIn("no auto translation", cm_rcs["role"])
        self.assertEqual(defs["Apollo.Probe"]["name"], "probe")
        self.assertEqual(defs["Apollo.Drogue"]["name"], "drogue")
        latch = {p["name"]: p.get("type") for p in defs["Apollo.Latch"]["compartments"]["properties"]}
        self.assertEqual(latch["count"], "12")
        inv = {p["name"]: p.get("type") for p in defs["Apollo.Inverter"]["compartments"]["properties"]}
        self.assertEqual(inv["output"], "117 V 400 Hz")
        self.assertEqual(defs["Apollo.AgZn_Des"]["compartments"]["properties"][1]["type"], "4")
        self.assertEqual(defs["Apollo.AgZn_Asc"]["compartments"]["properties"][1]["type"], "2")
        f1 = {p["name"]: p.get("type") for p in defs["Apollo.F1"]["compartments"]["properties"]}
        self.assertEqual(f1["thrust"], "1,530,000 lbf each")
        sps = {p["name"]: p.get("type") for p in defs["Apollo.SPS"]["compartments"]["properties"]}
        self.assertEqual(sps["thrustPk"], "20,500 lbf (PK)")
        self.assertEqual(sps["thrustTn"], "21,500 lbf vac (TN D-7375)")
        self.assertIn("cite both", sps["thrust"])
        self.assertIn("UNKNOWN", sps["loaded"])
        dps = {p["name"]: p.get("type") for p in defs["Apollo.DPS"]["compartments"]["properties"]}
        self.assertEqual(dps["thrustPk"], "9,870 lbf (PK)")
        self.assertEqual(dps["thrustTn"], "10,500 lbf (TN D-7143)")
        self.assertIn("cite both", dps["thrust"])
        self.assertIn("cite both", dps["throttle"])
        aps = {p["name"]: p.get("type") for p in defs["Apollo.APS"]["compartments"]["properties"]}
        self.assertEqual(aps["thrust"], "3,500 lbf")
        sat = {p["name"]: p.get("type") for p in defs["Apollo.SaturnV"]["compartments"]["properties"]}
        self.assertEqual(sat["vehicle"], "AS-506")
        self.assertEqual(sat["ignition"], "6,484,280 lb")
        self.assertEqual(sat["firstMotion"], "6,398,535 lb")
        self.assertNotIn("tankLoads", sat)
        self.assertIn("UNKNOWN", sat["deltaV"])
        self.assertIn("lunar", sat["deltaV"])
        sic = {p["name"]: p.get("type") for p in defs["Apollo.SIC"]["compartments"]["properties"]}
        self.assertEqual(sic["fueled"], "5,022,674 lb")
        self.assertEqual(sic["lox"], "3,307,855 lb")
        self.assertEqual(sic["rp1"], "1,426,069 lb")
        self.assertEqual(sic["liftoffThrust"], "7,653,854 lbf")
        self.assertIn("A11 Press Kit p.109", defs["Apollo.Note.TanksSourced"]["text"])
        self.assertNotIn("Apollo.Note.UnknownTanks", defs)
        self.assertIn("UNKNOWN", defs["Apollo.Note.UnknownDv"]["text"])
        self.assertIn("lunar", defs["Apollo.Note.UnknownDv"]["text"])
        self.assertIn("Comanche 055", defs["Apollo.Note.UnknownRope"]["text"])
        self.assertIn("LMY99", defs["Apollo.Note.UnknownRope"]["text"])
        self.assertIn("UNKNOWN", defs["Apollo.Note.UnknownRope"]["text"])
        self.assertIn("does not talk digital", defs["Apollo.Note.AgcLvdc"]["text"])
        self.assertIn("not global", defs["Apollo.Note.PNumbers"]["text"])
        self.assertIn("UNKNOWN", defs["Apollo.Note.UnknownSpsLoad"]["text"])
        ags_p = {p["name"]: p["type"] for p in defs["Apollo.AGS"]["compartments"]["properties"]}
        self.assertIn("UNKNOWN", ags_p["flightProgram"])
        cm = {p["name"]: p["type"] for p in defs["Apollo.CM"]["compartments"]["properties"]}
        sm = {p["name"]: p["type"] for p in defs["Apollo.SM"]["compartments"]["properties"]}
        lm = {p["name"]: p["type"] for p in defs["Apollo.LM"]["compartments"]["properties"]}
        iu = {p["name"]: p["type"] for p in defs["Apollo.IU"]["compartments"]["properties"]}
        lvdc = {p["name"]: p["type"] for p in defs["Apollo.LVDC"]["compartments"]["properties"]}
        self.assertEqual(cm["launch"], "12,250 lb")
        self.assertEqual(sm["launch"], "51,243 lb")
        self.assertEqual(lm["launch"], "33,205 lb LM-5")
        self.assertEqual(iu["mass"], "4,306 lb")
        self.assertEqual(lvdc["cycle"], "82.03125 µs")
        self.assertEqual(defs["Apollo.State.CMC.P61"]["name"], "P61")
        self.assertEqual(defs["Apollo.State.LGC.P66"]["name"], "P66")
        self.assertNotEqual(defs["Apollo.State.CMC.P63"]["id"], defs["Apollo.State.LGC.P63"]["id"])
        self.assertIn("ENTRY", (APOLLO / "apollo-cmc-stm.msmd").read_text(encoding="utf-8"))
        self.assertIn("LANDING", (APOLLO / "apollo-lgc-stm.msmd").read_text(encoding="utf-8"))
        self.assertNotIn("Apollo.State.LGC", (APOLLO / "apollo-cmc-stm.msmd").read_text(encoding="utf-8"))
        self.assertNotIn("Apollo.State.CMC", (APOLLO / "apollo-lgc-stm.msmd").read_text(encoding="utf-8"))
        self.assertIn("4096", defs["Apollo.Note.AgsSourced"]["text"])
        self.assertNotIn("UNKNOWN", defs["Apollo.Note.AgsSourced"]["text"])
        self.assertIn("100 lbf", defs["Apollo.Note.UnknownSmRcs"]["text"])
        self.assertIn("UNKNOWN", defs["Apollo.Note.UnknownSmRcs"]["text"])
        self.assertIn("loaded", defs["Apollo.Note.UnknownSmRcs"]["text"])
        self.assertIn("p.93", defs["Apollo.Note.UnknownSmRcs"]["text"])
        self.assertEqual(defs["Apollo.State.Mission.earthOrbit"]["do"], "100 nmi planned")
        self.assertNotEqual(defs["Apollo.AGC_CM"]["id"], defs["Apollo.AGC_LM"]["id"])
        self.assertNotEqual(defs["Apollo.AGS"]["id"], defs["Apollo.AGC_LM"]["id"])
        self.assertNotEqual(defs["Apollo.EMS"]["id"], defs["Apollo.AGC_CM"]["id"])
        self.assertNotEqual(defs["Apollo.LVDC"]["id"], defs["Apollo.AGC_CM"]["id"])
        self.assertNotEqual(defs["Apollo.DSKY"]["id"], defs["Apollo.DSKY2"]["id"])
        self.assertNotEqual(defs["Apollo.DSKY"]["id"], defs["Apollo.DSKY_LM"]["id"])
        root = {p["name"]: p["type"] for p in defs["Apollo"]["compartments"]["properties"]}
        self.assertIn("S-IC-6", root["serials"])
        self.assertIn("CSM-107", root["serials"])
        self.assertIn("LM-5", root["serials"])
        sat = {p["name"]: p.get("type") for p in defs["Apollo.SaturnV"]["compartments"]["properties"]}
        self.assertIn("no electrical power", sat["stagePower"])
        self.assertIn("no CSM–LM propellant crossfeed", sat["crossfeed"])
        self.assertEqual({p["name"]: p["type"] for p in defs["Apollo.SIC"]["compartments"]["properties"]}["serial"], "S-IC-6")
        mocr = {p["name"]: p["type"] for p in defs["Apollo.MOCR"]["compartments"]["properties"]}
        self.assertEqual(mocr["which"], "MOCR 2 (3rd floor)")
        ksc = {p["name"]: p["type"] for p in defs["Apollo.KSC_LCC"]["compartments"]["properties"]}
        self.assertIn("1-21", ksc["handoff"])
        self.assertIn("Petrone", ksc["commit"])
        afet = {p["name"]: p["type"] for p in defs["Apollo.AFETR"]["compartments"]["properties"]}
        self.assertEqual(afet["role"], "parallel destruct")
        vhf = {p["name"]: p["type"] for p in defs["Apollo.BackupVoice"]["compartments"]["properties"]}
        self.assertIn("296.8", vhf["vhf"])
        self.assertIn("243.0", vhf["beacon"])
        usb = {p["name"]: p["type"] for p in defs["Apollo.USB"]["compartments"]["properties"]}
        self.assertEqual(usb["csmUplink"], "2106.40625 MHz")
        self.assertEqual(usb["lmUplink"], "2101.802 MHz")
        sm = {p["name"]: p["type"] for p in defs["Apollo.SM"]["compartments"]["properties"]}
        self.assertIn("2 H2 + 2 O2", sm["cryo"])
        self.assertIn("not J-mission", sm["notJ"])
        aps = {p["name"]: p.get("type") for p in defs["Apollo.APS"]["compartments"]["properties"]}
        self.assertEqual(aps["thrust"], "3,500 lbf")
        self.assertEqual(aps["cant"], "1.5°")
        self.assertEqual(aps["gimbal"], "not gimbaled")
        hornet = {p["name"]: p["type"] for p in defs["Apollo.Hornet"]["compartments"]["properties"]}
        self.assertIn("195:18:35", hornet["splash"])
        self.assertIn("13 nmi", hornet["splash"])
        cdr = {p["name"]: p["type"] for p in defs["Apollo.CDR"]["compartments"]["properties"]}
        lmp = {p["name"]: p["type"] for p in defs["Apollo.LMP"]["compartments"]["properties"]}
        self.assertEqual(cdr["evaTime"], "2:48")
        self.assertEqual(lmp["evaTime"], "2:40")
        self.assertIn("2:31:37", defs["Apollo.Note.EvaTimes"]["text"])
        self.assertIn("2.26", defs["Apollo.Note.UnknownFood"]["text"])
        self.assertIn("UNKNOWN", defs["Apollo.Note.UnknownFood"]["text"])
        ecs = {p["name"]: p["type"] for p in defs["Apollo.LM_ECS"]["compartments"]["properties"]}
        self.assertIn("2800", ecs["descentO2"])
        self.assertIn("3000", ecs["descentO2"])
        self.assertIn("cite both", ecs["descentO2"])
        self.assertEqual(agc_cm["rope"], "Comanche 055")
        self.assertEqual(agc_lm["rope"], "LMY99 rev 001")
        self.assertEqual(sic["fueled"], "5,022,674 lb")

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
