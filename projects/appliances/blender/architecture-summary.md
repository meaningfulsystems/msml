# Smart Blender Architecture Summary

High-performance smart blender concept used to exercise IBD, activity, and state-machine views. Namespace `Blender`. File stem `blender`.

## Parts

SmartBlender composed of MotorBase, Motor, DriveCoupling, Container, BladeAssembly, Lid, Tamper, ControlPanel, and SmoothieCompleteSensor.

## Key numbers

This MSML blender is a compact coverage example. It does not invent certification numbers (rpm, dBA, interlock milliseconds) that are not on the model.

## Views

| View | File | Story |
| --- | --- | --- |
| IBD | `blender-ibd` | Internal structure |
| Activity | `blender-act` | Smoothie program |
| STM | `blender-stm` | Off / powered blend cycle |

![Smart blender internal structure](blender-ibd.png)

## Validate and render

```bash
msml-validate-all projects/appliances/blender --strict
msml-render-all projects/appliances/blender
```
