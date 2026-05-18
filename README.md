# MSML: Meaningful Systems Modeling Language

MSML is a scriptable graphical modeling language for systems modeling. It is inspired by SysML and PlantUML: SysML provides the systems-engineering diagram vocabulary, while PlantUML demonstrates the value of diagrams that can be generated, reviewed, versioned, and rendered from text.

This repository contains:

- the MSML v1.0 specification
- a Python PNG renderer for MSML diagram files
- a lightweight validator for MSML model and diagram files
- example MSML models, diagram views, and rendered diagrams
- early project models for appliances and humanity-scale systems

## Why MSML Exists

MSML is designed for human and AI collaboration on complex system models. The format is JSON. Complete model content lives in `.msml` files: definitions, relationships, behavior topology, ports, control nodes, sequence occurrences, and other model-backed things needed to recreate the diagram structure. Graphical diagram views live in `.msmd` files with explicit visual layout, routing, canvas, frame, and style.

That split is the core v1.0 direction: `.msml` is the source of truth, and `.msmd` is a view of that truth. Diagrams are deterministic, easy to diff, easy to regenerate, and suitable for publication alongside prose.

The current renderer supports the nine SysML 1.x diagram families represented in this repository:

- Block Definition Diagram
- Internal Block Diagram
- Activity Diagram
- Sequence Diagram
- State Machine Diagram
- Use Case Diagram
- Requirements Diagram
- Parametric Diagram
- Package Diagram

## Repository Layout

```text
.
├── msml-specification.md
├── render_msml.py
├── render_all.py
├── msml_validate.py
├── requirements.txt
├── ai-collab/
│   └── ...
└── projects/
    ├── appliances/
    │   └── toaster/
    │       ├── toaster-model.msml
    │       ├── toaster-*.msmd
    │       └── toaster-*.png
    └── humanity-optimization/
        ├── Humanity_Optimization_System_Brief.md
        ├── Humanity_Optimization_Operational_Concept.md
        ├── hos-model.msml
        ├── hos-*.msmd
        └── hos-*.png
```

## Quick Start

Create a virtual environment and install the one runtime dependency:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Render one MSML diagram file:

```bash
python3 render_msml.py projects/humanity-optimization/hos-context.msmd
```

Render all MSML diagram files under a folder:

```bash
python3 render_all.py projects/humanity-optimization
python3 render_all.py projects/appliances/toaster
python3 render_all.py projects
```

The renderer writes PNG files next to their `.msmd` sources. `.msml` model files are loaded by the diagram files and are not rendered directly. Rendering a `.msml` file directly is an error.

Validate one model or diagram file:

```bash
python3 msml_validate.py projects/appliances/toaster/toaster-bdd.msmd
python3 msml_validate.py projects/appliances/toaster/toaster-bdd.msmd --strict
python3 msml_validate.py projects/appliances/toaster/toaster-bdd.msmd --lint
```

`render_all.py` does not run `msml_validate.py` first. The renderer performs the checks needed to render safely, including rejecting singular `model_file`, missing `model_files`, missing `model_ref`, and missing `relationship_ref`. Use `msml_validate.py` when you want an explicit validation pass.

## File Model

MSML v1.0 uses two file types:

- `.msml`: complete model source. Contains model definitions and relationships. Does not contain diagram layout or visual styling.
- `.msmd`: diagram view. References one or more `.msml` files through `model_files`; every diagram element uses `model_ref`; every diagram relationship uses `relationship_ref`.

The singular `model_file` field is intentionally not supported. Use:

```json
{
  "msml_version": "1.0",
  "model_files": ["toaster-model.msml"],
  "diagram": {
    "type": "bdd"
  }
}
```

## Example: Humanity Optimization System

The Humanity Optimization System operational concept is a blog-post-style example of using MSML to model a civilization-scale decision-support system.

- [Operational concept](projects/humanity-optimization/Humanity_Optimization_Operational_Concept.md)
- [HOS model source](projects/humanity-optimization/hos-model.msml)
- [HOS definition BDD diagram source](projects/humanity-optimization/hos-context.msmd)
- [HOS context IBD diagram source](projects/humanity-optimization/hos-context-ibd.msmd)
- [Operating loop diagram source](projects/humanity-optimization/hos-operating-loop.msmd)
- [Decision-support sequence diagram source](projects/humanity-optimization/hos-decision-support-sequence.msmd)

## Example: Toaster Model

The toaster project is a compact example set that exercises all nine supported SysML-style diagram families.

- [Toaster project](projects/appliances/toaster)
- [Toaster feedback review](projects/appliances/toaster/codex-feedback-toaster.md)

## Current Status

MSML is an early prototype. The renderer is intentionally lightweight and currently targets PNG output through Pillow. The v1.0 direction is complete model/view separation: `.msml` for the model graph, `.msmd` for diagram views, validation through `msml_validate.py`, and PNGs rendered from those views.

## License

MIT License. See [LICENSE](LICENSE).
