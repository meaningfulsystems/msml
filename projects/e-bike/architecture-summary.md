# Electric Bike Architecture Summary

EU EPAC rear-geared hub bicycle. Namespace `ElectricBike`. File stem `e-bike`. Context is rider / charger / bike / road only. There is no `lockBike` use case and no throttle.

This is the publish hero. The same ElectricBike names appear in [SysML2d](https://github.com/meaningfulsystems/sysml2d); the files are not interchangeable.

## Parts

Frame, BatteryPack with nested `bms : BMS`, MotorController, Rear Geared Hub (id `HubMotor`), HumanInterface, BrakeSystem, `cadenceSensor`, and `wheelSpeedSensor`.

Charge path: charger → BMS → pack cells. The BMS sits inside the pack. Rider, charger, and road stay on the context view, not the IBD.

## Key numbers

| Quantity | Value | Meaning |
| --- | --- | --- |
| Pack energy | 500 Wh | Usable Tour-mode energy. |
| Range | ≥ 60 km | Tour-mode, not Eco / PAS-1. |
| Assist cutoff | 25 km/h | Cadence-only EPAC. |
| Continuous assist | **250 W** | EU continuous rating (`continuousAssist`). Not peak. |
| Hub torque | **40 N·m** | Hub **peak** torque (`peakTorque`). Not continuous. |
| Walk assist | ≤ 6 km/h | EPAC walk; not a throttle. |
| Brake | EN 15194 2 m / 5 m plus 50 ms electronic | Stopping distance plus inhibit latency. |
| Lighting | ISO 6742 / StVZO | Not UN ECE R113. |

## Views

| View | File | Story |
| --- | --- | --- |
| Context | `e-bike-ctx` | Rider · charger · bike · road |
| BDD | `e-bike-bdd` | Parts, nested BMS, sensors |
| IBD | `e-bike-ibd` | Internal structure; charger → BMS → pack |
| STM | `e-bike-stm` | Off / Standby / walk / Assist / charging / Fault |
| Activity | `e-bike-act` | Start ride; Pedal (EPAC) |
| Sequence | `e-bike-int` | Rear Geared Hub lifeline |
| Use case | `e-bike-uc` | Rider on Ride + Adjust; Charger on Charge only |
| Requirements | `e-bike-req` · `e-bike-reqt` | Sibling requirements; lockBike omitted |
| Parametric | `e-bike-par` | Tour energy / range / brake limits |
| Package | `e-bike-pkg` | Model packages |
| Allocation | `e-bike-alloc` · `e-bike-amx` | Assist Limit → `wheelSpeedSensor` |

![Electric bike internal structure](e-bike-ibd.png)

![Electric bike context](e-bike-ctx.png)

![Electric bike states](e-bike-stm.png)

## Validate and render

```bash
msml-validate-all projects/e-bike --strict
msml-render-all projects/e-bike
```
