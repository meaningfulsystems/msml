---
name: compose-views
description: Write MSML .msmd views and run msml-validate / msml-render / *-all. Use when adding or laying out diagrams. Shared slug compose-views; MSML’s verb is render.
---

# Compose MSML views (render)

The shared skill slug is **compose-views** so this repo and SysML2d keep the same names. In MSML the verb is **render**. There is no compose CLI. You write `.msmd` JSON and run `msml-render`.

## When to use

- Add a new diagram for an existing model.
- Move boxes, route connectors, or change canvas size.
- Run validate/render for one file or a folder.

Do not invent model ids here. If the meaning is missing, go to [author-model](../author-model/SKILL.md).

## Commands

```bash
msml-validate architecture/system-context.msmd --strict
msml-render architecture/system-context.msmd
msml-validate-all architecture --strict
msml-render-all architecture
```

`msml-render` writes `*.png` next to the `.msmd`. Model files (`.msml`) are not rendered.

## View file shape

```json
{
  "msml_version": "1.0",
  "model_files": ["system-model.msml"],
  "diagram": {
    "type": "ibd",
    "id": "ibd-system-context",
    "subject_ref": "ExampleSystem.SystemContext",
    "name": "System Context",
    "context": "ExampleSystem",
    "frame": { "visible": true, "style": {} },
    "canvas": { "width": 900, "height": 520, "background_color": "#FAFAFA" },
    "elements": [],
    "relationships": []
  }
}
```

Every element needs `model_ref` + `layout` (`x`, `y`, `width`, `height`). Every relationship needs `relationship_ref` pointing at a model relationship. Use `waypoints` for routing. Sequence messages use `layout.y`, not waypoints.

`ibd` and `parametric` require `subject_ref` on a **block**.

## All twelve view types

| `diagram.type` | Stem | What to show |
| --- | --- | --- |
| `bdd` | `*-bdd.msmd` | Blocks and composition. Multiplicity on the parts. |
| `ibd` | `*-ibd.msmd` | Parts, ports, connectors. Highest visual priority. |
| `activity` | `*-act.msmd` | Actions and control flows. |
| `sequence` | `*-seq.msmd` or `*-int.msmd` | Lifelines and messages (`layout.y`). |
| `state_machine` | `*-stm.msmd` | States and transitions. Keep Off↔Standby as two readable paths. |
| `use_case` | `*-uc.msmd` | Actors, boundary, include/extend. |
| `requirement` | `*-req.msmd` | Requirement boxes and refine/derive. |
| `parametric` | `*-par.msmd` | Constraints and binding connectors. |
| `package` | `*-pkg.msmd` | Packages and dependencies. |
| `requirement_table` | `*-reqt.msmd` | `diagram.table.columns`. |
| `allocation_table` | `*-alloc.msmd` | `diagram.table.columns`; rows are `allocate` refs. |
| `allocation_matrix` | `*-amx.msmd` | `diagram.matrix` plus elements with `matrix_role` `row` and `column`. |

SysML2d-only kinds (**flow**, **acase**, **vcase**, **intf**, **general**) are not MSML diagram types. Keep those elements in the `.msml` if needed; do not invent a fake view type.

## Layout rules

- **Connections never pass over boxes.** Route around. Hop-overs are only for line-on-line crossings.
- IBD ports sit on the part edge, not under a connector.
- Distinct connectors for distinct flows (mount vs assist vs inhibit vs power vs drive). Color structure / energy / control / actuation when it helps.
- Trim leftover canvas. Sequence height is last-message plus a small margin.
- Empty diagram `name` suppresses a model relationship name.

## Examples to copy from

- Context IBD: [projects/e-bike/e-bike-ctx.msmd](../../projects/e-bike/e-bike-ctx.msmd) — rider / charger / bike / road only. No Wheel Torque actor.
- Internal IBD: [projects/e-bike/e-bike-ibd.msmd](../../projects/e-bike/e-bike-ibd.msmd) — child-owned ports, Rear Geared Hub, mount / command / inhibit / pack power / phase drive. Cadence and wheel-speed when the layout stays clean.
- Full twelve-view set: [projects/appliances/toaster/](../../projects/appliances/toaster/).
- Full system + subsystem: [projects/apollo/](../../projects/apollo/) (vehicle IBD `apollo-ibd`, electrical IBD `apollo-eps`).

After render, run [vision-review](../vision-review/SKILL.md) on every PNG before commit.
