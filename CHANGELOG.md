# Changelog

## 0.1.1 — 2026-08-21

Public MSML v1.0 update. Andrew can paste the section below as the announcement.

### Public update

**MSML is a scriptable graphical systems modeling language.** You keep the system meaning in `.msml` model files and the picture layout in `.msmd` view files. The renderer writes PNG next to each view. Humans and AI edit the same artifacts; Git reviews the same files.

**What’s new**

- Twelve SysML 1 views: block definition, internal block, activity, sequence, state machine, use case, requirements, parametric, package, plus requirement table, allocation table, and allocation matrix.
- `allocate` as a first-class relationship, including the compact table and matrix views.
- A street-legal EU-class electric bike example at `projects/e-bike/` (`ElectricBike` namespace, `e-bike` file stem) with rider / charger / bike / road context, color-coded IBD, start-ride activity, and sibling requirements (60 km, 25 km/h, 50 ms).
- Visual QA across toaster, blender, HOS, and e-bike so the figures are announcement-ready.
- Start-your-own-system adoption pack: `AGENTS.md`, four Cursor/Claude skills (`skills/bootstrap-project`, `skills/author-model`, `skills/compose-views`, `skills/vision-review`), and `templates/new-project/`. Same skill slugs as SysML2d. MSML does not replace commercial SysML 2 tools.
- Full Apollo 11 / Block II system + subsystem example at `projects/apollo/` (AS-506; generic Saturn V + CSM + LM stack; public NASA architecture; 7 / 8 / 10 / 13 called out in notes only). Ground/crew/USB, vehicles/AGC, electrical/AGS/docking/RCS, A11 PK p.109 tank loads, and separate CMC entry / LGC landing STMs are on the model. Sourced: stage loads, Comanche 055 / LMY99 rev 001, SPS and DPS cited from both PK and TNs. UNKNOWN remains: official CSM lunar Δv table, CSM-107 SPS loaded lb, A11 AGS flight-program name, loaded SM/CM RCS propellant mass, A11 actual kcal — do not invent those. SM/LM RCS 100 lbf and CM 93 lbf are sourced (A11 PK p.93 / p.106). A11 addendum: MOCR 2 / Rule 1-21 / Petrone + AFETR; VHF 296.8/259.7 and 243.0 MHz beacon; SA-506 serials; 2 H2+2 O2 cryo; APS 1.5° cant; Hornet splash and EVA times; food 2.26 lb/man/day; descent O2 2800 vs 3000 psi cited both. Mission STM keeps `dockEject` as its own state (CMP-owned, SM RCS, probe-drogue) and does not skip translunar → LOI (A11 PK: TLI 02:44:15 → dock ~03:20 → extract ~04:09 → LOI-1 75:54:28).
- ElectricBike architecture corrections: Tour-mode range via `usableWh` / `energyPerKm`, EPAC / EN 15194 (no throttle), nested `bms : BMS` usage inside BatteryPack (`allocateChargeToBms` → `ElectricBike::BatteryPack::bms`), no `lockBikeUseCase`, EN 15194 stopping distance, StVZO/ISO 6742 lighting, fail-silent ride safety to brakes+controller+cadence+BMS, RideControl `walk` ≤ 6 km/h, Standby→Charging, `energyBalance` pack-only, Rear Geared Hub display, Wheel Speed Sensor with Assist Limit allocation, sibling walk (≤ 6 km/h) and 250 W requirements, Pedal (EPAC), Charger on Charge only.

**Install and render**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install git+https://github.com/meaningfulsystems/msml.git
msml-spec --copy architecture/
msml-validate-all projects --strict
msml-render-all projects
```

Specification: `msml-specification.md`. Examples: `projects/e-bike` (publish hero), `projects/apollo` (full system + subsystem), `projects/appliances/toaster` (coverage canary), `projects/appliances/blender`, `projects/humanity-optimization`. Start a new system from `templates/new-project/` and [AGENTS.md](AGENTS.md). Sibling toolchain: [SysML2d](https://github.com/meaningfulsystems/sysml2d) (git-native SysML v2 diagrams; different files).

### Internal notes

- Toaster remains the coverage canary for all twelve views.
- ElectricBike qualified names and file stems are frozen.
- Agent path is `AGENTS.md` + `skills/`. `ai-collab/` is archive.
- Checks: `python3 -m unittest`, `msml-validate-all projects --strict`, `msml-render-all projects`.
