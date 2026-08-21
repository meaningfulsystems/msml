# Electric Bike — Architecture / System Design

EU-class pedal-assist bicycle (EPAC / EN 15194) with a rear geared hub. Namespace `ElectricBike`. File stem `e-bike`. This note is the design argument for the model in this folder, not a catalog of pictures.

This is the publish hero. The same ElectricBike names appear in SysML2d; the files are not interchangeable. **250 W is the EU continuous assist rating, not peak power. 40 N·m is hub peak torque, not a continuous point at 250 W / 25 km/h.**

## 1. Purpose / context

The bike exists to carry a rider on the road with cadence-only pedal assist, to let the rider set assist level, and to accept charge from an off-board charger. Classification is one EN 15194 EPAC class: 25 km/h cutoff, no certified throttle, walk assist at or below 6 km/h, rear geared hub with no regeneration.

Throttle variants, mid-drive kits, and regenerative hubs are out of scope. There is no `lockBike` use case.

## 2. System boundary and actors

**Inside the bike:** Frame, BatteryPack with nested `bms : BMS`, MotorController, Rear Geared Hub (`HubMotor`), HumanInterface, BrakeSystem, `cadenceSensor`, `wheelSpeedSensor`.

**Outside (context only):** Rider, Charger, Road. Those three stay on `e-bike-ctx`. They are not parts on the IBD.

Use cases: Ride Bike, Adjust Assist, Charge Bike. Rider associates with Ride and Adjust (and also Charge as the person who plugs in). Charger associates with Charge only. Ride «include» Adjust. Road associates with Ride. Lock is omitted.

## 3. Requirements

Requirements are **siblings** under the bike. Brake Override refines Ride Safety. Battery Cutoff refines Charge Safety. Walk Assist and Continuous Power are siblings — they do not hang under Assist Limit.

| Id | Name | Text / numbers |
| --- | --- | --- |
| `ElectricBike.rideSafetyRequirement` | Ride Safety | Motor shall fail silent: brake inhibit, controller, cadence sensor, and BMS. Not brakes-only. |
| `ElectricBike.rangeRequirement` | Range (≥ 60 km Tour) | Tour-scenario binding: `usableWh` **500 Wh** / `energyPerKm` **~8.3 Wh/km** for 60 km. Not Eco / PAS-1. **500 Wh is not a pack nameplate.** |
| `ElectricBike.assistLimitRequirement` | Assist Limit (25 km/h) | EPAC / EN 15194: cadence-only assist, cut off at **25 km/h** (wheel speed). No throttle. |
| `ElectricBike.chargeSafetyRequirement` | Charge Safety | Stop on over-temp, over-voltage, or charger disconnect. BMS inside the pack opens the contactor. |
| `ElectricBike.brakeOverrideRequirement` | Brake Override (50 ms) | Motor inhibit within **50 ms** of either brake lever. **50 ms is an electronic inhibit budget.** Do not compare it to the EN 15194 distance test. |
| `ElectricBike.batteryCutoffRequirement` | Battery Cutoff | BMS inside the pack opens the contactor before any cell exceeds its V/T limit. |
| `ElectricBike.displayRequirement` | Display | Rider shall see speed, assist level, and remaining range hands-on-bars. |
| `ElectricBike.structuralRequirement` | Structural | Frame shall carry rider, cargo, and battery loads without yielding. |
| `ElectricBike.motorAssistCutoffRequirement` | motor-assist cut-off | EN 15194:**2017** **4.2.13 Power management**: motor-assist cut-off after pedaling stops is **2 m**, or **5 m** if brake-lever switches relax it. **Not vehicle brake distance.** Do not compare to the 50 ms inhibit budget. Do not allocate this shall to BrakeSystem. |
| `ElectricBike.lightingRequirement` | Lighting (StVZO / ISO 6742) | Lighting shall meet StVZO / ISO 6742. Not UN ECE R113. |
| `ElectricBike.walkAssistRequirement` | Walk Assist (≤ 6 km/h) | EPAC walk assist shall not exceed **6 km/h**. Walk assist is not a throttle. |
| `ElectricBike.continuousPowerRequirement` | Continuous Power (250 W) | Continuous assist shall not exceed **250 W**. EN 15194 EPAC continuous rating. |

## 4. Structure and interfaces

Hub properties on the model: `continuousAssist: 250 W`, `peakTorque: 40 N·m`, `location: rear geared hub`, `regen: none`.

Charge path (UL 2849, serial): bike boundary `chargerIn` → nested BMS `chargerIn` → BMS `packOut` → pack `cellsIn`. There is no parallel pack+BMS charge feed and no `chargeInputIn` on the pack itself.

Other IBD connectors:

- Frame mounts to battery, hub, HMI, and brakes
- Pack `pwr` → controller `pwr` (pack power)
- Controller `drv` → hub `drv` (phase drive)
- HMI `cmd` → controller `cmd` (command)
- Brakes `inh` → controller `inh` (inhibit)
- Cadence sensor → controller cadence
- Wheel-speed sensor → controller speed (the 25 km/h cut is not cadence-only)

Context exchanges (not on the IBD): rider commands, charger energy, road load.

## 5. States and modes

RideControl starts in `off`.

- `powerOn`: off → standby (enable sensors)
- `powerOff`: standby → off (readable path; do not draw a tight double arrow)
- cadence (EPAC): standby → assist (`do / modulateTorque()`)
- `startWalk`: standby → walk (`do / limitSpeed(<= 6 km/h)`)
- `charger in`: **off → charging only**. No Standby → Charging.
- `chargeComplete` / `unplug`: charging → off
- `faultFromAssist` / `faultFromWalk`: assist or walk → fault (`inhibitMotor`; `openContactor`)
- `resetFault`: fault → off (not standby)

Brake cut and stop-assist return assist or walk to standby.

## 6. Allocations (req → part)

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

Ride Safety is fail-silent across brakes + controller + cadence + BMS, not brakes-only. Charge safety is the nested BMS (UL 2849), not a sibling pack-level charge port.

## 7. Sourced numbers

| Quantity | Value | Meaning |
| --- | --- | --- |
| Continuous assist | 250 W | EU EPAC continuous (`continuousAssist`). Not peak. |
| Hub torque | 40 N·m | Hub **peak** (`peakTorque`). Not continuous. |
| Assist cutoff | 25 km/h | Wheel-speed cut; cadence PAS; no throttle. |
| Walk assist | ≤ 6 km/h | On the walk-state do-behavior. |
| Tour-scenario energy | 500 Wh | Binding on `usableWh` for the Tour range case. Not pack nameplate energy. |
| Brake inhibit | ≤ 50 ms | Electronic inhibit **budget**. Not a distance test. |
| Assist cut-off | 2 m / 5 m | EN 15194:2017 4.2.13 after pedaling stops. Lever switches relax 2 m → 5 m. Not vehicle brake distance. |
| Lighting | StVZO / ISO 6742 | Not UN ECE R113. |
| Frame yield margin | ≥ 1.5 | Aluminum frame. |

Parametric `energyBalance` is pack-only. Tour range binds `usableWh` and `energyPerKm` for that scenario. Do not read 500 Wh as a nameplate.

## 8. Open risks / TBD

- One EPAC class only; no type-approval dossier.
- Cell V/T limits are named (`Vmax`, `Tmax`) without filled chemistry numbers.
- Lighting is allocated to HMI; lamp hardware is not a separate part.
- Regen is explicitly none; do not add it.

## 9. Views in this folder

`e-bike-ctx.png`, `e-bike-bdd.png`, `e-bike-ibd.png`, `e-bike-stm.png`, `e-bike-act.png`, `e-bike-int.png`, `e-bike-uc.png`, `e-bike-req.png`, `e-bike-reqt.png`, `e-bike-par.png`, `e-bike-pkg.png`, `e-bike-alloc.png`, `e-bike-amx.png`.

![Electric bike internal structure](e-bike-ibd.png)

![Electric bike context](e-bike-ctx.png)

![Electric bike states](e-bike-stm.png)

```bash
msml-validate-all projects/e-bike --strict
msml-render-all projects/e-bike
```
