# Agent guide for MSML

This repository is **MSML**: a SysML 1-inspired modeling language. The model is JSON (`.msml`). The view and layout are JSON (`.msmd`). The renderer writes PNG next to each view.

It is **not** SysML v2, and it does **not** replace commercial SysML 2 tools.

## Sibling toolchain

[SysML2d](https://github.com/meaningfulsystems/sysml2d) is the paired git-native SysML v2 diagram toolchain (`.sysml` · intent JSON · `.sysmld` · SVG).

| | This repo (MSML) | SysML2d |
| --- | --- | --- |
| Language | SysML 1-inspired (not SysML v2) | SysML v2 |
| Files | `.msml` · `.msmd` · PNG | `.sysml` · intent JSON · `.sysmld` · SVG |
| Shared | ElectricBike *names* (frozen) | Same names — different language |

A first-time systems engineer picks **one** toolchain per project. Do not mix `.sysml` and `.msml` in the same model. The ElectricBike example uses the same qualified names in both repos so the Friday joint story can show the same bike.

## How an agent works here

Run this loop. The four skill slugs are locked so they match SysML2d.

1. **[bootstrap-project](skills/bootstrap-project/SKILL.md)** — copy `templates/new-project/`, copy the spec, write the first model and one view, validate and render.
2. **[author-model](skills/author-model/SKILL.md)** — edit `.msml` (blocks, parts, ports, requirements, allocate, states, activities).
3. **[compose-views](skills/compose-views/SKILL.md)** — write `.msmd` views. The shared slug is `compose-views`; MSML’s verb is **render** (`msml-render`, `msml-render-all`).
4. **[vision-review](skills/vision-review/SKILL.md)** — inspect every PNG with vision before commit.

Hard visual rule (via SysML2d): **connections never pass over boxes.** Hop-overs are only for line-on-line crossings. IBD is the highest visual priority.

Starter: [templates/new-project/](templates/new-project/). Spec: [msml-specification.md](msml-specification.md).

## ElectricBike locks

`projects/e-bike/` is the Friday hero. Namespace `ElectricBike`. File stem `e-bike`. Do not remap ids.

- Context is rider / charger / ElectricBike / road only. Do not promote Wheel Torque to a context actor.
- IBD is internal structure of ElectricBike. Do **not** put rider, charger, or road on the IBD — they belong on the context view. Charge, if shown, is a **boundary port** on the bike, not a charger part. Honest charge path is charger → bms → pack (UL 2849); do not feed pack and BMS in parallel. Nested `bms` stays inside BatteryPack. Connectors never pass through boxes. Child ports keep mount / command / inhibit / pack power / phase drive as distinct lines.
- Requirements are siblings. Brake Override refines Ride Safety; Battery Cutoff refines Charge Safety. Additional siblings: motor-assist cut-off (`motorAssistCutoffRequirement`, EN 15194:2017 **4.2.13 Power management**: 2 m, or 5 m if brake-lever switches relax it — **not** vehicle brake distance, **not** allocated to BrakeSystem), Lighting (StVZO / ISO 6742), Walk Assist (≤ 6 km/h), Continuous Power (250 W). Do **not** hang walk or 250 W under Assist Limit. 50 ms is an electronic inhibit budget on brake override only; do not compare it to the EN distance test.
- Range 500 Wh / 60 km is a **Tour-mode** scenario via `usableWh` / `energyPerKm` (~8.3 Wh/km), not Eco / PAS-1. `energyBalance` binds usable pack Wh + `energyPerKm`; do **not** add rider watts into pack energy.
- RideControl: off / standby / assist / walk (≤ 6 km/h, EPAC, not throttle) / charging / fault. `resetFault` is Fault→Off (not Standby). Standby —`powerOff`→ Off so a rider can power down without faulting. Charging from Off only — an EPAC choice on the do-behavior or a note; the state name is `charging`, not “Charging from Off only”. Do **not** add Standby→Charging.
- Classification is **EPAC / EN 15194** (cadence only, 25 km/h, no throttle). Display the motor as **Rear Geared Hub** (id stays `ElectricBike.HubMotor`); regen omitted. Hub properties: `continuousAssist` **250 W** (EU continuous, not peak) and `peakTorque` **40 N·m** (hub peak, not continuous).
- Nested usage `bms : BMS` lives inside BatteryPack (`ElectricBike::BatteryPack::bms`). `allocateChargeToBms` targets that usage, not the pack.
- Do **not** keep `lockBikeUseCase`. Empty use cases are not allowed.
- Ride safety is not brakes-only: allocate to BrakeSystem, MotorController, `cadenceSensor`, and `bms`. Allocate Assist Limit to `wheelSpeedSensor` (cadence-only cannot enforce 25 km/h). Usages: `cadenceSensor`, `wheelSpeedSensor`. Nested `bms : BMS` is on the IBD charge path when the layout stays readable.
- Ride «include» Adjust Assist. Rider on Ride + Adjust; Charger on Charge only. Do **not** put Charger on Adjust Assist.
- Activity action display is **Pedal (EPAC)**, not throttle.

## Apollo (publish)

`projects/apollo/` is a full system + subsystem example (morning deliverable with e-bike). Namespace `Apollo`. File stem `apollo`. Public NASA architecture only. Do not invent classified or biomedical detail.

- **Instance lock:** Apollo 11 / Block II, vehicle AS-506. The modeled stack is the generic Saturn V + CSM + LM used by lunar-landing missions.
- Where 11 is atypical, call it out in comments only. Do **not** stand up Apollo 7 / 8 / 10 / 13 as separate projects: 7 had no LM, 8 and 10 did not land, 13 aborted.
- **Names (exact):** SaturnV S-IC / S-II / S-IVB / IU; engines F-1 / J-2 (keep S-II and S-IVB J-2 separate); CSM CM / SM / SCS / AGC_CM / IMU / DSKY / DSKY2 / EMS / SPS (on SM, not CM) / RCS / ECLSS; LM descent / ascent / PNGS / AGC_LM / DSKY_LM / AGS (AEA+ASA+DEDA) / DPS / APS / RCS / landingRadar (descent, three-beam, P63–P64) / rendezvousRadar (ascent); IU LVDC + ST-124 + FCC; SLA 8 panels (4 jettison / 4 stay); electrical FuelCell ×3 / CM AgZn ×3 + LEB charger + pyro / LM AgZn 4+2 with ECA / 28 V DC / inverters; docking probe / drogue / 12 latches; Crew CDR / CMP / LMP each with A7L / bio / comm (PLSS+OPS on CDR/LMP EVA only); Ground as first-class parts: MCC-H (MOCR consoles, SSR, RTCC, CCATS), GSFC (NASCOM, NTTF, NST), MSFN (3×85-ft USB + named 30-ft only + 4 AIS + 8 ARIA + Goldstone 210-ft + Parkes), KSC LC-39, Recovery, RSO/AFETR outside MCC; plus SLA and LES.
- Do **not** collapse two AGCs, AGS (AEA+ASA+DEDA ≠ DSKY), IU LVDC, descent vs ascent, LES, CM 2 DSKY vs LM 1 DSKY, EMS, SM fuel cells vs CM AgZn vs LM batteries, SM quads vs CM dual 6-engine sets. Do collapse ullage/retro as sets, every verb/noun, F-1 hydraulics, other MSFN ships/aircraft, full loop directory, umbilical pinout. Do **not** merge GSFC-1968 and TN D-6723 into “the 14”.
- Sourced numbers only (USB RF, HGA, LM steerable, CM ECS, LM-5, A7L/PLSS, D-7720 April 1967 food plan 2800 kcal/man/day CM / 3200 LM — not A11 flown intake, A11 PK p.109 tank loads **UNRECONCILED** like Δv not a closed mass budget, engine thrusts cited from both PK and TNs when they conflict, Block II AGC AGCIS 30, A11 ropes Comanche 055 / LMY99 rev 001, AEA 4096×18-bit, SM/LM RCS 100 lbf and CM RCS 93 lbf from A11 PK p.93 / p.106, electrical topology). Mark UNKNOWN: RTCC MOC vs DSC on A11, 4th AIS ship, A11 food intake, entry blackout duration, official CSM lunar Δv table, CSM-107 SPS loaded lb, A11 AGS flight-program name, loaded SM/CM RCS propellant mass. Do not invent those. Crew Safety is not LES-only: allocate LES (pad / Mode I) + SPS abort + lunar abort (P70/P71) + crew/ECLSS.
- P-numbers are not global. CMC P61–P67 is ENTRY; LGC P63–P68 is LANDING — two STMs (`apollo-cmc-stm`, `apollo-lgc-stm`). AGC does not talk digital to LVDC. 1201/1202 is a software restart, not an abort. Cite both SPS 20,500 (PK) vs 21,500 vac (TN D-7375) and DPS 9,870 / 1,050–6,300 (PK) vs 10,500 and 10:1 (TN D-7143).
- Context is vehicle / crew / MCC / MSFN / Moon / Earth (RTCC sits with MCC). Uplink and downlink are distinct. Two command paths: (A) FC→CCC→RTCC→CCATS→site 642B→USB 70 kHz; (B) P27 V70–V73. Block II antennas are crew-selected.
- IBD connectors never pass through boxes. Saturn joints are adjacent only.
- Mission STM: countdown → boost → earthOrbit (100 nmi **planned**) → TLI → dockEject → translunar → LOI → undock → DOI → descent → surface/EVA → ascent → rendezvous → TEI → entry → recovery. `dockEject` is its own state (CMP-owned, SM RCS, probe-drogue). Sequence lock with SysML2d: **TLI → dockEject → translunar → LOI** (not translunar then dockEject). Do **not** jump TLI → translunar or dockEject → LOI. GET: planned vs flown — earth orbit 100 nmi is planned. TLI three labels (do not collapse): PK planned 02:44:15; A11-FP planned 2:44:26; flown 02:44:16 (MSC-00171). TDE ~03:20–04:09 is planned, not flown. LOI-1 two strings only: 75:54:28 GET is A11-FP planned; flown ~075:49:50 GET (PAD/MR). Do not call TLI 02:44:15, TDE, or LOI-1 75:54:28 flown. IU owns boost+TLI. RSO owns destruct until orbital safing. Abort machine in parallel: pad/LES, Modes I–IV, contingency TLI, SPS abort, lunar abort (P70 DPS / P71 APS). SPS is on the SM. landingRadar is on the descent stage, not PNGS / ascent.
- Vehicle lock: Apollo 11 / Block II, AS-506 = S-IC-6 / S-II-6 / S-IVB-6N / IU-6 / SLA-14 / CSM-107 / LM-5. Two AGCs (CM Colossus + 2 DSKY; LM Luminary + 1 DSKY). AGS is a separate computer (AEA+ASA+DEDA; abort-to-orbit / rendezvous only). P27 verbs remain V70–V73 only. A11 MCC is MOCR 2 (3rd floor); handoff Mission Rule 1-21 at umbilical-tower clear; Petrone commits launch; AFETR stays parallel destruct. A11 SM cryo is 2 H2 + 2 O2 (not J-mission). No electrical power between Saturn stages; no CSM–LM propellant crossfeed.
- Educational estimate scripts live in `projects/apollo/simulations/`. They print `ESTIMATE` ranges only. Simulation output is not a NASA fact. Do **not** copy it into the model, `architecture-summary.md`, or any shall. Leave official CSM lunar Δv, CSM-107 SPS loaded lb, and loaded SM/CM RCS propellant unmarked.

## Checks

```bash
python3 -m unittest
msml-validate-all projects --strict
msml-render-all projects
```

Canonical spec: [msml-specification.md](msml-specification.md). Working examples: [projects/e-bike](projects/e-bike) (publish hero), [projects/apollo](projects/apollo) (full system + subsystem), [projects/appliances/toaster](projects/appliances/toaster) (coverage canary).

Historical design notes from 2026-05 live under [ai-collab/](ai-collab/). They are archive. The living agent path is this file plus `skills/`.
