# Toaster — Architecture / System Design

Two-slice pop-up toaster used as the MSML coverage canary. Namespace `Toaster`. File stem `toaster`. This note is the design argument for the model in this folder, not a catalog of pictures.

The same appliance idea appears in SysML2d. The files are not interchangeable. Numbers below are only those already on `toaster-model.msml`. Unfilled types stay unfilled.

## 1. Purpose / context

The toaster exists to brown bread to a user-selected level and then present it. The design problem is a short, repeatable thermal cycle with a hard safety cutoff: heat the element, time the cycle, pop the carriage, and shut down if the surface is heading for overheat.

This is an example model for language coverage, not a certifiable appliance.

## 2. System boundary and actors

**Inside:** BrowningControl, Timer, Lever, Carriage, HeatingElement, ThermalCutoff.

**Outside:** User and Power Grid. Bread, toast, crumbs, and the kitchen air are implied by the toast cycle; they are not first-class actors on the MSML use-case view.

Use cases: Toast Bread (includes Activate Heating), Adjust Browning, Cancel Toast, Reset Error. The user associates with all four user-facing cases. The power grid associates with Toast Bread.

## 3. Requirements

| Id | Name | Text / numbers |
| --- | --- | --- |
| `Toaster.REQ-001` | Toasting Capability | Toast bread to the user-selected browning. |
| `Toaster.REQ-001.1` | Heat Control | Heating element shall reach target temperature within **30 s**. |
| `Toaster.REQ-001.2` | Timer Function | Timer shall support **1–5 min** browning settings. |
| `Toaster.REQ-001.3` | Carriage Mechanism | Carriage shall pop toast when the timer completes. |
| `Toaster.REQ-001.4` | Browning Repeatability | Same browning level shall produce **±5%** energy variance. |
| `Toaster.REQ-002` | Safety | Detect overheat and shut down automatically. |
| `Toaster.REQ-002.1` | Overheat Detection | ThermalCutoff shall trip **below 300 °C** surface temperature. |
| `Toaster.REQ-002.2` | Auto Shutoff | On trip: deactivate the element and release the carriage latch. |
| `Toaster.REQ-003` | User Controls | User shall control browning level and cancel toasting. |
| `Toaster.REQ-003.1` | Cancel / Eject | Lever-up during toasting shall cancel and eject. |

REQ-002 and REQ-003 derive from REQ-001. Only the numbers in that table are bound.

## 4. Structure and interfaces

Toaster properties on the model are typed (`voltage: V`, `maxPower: W`) without filled product values.

Parts:

- `BrowningControl` — `level`, `targetEnergy`
- `Timer` — `duration`, `browning`
- `Lever` — `position`
- `Carriage` — `position`
- `HeatingElement` — `resistance`, `power`
- `ThermalCutoff` — `cutoffTemp`, `tripped`

Connectors on the IBD:

- Lever `ctrl` → Timer `in`
- Timer `signal` → HeatingElement `ctrl`
- HeatingElement `heatSignal` → Carriage `heatSignal`

BrowningControl configures the Timer. ThermalCutoff monitors the HeatingElement.

## 5. States and modes

ToastingCycle: Idle → Toasting (`lever_down`) → Done (`timer_expired`) → Idle (`toast_removed`).

From Toasting: `lever_up` returns to Idle (cancel). `overheat_detected` goes to Error (deactivate element, release latch, alarm). Error → Idle on `reset`.

Done is a normal state, not a terminal node: toast can sit until the user removes it.

## 6. Allocations (req → part)

Satisfy mappings on the model:

| Requirement | Satisfied by |
| --- | --- |
| REQ-001 Toasting Capability | Toaster |
| REQ-001.1 Heat Control | HeatingElement |
| REQ-001.2 Timer Function | Timer |
| REQ-001.3 Carriage Mechanism | Carriage |
| REQ-001.4 Browning Repeatability | BrowningControl |
| REQ-002 Safety | ThermalCutoff |
| REQ-002.1 Overheat Detection | ThermalCutoff |
| REQ-002.2 Auto Shutoff | ThermalCutoff |
| REQ-003 User Controls | Toaster |
| REQ-003.1 Cancel / Eject | Lever |

Parametric properties on the model: `PV2R` (Heat Control), `Energy` (Browning Repeatability), `SafetyCheck` (Overheat Detection). Activity steps (insert bread, press lever, start timer, heat, pop) allocate to the same parts. There are no empty verification names.

## 7. Sourced numbers

All quantitative targets are model-local:

- 30 s to target temperature
- 1–5 min browning settings
- ±5% energy variance at the same level
- Thermal cutoff below 300 °C surface temperature

Root `voltage` and `maxPower` are typed, not filled. Do not promote view-only values into the model.

## 8. Open risks / TBD

- This stays an example model, not a certifiable appliance.
- No filled mains voltage or element wattage, so electrical-load analysis cannot close.
- No crumb-tray or chassis part.
- Safety is the ThermalCutoff trip (`overheat_detected` → Error) and Auto Shutoff on that part. Power is typed on Toaster / HeatingElement with no filled watts.
- Product-line variants are out of scope.

## 9. Views in this folder

`toaster-bdd.png`, `toaster-ibd.png`, `toaster-act.png`, `toaster-seq.png`, `toaster-stm.png`, `toaster-uc.png`, `toaster-req.png`, `toaster-reqt.png`, `toaster-par.png`, `toaster-pkg.png`, `toaster-alloc.png`, `toaster-amx.png`.

![Toaster block definitions](toaster-bdd.png)

![Toaster requirements table](toaster-reqt.png)

```bash
msml-validate-all projects/appliances/toaster --strict
msml-render-all projects/appliances/toaster
```
