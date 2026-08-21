# Electric Bike — MagicGrid architecture walkthrough

A student can follow this note with `e-bike-model.msml` open. It walks one Electrically Power Assisted Cycle (EPAC) from problem to solution in simplified MagicGrid order, then explains every generated view. This is not a Department of Defense Architecture Framework (DoDAF) product set.

Namespace `ElectricBike`. File stem `e-bike`. This is the publish hero. The same ElectricBike names appear in SysML2d; the files are not interchangeable.

**250 W is the EU continuous assist rating, not peak power. 40 N·m is hub peak torque, not a continuous point at 250 W / 25 km/h.**

## 1. Problem / context

**Who.** A rider pedals on the road, sets assist, and plugs in an off-board charger. The road is the tractive load. Rider, Charger, and Road stay on the context view. They are not parts on the internal block diagram (IBD).

**Boundary.** Inside the bike: Frame, BatteryPack with nested `bms : BMS` (battery management system), MotorController, Rear Geared Hub (`HubMotor`), HumanInterface, BrakeSystem, `cadenceSensor`, `wheelSpeedSensor`.

**Mission.** Assist cadence-only pedaling within the legal continuous-power and speed limits, cut torque on brake input, and accept charge through the pack BMS. Classification is one EN 15194 EPAC class: 25 km/h cutoff, no certified throttle, walk assist at or below 6 km/h, rear geared hub with no regeneration.

Throttle variants, mid-drive kits, and regenerative hubs are out of scope. There is no `lockBike` use case. Tour-mode range is the only bound range scenario.

## 2. Requirements and use cases

Requirements are **siblings** under the bike. Brake Override refines Ride Safety. Battery Cutoff refines Charge Safety. Walk Assist and Continuous Power are siblings — they do not hang under Assist Limit.

| Id | Name | Shall |
| --- | --- | --- |
| `ElectricBike.rideSafetyRequirement` | Ride Safety | Motor shall fail silent: brake inhibit, controller, cadence sensor, and BMS. Not brakes-only. |
| `ElectricBike.rangeRequirement` | Range (≥ 60 km Tour) | Tour-scenario binding: **500 Wh** / `energyPerKm` **~8.3 Wh/km** for 60 km. Not Eco / PAS-1 (pedal-assist sensor level 1). **500 Wh is not a pack nameplate.** The requirement text says `usableWh`; the parametric still uses `packEnergy`. |
| `ElectricBike.assistLimitRequirement` | Assist Limit (25 km/h) | EPAC / EN 15194: cadence-only assist, cut off at **25 km/h** (wheel speed). No throttle. |
| `ElectricBike.chargeSafetyRequirement` | Charge Safety | Stop on over-temp, over-voltage, or charger disconnect. BMS inside the pack opens the contactor. Underwriters Laboratories (UL) 2849 is **scope inspiration** for the serial charge path, not a certification shall. |
| `ElectricBike.brakeOverrideRequirement` | Brake Override (50 ms) | Motor inhibit within **50 ms** of either brake lever. **50 ms is an electronic inhibit budget.** Do not compare it to the EN 15194 distance test. |
| `ElectricBike.batteryCutoffRequirement` | Battery Cutoff | BMS inside the pack opens the contactor before any cell exceeds its V/T limit. |
| `ElectricBike.displayRequirement` | Display | Rider shall see speed, assist level, and remaining range hands-on-bars. |
| `ElectricBike.structuralRequirement` | Structural | Frame shall carry rider, cargo, and battery loads without yielding. |
| `ElectricBike.motorAssistCutoffRequirement` | motor-assist cut-off | EN 15194:**2017** **4.2.13 Power management**: motor-assist cut-off after pedaling stops is **2 m**, or **5 m** if brake-lever switches relax it. **Not vehicle brake distance.** Do not compare to the 50 ms inhibit budget. Do not allocate this shall to BrakeSystem. |
| `ElectricBike.lightingRequirement` | Lighting (StVZO / ISO 6742) | Lighting shall meet Straßenverkehrs-Zulassungs-Ordnung (StVZO) / International Organization for Standardization (ISO) 6742. Not United Nations Economic Commission for Europe (UN ECE) R113. |
| `ElectricBike.walkAssistRequirement` | Walk Assist (≤ 6 km/h) | EPAC walk assist shall not exceed **6 km/h**. Walk assist is not a throttle. |
| `ElectricBike.continuousPowerRequirement` | Continuous Power (250 W) | Continuous assist shall not exceed **250 W**. EN 15194 EPAC continuous rating. |

**Use cases.** Ride Bike, Adjust Assist, Charge Bike. Rider associates with Ride and Adjust (and also Charge as the person who plugs in). Charger associates with Charge only. Ride «include» Adjust. Road associates with Ride.

## 3. Structure

Hub properties on the model: `continuousAssist: 250 W`, `peakTorque: 40 N·m`, `location: rear geared hub`, `regen: none`.

```
ElectricBike
├── Frame
├── BatteryPack
│   └── bms : BMS
├── MotorController
├── HubMotor
├── HumanInterface
├── BrakeSystem
├── cadenceSensor
└── wheelSpeedSensor
```

**Charge path (serial):** bike boundary `ElectricBike.Port.chargerIn` → nested BMS `chargerIn` → BMS `packOut` → pack `cellsIn`. There is no parallel pack+BMS charge feed and no `chargeInputIn` on the pack itself. That serial topology is inspired by UL 2849. UL 2849 is not a certification shall on this model and is not allocated as one.

Other IBD connectors:

- Frame mounts to battery, hub, human–machine interface (HMI), and brakes
- Pack `pwr` → controller `pwr` (pack power)
- Controller `drv` → hub `drv` (phase drive)
- HMI `cmd` → controller `cmd` (command)
- Brakes `inh` → controller `inh` (inhibit)
- Cadence sensor → controller cadence
- Wheel-speed sensor → controller speed (the 25 km/h cut is not cadence-only)

Context exchanges (not on the IBD): rider commands, charger energy, road load.

Lighting is a shall on HumanInterface; lamp hardware is not a separate part.

## 4. Behavior

RideControl starts in `off`.

| From | Trigger | To | Notes |
| --- | --- | --- | --- |
| off | `powerOn` | standby | Enable sensors |
| standby | `powerOff` | off | Readable path; do not draw a tight double arrow |
| standby | cadence (EPAC) | assist | `do / modulateTorque()` |
| standby | `startWalk` | walk | `do / limitSpeed(<= 6 km/h)` |
| off | `charger in` | charging | **Off → charging only.** No Standby → Charging. |
| charging | `chargeComplete` / `unplug` | off | |
| assist or walk | fault | fault | `inhibitMotor`; `openContactor` |
| fault | `resetFault` | off | Not standby |
| assist or walk | brake cut / stop-assist | standby | |

The activity is power on → select assist → pedal → apply brake → inhibit motor → deliver torque, plus plug-in and stop-charge. The sequence (`e-bike-int`) is the same story on lifelines.

## 5. Parametrics

| Quantity | Value | Meaning |
| --- | --- | --- |
| Continuous assist | 250 W | EU EPAC continuous (`continuousAssist`). Not peak. |
| Hub torque | 40 N·m | Hub **peak** (`peakTorque`). Not continuous. |
| Assist cutoff | 25 km/h | Wheel-speed cut; cadence PAS; no throttle. |
| Walk assist | ≤ 6 km/h | On the walk-state do-behavior. |
| Tour-scenario energy | 500 Wh | Display name on `ElectricBike.PAR.packEnergy` is `usableWh: 500 Wh Tour`. The `energyBalance` **expression still uses `packEnergy`**: `packEnergy >= energyPerKm * 60`. 500 Wh is the Tour-scenario binding, not pack nameplate. |
| Brake inhibit | ≤ 50 ms | Electronic inhibit **budget**. Not a distance test. Constraint: `brakeLatency <= 50 ms`. |
| Assist cut-off | 2 m / 5 m | EN 15194:2017 4.2.13 after pedaling stops. Lever switches relax 2 m → 5 m. Not vehicle brake distance. |
| Lighting | StVZO / ISO 6742 | Not UN ECE R113. |

Parametric `energyBalance` is pack-only and still binds `packEnergy`, not a `usableWh` parameter. Do not add rider pedal watts into that expression. Do not read 500 Wh as a nameplate.

The unsourced frame `yieldMargin: ≥ 1.5` figure is **dropped** from the model. The structural shall stays qualitative: carry rider, cargo, and battery loads without yielding.

Cell V/T chemistry numbers are unmarked. F-E06 stays unmarked.

## 6. Allocations

| Requirement | Allocated to |
| --- | --- |
| Ride Safety | BrakeSystem, MotorController, `cadenceSensor`, nested `BatteryPack.bms` |
| Range (≥ 60 km Tour) | BatteryPack |
| Assist Limit (25 km/h) | MotorController, `wheelSpeedSensor` |
| Charge Safety | `BatteryPack.bms` |
| Brake Override (50 ms) | BrakeSystem |
| Battery Cutoff | `BatteryPack.bms` |
| Display | HumanInterface |
| Structural | Frame |
| motor-assist cut-off | MotorController, `cadenceSensor`, `wheelSpeedSensor` (power management — not BrakeSystem) |
| Lighting (StVZO / ISO 6742) | HumanInterface |
| Walk Assist (≤ 6 km/h) | MotorController |
| Continuous Power (250 W) | HubMotor |

Ride Safety is fail-silent across brakes + controller + cadence + BMS, not brakes-only. Charge safety is the nested BMS opening the contactor — not a UL 2849 certification allocate. Clause 4.2.13 does not move onto BrakeSystem.

## 7. Open risks / unmarked

- One EPAC class only; no type-approval dossier. UL 2849 is not a certification shall.
- Cell V/T limits are named (`Vmax`, `Tmax`) without filled chemistry numbers.
- Lighting is allocated to HMI; lamp hardware is not a separate part.
- Regen is explicitly none; do not add it.
- The unsourced frame `≥ 1.5` yield figure is dropped; the structural shall stays qualitative.
- F-E06 stays unmarked.

## Generated views

These figures illustrate the architecture above; they do not replace it.

**`e-bike-ctx.png` — context.** Rider, charger, bike, road only. No Wheel Torque actor. Read the three external exchanges before opening the IBD.

**`e-bike-bdd.png` — block definition diagram (BDD).** Bike composed of frame, pack (with nested BMS), controller, hub, HMI, brakes, and the two sensors. Hub compartment states 250 W continuous and 40 N·m peak separately.

**`e-bike-ibd.png` — internal block diagram (IBD).** Child-part ports only. Charge is serial through the nested BMS (view title cites UL 2849 as path inspiration, not a cert). Cadence and wheel-speed feed the controller. Connections do not pass over boxes.

**`e-bike-uc.png` — use cases.** Rider on Ride and Adjust; Charger on Charge only; Ride «include» Adjust. No `lockBike`.

**`e-bike-req.png` — requirement diagram.** Twelve sibling shalls. Brake Override refines Ride Safety; Battery Cutoff refines Charge Safety. Read 4.2.13 as motor-assist cut-off, not vehicle brake distance.

**`e-bike-reqt.png` — requirement table.** Same shalls as rows, with Satisfied By filled from the model.

**`e-bike-stm.png` — state machine (STM).** Off, Standby, Assist, walk, charging, fault. Charging from Off only. Fault resets to Off. Walk `do` is `limitSpeed(<= 6 km/h)`.

**`e-bike-act.png` — activity.** Start-ride and charge actions in control-flow order.

**`e-bike-int.png` — sequence.** Interaction among rider, HMI, controller, hub, and brakes for a ride-and-inhibit story.

**`e-bike-par.png` — parametrics.** Pack `energyBalance` still binds `packEnergy` (display name `usableWh: 500 Wh Tour`) and `brakeLatencyLimit`. Tour 500 Wh is a scenario binding, not nameplate.

**`e-bike-alloc.png` — allocation table.** Requirement and function → part, including 4.2.13 to controller + sensors (not BrakeSystem).

**`e-bike-amx.png` — allocation matrix.** Same allocates as marks.

**`e-bike-pkg.png` — packages.** Model packages and their dependencies.

```bash
msml-validate-all projects/e-bike --strict
msml-render-all projects/e-bike
```
