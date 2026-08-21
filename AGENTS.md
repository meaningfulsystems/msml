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

1. **[bootstrap-project](skills/bootstrap-project/SKILL.md)** — copy `template/new-project/`, copy the spec, write the first model and one view, validate and render.
2. **[author-model](skills/author-model/SKILL.md)** — edit `.msml` (blocks, parts, ports, requirements, allocate, states, activities).
3. **[compose-views](skills/compose-views/SKILL.md)** — write `.msmd` views. The shared slug is `compose-views`; MSML’s verb is **render** (`msml-render`, `msml-render-all`).
4. **[vision-review](skills/vision-review/SKILL.md)** — inspect every PNG with vision before commit.

Hard visual rule (Andrew, via SysML2d): **connections never pass over boxes.** Hop-overs are only for line-on-line crossings. IBD is the highest visual priority.

## Checks

```bash
python3 -m unittest
msml-validate-all projects --strict
msml-render-all projects
```

Canonical spec: [msml-specification.md](msml-specification.md). Working examples: [projects/e-bike](projects/e-bike) (publish hero), [projects/appliances/toaster](projects/appliances/toaster) (coverage canary).

Historical design notes from 2026-05 live under [ai-collab/](ai-collab/). They are archive. The living agent path is this file plus `skills/`.
