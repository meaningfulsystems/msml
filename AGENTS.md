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

Hard visual rule (Andrew, via SysML2d): **connections never pass over boxes.** Hop-overs are only for line-on-line crossings. IBD is the highest visual priority.

Starter: [templates/new-project/](templates/new-project/). Spec: [msml-specification.md](msml-specification.md).

## ElectricBike locks

`projects/e-bike/` is the Friday hero. Namespace `ElectricBike`. File stem `e-bike`. Do not remap ids.

- Context is rider / charger / ElectricBike / road only.
- IBD connectors never pass through boxes.
- Requirements are siblings. Brake Override refines Ride Safety; Battery Cutoff refines Charge Safety. Stopping Distance (EN 15194 5 m / 2 m) and Lighting (StVZO / ISO 6742) are additional siblings.
- Range 500 Wh / 60 km is a **Tour-mode** scenario (~8.3 Wh/km), not Eco / PAS-1. `energyBalance` binds usable pack Wh + `energyPerKm`; do **not** add rider watts into pack energy.
- RideControl includes EPAC **walk** (≤ 6 km/h). IBD ports stay on child parts (`owner_ref` on children); do not park every port on `ElectricBike`.
- Classification is **EPAC / EN 15194** (cadence only, 25 km/h, no throttle). Hub is a rear geared hub; regen omitted.
- Nested usage `bms : BMS` lives inside BatteryPack (`ElectricBike::BatteryPack::bms`). `allocateChargeToBms` targets that usage, not the pack.
- Do **not** keep `lockBikeUseCase`. Empty use cases are not allowed.
- Ride safety is not brakes-only: allocate to BrakeSystem, MotorController, sensors, and `bms`.
- Ride «include» Adjust Assist.
- STM `resetFault` is Fault→Off. Off↔Standby is two readable paths.

## Apollo (publish)

`projects/apollo/` is a full system + subsystem example (morning deliverable with e-bike). Namespace `Apollo`. File stem `apollo`. Public NASA architecture only. Do not invent classified or biomedical detail.

- **Instance lock:** Apollo 11 / Block II, vehicle AS-506. The modeled stack is the generic Saturn V + CSM + LM used by lunar-landing missions.
- Where 11 is atypical, call it out in comments only. Do **not** stand up Apollo 7 / 8 / 10 / 13 as separate projects: 7 had no LM, 8 and 10 did not land, 13 aborted.
- **Names (exact):** SaturnV S-IC / S-II / S-IVB / IU; engines F-1 / J-2 (keep S-II and S-IVB J-2 separate); CSM CM / SM / SCS / AGC_CM / IMU / DSKY / DSKY2 / EMS / SPS / RCS / ECLSS; LM descent / ascent / PNGS / AGC_LM / DSKY_LM / AGS (AEA+ASA+DEDA) / DPS / APS / RCS / landingRadar / rendezvousRadar; IU LVDC + ST-124 + FCC; electrical FuelCell ×3 / CM AgZn ×3 + LEB charger + pyro / LM AgZn 4+2 with ECA / 28 V DC / inverters; docking probe / drogue / 12 latches; Crew CDR / CMP / LMP each with A7L / bio / comm (PLSS+OPS on CDR/LMP EVA only); Ground as first-class parts: MCC-H (MOCR consoles, SSR, RTCC, CCATS), GSFC (NASCOM, NTTF, NST), MSFN (3×85-ft USB + named 30-ft only + 4 AIS + 8 ARIA + Goldstone 210-ft + Parkes), KSC LC-39, Recovery, RSO/AFETR outside MCC; plus SLA and LES.
- Do **not** collapse two AGCs, AGS (AEA+ASA+DEDA ≠ DSKY), IU LVDC, descent vs ascent, LES, CM 2 DSKY vs LM 1 DSKY, EMS, SM fuel cells vs CM AgZn vs LM batteries, SM quads vs CM dual 6-engine sets. Do collapse ullage/retro as sets, every verb/noun, F-1 hydraulics, other MSFN ships/aircraft, full loop directory, umbilical pinout. Do **not** merge GSFC-1968 and TN D-6723 into “the 14”.
- Sourced numbers only (USB RF, HGA, LM steerable, CM ECS, LM-5, A7L/PLSS, food plan, A11 PK masses, engine thrusts, Block II AGC AGCIS 30, AEA 4096×18-bit, CM RCS 93 lbf, electrical topology). Mark UNKNOWN: RTCC MOC vs DSC on A11, 4th AIS ship, A11 food intake, entry blackout duration, stage tank loads, Δv table, A11 rope IDs, SM RCS per-engine thrust. Do not invent those. Do not use 100 lbf for SM RCS unless cited.
- Context is vehicle / crew / MCC / MSFN / Moon / Earth (RTCC sits with MCC). Uplink and downlink are distinct. Two command paths: (A) FC→CCC→RTCC→CCATS→site 642B→USB 70 kHz; (B) P27 V70–V73. Block II antennas are crew-selected.
- IBD connectors never pass through boxes. Saturn joints are adjacent only.
- Mission STM: countdown → boost → earthOrbit (100 nmi planned) → TLI → translunar → dock/eject → LOI → undock → DOI → descent → surface/EVA → ascent → rendezvous → TEI → entry → recovery. IU owns boost+TLI. RSO owns destruct until orbital safing. Abort machine in parallel: pad/LES, Modes I–IV, contingency TLI, SPS abort, lunar abort (P70 DPS / P71 APS).
- Vehicle lock: Apollo 11 / Block II, AS-506. Two AGCs (CM Colossus + 2 DSKY; LM Luminary + 1 DSKY). AGS is a separate computer (AEA+ASA+DEDA; abort-to-orbit / rendezvous only). P27 verbs remain V70–V73 only.

## Checks

```bash
python3 -m unittest
msml-validate-all projects --strict
msml-render-all projects
```

Canonical spec: [msml-specification.md](msml-specification.md). Working examples: [projects/e-bike](projects/e-bike) (publish hero), [projects/apollo](projects/apollo) (full system + subsystem), [projects/appliances/toaster](projects/appliances/toaster) (coverage canary).

Historical design notes from 2026-05 live under [ai-collab/](ai-collab/). They are archive. The living agent path is this file plus `skills/`.
