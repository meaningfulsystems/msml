# Apollo Architecture Summary

Public NASA **Apollo 11 / Block II** instance on vehicle **AS-506**, using the generic Saturn V + CSM + LM stack. Namespace `Apollo`. File stem `apollo`. Civil / historical architecture only.

Apollo 7 / 8 / 10 / 13 are notes, not separate projects (7 had no LM; 8 and 10 did not land; 13 aborted).

Do **not** invent official CSM lunar Δv, CSM-107 SPS loaded lb, A11 AGS flight-program name, or other UNKNOWN values marked on the model.

## Parts (kept distinct)

Saturn V S-IC / S-II / S-IVB / IU; F-1 and separate S-II / S-IVB J-2; CSM CM / SM with AGC_CM, IMU, two DSKY, EMS, SPS, RCS, ECLSS; LM descent / ascent with AGC_LM, one DSKY, AGS (AEA+ASA+DEDA), DPS / APS, radars; IU LVDC + ST-124 + FCC; crew CDR / CMP / LMP; Ground MCC-H, GSFC, MSFN, KSC LC-39, Recovery, RSO/AFETR.

## Key sourced numbers

Use only numbers already on the model. Examples: A11 PK p.109 tank loads and launch masses; SM/LM RCS 100 lbf and CM RCS 93 lbf (A11 PK p.93 / p.106); Comanche 055 / LMY99 rev 001; SPS and DPS cited from both PK and TNs when they conflict; TLI 02:44:15 GET; TDE ~03:20–04:09 GET; LOI-1 75:54:28 GET; food 2.26 lb/man/day planned.

**UNKNOWN (do not invent):** official CSM lunar Δv table; CSM-107 SPS loaded lb; A11 AGS flight-program name; loaded SM/CM RCS propellant mass; A11 actual kcal; RTCC MOC vs DSC on A11; 4th AIS ship; entry blackout duration.

## Mission STM

countdown → boost → earthOrbit → TLI → dockEject → translunar → LOI → undock → DOI → descent → surface/EVA → ascent → rendezvous → TEI → entry → recovery.

`dockEject` is its own state (CMP-owned, SM RCS, probe-drogue). Do not put translunar before dockEject, and do not jump TLI → translunar or dockEject → LOI.

## Views

System: `apollo-pkg`, `apollo-bdd`, `apollo-ctx`, `apollo-ibd`, `apollo-stm`, `apollo-abort`, `apollo-act`, `apollo-seq`, `apollo-req`.

Subsystem: Saturn (`apollo-sat-bdd`, `apollo-sat-ibd`), CSM (`apollo-csm-bdd`, `apollo-csm`), LM (`apollo-lm-bdd`, `apollo-lm`), GNC (`apollo-gnc-pkg`, `apollo-cmc-stm`, `apollo-lgc-stm`), Ground (`apollo-gnd-bdd`, `apollo-gnd`, `apollo-crew`), comms (`apollo-usb`, `apollo-cmd`), ECLSS (`apollo-eclss`, `apollo-eclss-par`), electrical (`apollo-eps`), AGS (`apollo-ags-bdd`), docking (`apollo-dock`), RCS (`apollo-rcs`).

Full view table: [README.md](README.md).

![Apollo mission STM](apollo-stm.png)

![Apollo vehicle stack](apollo-ibd.png)

## Validate and render

```bash
msml-validate-all projects/apollo --strict
msml-render-all projects/apollo
```
