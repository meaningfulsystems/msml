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
- Requirements are siblings. Brake Override refines Ride Safety; Battery Cutoff refines Charge Safety.
- Ride «include» Adjust Assist.
- STM `resetFault` is Fault→Off. Off↔Standby is two readable paths.

## Apollo (in progress)

`projects/apollo/` is a full system + subsystem example (morning deliverable with e-bike). Namespace `Apollo`. File stem `apollo`. Public NASA architecture only. Do not invent classified or biomedical detail.

- **Instance lock:** Apollo 11 / Block II. The modeled stack is the generic Saturn V + CSM + LM used by lunar-landing missions.
- Where 11 is atypical, call it out in comments only. Do **not** stand up Apollo 7 / 8 / 10 / 13 as separate projects: 7 had no LM, 8 and 10 did not land, 13 aborted.
- **Names (exact):** SaturnV S-IC / S-II / S-IVB / IU; CSM CM / SM / SCS / AGC_CM / IMU / DSKY / SPS / RCS / ECLSS; LM descent / ascent / PNGS / AGC_LM / AGS / DPS / APS / RCS / landingRadar / rendezvousRadar; Crew CDR / CMP / LMP / A7L / PLSS; Ground KSC_LCC / MCC / RTCC / MSFN Goldstone / Madrid / Honeysuckle / NASCOM; plus SLA and LES.
- Do **not** collapse AGC_CM vs AGC_LM, DSKY, AGS, IU LVDC, or USB. Do collapse engine hydraulics and every MSFN ship (stations only).
- Context is vehicle / crew / MCC / MSFN / Moon / Earth (RTCC sits with MCC). Uplink and downlink are distinct.
- IBD connectors never pass through boxes. Saturn joints are adjacent only.
- Mission STM: countdown → boost → earthOrbit → TLI → translunar → LOI → undock → DOI → descent → surface/EVA → ascent → rendezvous → TEI → entry → recovery. Abort machine in parallel: pad, I–IV, contingency TLI, lunar, SPS.

## Checks

```bash
python3 -m unittest
msml-validate-all projects --strict
msml-render-all projects
```

Canonical spec: [msml-specification.md](msml-specification.md). Working examples: [projects/e-bike](projects/e-bike) (publish hero), [projects/apollo](projects/apollo) (in-progress full system), [projects/appliances/toaster](projects/appliances/toaster) (coverage canary).

Historical design notes from 2026-05 live under [ai-collab/](ai-collab/). They are archive. The living agent path is this file plus `skills/`.
