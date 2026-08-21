# Apollo — MagicGrid architecture walkthrough

A student can follow this note with `apollo-model.msml` open. It walks Apollo 11 / Block II on vehicle AS-506 from problem to solution in simplified MagicGrid order, then explains every generated view.

This is **not** a Department of Defense Architecture Framework (DoDAF) product set. There are no All Viewpoint (AV), Operational Viewpoint (OV), Systems Viewpoint (SV), Data and Information Viewpoint (DIV), or Technical Viewpoint (TV) products here.

NASA NPR 7123.1 (NASA Procedural Requirements 7123.1, NASA Systems Engineering Processes and Requirements) is the civil systems-engineering process this walkthrough teaches in **plain language**. Names stay MagicGrid, not NPR product titles. Do not treat MagicGrid section titles as NPR 7123.1 layer names.

| MagicGrid heading | NPR idea in plain language |
| --- | --- |
| 1. Problem / context | Who needs what from the mission |
| 2. Requirements and use cases | The shalls that implement those expectations, and the stories that use them |
| 3. Structure | How the stack is built — parts that realize the functions |
| 4. Behavior | How the design solution operates in time |
| 5. Parametrics | Sourced numbers and analyses that support the design |
| 6. Allocations | Which part satisfies which shall |
| 7. Open risks / unmarked | What the sources do not close — do not invent |

Namespace `Apollo`. File stem `apollo`. Civil / historical architecture only — no classified or biomedical detail. Numbers are from NASA primary sources; a few values (including an official Command/Service Module (CSM) lunar Δv table) are intentionally left unmarked.

The instance is Apollo 11 / Block II on vehicle AS-506: SA-506 = S-IC-6 / S-II-6 / S-IVB-6N / IU-6 / SLA-14 / CSM-107 / LM-5. Apollo 7, 8, 10, and 13 are notes, not separate projects (7 had no Lunar Module (LM); 8 and 10 did not land; 13 aborted).

## 1. Problem / context

**Who (stakeholders).** Flight crew: Commander (CDR), Command Module Pilot (CMP), Lunar Module Pilot (LMP). Launch commit at Kennedy Space Center (KSC) Launch Complex 39 (LC-39). Flight control after tower clear at Mission Control Center Houston (MCC-H). MCC is Mission Control Center Houston, not a midcourse correction burn. Apollo 11 used Mission Operations Control Room 2 (MOCR 2). Trajectory and uplink compute at the Real-Time Computer Complex (RTCC). Ground network: Goddard Space Flight Center (GSFC) / NASA Communications Network (NASCOM) and the Manned Space Flight Network (MSFN). Range Safety Officer (RSO) / Air Force Eastern Test Range (AFETR) owns destruct **outside** MCC. Recovery is Task Force 130 (TF-130) / USS *Hornet*. Earth and Moon are landing / launch-recovery context.

Handoff is KSC → MCC at tower clear — Mission Rule 1-21. RSO is not MCC.

**Boundary.** Inside the stack: Saturn V (S-IC, S-II, S-IVB, Instrument Unit (IU)), Launch Escape System (LES), Spacecraft-LM Adapter (SLA), CSM (Command Module (CM) + Service Module (SM)), LM-5 (descent + ascent). Ground facilities are first-class parts, not one Ground actor.

**Kept distinct, not folded:** two Apollo Guidance Computers (AGC) — `AGC_CM` Colossus / Comanche 055 + two Display and Keyboard (DSKY); `AGC_LM` Luminary 1A / LMY99 rev 001 + one DSKY; Abort Guidance System (AGS) = Abort Electronics Assembly (AEA) + Abort Sensor Assembly (ASA) + Data Entry and Display Assembly (DEDA), not a DSKY and not a landing computer; IU = Launch Vehicle Digital Computer (LVDC) + ST-124 + Flight Control Computer (FCC); no digital AGC↔LVDC; Entry Monitor System (EMS), independent of AGC; descent vs ascent; SM fuel cells vs CM silver-zinc (AgZn) vs LM AgZn; SM Reaction Control System (RCS) quads vs CM dual 6-engine sets; Unified S-Band (USB) vs Very High Frequency / High Frequency (VHF/HF) backup; RSO/AFETR outside MCC; crew as three parts.

**Mission.** Lunar-orbit rendezvous: boost and Translunar Injection (TLI) on Saturn, dock and extract the LM, coast translunar, Lunar Orbit Insertion (LOI), land, Extravehicular Activity (EVA), ascent, rendezvous, Trans-Earth Injection (TEI), entry, and recovery.

There is no stage-to-stage Launch Vehicle (LV) electrical power on Saturn, and no CSM–LM propellant crossfeed.

Sources used on the model include Apollo 11 Press Kit (PK) 69-83K, Saturn V Flight Manual extracts, Apollo Experience Reports, Apollo Guidance Computer Information Series (AGCIS) / Massachusetts Institute of Technology (MIT) Instrumentation Laboratory, and Technical Notes (TN) D-6718 / D-6724 / D-7082 / D-7143 / D-7375 / D-8093 / TN-7990 / D-7720. Values not in those extracts stay unmarked.

## 2. Requirements and use cases

The technical shalls that implement those stakeholder expectations:

| Id | Name | Text / numbers |
| --- | --- | --- |
| `Apollo.crewSafetyRequirement` (REQ-001) | Crew Safety | An abort path shall remain available from pad through TEI for the crew. **Not LES-only.** |
| `Apollo.landingRequirement` (REQ-002) | Landing | The LM shall land with remaining descent Δv margin at the site. (Margin is required; an official CSM lunar Δv table is **not** filled.) |
| `Apollo.commsContinuityRequirement` (REQ-003) | Comms Continuity | USB / MSFN shall carry voice and telemetry except known lunar occultation. |
| `Apollo.lesAbortRequirement` (REQ-004) | LES Abort | LES shall pull the CM clear of Saturn on a pad or Mode I abort. |
| `Apollo.eclssRequirement` (REQ-005) | Cabin Atmosphere | CM Environmental Control System (ECS) / Environmental Control and Life Support System (ECLSS): 3 crew / 14 d spec; **5.0 psia 100% O2**; CO2 ≤7.6 torr; SM O2 640 lb; potable 36 lb / waste 56 lb; LiOH 1.5 man-day, swap 12 h. A11 mission **196 h** vs 336 h spec. Vehicle ECLSS, not a biomedical model. |
| `Apollo.guidanceRequirement` (REQ-006) | Guidance | AGC_CM and AGC_LM shall provide Guidance, Navigation, and Control (GNC); AGS is the LM abort backup. |
| `Apollo.usbRfRequirement` (REQ-007) | USB Radio Frequency (RF) (sourced) | CSM **2106.40625** ↑ / **2287.5** Phase Modulation (PM) ↓ / **2272.5** Frequency Modulation (FM); LM **2101.802** ↑ / **2282.5**. Pulse-Code Modulation (PCM) 51.2 or 1.6 kbps. Uplink digital ~2 kbps. Pseudo-Random Noise (PRN) range 992 kbps, ±15 m, ~540,000 mi unambiguous. |
| `Apollo.p27Requirement` (REQ-008) | P27 uplink verbs | P27 uplink verbs **only V70–V73** into Command Module Computer (CMC) / LM Guidance Computer (LGC). Separate from the Command, Communications, and Telemetry System (CCATS) command-load path. Path A is the CCATS load. Path B is P27. |
| `Apollo.foodRequirement` (REQ-009) | Food plan (D-7720) | **D-7720 April 1967** plan baseline: **2800 kcal/man/day CM**, **3200 kcal/man/day LM**. Mass **2.26 lb/man/day** planned. 1967 plan, not A11 flown intake. A11 actual kcal still UNKNOWN. |
| `Apollo.lmEcsRequirement` (REQ-010) | LM-5 ECS (sourced) | Descent O2 ~48 lb @ **2800 vs 3000 psi** (TN D-6724 — cite both); ascent O2 ~2.4 lb ×2; descent water 332 lb; ascent water 42 lb ×2; Liquid Cooling Garment (LCG) 1200 Btu/man-h steady. |

There is no formal use-case package on this MSML model the way the appliances have `Toaster.UC.*`. The stakeholder stories are recovered from the mission state machine (STM), abort STM, activity, and sequences: fly the mission, abort, land, recover.

## 3. Structure

Decomposition of the stack into the parts that realize those functions, before reading a physical-subsystem diagram.

Pad stack: S-IC-6, S-II-6, S-IVB-6N, IU-6, SLA-14 (**8 panels: 4 jettison / 4 stay**; LM-5), SM (owns **SPS**), CM, LES.

Two AGCs stay separate from AGS. AGS ≠ DSKY. IU = LVDC + ST-124 + FCC; no digital AGC↔LVDC.

The design solution on the model:

**SPS is on the SM, not the CM.** Service Propulsion System (SPS) composition is `Apollo.SM` → `Apollo.SPS`. The CSM internal block diagram (IBD) nests `sps` inside `sm`. Do not hang SPS on the command module.

**Landing Radar (LR) is on the LM descent stage only** (three-beam, P63–P64). Composition is `Apollo.Descent` → `Apollo.LandingRadar`. **Rendezvous Radar (RR) is on the ascent stage only.** Composition is `Apollo.Ascent` → `Apollo.RendezvousRadar`. Primary Guidance and Navigation System (PNGS) is the cockpit switch label for Primary Guidance, Navigation and Control System (PGNCS). PNGS stays on the LM; AGC_LM stays under PNGS. Do not nest rendezvous radar in PNGS. Do not park landing radar under PNGS on the ascent tree.

Guidance computers stay separate:

- IU LVDC owns boost + TLI (82.03125 µs, 26+2 bits). No digital path from AGC to LVDC.
- AGC_CM (Block II, 2048 E / 36864 F, 11.7 µs, Comanche 055 + 2 DSKY) owns LOI / TEI / entry (P61–P67).
- AGC_LM (Luminary 1A + 1 DSKY) owns landing / ascent / LM abort (P63–P68 land; P70 Descent Propulsion System (DPS) / P71 Ascent Propulsion System (APS)). APS here is the LM Ascent Propulsion System, not S-IVB ullage (also historically called APS).
- AGS (AEA 4096×18, 5 µs, 32.7 lb, TN-7990) is abort-to-orbit / rendezvous only. DEDA is not a DSKY.

Electrical: SM three fuel cells on A11 2 H2 + 2 O2 cryo; CM three AgZn + Lower Equipment Bay (LEB) charger + separate pyro; LM four descent + two ascent AgZn with an Electronic Control Assembly (ECA) on each battery. No stage-to-stage LV electrical power.

Command paths stay distinct: Path A is Flight Controller (FC) → Command Control Console (CCC) → RTCC → CCATS → site 642B → USB 70 kHz. Path B is P27 V70–V73 into CMC/LGC.

VHF backup is 296.8 / 259.7 MHz (CSM–LM–EVA). Recovery beacon is 243.0 MHz, 3 W, 2 s on / 3 s off.

Docking hardware: CM probe, LM drogue, twelve ring latches. Soft dock then hard dock; hardware removed for transfer.

## 4. Behavior

How the design solution operates in time — mission, abort, and computer modes.

Mission STM (locked):

countdown → boost → earthOrbit → TLI → dockEject → translunar → LOI → undock → Descent Orbit Insertion (DOI) → descent → surface/EVA → ascent → rendezvous → TEI → entry → recovery.

`dockEject` is its own state (CMP-owned, SM RCS, probe-drogue). Do not draw TLI → translunar or dockEject → LOI, and do not put translunar before dockEject. The locked path is TLI → dockEject → translunar → LOI.

Ground Elapsed Time (GET): distinguish **planned** vs **flown**. Earth orbit **100 nmi is planned**. TLI has **three labeled numbers** (do not collapse): Press Kit **planned** `02:44:15`; A11-FP **planned** `2:44:26`; **flown** `02:44:16` (MSC-00171). TDE `~03:20–04:09` GET is **planned**, not flown. LOI-1 has **two strings only**: `75:54:28` GET is **A11-FP planned**; **flown** LOI-1 is `~075:49:50` GET (PAD/MR). Do **not** call TLI `02:44:15`, TDE, or LOI-1 `75:54:28` flown. Splash `195:18:35` Mission Elapsed Time (MET) / 13 nmi sits on Recovery as a sourced MET; that block is not labeled flown. P66 Rate of Descent (ROD) as the A11 landing program is a separate flown-program mark, not a GET clock.

Abort machine (parallel): pad/LES, Modes I–IV, contingency TLI, SPS abort, lunar abort (P70 DPS / P71 APS). Crew Safety ≠ LES-only.

CMC P61–P67 is entry only. LGC P63–P68 is landing only (A11 flew P66 Rate of Descent (ROD)). Do not share one P-number STM. Handoff is Mission Rule 1-21 at umbilical-tower clear. RSO ≠ MCC; RSO owns destruct until orbital safing.

The mission activity is the same phase list as a start-to-recovery flow. The landing sequence is MCC → MSFN → USB → AGC_LM / CDR / radar / DPS.

## 5. Parametrics

Analyses and sourced numbers that support the design. Conflicts stay **UNRECONCILED** — cite both, no silent winner.

A11 Press Kit p.109 tank loads and launch masses unless noted. **UNRECONCILED** — same flag as Δv. These are sourced stage loads, **not a closed mass budget**.

| Item | Value |
| --- | --- |
| S-IC (AS-506 / S-IC-6) | 7,653,854 lbf liftoff / 5,022,674 lb fueled (A11 PK p.109) |
| F-1 per engine | 1,530,000 lbf — **SA-507 citation** on the F-1 block. Not an AS-506 requirement. |
| S-II | 1,059,171 lb (S-II-6) |
| S-IVB | 260,523 lb (S-IVB-6N) |
| IU | 4,306 lb (IU-6) |
| CM | 12,250 lb |
| SM | 51,243 lb |
| LM-5 | 33,205 lb |
| DPS load | 18,100 lb |
| APS load | 5,214 lb |
| LM RCS | 604 lb; 100 lbf/engine (PK p.106) |
| SM RCS | 100 lbf/engine (PK p.93) |
| CM RCS | 93 lbf/engine, two 6-engine sets |
| LES | 8,930 lb |
| AGC | Block II 2048 E / 36864 F, 11.7 µs, 65 lb / 70 W; AGC_CM Comanche 055 + 2 DSKY; AGC_LM Luminary 1A + 1 DSKY |
| AEA | 4096 × 18-bit, 5 µs, 32.7 lb (TN-7990) |
| APS thrust | 3,500 lbf, 1.5° cant, not gimbaled (TN D-7082) |
| Portable Life Support System (PLSS) | 4 h / 1.04 lb O2 (CDR EVA 2:48, LMP 2:40) |

Cite **both** SPS figures: 20,500 lbf (PK) vs 21,500 lbf vac (TN D-7375). Cite **both** DPS figures: 9,870 / 1,050–6,300 lbf (PK) vs 10,500 lbf and 10:1 (TN D-7143). Descent O2 **2800 vs 3000 psi** (TN D-6724 — cite both). USB and VHF stay as already on the model (section 2 and 3).

The ECLSS parametric view binds the sourced CM / LM-5 / A7L (Apollo A7L pressure suit) numbers and the D-7720 food plan. A11 actual kcal and entry blackout stay UNKNOWN.

Fuel-cell wattage is not in the press kit; a secondary National Air and Space Museum (NASM) band is noted on the fuel-cell block and is not promoted to a requirement.

## 6. Allocations

Which part satisfies which shall:

| Requirement | Allocated to |
| --- | --- |
| Crew Safety | LES (pad / Mode I only), SPS (SPS abort), DPS (P70), APS (P71), AGS (lunar abort backup), ECLSS, CM RCS |
| Landing | Descent (DPS stage) |
| Comms Continuity | USB, MSFN |
| LES Abort | LES |
| Cabin Atmosphere | ECLSS |
| Guidance | AGC_CM, AGC_LM, AGS |
| USB RF | satisfied by USB |
| P27 uplink verbs | satisfied by P27 |

Food plan and LM-5 ECS are on the model as requirements; they do not have `allocate` edges. Treat them as sourced constraints on ECLSS / LM-5, not as invented allocations.

Design bindings that the structure already states (not extra req ids): boost/TLI → IU LVDC; LOI/TEI/entry → AGC_CM; landing/ascent/LM abort → AGC_LM with AGS backup (AGS does not land); EVA portable loop → PLSS on CDR/LMP only; trajectory/uplink compute → RTCC; launch commit → KSC; destruct → RSO; heat shield → CM only.

## 7. Open risks / unmarked

Left unmarked on purpose. Do **not** invent:

- Official CSM lunar Δv table
- CSM-107 SPS loaded mass
- Loaded SM RCS propellant mass
- Loaded CM RCS propellant mass
- A11 AGS flight-program name
- A11 actual kcal
- RTCC Mission Operations Computer (MOC) vs Dynamic Standby Computer (DSC) assignment on A11
- 4th Apollo Instrumentation Ship (AIS) identity
- Entry blackout duration
- Full 30-ft MSFN map

F-1 1,530,000 lbf stays the SA-507 per-engine citation. Do not promote it into an AS-506 requirement. AS-506 S-IC liftoff remains 7,653,854 lbf (PK p.109).

Descent O2 tank pressure is cited both ways (2800 vs 3000 psi, TN D-6724). Tank loads stay **UNRECONCILED**, same flag as Δv. SPS 20,500 vs 21,500 vac and DPS PK vs TN D-7143 stay cited both ways, no silent winner.

## Generated views

These figures illustrate the architecture above; they do not replace it. Every rendered figure in this folder is listed. Read them in MagicGrid order: context, requirements, structure, behavior, sourced numbers, then which part satisfies which shall. Do not treat those figure roles as NPR 7123.1 layer names.

**`apollo-pkg.png` — packages.** LaunchVehicle, Spacecraft, Crew, GNC, Ground, Comms, Mission. Read this first to see how the model is filed.

**`apollo-bdd.png` — block definition diagram (BDD).** Saturn V + CSM + LM + LES + SLA at system grain. Logical stack.

**`apollo-ctx.png` — context IBD.** Vehicle / crew / MCC / RTCC / MSFN / Moon / Earth. Externals stay here, not inside the stack IBD.

**`apollo-ibd.png` — stack IBD.** Vehicle stack + SLA/LES. Adjacent joints only; connections never pass over boxes.

**`apollo-stm.png` — mission STM.** countdown → TLI → dockEject → translunar → LOI → … → recovery. Confirm `dockEject` sits between TLI and translunar.

**`apollo-abort.png` — abort STM.** pad/LES, Modes I–IV, contingency TLI, SPS abort, P70 DPS / P71 APS. Crew Safety is not LES-only.

**`apollo-act.png` — mission activity.** Same phases as a start-to-recovery control flow. Functional.

**`apollo-seq.png` — landing sequence.** MCC → MSFN → USB → AGC_LM / CDR / radar / DPS.

**`apollo-req.png` — requirements.** Crew safety, landing, comms, LES, ECLSS, guidance, USB, P27, D-7720 food, LM-5 ECS.

**`apollo-sat-bdd.png` — Saturn V BDD.** A11 PK p.109 tank loads. S-IC / S-II / S-IVB / IU + engines. F-1 1,530,000 lbf is the SA-507 citation.

**`apollo-sat-ibd.png` — Saturn V IBD.** Stack joints + IU LVDC. No stage-to-stage LV electrical power.

**`apollo-csm-bdd.png` — CSM BDD.** CM/SM, Comanche 055 / Colossus, EMS, SPS cite both 20,500 and 21,500.

**`apollo-csm.png` — CSM IBD.** CM GNC. SM owns SPS. RCS and ECLSS. **SPS is on the SM.**

**`apollo-lm-bdd.png` — LM BDD.** Descent + landing radar (LR); ascent + rendezvous radar (RR); DPS/APS; AGC_LM + one DSKY; AGS.

**`apollo-lm.png` — LM IBD.** PNGS, AGC_LM, AGS, descent + landing radar (three-beam), ascent + rendezvous radar, DPS, APS. RR is not nested in PNGS.

**`apollo-gnc-pkg.png` — GNC packages.** AGC ≠ LVDC digital. CMC entry ≠ LGC landing. EMS separate.

**`apollo-cmc-stm.png` — CMC entry STM.** P61–P67 ENTRY only.

**`apollo-lgc-stm.png` — LGC landing STM.** P63–P68 LANDING. A11 flew P66 ROD.

**`apollo-gnd-bdd.png` — ground BDD.** MCC-H / GSFC / MSFN / LC-39 / Recovery, consoles, AIS, Apollo Range Instrumentation Aircraft (ARIA).

**`apollo-gnd.png` — ground IBD.** Facility wiring. RSO/AFETR outside MCC. UNKNOWN markers stay visible.

**`apollo-crew.png` — crew IBD.** CDR / CMP / LMP each in an A7L suit. PLSS + Oxygen Purge System (OPS) on CDR/LMP EVA only. OPS is the EVA Oxygen Purge System, not operations.

**`apollo-usb.png` — USB comms.** Sourced RF. Crew-selected antennas. P27 ≠ CCATS. Path A vs Path B.

**`apollo-cmd.png` — command sequence.** Path A FC→CCC→RTCC→CCATS→642B→USB 70 kHz; Path B P27 V70–V73.

**`apollo-eclss.png` — ECLSS activity.** Cabin atmosphere loop (vehicle, not biomedical).

**`apollo-eclss-par.png` — ECLSS parametrics.** Sourced CM / LM-5 / A7L numbers; D-7720 food plan; A11 intake and blackout UNKNOWN.

**`apollo-eps.png` — electrical IBD.** SM 3× fuel cells; CM 3× AgZn + LEB charger + pyro; LM 4+2 AgZn + ECA; 28 V / 117 V 400 Hz.

**`apollo-ags-bdd.png` — AGS BDD.** AEA + ASA (strapdown) + DEDA (not a DSKY). Sourced AEA memory (4096×18, 5 µs, 32.7 lb).

**`apollo-dock.png` — docking sequence.** Probe / drogue / soft capture / 12 latches / stow / transfer.

**`apollo-rcs.png` — RCS package.** SM / LM 100 lbf (A11 PK p.93 / p.106). CM dual 6-engine 93 lbf. Loaded mass UNKNOWN.

```bash
msml-validate-all projects/apollo --strict
msml-render-all projects/apollo
```
