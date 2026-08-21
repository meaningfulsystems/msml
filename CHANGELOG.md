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

**Install and render**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install git+https://github.com/meaningfulsystems/msml.git
msml-spec --copy architecture/
msml-validate-all projects --strict
msml-render-all projects
```

Specification: `msml-specification.md`. Examples: `projects/e-bike`, `projects/appliances/toaster`, `projects/appliances/blender`, `projects/humanity-optimization`.

### Internal notes

- Toaster remains the coverage canary for all twelve views.
- ElectricBike qualified names and file stems are frozen.
- Checks: `python3 -m unittest`, `msml-validate-all projects --strict`, `msml-render-all projects`.
