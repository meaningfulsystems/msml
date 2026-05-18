# MSML v1.0 Implementation Plan — Post-Review Pass

**Date:** 2026-05-17 21:13  
**Author:** Claude (Anthropic)  
**For:** Codex implementation  
**Source decisions:** `claude-feedback-20260517-2053.md` with Andrew and Codex responses  
**Status:** Codex-reviewed draft — Andrew resolved HD1/HD4 toward complete `.msml` model source of truth  

---

## 0. Scope Summary

This plan covers 5 phases of work resulting from the three-way feedback round (Claude review → Codex + Andrew responses). All 13 diagrams currently render correctly. The goal of this pass is correctness and completeness — not new features.

**Codex review note:** Andrew's comments resolve the model/view boundary: `.msml` is the source of truth, and `.msmd` is a view. The plan below has been adjusted away from diagram-local notation mechanics and toward complete model-backed diagrams.

| Phase | Area | Files changed |
|---|---|---|
| 1 | Specification | `msml-specification.md` |
| 2 | Model files | `toaster-model.msml`, `hos-model.msml` |
| 3 | Diagram files | All 13 `.msmd` files |
| 4 | Renderer | `render_msml.py` |
| 5 | Lightweight validator | `msml_validate.py` (new file) |

**Activity flow audit result:** The previous audit is superseded by Andrew's decision. Inline activity flows touching initial/final/fork/join/decision/merge nodes must be moved into the model by adding model definitions for those nodes and model relationships for those flows.

---

## 0.1 Resolved Model/View Decision

### C1 — "Complete model" does not necessarily mean "every drawn notation node is a model definition"

Andrew asked:

> are we supposed to be able to have something in a diagram that is not in the model itself? I think the model needs to be complete and a source of truth, then the .msmd files reference and visualize that truth.

Original Codex recommendation:

- The `.msml` model should be complete for **system semantics**: blocks, actors, requirements, actions, states, constraints, value properties, and semantic relationships.
- The `.msmd` diagram may still contain **notation-only view mechanics**: initial node, final node, fork, join, decision diamond, merge, execution occurrence, visual comments, and ports if ports remain view-local in v1.0.
- If Andrew wants absolutely every visible thing represented in `.msml`, then the spec must add semantic definition types for initial nodes, final nodes, forks, joins, decisions, merges, execution occurrences, and ports. That is a larger modeling-language decision and should not be treated as a small cleanup.

___Andrew:___ This is a very important decision.  Thank you Codex for resurfacing it.  if the diagram file .msmd is a view of the model, then it needs all these connections in the .msml model file.  The diagrams can be recreated with a working .msml model file.  that is why i think there should be the possibility of .msml files referencing a parent .msml file so the whole thing isn't a 100k line file.  example: earth as a system is a single .msml file, but oceans.msml references earth.msml.  Then pacific-ocean.msml can reference oceans.msml.  etc.  

___Codex Implementation Interpretation:___ Andrew chose a complete model source of truth. For this pass, every diagram element that represents model topology, behavior, interaction, requirement structure, parametric structure, package structure, or notation needed to recreate a diagram should have a `model_ref`. Every diagram relationship should have a `relationship_ref`. `.msmd` should retain layout, routing, canvas, frame, and style only.

The existing `model.imports` mechanism already supports Andrew's parent/child model example. The spec should clarify that a child model may import a parent model, e.g. `pacific-ocean.msml` imports `oceans.msml`, which imports `earth.msml`.

### C2 — Activity-flow options, expanded

Andrew asked for elaboration on HD4. These are the real options:

**Option A — Semantic-only model flows.**  
Only flows between semantic action definitions live in `.msml`. Flows involving initial/final/fork/join/decision/merge nodes stay in `.msmd` because those nodes are diagram notation. This keeps v1.0 simple and matches Claude/Codex's initial recommendation.

**Option B — Complete activity graph in model.**  
Every activity node and every control/object flow lives in `.msml`, including initial nodes, final nodes, forks, joins, decisions, merges, and guards. `.msmd` only positions those model nodes. This is more semantically complete but requires adding several model definition types and converting existing activity/state diagrams more deeply.

**Option C — Hybrid with explicit rule.**  
Keep v1.0 as Option A, but document that future v1.1/v2 may promote notation-only activity nodes into model definitions when a full executable behavior model is desired.

Original Codex recommendation: choose **Option C** for v1.0. It respects "model as source of truth" for real system semantics without turning this pass into a full activity metamodel implementation.

___Andrew:___Option B.  

___Codex Implementation Interpretation:___ Implement Option B. Add model definition types for activity/control notation nodes and state pseudostates as needed. Convert current diagram-local control flows/transitions into model relationships. The diagrams should only reference and route those model relationships.

---

## Phase 1 — Specification (`msml-specification.md`)

Make the following targeted edits. All section references are to the current file.

### 1.1 — Add inline relationship rule (S1 / HD1)

In **section 8** ("Diagram Relationships"), replace the paragraph beginning "Diagram relationships are view objects…" with:

> Diagram relationships are view objects for model relationships. In v1.0 repository examples, every diagram relationship must use `relationship_ref`. A diagram relationship may carry layout/routing/style fields such as `waypoints`, label offsets, and visual overrides, but the relationship meaning and endpoints live in `.msml`.
>
> Elements that were previously treated as notation-only — `initial_node`, `initial_pseudostate`, `activity_final_node`, `flow_final_node`, `fork_node`, `join_node`, `decision_node`, `merge_node`, `execution_occurrence`, and ports — are model-backed in MSML v1.0. They must have model definitions when they appear in a diagram. This lets a `.msmd` diagram be recreated from a working `.msml` model plus view layout.

### 1.1a — Add model definition types for diagram/control notation

Add a specification subsection covering these model definition types:

- `initial_node`
- `activity_final_node`
- `flow_final_node`
- `fork_node`
- `join_node`
- `decision_node`
- `merge_node`
- `initial_pseudostate`
- `final_state`
- `execution_occurrence`
- `port`
- `comment` or `annotation` if comments are intended to be reusable model annotations

Minimum common fields: `id`, `type`, `name`. Type-specific fields:

- `port`: `owner_ref`, `direction`, `interface_ref` or `item_type` when known
- `decision_node` / `merge_node`: optional `decision_input`
- `execution_occurrence`: optional `lifeline_ref`, `start_event_ref`, `finish_event_ref`
- `comment` / `annotation`: `body`, optional `annotated_refs`

These definitions are intentionally lightweight. They exist so the model graph can recreate the diagram topology without carrying layout.

### 1.1b — Clarify model imports / parent model references

In section 3.2, clarify that `model.imports` supports hierarchical source-of-truth models:

> A model may import parent or shared models. For example, `pacific-ocean.msml` may import `oceans.msml`, and `oceans.msml` may import `earth.msml`. Imported definitions and relationships are part of the loaded model graph for validation and rendering. Model files still do not reference diagrams.

### 1.2 — Unify to `model_files` (S2 / HD2)

In **section 6.1** ("Top-Level Structure"), remove the `model_file` single-string form entirely. The only valid field is `model_files` (always a JSON array):

```json
{
  "msml_version": "1.0",
  "model_files": ["hos-model.msml"],
  "diagram": { ... }
}
```

Replace the paragraph about both forms with:

> `model_files` is a JSON array of relative paths to `.msml` model files. It must always be an array, even when referencing a single model. The singular `model_file` field is not valid.

### 1.3 — Update renderer and validator fail-loud language (S3 / HD7)

In **section 2** and **section 10**, replace the existing "fails loudly" statements with:

> - Rendering a `.msml` model file directly is a hard error. Use `.msmd` diagram files with the renderer.
> - A missing or unresolvable file in `model_files` is always a hard error.
> - A `model_ref` or `relationship_ref` that does not resolve to a definition in the loaded model graph is always a hard error.
> - A model-mandatory element (type: `block`, `state`, `requirement`, `use_case`, `actor`, `action`, `constraint_property`, `value_property`, `part`, `lifeline`, `package`, `model`, `class`) that lacks `model_ref` is a validator strict-mode error and a lint-mode warning.
> - Renderer errors should include source file path, element or relationship `id` when applicable, field name, and a short rule code.
> - Validator errors must include source file path, element or relationship `id` when applicable, field name, and the rule code from the validator.

### 1.4 — Add lifeline classifier rule (S4)

In **section 5.2** ("Message Relationships"), add after the field table:

> `source_lifeline` and `target_lifeline` must reference a model definition of type `block` or `actor`. Referencing a definition of any other type is a strict-mode error.

### 1.5 — Rename `constraint` to `constraint_property` in spec (S5)

In **section 4.7**, change the definition type from `constraint` to `constraint_property` everywhere:

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

Update the section header to read "4.7 Constraint Property" and update all mentions of `constraint` type in that section.

### 1.6 — Add `subject_ref` field (S6 / HD6)

Add a new subsection in **section 6** after 6.2 ("Diagram Types"):

> **6.3 — Subject Reference**
>
> IBD and parametric diagrams should declare the model element whose interior or parametric context is being shown. Use the optional `subject_ref` field at `diagram.subject_ref`:
>
> ```json
> {
>   "diagram": {
>     "type": "ibd",
>     "subject_ref": "Toaster",
>     ...
>   }
> }
> ```
>
> `subject_ref` must resolve to a `block` definition in the loaded model. The renderer ignores it. The validator uses it in strict mode to confirm that the diagram subject exists and, in a future richer model, that `part` elements are valid parts of the subject block.

Renumber the remaining subsections (current 6.3 Canvas becomes 6.4, etc.).

### 1.7 — Document relationship ID convention (R3)

In **section 5** ("Model Relationships"), add after the uniqueness rule:

> **Recommended ID convention:** prefix relationship IDs with the diagram ID where they were first defined, separated by a dot. This prevents collisions when multiple diagrams share a model. Example: `bdd-toaster.comp-heating-element`, `sd-toaster.m1`, `stm-toaster.t-idle-toasting`.

### 1.8 — Update the example at the bottom of the spec (section 13)

Change `"model_file"` to `"model_files": ["example-model.msml"]` in the example diagram file.

---

## Phase 2 — Model Files

### 2.1 — `toaster-model.msml`: add PAR definitions (M1 / HD3)

Add the following 8 definitions to `model.definitions`. Insert them in alphabetical order by `id` alongside existing definitions.

**Four constraint_property definitions:**

```json
{
  "id": "Toaster.PAR.BreadHeat",
  "type": "constraint_property",
  "name": "Q_b = η × Q",
  "expression": "Q_b = eta * Q",
  "parameters": [
    { "name": "η", "type": "Real" },
    { "name": "Q", "type": "Real" },
    { "name": "Q_b", "type": "Real" }
  ]
},
{
  "id": "Toaster.PAR.Energy",
  "type": "constraint_property",
  "name": "Q = P × t",
  "expression": "Q = P * t",
  "parameters": [
    { "name": "P", "type": "Real" },
    { "name": "t", "type": "Real" },
    { "name": "Q", "type": "Real" }
  ]
},
{
  "id": "Toaster.PAR.PV2R",
  "type": "constraint_property",
  "name": "P = V² / R",
  "expression": "P = V**2 / R",
  "parameters": [
    { "name": "V", "type": "Real" },
    { "name": "R", "type": "Real" },
    { "name": "P", "type": "Real" }
  ]
},
{
  "id": "Toaster.PAR.SafetyCheck",
  "type": "constraint_property",
  "name": "T_elem < T_cutoff",
  "expression": "T_elem < T_cutoff",
  "parameters": [
    { "name": "T_elem", "type": "Real" },
    { "name": "T_cutoff", "type": "Real" }
  ]
}
```

**Four value_property definitions:**

```json
{
  "id": "Toaster.PAR.breadHeat",
  "type": "value_property",
  "name": "breadHeat: J",
  "value_type": "Real",
  "unit": "J"
},
{
  "id": "Toaster.PAR.efficiency",
  "type": "value_property",
  "name": "efficiency: η",
  "value_type": "Real",
  "unit": "dimensionless"
},
{
  "id": "Toaster.PAR.elemTemp",
  "type": "value_property",
  "name": "elemTemp: °C",
  "value_type": "Real",
  "unit": "degC"
},
{
  "id": "Toaster.PAR.totalHeat",
  "type": "value_property",
  "name": "totalHeat: J",
  "value_type": "Real",
  "unit": "J"
}
```

### 2.2 — `toaster-model.msml`: remove duplicate User block (M4 / HD5)

Remove the definition with `"id": "Toaster.User"` and `"type": "block"` from `model.definitions`. `Toaster.Actor.User` already exists as an actor definition and is the canonical reference.

Also remove `Toaster.User` from the `source_lifeline` / `target_lifeline` fields of message relationships in `model.relationships` — change `sd-toaster.m1` source_lifeline from `Toaster.User` to `Toaster.Actor.User`, and `sd-toaster.m6` target_lifeline from `Toaster.User` to `Toaster.Actor.User`.

### 2.3 — `hos-model.msml`: fix 5 camelCase names to PascalCase (M3)

Change the `name` field (not the `id`) for these five definitions:

| `id` | Current `name` | Corrected `name` |
|---|---|---|
| `HOS.DecisionMakers` | `decisionMakers` | `DecisionMakers` |
| `HOS.EarthBiosphere` | `earthBiosphere` | `EarthBiosphere` |
| `HOS.FutureGenerations` | `futureGenerations` | `FutureGenerations` |
| `HOS.Humanity` | `humanity` | `Humanity` |
| `HOS.TechnologyResources` | `technologyResources` | `TechnologyResources` |

Do not change the `id` field of any definition — IDs are stable.

### 2.4 — Add model definitions for all current diagram-only elements (C1/C2)

Audit all 13 `.msmd` files for elements without `model_ref`. Add corresponding definitions to the relevant `.msml` model file, then add `model_ref` to the diagram element.

This includes, at minimum:

- Activity diagram nodes: initial nodes, final nodes, forks, joins, decisions, merges.
- State machine pseudostates/final states.
- Sequence execution occurrences.
- IBD ports.
- Any comments/annotations that should survive model-based diagram regeneration.

Definition ID convention:

- Toaster activity nodes: `Toaster.ACT.<NameOrNodeId>`
- Toaster state pseudostates: `Toaster.STM.<NameOrNodeId>`
- Toaster ports: `Toaster.IBD.<Owner>.<PortName>`
- Toaster sequence execution occurrences: `Toaster.SEQ.<Lifeline>.<OccurrenceName>`
- HOS activity nodes: `HOS.Activity.<NameOrNodeId>`
- HOS context ports: `HOS.IBD.<Owner>.<PortName>`

Keep definitions lightweight and semantic. Do not put layout, style, waypoints, canvas, or frame data in `.msml`.

### 2.5 — Add model relationships for every current inline diagram relationship (C1/C2)

Audit all 13 `.msmd` files for relationships without `relationship_ref`. Add corresponding relationships to `model.relationships`, then update each diagram relationship with `relationship_ref`.

This includes:

- Activity control/object flows involving initial/final/fork/join/decision/merge nodes.
- State transitions involving initial pseudostates or final states.
- IBD connectors between ports.
- Parametric binding connectors.
- Any remaining use case, package, requirement, sequence, BDD, or HOS relationships that are still inline.

After this phase, current repository examples should have zero diagram relationships without `relationship_ref`.

---

## Phase 3 — Diagram Files

### 3.1 — All 13 `.msmd` files: `model_file` → `model_files` (HD2)

In every `.msmd` file, replace:
```json
"model_file": "xxx-model.msml"
```
with:
```json
"model_files": ["xxx-model.msml"]
```

Files to update (all 13):
- `projects/appliances/toaster/toaster-act.msmd`
- `projects/appliances/toaster/toaster-bdd.msmd`
- `projects/appliances/toaster/toaster-ibd.msmd`
- `projects/appliances/toaster/toaster-par.msmd`
- `projects/appliances/toaster/toaster-pkg.msmd`
- `projects/appliances/toaster/toaster-req.msmd`
- `projects/appliances/toaster/toaster-seq.msmd`
- `projects/appliances/toaster/toaster-stm.msmd`
- `projects/appliances/toaster/toaster-uc.msmd`
- `projects/humanity-optimization/hos-context.msmd`
- `projects/humanity-optimization/hos-context-ibd.msmd`
- `projects/humanity-optimization/hos-decision-support-sequence.msmd`
- `projects/humanity-optimization/hos-operating-loop.msmd`

### 3.2 — `toaster-par.msmd`: add model_refs to 8 orphaned elements (M1 / HD3)

Update these 8 elements in `diagram.elements` to add `model_ref`:

| element `id` | Add `model_ref` |
|---|---|
| `cp-ohms` | `"Toaster.PAR.PV2R"` |
| `cp-energy` | `"Toaster.PAR.Energy"` |
| `cp-bread-heat` | `"Toaster.PAR.BreadHeat"` |
| `cp-safety` | `"Toaster.PAR.SafetyCheck"` |
| `vp-heat-total` | `"Toaster.PAR.totalHeat"` |
| `vp-efficiency` | `"Toaster.PAR.efficiency"` |
| `vp-heat-bread` | `"Toaster.PAR.breadHeat"` |
| `vp-elem-temp` | `"Toaster.PAR.elemTemp"` |

### 3.3 — `toaster-seq.msmd`: update ll-user model_ref (M4 / HD5)

Change the `model_ref` on element `ll-user` from `"Toaster.User"` to `"Toaster.Actor.User"`.

### 3.4 — Add `subject_ref` to IBD and parametric diagrams (S6 / HD6)

Add `"subject_ref": "<model_ref>"` inside the `diagram` object of these files:

| File | `subject_ref` value |
|---|---|
| `toaster-ibd.msmd` | `"Toaster"` |
| `toaster-par.msmd` | `"Toaster"` |
| `hos-context-ibd.msmd` | `"HOS.HumanityOptimizationSystem"` |

Example placement (inside `diagram`, alongside `type`, `id`, `name`):
```json
{
  "diagram": {
    "type": "ibd",
    "id": "ibd-toaster",
    "subject_ref": "Toaster",
    "name": "Toaster Internal Structure",
    ...
  }
}
```

### 3.5 — Add `model_ref` to all remaining diagram elements (C1/C2)

After Phase 2.4 creates definitions, update every diagram element that lacks `model_ref`.

Target end state for repository examples:

- Every object in `diagram.elements[]` has `model_ref`.
- The only top-level diagram content without `model_ref` is non-element view data: frame, canvas, layout, style, and metadata.

### 3.6 — Add `relationship_ref` to all remaining diagram relationships (C1/C2)

After Phase 2.5 creates model relationships, update every diagram relationship that lacks `relationship_ref`.

Target end state for repository examples:

- Every object in `diagram.relationships[]` has `relationship_ref`.
- Diagram relationships keep only view-level routing and style fields plus the `relationship_ref`.

---

## Phase 4 — Renderer (`render_msml.py`)

### 4.1 — Only accept `model_files`, not `model_file` (HD2)

In the `render()` function and any model-loading code, remove all handling of `data.get("model_file")`. Only read `data.get("model_files", [])`. If `model_file` (singular) is present, raise a clear error:

```
ERROR: 'model_file' is not a valid field. Use 'model_files' (array). See MSML spec section 6.1.
```

and exit with a non-zero code from the CLI. Keep the Python `render()` function library-friendly by raising `ValueError` rather than calling `sys.exit()` directly inside `render()`.

### 4.2 — Reject `.msml` files at render entry point (R2)

At the top of `render()`, before loading JSON, add a clear `.msml` rejection. Prefer raising `ValueError` in `render()` and catching it in `main()` so direct function callers also get a useful exception:

```python
if Path(src).suffix == ".msml":
    raise ValueError(
        f"MSML-RENDER-001: {src} is a model file (.msml). "
        "The renderer only accepts diagram files (.msmd)."
    )
```

### 4.3 — Hard-error on missing or unresolved `model_ref` / `relationship_ref` (S3 / HD7 / C1)

When a diagram element has `model_ref` set and it does not resolve in the loaded model, raise immediately with:

```
ERROR: toaster-bdd.msmd  element[block-toaster]  model_ref='Toaster'  not found in model
       Rule: MSML-SCHEMA-005 — every model_ref must resolve to a model definition
```

When a diagram relationship has `relationship_ref` set and it does not resolve, raise with a similar message.

Because Andrew decided `.msmd` is a complete view of `.msml`, missing `model_ref` on any diagram element and missing `relationship_ref` on any diagram relationship should also be renderer errors in the repository's v1.0 format. Use the same clear file/scope/rule-code style as unresolved references.

### 4.4 — Confirm `role_name` and `display_name` rendering (R1)

Verify the `_resolve_element()` method applies these label rules in order:
1. If `display_name` present → use it as the rendered name
2. Else if `role_name` present on a `part` element → render as `role_name:ModelDefinitionName`
3. Else if `role_name` present on a `lifeline` element → render as `role_name`
4. Else → use the model definition's `name` field

After implementation, render `toaster-ibd.png` and `hos-context-ibd.png` and confirm part labels show `lever:Lever`, `timer:Timer`, `element:HeatingElement`, `carriage:Carriage` (or similar `role_name:DefinitionName` format). Record the observation in the session log; do not embed or copy PNG binaries into the session file.

---

## Phase 5 — New Validator (`msml_validate.py`)

Create a new file `msml_validate.py` at the project root.

### 5.1 — CLI interface

```
python3 msml_validate.py <file.msmd|file.msml> [--strict] [--lint]
```

- Default (no flags): schema mode
- `--strict`: schema + strict checks
- `--lint`: schema + strict + lint checks
- Exit code 0 = no errors (warnings in lint mode do not fail)
- Exit code 1 = one or more errors

### 5.2 — Error output format

Every error or warning must include:
```
LEVEL  filename  scope  rule-code: message
```

Where:
- `LEVEL` is `ERROR`, `WARN`, or `INFO`
- `filename` is the file path relative to the working directory
- `scope` is `element[id]`, `relationship[id]`, `model`, or `file`
- `rule-code` is a stable identifier (see 5.4)
- `message` is a human-readable description

Example output:
```
ERROR  projects/appliances/toaster/toaster-par.msmd  element[cp-ohms]  MSML-SCHEMA-005: model_ref missing; element type 'constraint_property' requires a model_ref
ERROR  projects/appliances/toaster/toaster-par.msmd  element[vp-heat-total]  MSML-SCHEMA-005: model_ref missing; element type 'value_property' requires a model_ref
WARN   projects/appliances/toaster/toaster-bdd.msmd  element[block-element]  MSML-LINT-003: relationship endpoint may not land on element boundary (check waypoints)

2 errors, 1 warning.
```

### 5.3 — Validation modes

**Schema mode (always runs):**
- JSON is valid and parseable
- Top-level shape is `.msmd` (`diagram` key) or `.msml` (`model` key)
- `msml_version` is present
- For `.msmd`: `model_files` is present and is an array; each path resolves
- For `.msmd`: `model_file` singular is an error in all modes, because Andrew decided there is no compatibility path
- For `.msmd`: every `model_ref` on any element resolves in the loaded model graph
- For `.msmd`: every `relationship_ref` on any relationship resolves in the loaded model graph
- For `.msmd`: every `diagram.elements[]` object has `model_ref`
- For `.msmd`: every `diagram.relationships[]` object has `relationship_ref`
- Element `id` values are unique within the diagram
- Model definition `id` values are unique within the loaded model graph (across imports)
- Colors match `#RRGGBB` or `#RRGGBBAA`
- `layout.x`, `layout.y`, `layout.width`, `layout.height` present on all diagram elements that render as positioned shapes

**Strict mode (adds these checks):**
- `source_lifeline` and `target_lifeline` in model relationships must reference definitions of type `block` or `actor`
- `subject_ref` in IBD and parametric diagrams must resolve to a `block` definition
- Model-backed notation definitions use valid endpoint/reference fields for their type, such as `port.owner_ref` and `execution_occurrence.lifeline_ref`

**Lint mode (adds these warnings):**
- Font size below 9pt on any element
- Canvas area used by elements < 40% of total canvas area
- Model definitions with no diagram element using them (orphaned definition)
- Model relationships with no `relationship_ref` usage in any diagram

### 5.4 — Rule code table

| Code | Mode | Description |
|---|---|---|
| MSML-SCHEMA-001 | schema | Invalid JSON or unparseable file |
| MSML-SCHEMA-002 | schema | Missing required top-level field (`msml_version`, `model_files`, `diagram` or `model`) |
| MSML-SCHEMA-003 | schema | Invalid color format (not `#RRGGBB` or `#RRGGBBAA`) |
| MSML-SCHEMA-004 | schema | Duplicate element or definition ID |
| MSML-SCHEMA-005 | schema | Missing or unresolvable `model_ref` |
| MSML-SCHEMA-006 | schema | Missing or unresolvable `relationship_ref` |
| MSML-SCHEMA-007 | schema | Missing `model_files` or unresolvable model file path |
| MSML-SCHEMA-008 | schema | Missing layout fields on non-notation element |
| MSML-SCHEMA-009 | schema | `model_file` (singular) used instead of `model_files` |
| MSML-STRICT-001 | strict | Reserved |
| MSML-STRICT-002 | strict | Reserved |
| MSML-STRICT-003 | strict | Reserved |
| MSML-STRICT-004 | strict | Lifeline typed by non-block/actor definition |
| MSML-STRICT-005 | strict | IBD/parametric `subject_ref` missing or not resolving to a block |
| MSML-LINT-001 | lint | Font size below 9pt |
| MSML-LINT-002 | lint | Canvas utilization below 40% |
| MSML-LINT-003 | lint | Relationship endpoint far from element boundary |
| MSML-LINT-004 | lint | Orphaned model definition (no diagram uses it) |
| MSML-LINT-005 | lint | Orphaned model relationship (no `relationship_ref` in any diagram) |

### 5.5 — Implementation notes

- Reuse `load_model()` from `render_msml.py` (or extract it to a shared utility)
- The validator must not import Pillow — it should run with no dependencies beyond stdlib
- Separate model loading from diagram validation: load all model files first, build a flat definition dict, then validate diagrams against it
- `render_all.py` may optionally call the validator in schema mode before rendering; for now, keep them separate

---

## Testing Checklist

After implementing all phases:

- [ ] `python3 render_all.py projects/` renders all 13 diagrams with exit code 0
- [ ] Visual output of all 13 PNGs is unchanged from pre-pass (compare manually or via pixel diff)
- [ ] `python3 render_msml.py projects/appliances/toaster/toaster-model.msml` prints a clear error and exits 1
- [ ] `python3 msml_validate.py projects/appliances/toaster/toaster-bdd.msmd` exits 0
- [ ] `python3 msml_validate.py projects/appliances/toaster/toaster-bdd.msmd --strict` exits 0
- [ ] `python3 msml_validate.py projects/appliances/toaster/toaster-bdd.msmd --lint` exits 0
- [ ] Temporarily remove a `model_ref` from one element; confirm renderer and validator report MSML-SCHEMA-005
- [ ] Temporarily remove a `relationship_ref` from one relationship; confirm renderer and validator report MSML-SCHEMA-006
- [ ] Temporarily set `model_file` instead of `model_files`; confirm renderer and validator both error on MSML-SCHEMA-009
- [ ] `toaster-ibd.png` part labels show `role_name:DefinitionName` format (confirm R1)
- [ ] `hos-context-ibd.png` part labels are PascalCase (confirm M3 fix is reflected)
- [ ] `toaster-par.msmd` has no elements with missing `model_ref` after the phase 3 update
- [ ] `rg -n '"relationship_ref"' projects/**/*.msmd` count equals the total number of diagram relationships.
- [ ] `rg -n '"model_ref"' projects/**/*.msmd` count equals the total number of diagram elements.

---

## What NOT to Change

- PNG files by hand. If rendering changes a PNG because the source model/diagram changed, commit the regenerated output.
- `render_all.py` logic beyond model_files handling
- A `decisions/` directory; that content now lives under `ai-collab/`.
- Existing `ai-collab/sessions/` files, except append-only updates to the active session log.
- Any `.msmd` relationship waypoints or style fields
- HOS block `id` fields (only `name` fields change in M3)
- The `msml-requirements.md` file (superseded by `msml-specification.md`)
