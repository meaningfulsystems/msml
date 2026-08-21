# Apollo Architecture Summary

Apollo is a full lunar-orbit-rendezvous example: Saturn V, Block II CSM, LM-5, crew, and the ground network for Apollo 11 (AS-506). Read it as a system-of-systems model. Numbers are from NASA primary sources; a few values (including an official CSM lunar Δv table) are intentionally left unmarked.

Namespace `Apollo`. File stem `apollo`. Civil / historical architecture only.

Apollo 7 / 8 / 10 / 13 are notes, not separate projects (7 had no LM; 8 and 10 did not land; 13 aborted).

## Parts (kept distinct)

Saturn V S-IC / S-II / S-IVB / IU; F-1 and separate S-II / S-IVB J-2; CSM CM / SM with AGC_CM, IMU, two DSKY, EMS, SPS, RCS, ECLSS; LM descent / ascent with AGC_LM, one DSKY, AGS (AEA+ASA+DEDA), DPS / APS, radars; IU LVDC + ST-124 + FCC; crew CDR / CMP / LMP; Ground MCC-H, GSFC, MSFN, KSC LC-39, Recovery, RSO/AFETR.

## Key sourced numbers

Use only numbers already on the model. A11 Press Kit p.109 tank loads and launch masses:

| Item | Value |
| --- | --- |
| S-IC | 7,653,854 lbf / 5,022,674 lb fueled |
| S-II | 1,059,171 lb |
| S-IVB | 260,523 lb |
| IU | 4,306 lb |
| CM | 12,250 lb |
| SM | 51,243 lb |
| DPS | 18,100 lb |
| APS | 5,214 lb |
| RCS | SM/LM 100 lbf · CM 93 lbf (A11 PK p.93 / p.106) |
| AGC ropes | Comanche 055 / Luminary 1A |
| AEA | 4096 × 18-bit words |

Cite both SPS figures: 20,500 lbf (PK) vs 21,500 lbf vac (TN D-7375). Cite both DPS figures: 9,870 / 1,050–6,300 lbf (PK) vs 10,500 lbf and 10:1 (TN D-7143). USB RF is sourced; VHF is 296.8 / 259.7 MHz (CSM–LM–EVA) and 243.0 MHz recovery beacon.

**UNKNOWN (do not invent):** official CSM lunar Δv table; CSM-107 SPS loaded lb; loaded SM/CM RCS propellant mass; A11 AGS flight-program name; A11 actual kcal; RTCC MOC vs DSC on A11; 4th AIS ship; entry blackout duration.

## Mission STM

countdown → boost → earthOrbit → TLI → dockEject → translunar → LOI → undock → DOI → descent → surface/EVA → ascent → rendezvous → TEI → entry → recovery.

`dockEject` is its own state (CMP-owned, SM RCS, probe-drogue). Do not put translunar before dockEject, and do not jump TLI → translunar or dockEject → LOI. A11 TDE is ~03:20–04:09 GET; the long coast after extract is translunar until LOI-1 75:54:28 GET.

## Views in this folder

System:

| View | File |
| --- | --- |
| Packages | `apollo-pkg` |
| BDD | `apollo-bdd` |
| Context IBD | `apollo-ctx` |
| Stack IBD | `apollo-ibd` |
| Mission STM | `apollo-stm` |
| Abort STM | `apollo-abort` |
| Activity | `apollo-act` |
| Sequence | `apollo-seq` |
| Requirements | `apollo-req` |

Subsystem:

| View | File |
| --- | --- |
| Saturn V BDD / IBD | `apollo-sat-bdd` · `apollo-sat-ibd` |
| CSM BDD / IBD | `apollo-csm-bdd` · `apollo-csm` |
| LM BDD / IBD | `apollo-lm-bdd` · `apollo-lm` |
| GNC package | `apollo-gnc-pkg` |
| CMC entry STM | `apollo-cmc-stm` |
| LGC landing STM | `apollo-lgc-stm` |
| Ground BDD / IBD | `apollo-gnd-bdd` · `apollo-gnd` |
| Crew | `apollo-crew` |
| USB / command | `apollo-usb` · `apollo-cmd` |
| ECLSS / parametric | `apollo-eclss` · `apollo-eclss-par` |
| Electrical | `apollo-eps` |
| AGS BDD | `apollo-ags-bdd` |
| Docking | `apollo-dock` |
| RCS | `apollo-rcs` |

Full captions: [README.md](README.md).

![Apollo mission STM](apollo-stm.png)

![Apollo block definitions](apollo-bdd.png)

![Apollo vehicle stack](apollo-ibd.png)

![Apollo context](apollo-ctx.png)

![Apollo CSM](apollo-csm.png)

![Apollo LM](apollo-lm.png)

![Apollo ground](apollo-gnd.png)

## Validate and render

```bash
msml-validate-all projects/apollo --strict
msml-render-all projects/apollo
```
