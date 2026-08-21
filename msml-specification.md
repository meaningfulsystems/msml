# MSML v1.0 Specification

**Meaningful Systems Modeling Language**  
**Version:** 1.0  
**Date:** 2026-08-21  
**Status:** Public specification

MSML is a scriptable graphical systems modeling language inspired by SysML 1.x and PlantUML. SysML provides the systems-engineering vocabulary. PlantUML demonstrates the value of diagrams that are generated, reviewed, versioned, and rendered from text. MSML combines those ideas into JSON files that can be produced by humans or AI and rendered into graphical diagrams.

MSML v1.0 uses two file types:

| Extension | Name | Purpose |
|---|---|---|
| `.msml` | MSML model file | Complete system model: definitions and relationships. No layout or visual styling. |
| `.msmd` | MSML diagram file | Graphical diagram view: canvas, frame, positioned view elements, style, and relationship routing. |

Model files do not reference diagrams. Diagram files reference model files. A diagram is a view of the loaded model graph; repository diagrams must not introduce model elements or relationships that are absent from `.msml`.

---

## 1. Design Goals

MSML v1.0 is designed for:

1. **AI and human authoring** - JSON, explicit fields, stable IDs, and no indentation-sensitive syntax.
2. **Scriptable graphical modeling** - diagrams are generated from text and rendered to PNG.
3. **Model/view separation** - model definitions and relationships live in `.msml`; diagram layout lives in `.msmd`.
4. **SysML 1.x coverage** - the nine SysML 1.x diagram families plus the common requirement-table, allocation-table, and allocation-matrix views.
5. **Deterministic rendering** - diagram files carry explicit coordinates and styles.
6. **Small implementation surface** - v1.0 stays practical enough to build and inspect in one repository.

---

## 2. Encoding and Parsing

- File format: JSON
- Encoding: UTF-8
- JSON parser: Python stdlib `json`
- Colors: hex strings only, `#RRGGBB` or `#RRGGBBAA`
- Dates: ISO-style date strings, e.g. `2026-05-17`

The renderer and parser must reject malformed JSON. Diagram rendering must fail loudly when a `.msmd` file references a missing model file, omits or references a missing model definition, or omits or references a missing model relationship.

---

## 3. Model Files (`.msml`)

A `.msml` file is a model file. It contains the definitions and relationships needed to recreate diagram topology and system meaning. It does not contain diagram frames, canvases, coordinates, waypoints, z-indexes, or visual styles.

### 3.1 Top-Level Structure

```json
{
  "msml_version": "1.0",
  "model": {
    "id": "hos-model",
    "name": "Humanity Optimization System",
    "namespace": "HOS",
    "imports": [],
    "definitions": [],
    "relationships": [],
    "metadata": {
      "author": "Andrew Fried",
      "created": "2026-05-17",
      "modified": "2026-05-17",
      "tags": []
    }
  }
}
```

### 3.2 Model Imports

`model.imports` is optional. It is a list of relative paths to other `.msml` files.

```json
{
  "imports": ["../common/common-model.msml"]
}
```

Imports are resolved relative to the importing model file. Imported definitions and relationships are available to diagrams that load the importing model.

Models may import parent or shared models to keep large systems modular. For example, `pacific-ocean.msml` may import `oceans.msml`, and `oceans.msml` may import `earth.msml`. Model files still do not reference diagrams.

v1.0 rule: if the same definition ID appears more than once after imports are loaded, the later local definition wins.

### 3.3 Definition IDs

Every model definition has a stable dot-notation `id`.

Examples:

- `Toaster.HeatingElement`
- `Toaster.REQ-001.1`
- `HOS.HumanityOptimizationSystem`
- `HOS.Activity.ModelFutures`

Definition IDs are the values used by diagram elements as `model_ref`.

Definition IDs should describe the model element's intent, not the diagram family where the element first appears. For example, prefer semantic IDs such as `Toaster.Behavior.Toasting.Start`, `Toaster.Port.TimerSignalOutput`, or `HOS.Sequence.Execution.HosAnalysis` over IDs that only encode view origin such as `Toaster.ACT.Init` or `HOS.IBD.Port1`.

Relationship IDs may still use diagram-origin prefixes such as `act-toaster.f1` or `ibd-toaster.conn-power` when that makes generated diagram references easier to trace.

### 3.4 Definition Object

Every definition has:

```json
{
  "id": "HOS.ScenarioModel",
  "type": "block",
  "name": "ScenarioModel"
}
```

Common fields:

| Field | Required | Description |
|---|---:|---|
| `id` | yes | Stable dot-notation model reference. |
| `type` | yes | Definition type. |
| `name` | yes | Human-readable model name. |
| `description` | no | Optional explanatory text. |
| `metadata` | no | Optional definition metadata. |

Definitions must not include `layout`, `style`, `canvas`, `frame`, `waypoints`, `z_index`, or `rotation`.

---

## 4. Supported Definition Types

MSML v1.0 supports definitions needed for all SysML 1.x-style model content and diagram topology in this repository.

### 4.1 Block

```json
{
  "id": "Toaster.HeatingElement",
  "type": "block",
  "name": "HeatingElement",
  "stereotype": "block",
  "is_abstract": false,
  "compartments": {
    "properties": [
      { "name": "resistance", "type": "Ohm", "multiplicity": "1" }
    ],
    "operations": [
      { "name": "activate", "parameters": [], "return_type": "void" }
    ],
    "constraints": []
  }
}
```

### 4.2 Requirement

```json
{
  "id": "Toaster.REQ-001.1",
  "type": "requirement",
  "name": "Heat Control",
  "req_id": "REQ-001.1",
  "text": "Heating element shall reach target temperature within 30 seconds.",
  "kind": "performance",
  "priority": "high",
  "status": "approved"
}
```

Allowed `kind` values:

- `functional`
- `performance`
- `interface`
- `physical`
- `design_constraint`
- `extended`

Allowed `priority` values:

- `high`
- `medium`
- `low`

Allowed `status` values:

- `proposed`
- `approved`
- `deprecated`

### 4.3 State

```json
{
  "id": "Toaster.State.ToastingCycle.Toasting",
  "type": "state",
  "name": "Toasting",
  "kind": "simple",
  "entry": "start_timer()",
  "do": "heat_element()",
  "exit": "stop_timer()"
}
```

### 4.4 Action

```json
{
  "id": "HOS.Activity.ModelFutures",
  "type": "action",
  "name": "Model Possible Futures",
  "kind": "opaque",
  "pins": {
    "input": [],
    "output": []
  }
}
```

### 4.5 Use Case

```json
{
  "id": "Toaster.UC.ToastBread",
  "type": "use_case",
  "name": "Toast Bread",
  "extension_points": []
}
```

### 4.6 Actor

```json
{
  "id": "Toaster.Actor.User",
  "type": "actor",
  "name": "User"
}
```

### 4.7 Constraint Property

```json
{
  "id": "Toaster.PAR.PV2R",
  "type": "constraint_property",
  "name": "P = V^2 / R",
  "expression": "P = V**2 / R",
  "parameters": [
    { "name": "V", "type": "Real" },
    { "name": "R", "type": "Real" },
    { "name": "P", "type": "Real" }
  ]
}
```

### 4.8 Value Property

```json
{
  "id": "Toaster.HeatingElement.resistance",
  "type": "value_property",
  "name": "resistance: Ohm",
  "value_type": "Real",
  "unit": "Ohm"
}
```

### 4.9 Package / Model / Class

```json
{
  "id": "Toaster.Model.Structural",
  "type": "package",
  "name": "Structural"
}
```

`type` may be `model`, `package`, or `class`.

### 4.10 Control and Notation Nodes

Diagram control/topology nodes are model definitions in MSML v1.0. They are lightweight definitions so a diagram can be recreated from the loaded `.msml` model graph plus `.msmd` view layout.

```json
{
  "id": "Toaster.Behavior.Toasting.Start",
  "type": "initial_node",
  "name": "Initial"
}
```

Supported control and notation definition types:

- `initial_node`
- `activity_final_node`
- `flow_final_node`
- `fork_node`
- `join_node`
- `decision_node`
- `merge_node`
- `partition`
- `initial_pseudostate`
- `final_state`
- `execution_occurrence`
- `system_boundary`
- `port`
- `comment`
- `annotation`

Ports include ownership information:

```json
{
  "id": "Toaster.Port.LeverControlOutput",
  "type": "port",
  "name": "ctrl",
  "owner_ref": "Toaster.Lever",
  "direction": "out"
}
```

Execution occurrences may reference the lifeline they belong to:

```json
{
  "id": "Toaster.Sequence.Execution.ToasterActivation",
  "type": "execution_occurrence",
  "name": "Toaster execution",
  "lifeline_ref": "Toaster"
}
```

Activity partitions are model-backed definitions used to represent swimlanes or responsibility regions:

```json
{
  "id": "Blender.Behavior.MakeSmoothie.UserPartition",
  "type": "partition",
  "name": "User"
}
```

---

## 5. Model Relationships

Model relationships live in `model.relationships`. A relationship may appear in zero, one, or many diagrams. Diagrams reference model relationships with `relationship_ref`.

Common relationship fields:

```json
{
  "id": "rel-hos-scenario",
  "type": "composition",
  "name": "scenario component",
  "source": "HOS.HumanityOptimizationSystem",
  "target": "HOS.ScenarioModel",
  "multiplicity_source": "1",
  "multiplicity_target": "1"
}
```

Relationship IDs are stable model IDs. They do not need dot notation, but they must be unique within the loaded model graph.

Recommended convention: prefix relationship IDs with the diagram ID where they were first defined, separated by a dot. Examples: `bdd-toaster.comp-heating-element`, `sd-toaster.m1`, `stm-toaster.t-idle-toasting`.

### 5.1 Supported Relationship Types

Structural:

- `association`
- `composition`
- `aggregation`
- `generalization`
- `dependency`
- `realization`

Requirements:

- `containment`
- `derive`
- `satisfy`
- `verify`
- `refine`
- `trace`
- `copy`

Allocation:

- `allocate`

Activity:

- `control_flow`
- `object_flow`

Sequence:

- `message`

State machine:

- `transition`

Internal block / parametric:

- `connector`
- `binding_connector`

Package:

- `package_merge`
- `package_import`
- `element_import`
- `profile_application`

Use case:

- `include`
- `extend`
- `association`
- `generalization`

### 5.2 Message Relationships

Sequence messages use model references for lifelines:

```json
{
  "id": "msg-hos-request-support",
  "type": "message",
  "name": "request support",
  "source_lifeline": "HOS.DecisionMakers",
  "target_lifeline": "HOS.HumanityOptimizationSystem",
  "message_sort": "synch_call"
}
```

Allowed `message_sort` values:

- `synch_call`
- `asynch_call`
- `asynch_signal`
- `reply`
- `create`
- `destroy`
- `found`
- `lost`

`source_lifeline` and `target_lifeline` must reference model definitions of type `block` or `actor`. Referencing any other definition type is a strict validation error.

### 5.3 State Transitions

```json
{
  "id": "trans-toasting-done",
  "type": "transition",
  "source": "Toaster.State.ToastingCycle.Toasting",
  "target": "Toaster.State.ToastingCycle.Done",
  "trigger": "timer_expired",
  "guard": "",
  "effect": "deactivate_element()"
}
```

---

## 6. Diagram Files (`.msmd`)

A `.msmd` file is a diagram view. It references one or more `.msml` model files.

### 6.1 Top-Level Structure

```json
{
  "msml_version": "1.0",
  "model_files": ["hos-model.msml"],
  "diagram": {
    "type": "bdd",
    "id": "bdd-hos-definition",
    "name": "Humanity Optimization System Definition",
    "context": "HOS",
    "frame": {},
    "canvas": {},
    "elements": [],
    "relationships": [],
    "metadata": {}
  }
}
```

`model_files` is a JSON array of relative paths to `.msml` model files. It must always be an array, even when referencing a single model. The singular `model_file` field is not valid.

```json
{
  "model_files": ["hos-model.msml", "../common/common-model.msml"]
}
```

### 6.2 Diagram Types

Canonical diagram type values:

| Diagram | `diagram.type` | Frame abbreviation | Filename convention |
|---|---|---|---|
| Block Definition Diagram | `bdd` | `bdd` | `*-bdd.msmd` |
| Internal Block Diagram | `ibd` | `ibd` | `*-ibd.msmd` |
| Activity Diagram | `activity` | `act` | `*-act.msmd` |
| Sequence Diagram | `sequence` | `sd` | `*-seq.msmd` |
| State Machine Diagram | `state_machine` | `stm` | `*-stm.msmd` |
| Use Case Diagram | `use_case` | `uc` | `*-uc.msmd` |
| Requirements Diagram | `requirement` | `req` | `*-req.msmd` |
| Parametric Diagram | `parametric` | `par` | `*-par.msmd` |
| Package Diagram | `package` | `pkg` | `*-pkg.msmd` |
| Requirement Table | `requirement_table` | `reqt` | `*-reqt.msmd` |
| Allocation Table | `allocation_table` | `alloc` | `*-alloc.msmd` |
| Allocation Matrix | `allocation_matrix` | `amx` | `*-amx.msmd` |

The first nine types are the official OMG SysML 1.6 diagram families. Requirement tables, allocation tables, and allocation matrices are the common SysML 1 tabular views shown in Annex D. They are first-class `.msmd` views in MSML: the model still owns requirements and `allocate` relationships; the diagram file owns columns, row order, and layout.

### 6.2.1 Allocate Relationships

`allocate` is a SysML 1 mapping from a source element (often a behavior or use case) to a target element (often a block or part). Use it for functional, behavioral, or structural allocation:

```json
{
  "id": "alloc-toaster.heat-element",
  "type": "allocate",
  "kind": "functional",
  "name": "functional allocation",
  "source": "Toaster.ToastingActivity.HeatElement",
  "target": "Toaster.HeatingElement"
}
```

Allowed `kind` values are informational: `functional`, `behavioral`, and `structural`. Diagrams render `allocate` as a dashed open arrow labeled `«allocate»`. Allocation tables and matrices are compact views of the same relationships.

### 6.2.2 Tabular Views

Requirement tables declare `diagram.table.columns` and one view element per shown requirement. The renderer reads `req_id`, `name`, `kind`, `priority`, `status`, and `text` from the model. If the loaded model contains `satisfy` or `verify` relationships, the table may also show `satisfied_by` and `verified_by`.

Allocation tables declare `diagram.table.columns` and one diagram relationship per shown `allocate` relationship. Rows are derived from those relationships.

Allocation matrices declare `diagram.matrix` plus elements with `matrix_role` of `row` or `column`. A marked cell means an `allocate` relationship exists from the row `model_ref` to the column `model_ref`.

### 6.3 Subject Reference

IBD and parametric diagrams should declare the model element whose interior or parametric context is being shown. Use the optional `subject_ref` field at `diagram.subject_ref`:

```json
{
  "diagram": {
    "type": "ibd",
    "subject_ref": "Toaster"
  }
}
```

`subject_ref` must resolve to a `block` definition in the loaded model. The renderer ignores it. Validators use it to confirm the diagram subject exists and, in future richer models, that parts are valid features of the subject block.

### 6.4 Diagram Frame

Every rendered diagram has a SysML-style frame:

```json
{
  "frame": {
    "visible": true,
    "style": {
      "border_color": "#333333",
      "border_width": 1.5,
      "border_style": "solid",
      "fill_color": "#FFFFFF",
      "tab": {
        "fill_color": "#FFFFFF",
        "border_color": "#333333",
        "padding_x": 8,
        "padding_y": 4,
        "font": {
          "family": "Arial",
          "size": 11,
          "bold": false,
          "color": "#000000"
        }
      }
    }
  }
}
```

The frame label is:

```text
<diagram abbreviation> [<context>] <diagram name>
```

### 6.5 Canvas

```json
{
  "canvas": {
    "width": 1000,
    "height": 700,
    "background_color": "#FAFAFA",
    "grid": {
      "enabled": true,
      "size": 10,
      "snap": true
    }
  }
}
```

Coordinates are in canvas pixels and are relative to the diagram canvas interior.

---

## 7. Diagram Elements

Diagram elements are view objects. Every diagram element in repository `.msmd` files must use `model_ref`; the model definition provides the element meaning, and the diagram element provides layout and style.

### 7.1 Model-Backed Element

```json
{
  "type": "block",
  "id": "block-scenarios",
  "model_ref": "HOS.ScenarioModel",
  "layout": {
    "x": 310,
    "y": 330,
    "width": 220,
    "height": 135,
    "z_index": 1
  },
  "style": {
    "fill_color": "#F2ECF8",
    "border_color": "#6D4C9A"
  }
}
```

Required fields:

- `type`
- `id`
- `model_ref`
- `layout.x`
- `layout.y`
- `layout.width`
- `layout.height`

### 7.2 View Labels

Diagram-local label fields:

| Field | Purpose |
|---|---|
| `role_name` | Instance/role name, used mainly for IBD parts and lifelines. |
| `display_name` | Visual override rendered instead of the model definition name. |

Rules:

- If `display_name` exists, render it exactly.
- Else if `role_name` exists on a part, render `role_name:ModelDefinitionName`.
- Else if `role_name` exists on a lifeline, render `role_name`.
- Else render the model definition `name`.

### 7.3 Control, Partition, Port, and Annotation Elements

Control nodes, activity partitions, pseudostates, execution occurrences, system boundaries, ports, comments, and annotations are model-backed elements in MSML v1.0. They still carry diagram layout and style in `.msmd`.

Example port view:

```json
{
  "type": "port",
  "id": "port-hos-values",
  "model_ref": "HOS.Port.HosValuesInput",
  "layout": { "x": 399, "y": 282, "width": 12, "height": 12, "z_index": 2 },
  "style": { "fill_color": "#FFFFFF", "border_color": "#9A6418" }
}
```

---

## 8. Diagram Relationships

Diagram relationships are view objects for model relationships. Every diagram relationship in repository `.msmd` files must use `relationship_ref`. A diagram relationship may carry layout/routing/style fields such as `waypoints`, `label_offset`, and visual overrides, but the relationship meaning and endpoints live in `.msml`.

```json
{
  "id": "view-rel-hos-scenario",
  "relationship_ref": "rel-hos-scenario",
  "waypoints": [
    { "x": 550, "y": 230 },
    { "x": 550, "y": 330 }
  ],
  "style": {
    "line_color": "#2E5E87",
    "line_width": 1.5,
    "line_style": "solid",
    "source_arrowhead": "composition",
    "target_arrowhead": "none"
  }
}
```

The renderer resolves the `relationship_ref` and merges the semantic relationship into the diagram relationship before drawing.

Diagram-local fields:

- `id`
- `relationship_ref`
- `waypoints`
- `layout`
- `label_position`
- `style`

The renderer resolves `relationship_ref` against the loaded model graph. Missing or unresolved `relationship_ref` is an error.

### 8.1 Relationship Style

```json
{
  "style": {
    "line_color": "#333333",
    "line_width": 1.5,
    "line_style": "solid",
    "corner_radius": 10,
    "source_arrowhead": "none",
    "target_arrowhead": "open",
    "label_offset": { "x": 0, "y": 0 }
  }
}
```

Allowed `line_style` values:

- `solid`
- `dashed`
- `dotted`

Allowed arrowhead values:

- `none`
- `open`
- `filled`
- `diamond`
- `open_diamond`
- `composition`
- `aggregation`
- `triangle`

---

## 9. Layout and Style

Every rendered element must have explicit layout:

```json
{
  "layout": {
    "x": 0,
    "y": 0,
    "width": 200,
    "height": 100,
    "z_index": 0,
    "rotation": 0
  }
}
```

Common style fields:

```json
{
  "style": {
    "fill_color": "#DDEEFF",
    "border_color": "#336699",
    "border_width": 2,
    "border_style": "solid",
    "opacity": 1.0,
    "corner_radius": 0,
    "font": {
      "family": "Arial",
      "size": 12,
      "color": "#000000",
      "bold": false,
      "italic": false,
      "underline": false
    }
  }
}
```

---

## 10. Renderer Requirements

The v1.0 renderer:

- renders `.msmd` files only
- loads `model_files`
- loads imported model files
- resolves diagram `model_ref` values to model definitions
- resolves diagram `relationship_ref` values to model relationships
- fails loudly on singular `model_file`, missing model files, missing or unresolved model refs, and missing or unresolved relationship refs
- writes PNG output next to the `.msmd` file unless an explicit output path is provided
- does not render `.msml` files directly

CLI:

```bash
msml-render path/to/diagram.msmd
msml-render-all projects/humanity-optimization
```

`msml-render-all` searches for `.msmd` files only.

---

## 11. Validation Requirements

The validator provides three levels:

### 11.1 Schema

- JSON is valid.
- Top-level file shape is valid for `.msml` or `.msmd`.
- Required fields exist.
- `.msmd` files use `model_files`; singular `model_file` is invalid.
- Model files declared by `.msmd` files resolve.
- Every diagram element has `model_ref`, and every `model_ref` resolves.
- Every diagram relationship has `relationship_ref`, and every `relationship_ref` resolves.
- IDs are unique within their scope.
- Colors match hex format.
- Numeric ranges are valid.

### 11.2 Strict

- Relationship endpoints resolve to model definitions.
- Diagram relationship endpoints can be mapped to visible diagram elements.
- Message lifelines reference `block` or `actor` definitions.
- `subject_ref` on IBD and parametric diagrams resolves to a `block`.
- Ports with `owner_ref` reference model definitions.
- `requirement_table` and `allocation_table` diagrams declare `diagram.table.columns`.
- `allocation_matrix` diagrams declare `diagram.matrix` and include both row and column elements.

### 11.3 Lint

- Font sizes below readable thresholds.
- Relationship endpoints do not land near element boundaries.
- Labels likely overlap.
- Large unused canvas area.
- Missing views for major model definitions.
- Model relationships with no diagram view.

---

## 12. v1.0 Constraints

- JSON only.
- PNG output only.
- No automatic layout.
- No graphical editor.
- No symbolic parametric evaluation.
- No XMI or SysML 2 export.
- No compatibility mode for old `.msml` diagram files.

---

## 13. Example

Model file:

```json
{
  "msml_version": "1.0",
  "model": {
    "id": "example-model",
    "name": "Example",
    "namespace": "Example",
    "definitions": [
      {
        "id": "Example.System",
        "type": "block",
        "name": "System",
        "stereotype": "block"
      },
      {
        "id": "Example.Component",
        "type": "block",
        "name": "Component",
        "stereotype": "block"
      }
    ],
    "relationships": [
      {
        "id": "rel-system-component",
        "type": "composition",
        "source": "Example.System",
        "target": "Example.Component",
        "multiplicity_source": "1",
        "multiplicity_target": "1"
      }
    ],
    "metadata": {
      "author": "Meaningful Systems",
      "created": "2026-05-17",
      "modified": "2026-05-17",
      "tags": ["example"]
    }
  }
}
```

Diagram file:

```json
{
  "msml_version": "1.0",
  "model_files": ["example-model.msml"],
  "diagram": {
    "type": "bdd",
    "id": "bdd-example",
    "name": "Example Definition",
    "context": "Example",
    "frame": { "visible": true, "style": {} },
    "canvas": {
      "width": 600,
      "height": 400,
      "background_color": "#FFFFFF",
      "grid": { "enabled": true, "size": 10, "snap": true }
    },
    "elements": [
      {
        "type": "block",
        "id": "view-system",
        "model_ref": "Example.System",
        "layout": { "x": 200, "y": 40, "width": 200, "height": 80, "z_index": 1 },
        "style": { "fill_color": "#DDEEFF", "border_color": "#336699" }
      },
      {
        "type": "block",
        "id": "view-component",
        "model_ref": "Example.Component",
        "layout": { "x": 200, "y": 220, "width": 200, "height": 80, "z_index": 1 },
        "style": { "fill_color": "#DDEEFF", "border_color": "#336699" }
      }
    ],
    "relationships": [
      {
        "id": "view-rel-system-component",
        "relationship_ref": "rel-system-component",
        "waypoints": [
          { "x": 300, "y": 120 },
          { "x": 300, "y": 220 }
        ],
        "style": {
          "line_color": "#336699",
          "source_arrowhead": "composition",
          "target_arrowhead": "none"
        }
      }
    ],
    "metadata": {
      "author": "Meaningful Systems",
      "created": "2026-05-17",
      "modified": "2026-05-17",
      "tags": ["example"]
    }
  }
}
```

---

## 14. Repository Examples

The `projects/` tree in this repository is the working illustration of MSML v1.0:

- `projects/appliances/toaster` — coverage canary for all twelve SysML 1 views, including `requirement_table`, `allocation_table`, and `allocation_matrix`.
- `projects/appliances/blender` — compact IBD, activity, and state-machine set.
- `projects/e-bike` — street-legal EU-class pedal-assist bike. Namespace `ElectricBike`. File stem `e-bike`. Full view set plus a rider / charger / bike / road context IBD.
- `projects/humanity-optimization` — civilization-scale decision-support concept.

Qualified names and file stems in `projects/e-bike` are frozen. Layout may change; ElectricBike ids do not.
