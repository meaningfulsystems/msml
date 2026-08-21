# Apollo — Architecture / System Design

Apollo is a full lunar-orbit-rendezvous example: Saturn V, Block II CSM, LM-5, crew, and the ground network for Apollo 11 (AS-506). Read it as a system-of-systems model. Numbers are from NASA primary sources; a few values (including an official CSM lunar Δv table) are intentionally left unmarked.

Namespace `Apollo`. File stem `apollo`. Civil / historical architecture only — no classified or biomedical detail. This note is the design argument for the model in this folder, not a catalog of pictures.

Apollo 7, 8, 10, and 13 are notes, not separate projects (7 had no LM; 8 and 10 did not land; 13 aborted).

## 1. Purpose / context

The instance is Apollo 11 / Block II on vehicle AS-506: SA-506 = S-IC-6 / S-II-6 / S-IVB-6N / IU-6 / SLA-14 / CSM-107 / LM-5. The job is lunar-orbit rendezvous: boost and TLI on Saturn, dock and extract the LM, coast translunar, LOI, land, EVA, ascent, rendezvous, TEI, entry, and recovery.

Sources used on the model include Apollo 11 Press Kit 69-83K, Saturn V Flight Manual extracts, Apollo Experience Reports, AGCIS / MIT IL, and TN D-6718 / D-6724 / D-7082 / D-7143 / D-7375 / D-8093 / TN-7990. Values not in those extracts stay unmarked.

## 2. System boundary and actors

**Inside the stack:** Saturn V (S-IC, S-II, S-IVB, IU), LES, SLA, CSM (CM + SM), LM-5 (descent + ascent).

**Kept distinct, not folded:** two AGCs (`AGC_CM` Colossus / Comanche 055 + two DSKY; `AGC_LM` Luminary 1A / LMY99 rev 001 + one DSKY); AGS (AEA + ASA + DEDA, not a DSKY and not a landing computer); IU LVDC + ST-124 + FCC; EMS (independent of AGC); descent vs ascent; SM fuel cells vs CM AgZn vs LM AgZn; SM RCS quads vs CM dual 6-engine sets; USB vs VHF/HF backup; RSO/AFETR outside MCC; crew as three parts (CDR, CMP, LMP).

**Ground (first-class parts, not one Ground actor):** MCC-H (A11 used MOCR 2), GSFC / NASCOM, MSFN (Goldstone / Madrid / Honeysuckle 85-ft plus named 30-ft, AIS ships, ARIA), KSC LC-39, Recovery / TF-130 / Hornet, RSO and AFETR.

**Outside the vehicle:** Moon and Earth as landing / launch-recovery context.

There is no stage-to-stage electrical power on Saturn, and no CSM–LM propellant crossfeed.

## 3. Requirements

| Id | Name | Text / numbers |
| --- | --- | --- |
| `Apollo.crewSafetyRequirement` (REQ-001) | Crew Safety | An abort path shall remain available from pad through TEI for the crew. **Not LES-only.** |
| `Apollo.landingRequirement` (REQ-002) | Landing | The LM shall land with remaining descent Δv margin at the site. (Margin is required; an official CSM lunar Δv table is **not** filled.) |
| `Apollo.commsContinuityRequirement` (REQ-003) | Comms Continuity | USB / MSFN shall carry voice and telemetry except known lunar occultation. |
| `Apollo.lesAbortRequirement` (REQ-004) | LES Abort | LES shall pull the CM clear of Saturn on a pad or Mode I abort. |
| `Apollo.eclssRequirement` (REQ-005) | Cabin Atmosphere | CM ECS: 3 crew / 14 d spec; **5.0 psia 100% O2**; CO2 ≤7.6 torr; SM O2 640 lb; potable 36 lb / waste 56 lb; LiOH 1.5 man-day, swap 12 h. A11 mission **196 h** vs 336 h spec. Vehicle ECLSS, not a biomedical model. |
| `Apollo.guidanceRequirement` (REQ-006) | Guidance | AGC_CM and AGC_LM shall provide GNC; AGS is the LM abort backup. |
| `Apollo.usbRfRequirement` (REQ-007) | USB RF (sourced) | CSM **2106.40625** ↑ / **2287.5** PM ↓ / **2272.5** FM; LM **2101.802** ↑ / **2282.5**. PCM 51.2 or 1.6 kbps. Uplink digital ~2 kbps. PRN range 992 kbps, ±15 m, ~540,000 mi unambiguous. |
| `Apollo.p27Requirement` (REQ-008) | P27 uplink verbs | P27 uplink verbs **only V70–V73** into CMC/LGC. Separate from the CCATS command-load path. |
| `Apollo.foodRequirement` (REQ-009) | Food plan (D-7720) | **D-7720 April 1967** plan baseline: **2800 kcal/man/day CM**, **3200 kcal/man/day LM**. Mass **2.26 lb/man/day** planned. 1967 plan, not A11 flown intake. A11 actual kcal still UNKNOWN. |
| `Apollo.lmEcsRequirement` (REQ-010) | LM-5 ECS (sourced) | Descent O2 ~48 lb @ **2800 vs 3000 psi** (TN D-6724 — cite both); ascent O2 ~2.4 lb ×2; descent water 332 lb; ascent water 42 lb ×2; LCG 1200 Btu/man-h steady. |

## 4. Structure and interfaces

Pad stack: S-IC-6, S-II-6, S-IVB-6N, IU-6, SLA-14 (8 panels: 4 jettison / 4 stay; LM-5), SM (owns **SPS**), CM, LES.

**SPS is on the SM, not the CM.** Composition is `Apollo.SM` → `Apollo.SPS`. The CSM IBD nests `sps` inside `sm`. Do not hang SPS on the command module.

**Landing radar is on the LM descent stage** (three-beam, P63–P64), not ascent PNGS. Composition is `Apollo.Descent` → `Apollo.LandingRadar`. **Rendezvous radar is on the ascent stage.** Composition is `Apollo.Ascent` → `Apollo.RendezvousRadar`. PNGS stays on the LM; AGC_LM stays under PNGS. Do not park landing radar under PNGS on the ascent tree.

Guidance computers stay separate:

- IU LVDC owns boost + TLI (82.03125 µs, 26+2 bits). No digital path from AGC to LVDC.
- AGC_CM (Block II, 2048 E / 36864 F, 11.7 µs, Comanche 055) owns LOI / TEI / entry (P61–P67).
- AGC_LM (Luminary 1A) owns landing / ascent / LM abort (P63–P68 land; P70 DPS / P71 APS).
- AGS (AEA 4096×18, 5 µs) is abort-to-orbit / rendezvous only. DEDA is not a DSKY.

Electrical: SM three fuel cells on A11 2 H2 + 2 O2 cryo; CM three AgZn + LEB charger + separate pyro; LM four descent + two ascent AgZn with an ECA on each battery. No stage-to-stage electrical power.

Command paths stay distinct: Path A is FC → CCC → RTCC → CCATS → site 642B → USB 70 kHz. Path B is P27 V70–V73 into CMC/LGC.

VHF backup is 296.8 / 259.7 MHz (CSM–LM–EVA). Recovery beacon is 243.0 MHz, 3 W, 2 s on / 3 s off.

Docking hardware: CM probe, LM drogue, twelve ring latches. Soft dock then hard dock; hardware removed for transfer.

## 5. States and modes

Mission STM (locked):

countdown → boost → earthOrbit → TLI → dockEject → translunar → LOI → undock → DOI → descent → surface/EVA → ascent → rendezvous → TEI → entry → recovery.

`dockEject` is its own state (CMP-owned, SM RCS, probe-drogue). Do not draw TLI → translunar or dockEject → LOI, and do not put translunar before dockEject.

GET: distinguish **planned** vs **flown**. Earth orbit **100 nmi is planned**. A11 **flown**: TLI 02:44:15 GET; TDE ~03:20–04:09 GET; LOI-1 75:54:28 GET; splash 195:18:35 MET / 13 nmi (Hornet / TF-130).

Abort machine (parallel): pad/LES, Modes I–IV, contingency TLI, SPS abort, lunar abort (P70 DPS / P71 APS).

CMC P61–P67 is entry only. LGC P63–P68 is landing only (A11 flew P66 ROD). Do not share one P-number STM. Handoff is Mission Rule 1-21 at umbilical-tower clear. RSO ≠ MCC; RSO owns destruct until orbital safing.

## 6. Allocations (req → part)

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

## 7. Sourced numbers

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
| AGC | 2048 E / 36864 F, 11.7 µs, 65 lb / 70 W; Comanche 055 / Luminary 1A |
| AEA | 4096 × 18-bit, 5 µs, 32.7 lb (TN-7990) |
| APS thrust | 3,500 lbf, 1.5° cant, not gimbaled (TN D-7082) |
| PLSS | 4 h / 1.04 lb O2 (CDR EVA 2:48, LMP 2:40) |

Cite **both** SPS figures: 20,500 lbf (PK) vs 21,500 lbf vac (TN D-7375). Cite **both** DPS figures: 9,870 / 1,050–6,300 lbf (PK) vs 10,500 lbf and 10:1 (TN D-7143). USB and VHF stay as already on the model (section 3 and 4).

## 8. Open risks / TBD

Left unmarked on purpose. Do **not** invent:

- Official CSM lunar Δv table
- CSM-107 SPS loaded mass
- Loaded SM RCS propellant mass
- Loaded CM RCS propellant mass
- A11 AGS flight-program name
- A11 actual kcal
- RTCC MOC vs DSC assignment on A11
- 4th AIS ship identity
- Entry blackout duration

F-1 1,530,000 lbf stays the SA-507 per-engine citation. Do not promote it into an AS-506 requirement. AS-506 S-IC liftoff remains 7,653,854 lbf (PK p.109).

Descent O2 tank pressure is cited both ways (2800 vs 3000 psi, TN D-6724). Fuel-cell wattage is not in the press kit; a secondary NASM band is noted on the fuel-cell block and is not promoted to a requirement.

## 9. Views in this folder

Every rendered figure that is actually here:

`apollo-pkg.png`, `apollo-bdd.png`, `apollo-ctx.png`, `apollo-ibd.png`, `apollo-stm.png`, `apollo-abort.png`, `apollo-act.png`, `apollo-seq.png`, `apollo-req.png`, `apollo-sat-bdd.png`, `apollo-sat-ibd.png`, `apollo-csm-bdd.png`, `apollo-csm.png`, `apollo-lm-bdd.png`, `apollo-lm.png`, `apollo-gnc-pkg.png`, `apollo-cmc-stm.png`, `apollo-lgc-stm.png`, `apollo-gnd-bdd.png`, `apollo-gnd.png`, `apollo-crew.png`, `apollo-usb.png`, `apollo-cmd.png`, `apollo-eclss.png`, `apollo-eclss-par.png`, `apollo-eps.png`, `apollo-ags-bdd.png`, `apollo-dock.png`, `apollo-rcs.png`.

![Apollo mission STM](apollo-stm.png)

![Apollo block definitions](apollo-bdd.png)

![Apollo vehicle stack](apollo-ibd.png)

![Apollo context](apollo-ctx.png)

![Apollo CSM](apollo-csm.png)

![Apollo LM](apollo-lm.png)

![Apollo ground](apollo-gnd.png)

```bash
msml-validate-all projects/apollo --strict
msml-render-all projects/apollo
```
