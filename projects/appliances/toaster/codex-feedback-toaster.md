# Codex Feedback: Toaster MSML Model

Review scope: `msml-specification.md` and all nine toaster diagrams in `projects/appliances/toaster`: package, requirements, block definition, internal block, activity, sequence, state machine, use case, and parametric.

Status note: this review was written before the v1.0 model/view split was implemented. The current repository uses `.msml` for semantic model files and `.msmd` for diagram view files.

## Executive Summary

The toaster model is a useful end-to-end exercise for MSML because it touches all nine SysML 1.x diagram families and produces readable PNG output. It currently reads more like a diagram rendering demo than an engineering model of a toaster. The main gaps are weak cross-diagram traceability, an underspecified safety model, simplified toaster physics, and inconsistent use of MSML diagram type names and relationship fields.

MSML itself has a strong premise: JSON, one diagram per file, explicit coordinates, and strict validation are good choices for AI-generated diagrams. The language needs tighter internal consistency, better reusable style/default mechanisms, richer cross-diagram references, and validator rules that catch semantic drift between diagrams, not just malformed JSON.

## Toaster Model Strengths

- All nine diagram types are represented, which makes this a good regression set for the renderer.
- Diagram frames render consistently and make diagram kind/context easy to identify.
- The same core components recur across views: `Toaster`, `HeatingElement`, `Timer`, `Carriage`, and `Lever`.
- The rendered layouts are generally legible, with enough spacing to inspect connections and labels.
- The state machine includes an overheat/error path, which is the right direction for a real appliance model.

## Toaster Model Issues

### 1. Requirements are too sparse for an appliance

The requirements diagram has only five requirements and misses core product constraints:

- electrical safety and insulation
- thermal safety on external surfaces
- cancel/eject behavior
- crumb tray/fire risk
- bread detection or carriage latch behavior
- user controls and browning repeatability
- power input assumptions
- regulatory constraints such as UL/IEC style safety categories
- verification methods and acceptance criteria

Recommendation: expand requirements into functional, safety, performance, interface, and verification groups. Add `satisfy` and `verify` links from blocks/test cases to requirements so this becomes a requirements model, not just a requirement tree.

### 2. Safety behavior is inconsistent across diagrams

`REQ-002` says the system detects overheat and shuts down automatically. The state machine sends `overheat_detected` to `Error` with `entry / sound_alarm()`, but it does not explicitly deactivate the heating element, release the carriage, or prevent restart. The sequence and activity diagrams omit overheat behavior entirely.

Recommendation: add a safety controller or thermal cutoff component and show it in BDD, IBD, STM, sequence, and requirements. The state transition to `Error` should have an effect such as `deactivate_element(); release_latch()` or the `Error` entry should include shutdown behavior.

### 3. The toaster architecture is missing important parts

The BDD and IBD include `HeatingElement`, `Timer`, `Carriage`, and `Lever`, but a practical toaster also needs at least:

- power supply / mains interface
- browning control
- thermostat or thermal sensor
- latch / electromagnet
- cancel button
- housing / slots / crumb tray
- optional indicator or audible signal

Recommendation: separate mechanical, electrical, and control concerns. Add a `Controller` or `SafetyController` block and define clear interfaces between user input, timing, heat control, and latch release.

### 4. Cross-diagram names are not consistently aligned

The same concept appears with different names and abstractions:

- BDD has `HeatingElement`, IBD has `element:HeatingElement`, sequence has `:HeatingElement`.
- Use case has `Activate Heating`, activity has `Heat Element`, sequence has `activate()`.
- Requirements mention `Timer Function`, BDD has `Timer`, sequence uses `start(90s)`.

Recommendation: define canonical model element IDs and allow diagrams to reference them. The toaster examples should use stable cross-diagram references so a renderer or validator can confirm that `ll-element`, `part-element`, and `block-element` refer to the same model concept.

### 5. Some SysML semantics are simplified or misleading

- The BDD composition diamonds are visually large and stacked near the parent block, making the part relationships look cluttered.
- The IBD models `heat` as a connector from `HeatingElement` to `Carriage`, but bread is the heated object; carriage is a mechanical holder.
- The use case diagram associates `Power Grid` with `Toast Bread`, but the power grid is not a goal-seeking actor in the usual use-case sense. It is better modeled as an external system/interface in BDD/IBD.
- The activity diagram forks `Start Timer` and `Heat Element`, then joins them before popping carriage. That implies both complete before pop, but heating is normally controlled until timer expiration. This should be a loop/interruptible activity or an event-driven behavior.
- The sequence diagram lacks `Carriage`, `Lever`, `BrowningControl`, and cancel/overheat alternatives, so it does not match the state machine or requirements.

Recommendation: use the toaster model to demonstrate real SysML intent. Add alternate flows for cancel and overheat, and make activity/sequence/state behavior agree.

### 6. Parametric model is physically underdeveloped

`P = V * I` and `Q = P * t` are a start, but a toaster model needs resistance and heat transfer assumptions:

- `P = V^2 / R` or `P = I^2 * R`
- efficiency from electrical power to bread heat
- heat loss to environment
- temperature rise relation such as `Q = m * c * deltaT`
- browning setting mapped to target energy or time
- safety cutoff threshold

Recommendation: add value properties for resistance, bread mass, heat capacity, ambient temperature, efficiency, target browning energy, and cutoff temperature. Then link parametric constraints to performance and safety requirements.

### 7. Rendered diagram issues

- Requirements diagram: the vertical red derive relationship overlaps the center requirement and makes the text harder to read.
- BDD: composition arrowheads/diamonds stack tightly under `Toaster`; multiplicity labels are not visible in the PNG.
- Sequence diagram: message labels are small and some are close to lifelines/activation bars.
- State machine: transition labels are small and several sit close to lines or state boundaries.
- IBD: port labels are tiny and hard to read; port ownership depends entirely on coordinates.
- Package diagram: much of the canvas is unused, and nested classes look more like boxes than package contents.

Recommendation: add validator or linter checks for label overlap, very small font sizes, unused canvas, connectors crossing labels, and relationship endpoints that do not land on expected element edges.

## MSML Language Issues

### 1. The requirements document contradicts itself on JSON vs YAML

The file format section correctly says MSML uses JSON parsed by Python stdlib `json`. Earlier drafts had leftover YAML language in module descriptions.

Recommendation: make JSON the single v1 serialization everywhere, or explicitly define a separate YAML import/export format. For v1, keeping JSON-only is better aligned with the stated AI-generation goals.

### 2. Diagram type names are inconsistent

The overview table uses abbreviations like `bdd`, `ibd`, `act`, `sd`, `stm`, `uc`, `req`, `par`, and `pkg`, but the detailed schema sections use names like `activity`, `sequence`, `state_machine`, `use_case`, `requirement`, `parametric`, and `package`. The toaster files use the long names for most diagram types but `bdd` and `ibd` for two of them.

Recommendation: define one canonical enum. A practical approach:

- `type`: canonical long semantic value, such as `activity` or `state_machine`
- `frame.abbreviation`: derived by renderer, such as `act` or `stm`

Do not make authors choose between abbreviation and semantic type.

### 3. Relationships have inconsistent arrowhead fields

The common relationship schema uses `source_arrowhead` and `target_arrowhead`, while state transitions use `arrowhead`. Sequence messages use `arrowhead` in the documentation but toaster examples omit it and rely on renderer defaults.

Recommendation: normalize relationship style fields by relationship family. For example, all edge-like relationships should use `source_arrowhead` and `target_arrowhead`, even if one side defaults to `none`.

### 4. Explicit coordinates are useful but too brittle by themselves

The explicit layout rule makes rendering deterministic, which is good for AI-generated assets. The downside is that the semantic model and visual model are fused. A minor content change can require many coordinate edits, and validators can pass diagrams that are semantically poor but geometrically valid.

Recommendation: keep explicit coordinates in v1, but add optional layout helpers that do not require full auto-layout:

- named anchor points, such as `source_anchor: bottom:5`
- relative placement hints, such as `below: req-001`
- reusable spacing constants
- linter-only layout checks
- optional generated layout metadata that can be overwritten

### 5. Port ownership should be semantic, not only spatial

IBD ports are separate elements placed near part rectangles. In the toaster IBD, a port belongs to a part because it is visually adjacent. That is fragile for validation and editing.

Recommendation: add `owner_ref` to ports and require it in strict mode. The renderer can still honor exact coordinates, but the model should know which part owns each port.

### 6. Cross-diagram references need first-class support

The requirements mention file-relative paths and element IDs, but the element schemas mostly use local IDs. The toaster model demonstrates why this matters: there is no machine-checkable link from a requirement to the block satisfying it, from a use case to the sequence realizing it, or from a BDD block to an IBD part typed by it.

Recommendation: add a common `model_ref` field to elements and relationships. Example:

```json
{
  "id": "part-element",
  "type": "part",
  "name": "element",
  "type_ref": "toaster-bdd.msmd#block-element",
  "model_ref": "model:Toaster.HeatingElement"
}
```

### 7. Style repetition is excessive

Every toaster file repeats nearly identical frame and style blocks. This is good for self-contained rendering, but noisy for AI generation and review. It also increases the chance of inconsistency.

Recommendation: support named style presets inside each file, while still expanding to complete defaults during validation or serialization. For example: `style_ref: "toaster.heating_element"` plus optional overrides.

### 8. Validation should include semantic linting

Current validator requirements focus on syntax, IDs, colors, numeric ranges, and required fields. The toaster set would benefit from deeper checks:

- diagram type is canonical
- relationship types are valid for the diagram type
- relationship endpoint IDs are semantically valid, such as connectors between ports
- BDD blocks referenced by IBD `type_ref` exist
- sequence message lifelines exist and message order is monotonic
- requirement relationships use allowed direction
- labels and connectors do not overlap major element text
- fonts are above a minimum readable size
- all requirement IDs are unique and stable

Recommendation: split validation into `schema`, `strict`, and `lint`. `lint` can warn without blocking rendering.

## Recommended Next Iteration

1. Normalize the MSML spec around JSON and a single diagram type enum.
2. Add `model_ref`, `owner_ref`, and file-relative `type_ref` conventions.
3. Expand toaster requirements to include safety, controls, user interaction, electrical assumptions, and verification.
4. Add missing toaster components: browning control, cancel button, latch/electromagnet, thermal sensor/cutoff, power interface, and bread/slot/housing abstractions.
5. Align behavior diagrams around the same scenarios: normal toast, cancel, overheat shutdown, and reset.
6. Improve parametrics with resistance, heat transfer, efficiency, temperature, and safety thresholds.
7. Add diagram linting for endpoint anchors, overlap, label readability, and cross-diagram consistency.

## Bottom Line

The toaster folder is a solid renderer smoke test but not yet a strong systems model. The best improvement is to make the toaster model traceable: requirements should drive structure, behavior should realize use cases, parametrics should justify performance claims, and safety behavior should appear consistently across diagrams. MSML should evolve from "valid visual JSON" toward "valid visual JSON plus checkable model semantics."
