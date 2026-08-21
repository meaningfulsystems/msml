# Apollo (system + subsystem)

Public NASA **Apollo 11 / Block II** instance on the generic Saturn V + CSM + LM stack. Civil / historical architecture only — no classified or biomedical detail.

Namespace `Apollo`. File stem `apollo`. Layout is `projects/apollo/`.

**Where 11 is atypical (notes only — not full examples):** Apollo 7 had no LM; 8 and 10 did not land; 13 aborted. Those missions are not separate projects.

Kept distinct: `AGC_CM`, `AGC_LM`, `DSKY`, `AGS`, IU `LVDC`, `USB`. Collapsed: engine hydraulics; MSFN ships (stations only).

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
| Ground IBD | `apollo-gnd` | KSC_LCC, MCC, RTCC, NASCOM, MSFN Goldstone / Madrid / Honeysuckle |
| ECLSS activity | `apollo-eclss` | Cabin atmosphere loop (vehicle, not biomedical) |

Mission STM: countdown → boost → earthOrbit → TLI → translunar → LOI → undock → DOI → descent → surface/EVA → ascent → rendezvous → TEI → entry → recovery.

Abort machine (parallel): pad, I–IV, contingency TLI, lunar, SPS.
