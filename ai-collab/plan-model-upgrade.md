# Plan: MSML v1.0 Model / Diagram Split

**For:** Human review before implementation  
**Date:** 2026-05-17  
**Status:** Approved for implementation with Andrew's decisions recorded  
**Scope:** `projects/`, `render_msml.py`, `render_all.py`, `README.md`, `msml-specification.md`

This is intentionally scoped as a v1.0 weekend-scale upgrade. The goal is not to design a perfect modeling platform. The goal is to split semantic model content from diagram layout while keeping the renderer simple and keeping the existing examples publishable.

---

## 1. Goal

MSML v1.0 will use two JSON file types:

| Extension | Role | Contains |
|---|---|---|
| `.msml` | Model file | Semantic definitions and semantic relationships. No layout, coordinates, canvas, frame, or visual style. |
| `.msmd` | Diagram file | A visual diagram view: canvas, frame, positioned elements, ports, rendered relationships, waypoints, style, and references to `.msml` model definitions. |

The practical outcome:

- Definitions live once in a model file.
- Diagrams become reusable views of those definitions.
- PNG output should stay visually close to the current output.
- The renderer remains small enough to understand in one file.

**Human decision point 1:** Confirm that `.msml` means "model" and `.msmd` means "diagram" for v1.0, even though this changes the current meaning of `.msml`.

__Andrew's Decision__:yes.  msml is the model file, and there can be multiple model files with nesting.  then .msmd is a diagram file that references a model file.  models don't reference diagrams, but diagrams can use models and defintions from models.  

---

## 2. Design Principles

1. Keep v1.0 simple.
2. Preserve the current visual renderer as much as possible.
3. Keep diagram files self-contained for layout and styling.
4. Move reusable semantic definitions into model files.
5. Fail loudly when a diagram references a missing model definition.
6. Keep this as a v1.0 weekend pass, but make the core direction clean: no compatibility mode for old diagram-style `.msml` files.

This split should make the examples better without turning the project into a full SysML repository implementation.

---

## 3. Proposed File Structure

```text
projects/appliances/toaster/
  toaster-model.msml
  toaster-bdd.msmd
  toaster-ibd.msmd
  toaster-act.msmd
  toaster-seq.msmd
  toaster-stm.msmd
  toaster-uc.msmd
  toaster-req.msmd
  toaster-par.msmd
  toaster-pkg.msmd

projects/humanity-optimization/
  hos-model.msml
  hos-context.msmd
  hos-context-ibd.msmd
  hos-operating-loop.msmd
  hos-decision-support-sequence.msmd
```

Existing PNG files remain next to their diagram sources.

---

## 4. Model File Format (`.msml`)

Top-level structure:

```json
{
  "msml_version": "1.0",
  "model": {
    "id": "hos-model",
    "name": "Humanity Optimization System",
    "namespace": "HOS",
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

### 4.1 Definitions

Every definition has:

- `id`: stable dot-notation model reference, such as `HOS.ScenarioModel`
- `type`: model element type, such as `block`, `requirement`, `state`, `action`
- `name`: human-readable model name
- type-specific semantic fields

Definitions must not include:

- `layout`
- `style`
- `canvas`
- `frame`
- `waypoints`
- diagram-only display labels

Example block:

```json
{
  "id": "HOS.ScenarioModel",
  "type": "block",
  "name": "ScenarioModel",
  "stereotype": "block",
  "compartments": {
    "properties": [
      { "name": "futures", "type": "PossibleFuture", "multiplicity": "*" }
    ],
    "operations": [
      { "name": "simulatePathways", "parameters": [], "return_type": "ScenarioSet" }
    ]
  }
}
```

### 4.2 Model Relationships

Semantic relationships should be available across diagrams. Put these in `model.relationships`:

- BDD structural relationships: `composition`, `aggregation`, `generalization`, `association`, `dependency`
- requirement relationships: `containment`, `derive`, `satisfy`, `verify`, `refine`, `trace`
- state transitions if they represent the actual state machine
- activity control/object flows if they represent the actual behavior model
- package dependencies/imports

Example:

```json
{
  "id": "rel-hos-scenario",
  "type": "composition",
  "source": "HOS.HumanityOptimizationSystem",
  "target": "HOS.ScenarioModel",
  "multiplicity_source": "1",
  "multiplicity_target": "1"
}
```

Diagram files should normally reference semantic relationships with `relationship_ref`. They may carry diagram-only routing, label placement, or rendering overrides, but the relationship meaning belongs in the model.

**Human decision point 2:** Decide how much to move into `model.relationships` in this pass. Initial recommendation was to move only BDD composition/dependency and requirement hierarchy, but this was superseded by Andrew's decision below.

__Andrew's Decision__: no, i want all the sysml v1.x modeling capabilities in the .msml file.  All the relationship types should be possible.  the full msml-specification.md should include all this.  Diagrams should just be views of the model with certain layouts.  

---

## 5. Diagram File Format (`.msmd`)

Top-level structure:

```json
{
  "msml_version": "1.0",
  "model_file": "hos-model.msml",
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

### 5.1 Diagram Elements Referencing Model Definitions

For model-backed elements, the diagram element keeps visual/view information and points to the semantic definition:

```json
{
  "type": "block",
  "id": "block-scenarios",
  "model_ref": "HOS.ScenarioModel",
  "layout": { "x": 310, "y": 330, "width": 220, "height": 135, "z_index": 1 },
  "style": { "fill_color": "#F2ECF8", "border_color": "#6D4C9A" }
}
```

The renderer resolves `model_ref` against the model file and merges the semantic fields before drawing.

### 5.2 Diagram-Local Role and Display Fields

Some diagram elements need labels that are not the same as the model definition name. Keep these in the diagram:

- `role_name`: instance/part/lifeline role, such as `hos`
- `display_name`: diagram-specific label override
- `type_ref`: allowed for v1.0 IBD part labels when a diagram needs an explicit displayed type name

Example IBD part:

```json
{
  "type": "part",
  "id": "part-hos",
  "model_ref": "HOS.HumanityOptimizationSystem",
  "role_name": "hos",
  "layout": { "x": 405, "y": 250, "width": 310, "height": 120, "z_index": 1 },
  "style": { "fill_color": "#EAF2F8", "border_color": "#2E5E87" }
}
```

**Human decision point 3:** Choose whether v1.0 should use `role_name`, `display_name`, both, or simply keep existing `name` fields on view instances. Recommended: use `role_name` for parts/lifelines and `display_name` for any visual override.

__Andrew's Decision__:Sure, follow the recommendation.  

### 5.3 Notation-Only Elements

These can stay entirely in `.msmd` with no `model_ref`:

- `initial_node`
- `initial_pseudostate`
- `activity_final_node`
- `final_state`
- `fork_node`
- `join_node`
- `decision_node`
- `merge_node`
- `execution_occurrence`
- `system_boundary`
- `port`
- `comment`

Ports remain diagram-local in v1.0. Keep `name` and `owner_ref` on ports.

---

## 6. Renderer Changes

### 6.1 Load Model Files

Add:

```python
def load_model(model_path: Path) -> dict:
    """Return {definition_id: definition_dict} from a .msml model file."""
```

If `model.relationships` is used, return both definitions and relationships or a small model object:

```python
{
  "definitions": { "HOS.ScenarioModel": {...} },
  "relationships": [ ... ]
}
```

### 6.2 Accept `.msmd`

`render_msml.py` should accept a diagram file path. If the input has `model_file`, load it relative to the diagram file.

The output file should still default to the same basename with `.png`.

### 6.3 Resolve Elements

Renderer base class gets:

```python
def __init__(self, data: dict, model: dict | None = None):
    self.model = model or {}
```

Add `_resolve(el)`:

```python
def _resolve(self, el: dict) -> dict:
    model_ref = el.get("model_ref")
    if not model_ref:
        return el
    definitions = self.model.get("definitions", self.model)
    if model_ref not in definitions:
        raise KeyError(f"Unresolved model_ref {model_ref!r} in element {el.get('id')!r}")
    return {**definitions[model_ref], **el}
```

Diagram fields override model fields.

### 6.4 Handle Role Labels

At minimum:

- `_draw_part` should prefer `role_name` plus model `name` for `role:Type`.
- `_draw_lifeline` should prefer `display_name`, then `role_name`, then model `name`.
- `_draw_class`, `_draw_package`, `_draw_use_case`, `_draw_actor`, `_draw_state`, `_draw_requirement`, `_draw_action`, and `_draw_block` can use resolved `name`.

**Human decision point 4:** Decide whether to update renderer draw methods for `role_name` now, or keep `name` on diagram elements for v1.0 to reduce renderer changes.

__Andrew's Decision__: what is your recommendation?  

__Codex Recommendation__: update renderer draw methods now. `role_name` and `display_name` keep diagram labels honest without duplicating semantic names in the diagram view.

---

## 7. `render_all.py` Changes

Change it to render diagram files only:

```python
files = sorted(root.rglob("*.msmd"))
```

There is no `.msml` diagram fallback. `.msml` is model-only.

---

## 8. Migration Plan

### 8.1 Humanity Optimization

Create `projects/humanity-optimization/hos-model.msml`.

Definitions to include:

- `HOS.HumanityOptimizationSystem`
- `HOS.EvidenceRepository`
- `HOS.ScenarioModel`
- `HOS.InterventionEvaluator`
- `HOS.EthicalConstraintGuard`
- `HOS.DecisionBriefingInterface`
- `HOS.Humanity`
- `HOS.EarthBiosphere`
- `HOS.FutureGenerations`
- `HOS.DecisionMakers`
- `HOS.TechnologyResources`
- `HOS.EvidenceAndModels`
- `HOS.GovernanceSystem`
- `HOS.Activity.ObserveWorld`
- `HOS.Activity.ModelFutures`
- `HOS.Activity.IdentifyRisks`
- `HOS.Activity.EvaluatePortfolios`
- `HOS.Activity.CheckEthics`
- `HOS.Activity.InformDecisions`

Create `.msmd` diagram files:

- `hos-context.msmd`
- `hos-context-ibd.msmd`
- `hos-operating-loop.msmd`
- `hos-decision-support-sequence.msmd`

### 8.2 Toaster

Create `projects/appliances/toaster/toaster-model.msml`.

Use existing `model_ref` values already present in the toaster diagrams as the first-pass definition IDs.

Create `.msmd` diagram files:

- `toaster-bdd.msmd`
- `toaster-ibd.msmd`
- `toaster-act.msmd`
- `toaster-seq.msmd`
- `toaster-stm.msmd`
- `toaster-uc.msmd`
- `toaster-req.msmd`
- `toaster-par.msmd`
- `toaster-pkg.msmd`

**Human decision point 5:** Decide whether to delete old diagram `.msml` files immediately or keep them for one commit as reference. Initial recommendation was to keep them temporarily, but this was superseded by Andrew's decision below.

__Andrew's Decision__: go ahead and rename them to msmd then edit them to msmd according to the new specification.  

---

## 9. Documentation Updates

Update:

- `msml-specification.md`
- `README.md`
- `projects/humanity-optimization/Humanity_Optimization_Operational_Concept.md`

Required wording changes:

- `.msml` is now the model file format.
- `.msmd` is now the diagram file format.
- PNGs are rendered from `.msmd` files that reference `.msml` model files.
- The repo is still v1.0 because this is the first published weekend version, not a compatibility promise to an installed user base.

**Human decision point 6:** Confirm that keeping `msml_version: "1.0"` is intentional because the project is still pre-release / first-public weekend work.

__Andrew's Decision__: yes.  1.0.  

---

## 10. Testing Checklist

After implementation:

- [x] `python3 render_all.py projects/humanity-optimization` renders 4 HOS PNGs.
- [x] `python3 render_all.py projects/appliances/toaster` renders 9 toaster PNGs.
- [x] HOS BDD names and compartments render from `hos-model.msml`.
- [x] HOS IBD part labels remain readable.
- [x] Toaster requirements text renders from `toaster-model.msml`.
- [x] Toaster state entry/do/exit text renders from `toaster-model.msml`.
- [x] Rendering a `.msmd` with a missing `model_file` fails loudly.
- [x] Rendering a `.msmd` with an unknown `model_ref` fails loudly.
- [x] Rendering a `.msml` model file directly fails loudly.
- [x] Model files contain no `layout`, `style`, `canvas`, `frame`, or `waypoints`.
- [x] No generated/cache files are staged.

---

## 11. Implementation Order

1. Update renderer to load model files and resolve `model_ref`.
2. Update `render_all.py` to render `.msmd` only.
3. Create `hos-model.msml` and migrate HOS diagrams.
4. Render and compare HOS PNGs.
5. Create `toaster-model.msml` and migrate toaster diagrams.
6. Render and compare toaster PNGs.
7. Update docs and blog links.
8. Delete old diagram `.msml` files after successful `.msmd` render verification.
9. Commit.

---

## 12. Things Not To Overbuild Yet

Do not add these in this pass unless a human explicitly decides otherwise:

- full schema validator
- XMI export
- SysML 2 textual export
- automatic layout
- multi-model imports
- package namespace resolver
- symbolic parametric solver
- model relationship renderer that automatically lays out relationship views

The point of this pass is one clean split: semantic definitions in `.msml`, diagram views in `.msmd`, PNGs still rendering.
