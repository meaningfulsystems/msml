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
- Full Apollo 11 / Block II system + subsystem example at `projects/apollo/` (AS-506; generic Saturn V + CSM + LM stack; public NASA architecture; 7 / 8 / 10 / 13 called out in notes only). Ground/crew/USB, vehicles/AGC, and the last electrical/AGS/docking/RCS slice are on the model. Sourced: three SM fuel cells, CM AgZn + pyro, LM 4+2 AgZn with ECA, AEA 4096×18-bit, probe/drogue/12 latches, CM RCS 93 lbf. UNKNOWN remains: tank loads, Δv, A11 rope IDs, SM RCS thrust — do not invent those.
- ElectricBike architecture corrections: Tour-mode range, EPAC / EN 15194 (no throttle), nested `bms : BMS` usage inside BatteryPack (`allocateChargeToBms` → `ElectricBike::BatteryPack::bms`), no `lockBikeUseCase`, EN 15194 stopping distance, StVZO/ISO 6742 lighting, fail-silent ride safety.

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
