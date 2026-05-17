# MSML: Meaningful Systems Modeling Language

MSML is a scriptable graphical modeling language for systems modeling. It is inspired by SysML and PlantUML: SysML provides the systems-engineering diagram vocabulary, while PlantUML demonstrates the value of diagrams that can be generated, reviewed, versioned, and rendered from text.

This repository contains:

- the MSML v1.0 specification
- a Python PNG renderer for MSML diagram files
- example MSML models, diagram views, and rendered diagrams
- early project models for appliances and humanity-scale systems

## Why MSML Exists

MSML is designed for human and AI collaboration on complex system models. The format is JSON. Semantic model content lives in `.msml` files, while graphical diagram views live in `.msmd` files with explicit visual layout. That makes diagrams deterministic, easy to diff, easy to regenerate, and suitable for publication alongside prose.

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
```

The renderer writes PNG files next to their `.msmd` sources. `.msml` model files are loaded by the diagram files and are not rendered directly.

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

MSML is an early prototype. The renderer is intentionally lightweight and currently targets PNG output through Pillow. The v1.0 direction is model/view separation: `.msml` for semantic models, `.msmd` for diagram views, and PNGs rendered from those views.

## License

MIT License. See [LICENSE](LICENSE).
