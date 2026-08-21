# Apollo (system + subsystem)

Public NASA **Apollo 11 / Block II** instance, vehicle **AS-506**, on the generic Saturn V + CSM + LM stack. Civil / historical architecture only — no classified or biomedical detail.

Namespace `Apollo`. File stem `apollo`. Layout is `projects/apollo/`.

**Where 11 is atypical (notes only — not full examples):** Apollo 7 had no LM; 8 and 10 did not land; 13 aborted. Those missions are not separate projects.

Kept distinct: two AGCs (`AGC_CM` Colossus + 2 DSKY, `AGC_LM` Luminary + 1 DSKY), `AGS` (AEA+ASA+DEDA, not a DSKY), IU `LVDC` + ST-124 + FCC, `EMS`, descent vs ascent, `LES`, SM fuel cells vs CM AgZn vs LM batteries, SM RCS quads vs CM dual 6-engine sets, `USB`, RSO vs FLIGHT, crew as three parts, P27 vs CCATS. Collapsed: ullage/retro as sets, every verb/noun, F-1 hydraulics, other MSFN ships/aircraft beyond the named 4 AIS + 8 ARIA, full loop directory, umbilical pinout. Named 30-ft only — do not merge GSFC-1968 and TN D-6723 into “the 14”.

Sourced numbers are on the model (USB RF kept; VHF 296.8 / 259.7 and 243.0 MHz beacon; HGA, LM steerable, CM ECS, LM-5, A7L/PLSS, food 2.26 lb/man/day planned, A11 PK p.109 tank loads and launch masses, stack serials SA-506 = S-IC-6 / S-II-6 / S-IVB-6N / IU-6 / SLA-14 / CSM-107 / LM-5, F-1 / J-2, SPS and DPS cited from both PK and TNs, Block II AGC AGCIS 30, A11 ropes Comanche 055 / LMY99 rev 001, AEA 4096×18-bit, SM/LM RCS 100 lbf and CM RCS 93 lbf, A11 SM cryo 2 H2 + 2 O2, APS 3,500 lbf 1.5° cant not gimbaled, Hornet / TF-130 splash 195:18:35 MET 13 nmi, EVA CDR 2:48 / LMP 2:40). **UNKNOWN** (visible on the diagrams): RTCC MOC vs DSC on A11; 4th AIS ship; A11 actual kcal; entry blackout duration; official CSM lunar Δv table; CSM-107 SPS loaded lb; A11 AGS flight-program name; loaded SM/CM RCS propellant mass. Descent O2 tank pressure is 2800 vs 3000 psi (TN D-6724 — cite both). Do not invent those.

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
| SaturnV BDD | `apollo-sat-bdd` | A11 PK p.109 tank loads · S-IC / S-II / S-IVB / IU + engines · AS-506 |
| SaturnV IBD | `apollo-sat-ibd` | Stack joints + IU LVDC |
| CSM BDD | `apollo-csm-bdd` | CM/SM, Comanche 055 / Colossus 2A, EMS, SPS cite both |
| CSM IBD | `apollo-csm` | AGC_CM, IMU, DSKY, SCS, SPS, RCS, ECLSS |
| LM BDD | `apollo-lm-bdd` | descent/ascent, DPS/APS, AGC_LM + 1 DSKY, AGS (AEA+ASA) |
| LM IBD | `apollo-lm` | PNGS, AGC_LM, AGS, DPS, APS, radars |
| GNC package | `apollo-gnc-pkg` | AGC ≠ LVDC digital · CMC entry ≠ LGC landing · EMS |
| CMC entry STM | `apollo-cmc-stm` | P61–P67 ENTRY only — not LGC landing |
| LGC landing STM | `apollo-lgc-stm` | P63–P68 LANDING · A11 P66 ROD — not CMC entry |
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
| RCS package | `apollo-rcs` | SM / LM 100 lbf (A11 PK p.93 / p.106) · CM dual 6-engine 93 lbf · loaded mass UNKNOWN |

Mission STM: countdown → boost → earthOrbit (100 nmi planned) → TLI → translunar → dock/eject → LOI → undock → DOI → descent → surface/EVA → ascent → rendezvous → TEI → entry → recovery. IU owns boost+TLI; RSO owns destruct until orbital safing.

Abort machine (parallel): pad/LES, Modes I–IV, contingency TLI, SPS abort, lunar abort (P70 DPS / P71 APS).
