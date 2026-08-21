# Apollo (system + subsystem)

Public NASA **Apollo 11 / Block II** instance on the generic Saturn V + CSM + LM stack. Civil / historical architecture only — no classified or biomedical detail.

Namespace `Apollo`. File stem `apollo`. Layout is `projects/apollo/`.

**Where 11 is atypical (notes only — not full examples):** Apollo 7 had no LM; 8 and 10 did not land; 13 aborted. Those missions are not separate projects.

Kept distinct: `AGC_CM`, `AGC_LM`, `DSKY`, `AGS`, IU `LVDC`, `USB`, RSO vs FLIGHT, crew as three parts, P27 vs CCATS. Collapsed: other MSFN ships/aircraft beyond the named 4 AIS + 8 ARIA; full loop directory; engine hydraulics; umbilical pinout. Named 30-ft only — do not merge GSFC-1968 and TN D-6723 into “the 14”.

Sourced numbers are on the model (USB RF, HGA, LM steerable, CM ECS, LM-5, A7L/PLSS, food plan). **UNKNOWN** (visible on the diagrams): RTCC MOC vs DSC on A11; 4th AIS ship; A11 actual food intake; entry blackout duration. Vehicles + AGC research is still incoming — those packages stay ready to fill.

## System views

| View | File | Story |
| --- | --- | --- |
| Packages | `apollo-pkg` | LaunchVehicle, Spacecraft, Crew, GNC, Ground, Comms, Mission |
| BDD | `apollo-bdd` | Saturn V + CSM + LM + LES + SLA |
| Context IBD | `apollo-ctx` | Vehicle / crew / MCC / RTCC / MSFN / Moon / Earth |
| Stack IBD | `apollo-ibd` | CSM–LM–Saturn interfaces (adjacent joints only) |
| STM | `apollo-stm` | countdown → … → recovery, plus abort machine |
| Activity | `apollo-act` | Same mission phases as a start-to-recovery flow |
| Sequence | `apollo-seq` | Landing: MCC → MSFN → USB → AGC_LM / CDR / radar / DPS |
| Requirements | `apollo-req` | Crew safety, landing, comms, LES, ECLSS, guidance |

## Subsystem views

| View | File | Story |
| --- | --- | --- |
| SaturnV BDD | `apollo-sat-bdd` | S-IC, S-II, S-IVB, IU, LVDC |
| SaturnV IBD | `apollo-sat-ibd` | Stack joints + IU LVDC |
| CSM IBD | `apollo-csm` | AGC_CM, IMU, DSKY, SCS, SPS, RCS, ECLSS |
| LM IBD | `apollo-lm` | PNGS, AGC_LM, AGS, DPS, APS, radars |
| Ground BDD | `apollo-gnd-bdd` | MCC-H / GSFC / MSFN / LC-39 / Recovery + consoles, AIS, ARIA |
| Ground IBD | `apollo-gnd` | Facility IBD; RSO/AFETR outside MCC; UNKNOWN marked |
| Crew IBD | `apollo-crew` | CDR / CMP / LMP each A7L · bio · comm; PLSS+OPS on CDR/LMP EVA only |
| USB comms | `apollo-usb` | Sourced RF; crew-selected antennas; P27 ≠ CCATS |
| Command sequence | `apollo-cmd` | Path A FC→CCC→RTCC→CCATS→642B→USB 70 kHz; Path B P27 V70–V73 |
| ECLSS activity | `apollo-eclss` | Cabin atmosphere loop (vehicle, not biomedical) |
| ECLSS parametric | `apollo-eclss-par` | Sourced CM / LM-5 / A7L numbers; food and blackout UNKNOWN |

Mission STM: countdown → boost → earthOrbit → TLI → translunar → LOI → undock → DOI → descent → surface/EVA → ascent → rendezvous → TEI → entry → recovery.

Abort machine (parallel): pad, I–IV, contingency TLI, lunar, SPS.
