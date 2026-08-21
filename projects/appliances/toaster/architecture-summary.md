# Toaster — MagicGrid architecture walkthrough

A student can follow this note with `toaster-model.msml` open. It walks the two-slice pop-up toaster from problem to solution in simplified MagicGrid order, then explains every generated view. This is not a Department of Defense Architecture Framework (DoDAF) product set.

Namespace `Toaster`. File stem `toaster`. The same appliance idea appears in SysML2d (`examples/toaster/toaster.sysml`). The files are not interchangeable. Pick one toolchain. Every number below is already on `toaster-model.msml`. Unfilled types stay unfilled.

This is an example model for language coverage, not a certifiable appliance.

## 1. Problem / context

**Who.** The user browns bread and empties crumbs. A service technician is implied by a serviceability shall but is not a modeled actor. The Power Grid supplies household mains.

**Boundary.** Inside the toaster: BrowningControl, Timer, Lever, Carriage, HeatingElement, ThermalCutoff, CrumbTray, Chassis. Outside: User and Power Grid. Bread, toast, crumbs, and kitchen air are implied by the toast cycle; they are not first-class actors on the use-case view.

**Mission.** Accept bread, apply controlled heat for a selected browning level, present toast, and let the user cancel a cycle or remove the crumb tray without tools. If the element exceeds a safe threshold, heating must stop.

The model is one two-slice baseline. Four-slice, bagel, defrost, and wide-slot variants are out of scope.

## 2. Requirements and use cases

Fourteen sibling shalls. There is no containment or derive tree. Only the four numbered targets below are filled; the rest stay qualitative.

| Id | Name | Shall |
| --- | --- | --- |
| `Toaster.toastSafetyRequirement` | toast safety | No burns, electrical shock, or fire under normal operating conditions. |
| `Toaster.electricalSafetyRequirement` | electrical safety | Comply with applicable household electrical safety standards. No standard name is filled. |
| `Toaster.browningRequirement` | uniform browning | Uniform browning across the full bread surface for each browning level. |
| `Toaster.timingRequirement` | timing accuracy | Timer within **±5%** of the selected setting across all browning levels. |
| `Toaster.userInterfaceRequirement` | user interface | Insert bread, select a browning level, and cancel without tools. |
| `Toaster.cleanabilityRequirement` | cleanability | Crumb tray removable and washable without tools. |
| `Toaster.serviceabilityRequirement` | serviceability | Serviceable by a qualified technician without specialized equipment. |
| `Toaster.powerRatingRequirement` | power rating | Operate within rated power consumption. Watts unmarked. |
| `Toaster.surfaceTemperatureRequirement` | surface temperature | Exterior surfaces stay within safe-touch limits. °C unmarked. |
| `Toaster.thermalCutoffRequirement` | thermal cutoff | A thermal cutoff disables heating above a safe threshold. Threshold unmarked. |
| `Toaster.browningLevelsRequirement` | browning levels | At least **three** distinct and repeatable settings (**≥3**). |
| `Toaster.carriageReleaseRequirement` | carriage release | Carriage releases automatically when the timer expires or the user cancels. |
| `Toaster.crumbTrayForceRequirement` | crumb tray force | Crumb tray removal force **≤10 N**. |
| `Toaster.cycleLifeRequirement` | cycle life | At least **10,000** toast cycles before maintenance. |

**Use cases** on the model: Toast Bread (includes Activate Heating), Adjust Browning, Cancel Toast, Reset Error. The user associates with all four user-facing cases. The power grid associates with Toast Bread.

## 3. Structure

Read the block definition diagram (BDD) first, then the internal block diagram (IBD).

Toaster root properties are typed (`voltage: V`, `maxPower: W`) without filled product values.

```
Toaster
├── BrowningControl     level, targetEnergy
├── Timer               duration, browning
├── Lever               position
├── Carriage            position
├── HeatingElement      resistance, power
├── ThermalCutoff       cutoffTemp: degC (unfilled), tripped
├── CrumbTray
└── Chassis
```

IBD connectors (why they exist):

- Lever `ctrl` → Timer `in` — user start latches the timed cycle
- Timer `signal` → HeatingElement `ctrl` — timer commands heat on and off
- HeatingElement `heatSignal` → Carriage `heatSignal` — heat reaches the bread

BrowningControl configures the Timer. ThermalCutoff monitors the HeatingElement.

## 4. Behavior

**State machine (STM).** ToastingCycle: Idle → Toasting (`lever_down`) → Done (`timer_expired`) → Idle (`toast_removed`). From Toasting, `lever_up` returns to Idle (cancel). `overheat_detected` goes to Error (deactivate element, release latch, alarm). Error → Idle on `reset`. Done is a normal state, not a final node: toast can sit until the user removes it.

**Activity.** Insert bread → press lever → fork to start timer and heat element → join → pop carriage.

**Sequence.** User `pressLever()` to the toaster; toaster `start()` to the Timer and `activate()` to the HeatingElement; Timer returns `timerExpired`; toaster `deactivate()` and replies `:ready`. The start message is `start()`, not a filled duration.

## 5. Parametrics

Constraint properties on the model (typed, unfilled):

- `PV2R`: `P = V² / R`
- `Energy`: `Q = P × t`
- `BreadHeat`: `Q_b = η × Q`
- `SafetyCheck`: `T_elem < T_cutoff`

Sourced numbers only:

- at least three browning levels (**≥3**)
- crumb tray **≤10 N**
- at least **10,000** toast cycles
- timer **±5%** of the selected setting

`Energy` verifies timing accuracy. `SafetyCheck` verifies thermal cutoff without a product °C.

## 6. Allocations

Satisfy mappings (requirement → part):

| Requirement | Satisfied by |
| --- | --- |
| toast safety | ThermalCutoff |
| electrical safety | HeatingElement |
| uniform browning | BrowningControl |
| timing accuracy | Timer |
| user interface | Lever |
| cleanability | CrumbTray |
| serviceability | Toaster |
| power rating | HeatingElement |
| surface temperature | Chassis |
| thermal cutoff | ThermalCutoff |
| browning levels | BrowningControl |
| carriage release | Carriage |
| crumb tray force | CrumbTray |
| cycle life | Toaster |

Activity steps allocate to the same parts: insert bread and pop → Carriage; press lever → Lever; start timer → Timer; heat → HeatingElement. The Toasting state allocates to Toaster; Error allocates to ThermalCutoff.

## 7. Open risks / unmarked

- Example model, not a certifiable appliance.
- Mains voltage, element wattage, touch-temperature limit, and cutoff threshold are unmarked. Electrical-load analysis cannot close.
- Product-line variants are out of scope.

## Generated views

These figures illustrate the architecture above; they do not replace it. Open the matching `.msmd` next to the PNG.

**`toaster-bdd.png` — block definition diagram (BDD).** Ownership tree. Composition diamonds from Toaster to the eight parts. Dashed associations: ThermalCutoff *monitors* HeatingElement; BrowningControl *configures* Timer. Types (`V`, `W`, `degC`) are unfilled.

**`toaster-ibd.png` — internal block diagram (IBD).** Ports and connectors inside one toaster. Read left-to-right: lever command → timer → heater control → heat into the carriage. Lines stay off boxes.

**`toaster-uc.png` — use cases.** User on Toast Bread, Adjust Browning, Cancel Toast, Reset Error. Power Grid on Toast Bread. Toast Bread «include» Activate Heating.

**`toaster-req.png` — requirement diagram.** Fourteen sibling boxes. No containment arrows. Read the Id and the shall text; the numbered targets are ≥3, ±5%, ≤10 N, and 10,000 cycles.

**`toaster-reqt.png` — requirement table.** Same fourteen shalls as rows, with Satisfied By and Verified By filled from the model.

**`toaster-stm.png` — state machine (STM).** Idle / Toasting / Done / Error. Done is a waiting state. Error is the overheat path.

**`toaster-act.png` — activity.** Toast-cycle control flow, including the fork after the lever press.

**`toaster-seq.png` — sequence.** Lifelines User, Toaster, Timer, HeatingElement. Message names come from the model (`start()`, not a filled time).

**`toaster-par.png` — parametrics.** Bindings among voltage, resistance, power, duration, heat, and the unfilled safety check.

**`toaster-alloc.png` — allocation table.** Rows are «allocate» relationships: activity/state/use-case/requirement → part.

**`toaster-amx.png` — allocation matrix.** Same functional and behavioral allocates as marks at action/state/use-case × part.

**`toaster-pkg.png` — packages.** Structural, Behavioral, and Control packages and their dependencies.

```bash
msml-validate-all projects/appliances/toaster --strict
msml-render-all projects/appliances/toaster
```
