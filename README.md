# MSML: Meaningful Systems Modeling Language

MSML is a scriptable graphical modeling language for systems modeling. It is inspired by SysML and PlantUML: SysML provides the systems-engineering diagram vocabulary, while PlantUML demonstrates the value of diagrams that can be generated, reviewed, versioned, and rendered from text.

This repository contains:

- the MSML v1 requirements/specification draft
- a Python PNG renderer for MSML files
- example MSML models and rendered diagrams
- early project models for appliances and humanity-scale systems

## Why MSML Exists

MSML is designed for human and AI collaboration on complex system models. The format is JSON, one diagram per file, with explicit visual layout. That makes diagrams deterministic, easy to diff, easy to regenerate, and suitable for publication alongside prose.

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
├── msml-requirements.md
├── render_msml.py
├── render_all.py
├── requirements.txt
├── decisions/
│   └── codex-feedback-decisions.md
└── projects/
    ├── appliances/
    │   └── toaster/
    │       ├── toaster-*.msml
    │       └── toaster-*.png
    └── humanity-optimization/
        ├── Humanity_Optimization_System_Brief.md
        ├── Humanity_Optimization_Operational_Concept.md
        ├── hos-*.msml
        └── hos-*.png
```

## Quick Start

Create a virtual environment and install the one runtime dependency:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Render one MSML file:

```bash
python3 render_msml.py projects/humanity-optimization/hos-context.msml
```

Render all MSML files under a folder:

```bash
python3 render_all.py projects/humanity-optimization
python3 render_all.py projects/appliances/toaster
```

The renderer writes PNG files next to their `.msml` sources.

## Example: Humanity Optimization System

The Humanity Optimization System operational concept is a blog-post-style example of using MSML to model a civilization-scale decision-support system.

- [Operational concept](projects/humanity-optimization/Humanity_Optimization_Operational_Concept.md)
- [Context diagram source](projects/humanity-optimization/hos-context.msml)
- [Operating loop source](projects/humanity-optimization/hos-operating-loop.msml)
- [Decision-support sequence source](projects/humanity-optimization/hos-decision-support-sequence.msml)

## Example: Toaster Model

The toaster project is a compact example set that exercises all nine supported SysML-style diagram families.

- [Toaster project](projects/appliances/toaster)
- [Toaster feedback review](projects/appliances/toaster/codex-feedback-toaster.md)

## Current Status

MSML is an early prototype. The renderer is intentionally lightweight and currently targets PNG output through Pillow. The specification is still evolving, especially around validation, semantic linting, cross-diagram references, and model/package structure.

## License

MIT License. See [LICENSE](LICENSE).
