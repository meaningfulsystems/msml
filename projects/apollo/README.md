# Apollo (system + subsystem)

Public NASA **Apollo 11 / Block II** instance, vehicle **AS-506**, on the generic Saturn V + CSM + LM stack. Civil / historical architecture only — no classified or biomedical detail.

Namespace `Apollo`. File stem `apollo`. Layout is `projects/apollo/`.

**Where 11 is atypical (notes only — not full examples):** Apollo 7 had no LM; 8 and 10 did not land; 13 aborted. Those missions are not separate projects.

Kept distinct: two AGCs (`AGC_CM` Colossus + 2 DSKY, `AGC_LM` Luminary + 1 DSKY), `AGS` (AEA+ASA+DEDA, not a DSKY), IU `LVDC` + ST-124 + FCC, `EMS`, descent vs ascent, `LES`, SM fuel cells vs CM AgZn vs LM batteries, SM RCS quads vs CM dual 6-engine sets, `USB`, RSO vs FLIGHT, crew as three parts, P27 vs CCATS. Collapsed: ullage/retro as sets, every verb/noun, F-1 hydraulics, other MSFN ships/aircraft beyond the named 4 AIS + 8 ARIA, full loop directory, umbilical pinout. Named 30-ft only — do not merge GSFC-1968 and TN D-6723 into “the 14”.

Sourced numbers are on the model (USB RF, HGA, LM steerable, CM ECS, LM-5, A7L/PLSS, food plan, A11 PK masses, F-1 / J-2 / SPS / DPS / APS thrusts, Block II AGC AGCIS 30, AEA 4096×18-bit, CM RCS 93 lbf, electrical topology). **UNKNOWN** (visible on the diagrams): RTCC MOC vs DSC on A11; 4th AIS ship; A11 actual food intake; entry blackout duration; stage tank loads; Δv table; A11 rope IDs; SM RCS per-engine thrust (do not use 100 lbf unless cited). Do not invent those.

## System views

| View | File | Story |
| --- | --- | --- |
| Packages | `apollo-pkg` | LaunchVehicle, Spacecraft, Crew, GNC, Ground, Comms, Mission |
| BDD | `apollo-bdd` | Saturn V + CSM + LM + LES + SLA |
| Context IBD | `apollo-ctx` | Vehicle / crew / MCC / RTCC / MSFN / Moon / Earth |
| Stack IBD | `apollo-ibd` | Vehicle stack + SLA/LES (adjacent joints only; no line over boxes) |
| STM | `apollo-stm` | countdown → earthOrbit (100 nmi) → dock/eject → … → recovery |
| Abort STM | `apollo-abort` | pad/LES · Modes I–IV · contingency TLI · SPS · P70 DPS / P71 APS |
| Activity | `apollo-act` | Same mission phases as a start-to-recovery flow |
| Sequence | `apollo-seq` | Landing: MCC → MSFN → USB → AGC_LM / CDR / radar / DPS |
| Requirements | `apollo-req` | Crew safety, landing, comms, LES, ECLSS, guidance |

## Subsystem views

| View | File | Story |
| --- | --- | --- |
| SaturnV BDD | `apollo-sat-bdd` | S-IC / S-II / S-IVB / IU + F-1 ×5 / J-2 thrusts · AS-506 |
| SaturnV IBD | `apollo-sat-ibd` | Stack joints + IU LVDC |
| CSM BDD | `apollo-csm-bdd` | CM/SM, AGC_CM + 2 DSKY, EMS, SPS 20,500 lbf |
| CSM IBD | `apollo-csm` | AGC_CM, IMU, DSKY, SCS, SPS, RCS, ECLSS |
| LM BDD | `apollo-lm-bdd` | descent/ascent, DPS/APS, AGC_LM + 1 DSKY, AGS (AEA+ASA) |
| LM IBD | `apollo-lm` | PNGS, AGC_LM, AGS, DPS, APS, radars |
| GNC package | `apollo-gnc-pkg` | AGC_CM (2 DSKY) vs AGC_LM (1 DSKY) vs AGS vs IU LVDC vs EMS |
| Ground BDD | `apollo-gnd-bdd` | MCC-H / GSFC / MSFN / LC-39 / Recovery + consoles, AIS, ARIA |
| Ground IBD | `apollo-gnd` | Facility IBD; RSO/AFETR outside MCC; UNKNOWN marked |
| Crew IBD | `apollo-crew` | CDR / CMP / LMP each A7L · bio · comm; PLSS+OPS on CDR/LMP EVA only |
| USB comms | `apollo-usb` | Sourced RF; crew-selected antennas; P27 ≠ CCATS |
| Command sequence | `apollo-cmd` | Path A FC→CCC→RTCC→CCATS→642B→USB 70 kHz; Path B P27 V70–V73 |
| ECLSS activity | `apollo-eclss` | Cabin atmosphere loop (vehicle, not biomedical) |
| ECLSS parametric | `apollo-eclss-par` | Sourced CM / LM-5 / A7L numbers; food and blackout UNKNOWN |
| Electrical IBD | `apollo-eps` | SM 3× fuel cells · CM 3× AgZn + LEB charger + pyro · LM 4+2 AgZn + ECA · 28 V / 117 V 400 Hz |
| AGS BDD | `apollo-ags-bdd` | AEA + ASA (strapdown) + DEDA (not a DSKY); sourced AEA memory |
| Docking sequence | `apollo-dock` | Probe / drogue / soft capture / 12 latches / stow / transfer |
| RCS package | `apollo-rcs` | SM four quads (thrust UNKNOWN) · CM dual 6-engine 93 lbf sets |

Mission STM: countdown → boost → earthOrbit (100 nmi planned) → TLI → translunar → dock/eject → LOI → undock → DOI → descent → surface/EVA → ascent → rendezvous → TEI → entry → recovery. IU owns boost+TLI; RSO owns destruct until orbital safing.

Abort machine (parallel): pad/LES, Modes I–IV, contingency TLI, SPS abort, lunar abort (P70 DPS / P71 APS).
