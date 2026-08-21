---
name: author-model
description: Write or edit MSML .msml model files (blocks, parts, ports, requirements, allocate, states, activities). Use when changing system meaning, not layout.
---

# Author an MSML model

The `.msml` file is the source of truth. It holds definitions and relationships. It must not contain `layout`, `style`, `canvas`, `frame`, `waypoints`, or `z_index`.

## When to use

- Add or rename a block, actor, port, requirement, state, action, or allocate.
- Change topology (composition, connector, include, refine, transition).

Do not use this skill to move boxes or route lines — that is [compose-views](../compose-views/SKILL.md).

## Spec and examples

Read [msml-specification.md](../../msml-specification.md) before inventing fields.

| Example | Why it exists |
| --- | --- |
| [projects/e-bike/e-bike-model.msml](../../projects/e-bike/e-bike-model.msml) | Publish hero. Frozen `ElectricBike::` names. |
| [projects/apollo/apollo-model.msml](../../projects/apollo/apollo-model.msml) | Full system + subsystem. Apollo 11 / Block II instance on the generic Saturn V + CSM + LM stack. |
| [projects/appliances/toaster/toaster-model.msml](../../projects/appliances/toaster/toaster-model.msml) | Coverage canary for all twelve views. |

Copy *patterns* from those files. Do not remap ElectricBike ids.

## File shape

```json
{
  "msml_version": "1.0",
  "model": {
    "id": "system-model",
    "name": "Example System Model",
    "namespace": "ExampleSystem",
    "imports": [],
    "definitions": [],
    "relationships": []
  }
}
```

Definition ids are stable strings. Prefer `Namespace.Name` (e.g. `ElectricBike.BatteryPack`).

## What to put in the model

**Blocks and parts.** A `block` is a definition. Composition relationships (`type: "composition"`) say the system owns its parts. Usages on diagrams (`role_name` like `batteryPack`) are view-side; the definition name stays PascalCase.

**Actors and context.** Context members are usually an operator, the system, and the environment. For the e-bike, context is **rider / charger / ElectricBike / road only**. Do not promote a flow item (for example Wheel Torque) to a context actor.

**Ports and connectors.** Ports are definitions with `type: "port"` and `owner_ref` on the owning block. Connectors (`type: "connector"`) join two ports. Keep energy, control, and structure on **distinct** connectors. Do not merge command and charge onto one inbound line.

**Requirements.** Keep them **siblings** under the system unless the user asks for a real refine. Ids in the e-bike are frozen: `rideSafetyRequirement`, `rangeRequirement`, `assistLimitRequirement`, `chargeSafetyRequirement`, `brakeOverrideRequirement`, `batteryCutoffRequirement`, `displayRequirement`, `structuralRequirement`, plus siblings `stoppingDistanceRequirement` (EN 15194 5 m / 2 m) and `lightingRequirement` (StVZO / ISO 6742). Display and Structural are not children of Range or Assist Limit. Brake Override may refine Ride Safety. Range 500 Wh / 60 km is Tour-mode (~8.3 Wh/km), not Eco / PAS-1. `allocateChargeToBms` targets the BMS part inside BatteryPack.

**Allocate.** `type: "allocate"` maps a requirement or action onto a block (`kind`: `functional`, `behavioral`, or `structural`). Tables and the matrix are views of the same relationships.

**States.** State definitions plus `transition` relationships. E-bike `RideControl` states: `off`, `standby`, `assist`, `charging`, `fault`. `resetFault` is **Fault→Off**, not Fault→Standby.

**Activities.** Actions, initial/final/decision/fork/join nodes, and `control_flow` relationships. Guards live on the flow (`"guard": "yes"`).

**Use cases.** Associations from actors to use cases. `include` source is the including use case. E-bike: Ride «include» Adjust Assist (not the reverse). Rider on ride/adjust/lock; Charger on Charge Bike.

**Sequence.** `type: "message"` with `source_lifeline` and `target_lifeline` pointing at block or actor definitions.

## After you edit

```bash
msml-validate path/to/view.msmd --strict
```

Every new definition that should appear on a picture also needs a view element in some `.msmd` (compose-views). `--strict` does not require every model element to appear on a diagram; `--lint` warns about orphans.
