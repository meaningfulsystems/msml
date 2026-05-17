# Decisions: Codex Feedback on Toaster MSML Model

Source: `projects/appliances/toaster/codex-feedback-toaster.md`  
Date: 2026-05-17  
Scope: `msml-specification.md` and all nine toaster diagrams

Status note: this decision log predates the v1.0 model/view split implementation. File references below have been updated to current extensions where they describe active files: `.msml` for semantic models and `.msmd` for diagram views.

Each item is marked **Accept**, **Accept (Defer)**, **Accept (Modified)**, or **Reject**, followed by rationale and any action.

---

## MSML Language Decisions

### L1 — JSON/YAML contradiction in the spec
**ACCEPT**

The requirements doc still has leftover YAML references in the Python module table and serializer section. JSON is the correct and intended format. This is a documentation error, not a design question.

**Action:** Audit `msml-specification.md` and replace all remaining YAML references with JSON. Remove `PyYAML`/`ruamel.yaml` from module descriptions. Make `msml.serializer` write JSON.

---

### L2 — Diagram type names: long vs. abbreviation
**ACCEPT (MODIFIED)**

Codex is right that the spec conflates the canonical `type` enum with frame abbreviations. The current file `type` field correctly uses long canonical names (`activity`, `state_machine`, etc.). The file naming convention (`toaster-act.msmd`, `toaster-seq.msmd`) rightly uses abbreviations. These are different concerns and should not share a namespace.

**Decision:**
- `diagram.type` field: always the canonical long name (`activity`, `sequence`, `state_machine`, `use_case`, `requirement`, `parametric`, `package`, `bdd`, `ibd`). `bdd` and `ibd` are already accepted abbreviations in SysML and remain unchanged.
- Frame header abbreviation (`act`, `sd`, etc.): renderer-computed from `DIAGRAM_ABBREV` map, never authored.
- File naming: use the SysML standard abbreviation (short form). This is a convention, not a schema field.

**Action:** Document this three-layer separation in the spec. No schema change required; the current design already follows it.

---

### L3 — Arrowhead fields: `arrowhead` vs. `source_arrowhead`/`target_arrowhead`
**ACCEPT**

Two different field names exist across the spec. `source_arrowhead` and `target_arrowhead` are the correct canonical form since every edge has two ends. The single `arrowhead` shorthand is ambiguous.

**Decision:** All relationship styles use `source_arrowhead` and `target_arrowhead`. The `arrowhead` field is removed from all schemas. Renderer and validator treat `arrowhead` as an unknown field and warn in strict mode.

**Action:** Remove `arrowhead` from the sequence message style schema. Audit all toaster diagrams for lone `arrowhead` usage and migrate. Update requirements doc section 3.4.

---

### L4 — Explicit coordinates are brittle; add layout helpers
**ACCEPT (DEFER to v1.1)**

Explicit coordinates are the right v1.0 choice for AI-generated diagrams: deterministic, auditable, no hidden layout engine. The brittleness Codex identifies is real but is a second-order problem — it matters when iterating on a model, not when generating a first draft.

**Decision:** Keep mandatory explicit coordinates in v1.0. Add the following lightweight helpers in v1.1:
- `source_anchor: "bottom:5"` notation on waypoints (first/last point computed from formula if present)
- `relative_to` placement hint (informational only, validator checks consistency)
- Linter warning when `width` or `height` is very small relative to content

Reject style-constant reuse at this stage — that belongs in a theme/profile layer.

**Action:** Add v1.1 planning note to requirements section 10.

---

### L5 — Port ownership: add `owner_ref`
**ACCEPT**

IBD ports are currently owned by proximity, which is valid for rendering but breaks validation and cross-diagram referencing. A port that drifts 10px off its element boundary silently changes meaning.

**Decision:** Add optional `owner_ref: "<element_id>"` to port elements. Strict-mode validator requires it. Renderer continues to use explicit coordinates; `owner_ref` is used for semantic checks only (e.g., "port must lie on or adjacent to owner boundary").

**Action:** Add `owner_ref` to IBD port schema in the specification. Update `toaster-ibd.msmd` to include it on all ports. Add validator rule.

---

### L6 — Cross-diagram references: add `model_ref` and `type_ref`
**ACCEPT (DEFER file-relative paths to v1.1)**

The need is real and well-stated: there is currently no machine-checkable link between `req-001`, the block that satisfies it, and the test case that verifies it. However, a full cross-file reference resolver is too large for v1.0.

**Decision (v1.0):** Add two optional fields to element schemas:
- `model_ref: "<namespace>.<path>"` — a stable logical identifier independent of file or diagram (e.g., `"Toaster.HeatingElement"`). String, no resolution in v1.0; reserved for tooling.
- `type_ref: "<element_id>"` — reference to a block/classifier within the same file. Already partially in use in IBD parts (`"type_ref": "HeatingElement"`).

**Decision (v1.1):** File-relative `type_ref` in the form `"toaster-bdd.msmd#block-element"`. Validator resolves cross-file references when `--strict` is active.

**Action:** Document `model_ref` as a string metadata field on all elements. Expand `type_ref` definition. Update toaster IBD parts to use `type_ref` pointing to BDD block IDs. Defer cross-file resolution.

---

### L7 — Style repetition: add named style presets
**REJECT for v1.0 — REVISIT in v2.0**

Named style presets would reduce file size and noise, but they add a style-resolution layer that complicates the one-diagram-per-file principle. In v1.0, self-contained files are a feature: any file can be rendered in isolation without external dependencies.

**Decision:** Keep fully expanded style blocks in every element. Accept the verbosity. If AI generation is the primary author, style repetition is not a human authoring burden — it is only a token cost.

Revisit when multi-diagram models or shared profile files are introduced in v2.0.

---

### L8 — Semantic validation: add lint mode
**ACCEPT**

The current validator is syntax-only. Codex correctly identifies that semantic drift between diagrams (a block in BDD not appearing in IBD, a requirement with no satisfy link, a sequence message referencing a lifeline that does not exist) is the class of error that matters most for model quality.

**Decision:** Split validation into three modes:
- `schema` — current behavior: JSON structure, required fields, color format, ID uniqueness, `id_ref` resolution within file.
- `strict` — schema plus: unknown fields are errors, `owner_ref` required on ports, `type_ref` must resolve within file, message lifeline IDs must exist.
- `lint` — strict plus warnings: font size below 9pt, canvas over 80% empty, label likely overlapping an element, relationship endpoints not landing on element boundary (within 5px tolerance), monotonic message Y ordering in sequence diagrams, all BDD blocks referenced by at least one IBD `type_ref`.

Lint warnings do not block rendering.

**Action:** Add lint mode specification to requirements section 5.4. Implement in `msml.validator`.

---

## Toaster Model Decisions

### T1 — Requirements are too sparse
**ACCEPT (DEFER full expansion)**

Five requirements are demonstrably insufficient for a real appliance. The feedback is correct. However, expanding to a full requirements model for a toaster is a scope decision for the next toaster model iteration, not a language change.

**Decision:** Keep the current five requirements as a minimal working example. Create `toaster-req-v2.msmd` in a follow-up that adds:
- Safety group (electrical insulation, surface temperature, crumb tray, regulatory reference)
- User controls group (cancel, browning repeatability, indicator feedback)
- Verification links: `satisfy` from BDD blocks, `verify` from test cases

**Action:** Add `toaster-req-v2.msmd` to the backlog. No change to current files.

---

### T2 — Safety behavior inconsistent across diagrams
**ACCEPT**

This is the most substantive modeling critique. `REQ-002` claims automatic shutdown, but the `Error` state only sounds an alarm and has no explicit deactivation or latch release. The activity and sequence diagrams have no overheat path.

**Decision:**
- Add `deactivate_element(); release_latch()` to the `Error` state entry action in `toaster-stm.msmd`.
- Add a `ThermalCutoff` component to BDD and IBD (minimum: new block, connection from `HeatingElement` to `ThermalCutoff`, connection from `ThermalCutoff` to `Toaster` controller).
- Add an overheat alternative fragment to the sequence diagram in a v2 pass.
- Activity diagram: add an interrupt edge from `Heat Element` to a `Shutdown` action.

**Action:** Update `toaster-stm.msmd` entry action now. Flag BDD/IBD/sequence/activity toaster model updates for next iteration.

---

### T3 — Missing architecture components
**ACCEPT (MODIFIED)**

Adding every real toaster component at once would make the example unwieldy. Accept the critique directionally and add the highest-signal missing parts.

**Decision:** Add to the next BDD/IBD iteration:
- `ThermalCutoff` (required — closes the safety gap in T2)
- `BrowningControl` (required — connects Timer browning level to user intent)
- `PowerInterface` (value type — makes the parametric model coherent)

Defer to v2 toaster model:
- Housing, crumb tray, bread slots (mechanical detail, low modeling value for current exercises)
- Latch/electromagnet (mechanical, relevant only when IBD has richer connector semantics)
- Indicator/audible signal (peripheral to the core behavioral model)

---

### T4 — Cross-diagram naming inconsistencies
**ACCEPT**

`HeatingElement`, `element:HeatingElement`, and `:HeatingElement` all refer to the same thing. Once `model_ref` is added (L6), these can be linked. For now the naming should at least be consistent.

**Decision:** Establish a canonical name table for the toaster model:

| Concept | BDD id | IBD id | Sequence lifeline | model_ref |
|---|---|---|---|---|
| Heating element | `block-element` | `part-element` | `ll-element` | `Toaster.HeatingElement` |
| Timer | `block-timer` | `part-timer` | `ll-timer` | `Toaster.Timer` |
| Carriage | `block-carriage` | `part-carriage` | — | `Toaster.Carriage` |
| Lever | `block-lever` | `part-lever` | — | `Toaster.Lever` |

**Action:** Add `model_ref` to all matching elements in the nine toaster files. Normalize display names to match the BDD block names (e.g., sequence lifeline names use the BDD `name` field value).

---

### T5 — SysML semantics simplified or misleading
**ACCEPT (MODIFIED)**

Accept the substance; push back on scope for the current example files.

Specific decisions:
- **Power Grid actor**: Reject removing it — it is pedagogically useful to show an external power actor, even if purists would model it differently. Add a comment noting it represents an external dependency, not a goal-seeking actor.
- **IBD heat connector (element→carriage)**: Accept the critique. Rename the port to `heatSignal` and document it as a control signal triggering carriage release, not a thermal connection to bread.
- **Activity fork/join semantics**: Accept. The fork/join is misleading. Replace with an interruptible region or event-receive edge in the v2 activity diagram. Keep current v1 as a structural demo.
- **Sequence missing cancel/overheat**: Accept. Flag for v2 sequence diagram with `alt` combined fragment.
- **BDD composition diamond placement**: This is a renderer issue, not a model issue. See T7.

---

### T6 — Parametric model underdeveloped
**ACCEPT (DEFER)**

`P = V×I` and `Q = P×t` are minimal but correct starting points. The full thermal model (resistance, efficiency, heat capacity, cutoff temperature) is the right next step but is a content expansion, not a language fix.

**Decision:** Add `toaster-par-v2.msmd` to the backlog with:
- `P = V² / R` constraint (introduces resistance value property)
- `Q_bread = η × Q_total` (efficiency factor)
- `ΔT = Q / (m × c)` (temperature rise of bread)
- `T_surface < T_cutoff` (safety constraint, links to REQ-002)
- Binding connectors from value properties to REQ-002 verification

---

### T7 — Rendered diagram issues
**ACCEPT (MODIFIED)**

Some are renderer bugs, some are layout issues in the `.msml` files, and some are linter rules.

| Issue | Type | Decision |
|---|---|---|
| Derive line overlaps center req | Layout in `.msmd` | Move derive line waypoints to avoid overlap |
| BDD diamonds stack tightly | Renderer | Reduce diamond size; increase spacing in BDD layout |
| Multiplicity labels not visible | Renderer | Add multiplicity label rendering to `_draw_relationship` |
| Sequence labels small/cramped | Layout | Increase canvas width; spread lifelines |
| STM transition labels small | Layout | Acceptable for v1; increase font to 11pt in v2 |
| IBD port labels tiny | Renderer | Increase port label font to 9pt minimum |
| Package diagram mostly empty | Layout | Reduce canvas; tighten layout |

**Action (immediate):** Fix multiplicity label rendering in BDD. Fix port label font size in IBD. Fix derive line routing in requirements diagram.

**Action (lint rule):** Add lint warning when relationship label text overlaps an element boundary box, and when canvas utilization is below 40%.

---

## Implementation Status (completed 2026-05-17)

| Item | Status | Notes |
|---|---|---|
| L1 — JSON/YAML spec fix | ✅ Done | Specification updated |
| L2 — Type naming doc | ✅ Done | Section 2.7 added to requirements |
| L3 — Arrowhead normalization | ✅ Done | Sequence message and STM transition schemas fixed |
| L4 — Layout helpers | ✅ Deferred v1.1 | Note in requirements section 10 |
| L5 — Port owner_ref | ✅ Done | IBD schema + all toaster-ibd ports have owner_ref |
| L6 — model_ref / type_ref | ✅ Done | Section 2.8 added; all 9 toaster files have model_ref |
| L7 — Style presets | ✅ Rejected | Rationale documented |
| L8 — Lint mode | ✅ Done | Three-mode spec (schema/strict/lint) in section 5.4 |
| T1 — Expand requirements | ✅ Done | 10 requirements across 3 groups (functional, safety, controls) |
| T2 — Safety consistency | ✅ Done | STM Error entry: deactivate_element(); release_latch(); sound_alarm() |
| T3 — Missing architecture | ✅ Done | ThermalCutoff + BrowningControl added to BDD with associations |
| T4 — Naming consistency | ✅ Done | model_ref on all elements; canonical name table defined |
| T5 — SysML semantics | ✅ Done | heatSignal rename; Power Grid actor retained with note |
| T6 — Parametric depth | ✅ Done | P=V²/R, Q=P×t, Q_b=η×Q, T_elem<T_cutoff constraints added |
| T7 — Render issues | ✅ Done | Multiplicity labels, port font size, derive waypoints fixed |

## Open Questions for Human Decision

### OQ-1: Activity diagram fork/join semantics
The current `toaster-act.msmd` uses a fork/join to show `Start Timer` and `Heat Element` running concurrently, then joining before `Pop Carriage`. This is semantically misleading — heating is controlled until timer expiration, not a fixed-duration parallel branch.

**Options:**
- **A)** Replace fork/join with an `interruptible_region` element wrapping `Heat Element`, interrupted by a timer-expired event — correct SysML construct, requires new renderer element type
- **B)** Add a decision-node loop: Heat Element loops back until a `timerExpired` event, then exits to Pop Carriage
- **C)** Keep current structure as a simplified structural demo; add a `comment` element documenting the simplification
- **D)** Redesign as a single `Toast` action; detailed concurrency lives in IBD and STM only

**Recommendation:** A if the activity diagram should be semantically correct; C if it is a renderer exercise only.

### OQ-2: Sequence diagram — cancel and overheat alternate flows
The current `toaster-seq.msmd` shows only the happy path. Codex recommends adding cancel and overheat alternates.

**Options:**
- **A)** Add a `combined_fragment` of kind `alt` to the existing file — requires implementing `combined_fragment` rendering in `SequenceRenderer`
- **B)** Create a second file `toaster-seq-safety.msmd` for the overheat/cancel path — no renderer changes needed, just a new diagram
- **C)** Leave as-is; safety behavior is fully covered by the STM

**Recommendation:** B — a second sequence file for the safety scenario is the cleanest split and avoids scope-creeping the renderer now.
