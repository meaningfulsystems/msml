# Smart Blender — MagicGrid architecture walkthrough

A student can follow this note with `blender-model.msml` open. It walks the countertop blender from problem to solution in simplified MagicGrid order, then explains every generated view. This is not a Department of Defense Architecture Framework (DoDAF) product set.

Namespace `Blender`. File stem `blender`. The same appliance idea appears in SysML2d (`examples/blender/blender.sysml`). The files are not interchangeable. Pick one toolchain. Every number below is already on `blender-model.msml`.

This is an example model for language coverage, not a certifiable appliance.

## 1. Problem / context

**Who.** The user loads ingredients, seats the container, closes the lid, starts or stops a smoothie program, and pours. Mains power is implied by the Off / Ready switch; there is no Power Grid actor on this model.

**Boundary.** Inside: MotorBase, Motor, DriveCoupling, Container, BladeAssembly, Lid, Tamper, ControlPanel, SmoothieCompleteSensor. Outside: User.

**Mission.** Blend ingredients under program control until a smoothness estimate says stop — or the user stops, a timeout fires, or power goes off. The motor must not run unless the lid is seated and locked. Overcurrent must cut power before the motor is damaged.

The model is one baseline smart blender, not a product line.

## 2. Requirements and use cases

Thirteen sibling shalls bound from SysML2d `blender.sysml`. No extras. There are **no formal use-case definitions** on `blender-model.msml`. The operator story is recovered from the activity and the state machine (STM): load, secure lid, start, blend until smooth, stop.

| Id | Name | Shall |
| --- | --- | --- |
| `Blender.lidInterlockRequirement` | lid interlock | Motor shall not run unless the lid is fully seated and locked. |
| `Blender.motorControlRequirement` | motor control | Start, pause, and stop within **200 ms**. |
| `Blender.smoothnessDetectionRequirement` | smoothness detection | Sensor detects completion and signals the control panel. |
| `Blender.powerRequirement` | power rating | Operate within the rated power envelope. Watts unmarked. |
| `Blender.userControlsRequirement` | user controls | Start, pause, and stop without tools. |
| `Blender.cleaningRequirement` | cleaning | Container, lid, and blade dishwasher-safe or washable. |
| `Blender.serviceRequirement` | serviceability | Serviceable without specialized equipment. |
| `Blender.motorSpeedRequirement` | motor speed | Set speed within **±10%**. |
| `Blender.interlockLatencyRequirement` | interlock latency | Lid interlock disables the motor within **50 ms** of lid removal. |
| `Blender.overcurrentProtectionRequirement` | overcurrent protection | Cuts power before motor damage. Trip time unmarked. |
| `Blender.smoothnessThresholdRequirement` | smoothness threshold | Configurable threshold; at least **three** blend program profiles. |
| `Blender.noiseRequirement` | noise | Below **85 dB(A)** at the operator position. |
| `Blender.containerSeatRequirement` | container seat | Positive mechanical lock to the base; deliberate release. |

Pause is required in the motor-control and user-controls shalls. The STM has no pause state; that gap stays unmarked as a state, not filled with an invented mode.

## 3. Structure

There is no blender block definition diagram (BDD) in this folder. Read structure from the model parts and the internal block diagram (IBD).

```
Blender
├── MotorBase
├── Motor                 speed: RPM (revolutions per minute; typed, unfilled)
├── DriveCoupling
├── Container
│   └── BladeAssembly     (composition: contains)
├── Lid
├── Tamper
├── ControlPanel          variableSpeed, pulse, smoothieProgram
└── SmoothieCompleteSensor   loadProxy, vibrationProxy, textureEstimate
```

The blender block also holds `program` and `smoothnessThreshold` as typed properties without filled product values.

**Command / drive / sense (IBD):**

- ControlPanel `motorCommand` (out) → Motor `cmd` (in)
- Motor `drive` (out) → DriveCoupling `driveIn` (in)
- DriveCoupling `driveOut` (out) → BladeAssembly `drive` (in)
- DriveCoupling `vibrationProxy` (out) → SmoothieCompleteSensor `vibrationProxy` (in)
- SmoothieCompleteSensor `complete` (out) → ControlPanel `complete` (in)

**Mechanical seats:**

- MotorBase `mechanical` ↔ Container `mechanical` (container on base)
- Lid `containerSeat` ↔ Container `lidSeat`
- Tamper `lidOpening` ↔ Lid `tamperOpening` (tamper through the lid)

There is no separate interlock part. Lid seating is the mechanical connector plus the two interlock shalls.

## 4. Behavior

**State machine (STM).** SmoothieProgram: Off → Ready (`on switch`) → Blending (`start command`). From Blending, `smoothie complete`, `stop command`, or `timeout` return to Ready. `off switch` from Ready or Blending returns to Off.

The STM keeps Off / Ready / Blending. Lid-open and overcurrent are requirements allocated to ControlPanel and MotorBase; they are not extra STM event names on this view.

**Activity.** Load ingredients → secure lid → select smoothie program → ramp motor → blend and sense → decision (loop while not smooth) → stop motor → signal complete → serve.

Timeout duration is unmarked.

## 5. Parametrics

This folder has no parametric diagram. Sourced numbers live on the requirement texts:

- motor start / pause / stop within **200 ms**
- set speed within **±10%**
- lid interlock disables the motor within **50 ms**
- noise below **85 dB(A)** at the operator
- at least three blend program profiles

`speed: RPM` and `smoothnessThreshold: Real` are types, not values. Rated watts and overcurrent trip time stay unmarked.

## 6. Allocations

Satisfy mappings on the model:

| Requirement | Satisfied by |
| --- | --- |
| lid interlock | ControlPanel |
| motor control | Motor |
| smoothness detection | SmoothieCompleteSensor |
| power rating | Motor |
| user controls | ControlPanel |
| cleaning | Container |
| serviceability | Blender |
| motor speed | Motor |
| interlock latency | ControlPanel |
| overcurrent protection | MotorBase |
| smoothness threshold | SmoothieCompleteSensor |
| noise | Motor |
| container seat | Container |

SysML2d allocation names kept where they map: `allocateInterlockToControlPanel`, `allocateTorqueToMotor`, `allocateSmoothnessToSensor`, `allocateCleaningToContainer`, `allocateProtectionToMotorBase`, `allocateInterfaceToControlPanel`.

## 7. Open risks / unmarked

- Example model, not a certifiable appliance.
- Rated power magnitude, blend timeout, and overcurrent trip time are unmarked.
- Pause is required in two shalls and has no STM state.
- No mains / thermal analysis. No BDD, sequence, or parametric view in this folder.

## Generated views

These figures illustrate the architecture above; they do not replace it.

**`blender-ibd.png` — internal block diagram (IBD).** The only structure picture. Read two paths: command/drive/sense (panel → motor → coupling → blades, with vibration back to the sensor) and mechanical seats (base ↔ container, lid ↔ container, tamper through lid). Lines stay off boxes.

**`blender-act.png` — activity.** Smoothie program as a swim of actions. The decision node is “smoothness reached?”; the loop guard is `not smooth`.

**`blender-stm.png` — state machine (STM).** Off, Ready, Blending. Triggers are switch, start, complete, stop, timeout. No Error box on this view.

**`blender-req.png` — requirement diagram.** Thirteen sibling boxes. Read the numbered targets (200 ms, ±10%, 50 ms, 85 dB(A), three profiles) and the qualitative shalls.

**`blender-reqt.png` — requirement table.** Same thirteen shalls as rows, with Satisfied By filled from the model.

```bash
msml-validate-all projects/appliances/blender --strict
msml-render-all projects/appliances/blender
```
