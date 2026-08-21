# MSML: Meaningful Systems Modeling Language

MSML is a scriptable graphical modeling language for systems thinking, architecture, and human/AI collaboration.

The purpose of MSML is to make system models readable, versionable, reviewable, and renderable. Instead of keeping architecture diagrams as one-off drawings, MSML keeps the system meaning in model files and the diagram layout in view files. That makes the model easier to inspect in Git, revise with scripts or AI assistants, and regenerate as diagrams for communication.

MSML is inspired by SysML and PlantUML. SysML provides the systems-engineering vocabulary: blocks, internal structure, activities, sequences, states, requirements, parametrics, packages, and use cases. PlantUML demonstrates the value of text-based diagrams that can be regenerated reliably. MSML combines those ideas into a model-first format designed for plain-text workflows.

This project is early and intentionally practical. MSML v1.0 covers the SysML 1.6 diagram families plus the common requirement-table, allocation-table, and allocation-matrix views.

## Why MSML Exists

Complex systems are hard to reason about from prose alone. They need explicit structure, behavior, constraints, assumptions, and views.

MSML is built around a few principles:

- **Models should be source-controlled.** Each MSML model (`.msml`) is text.
- **Diagrams should be reproducible.** Each MSML diagram (`.msmd`) can be rendered again from the same source.
- **The model should be the source of truth.** MSML model (`.msml`) files contain the model graph. MSML diagram (`.msmd`) files contain layout and view information.
- **Humans and AI should edit the same artifacts.** The format is structured enough for tools and explicit enough for people to review.
- **The language should stay useful while it evolves.** MSML v1.0 is a small working language for real examples.

## File Types

MSML uses two source file types:

- MSML model (`.msml`): definitions, relationships, behavior topology, ports, requirements, state nodes, sequence occurrences, and other model-backed content.
- MSML diagram (`.msmd`): a diagram view that references one or more MSML model (`.msml`) files and provides canvas, layout, routing, frame, and style.

Rendered PNG files are generated outputs. MSML model (`.msml`) files are not rendered directly; MSML diagram (`.msmd`) files are rendered.

The current renderer supports these SysML 1 views:

- Block Definition Diagram
- Internal Block Diagram
- Activity Diagram
- Sequence Diagram
- State Machine Diagram
- Use Case Diagram
- Requirements Diagram
- Parametric Diagram
- Package Diagram
- Requirement Table
- Allocation Table
- Allocation Matrix

## Install

MSML is installable from this repository:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install git+https://github.com/meaningfulsystems/msml.git
```

For local development on MSML itself:

```bash
git clone https://github.com/meaningfulsystems/msml.git
cd msml
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

The package name is `msml`. It is not published to PyPI yet. Package version `0.1.x` implements the MSML v1.0 specification.

## Use MSML in Another Project

A recommended structure is to keep architecture artifacts together:

```text
my-system/
└── architecture/
    ├── msml-specification.md
    ├── system-model.msml
    ├── system-context.msmd
    ├── system-ibd.msmd
    └── system-sequence.msmd
```

Copy the specification into your project so humans and AI assistants have the modeling rules next to the model:

```bash
mkdir -p architecture
msml-spec --copy architecture/
```

Validate and render one MSML diagram (`.msmd`):

```bash
msml-validate architecture/system-context.msmd --strict
msml-render architecture/system-context.msmd
```

Validate and render a full folder:

```bash
msml-validate-all architecture --strict
msml-render-all architecture
```

The renderer writes PNG files next to their MSML diagram (`.msmd`) sources.

The full setup guide is in [quick-start.md](quick-start.md).

## Python API

MSML can also be used from Python:

```python
from pathlib import Path

from msml import render, validate, validate_all

diagram = Path("architecture/system-context.msmd")

report = validate(diagram, strict=True)
if report.errors:
    raise SystemExit(1)

render(diagram)

project_report = validate_all(Path("architecture"), strict=True)
```

## Command Line Tools

Installing MSML provides these commands:

- `msml-spec`
- `msml-validate`
- `msml-validate-all`
- `msml-render`
- `msml-render-all`

Useful examples:

```bash
msml-spec
msml-spec --path
msml-spec --copy architecture/
msml-validate-all projects --strict
msml-render-all projects
```

## Repository Layout

```text
.
├── msml-specification.md
├── pyproject.toml
├── quick-start.md
├── src/
│   └── msml/
├── tests/
└── projects/
    ├── appliances/
    │   ├── toaster/
    │   │   ├── toaster-model.msml
    │   │   ├── toaster-*.msmd
    │   │   └── toaster-*.png
    │   └── blender/
    │       ├── blender-model.msml
    │       ├── blender-*.msmd
    │       └── blender-*.png
    └── humanity-optimization/
        ├── Humanity_Optimization_System_Brief.md
        ├── Humanity_Optimization_Operational_Concept.md
        ├── hos-model.msml
        ├── hos-*.msmd
        └── hos-*.png
```

## Examples

### Humanity Optimization System

The Humanity Optimization System is a civilization-scale decision-support concept modeled with MSML.

- [Operational concept](projects/humanity-optimization/Humanity_Optimization_Operational_Concept.md)
- [HOS MSML model (`.msml`)](projects/humanity-optimization/hos-model.msml)
- [HOS block definition diagram (`.msmd`)](projects/humanity-optimization/hos-context.msmd)
- [HOS context internal block diagram (`.msmd`)](projects/humanity-optimization/hos-context-ibd.msmd)
- [HOS operating loop activity diagram (`.msmd`)](projects/humanity-optimization/hos-operating-loop.msmd)
- [HOS decision-support sequence diagram (`.msmd`)](projects/humanity-optimization/hos-decision-support-sequence.msmd)

### Appliance Models

The appliance examples are compact systems used to exercise the language.

- [Toaster project](projects/appliances/toaster): all nine SysML 1.6 diagram families plus requirement table (`toaster-reqt`), allocation table (`toaster-alloc`), and allocation matrix (`toaster-amx`) views.
- [Smart blender project](projects/appliances/blender): internal block, activity, and state machine views for a high-performance smart blender concept.

## Development Checks

After installing locally with `pip install -e .`, run:

```bash
python3 -m unittest
msml-validate-all projects --strict
msml-render-all projects
```

## Current Status

MSML is an early prototype. The renderer targets PNG output through Pillow. The validator checks MSML model (`.msml`) and MSML diagram (`.msmd`) consistency, including model references, relationship references, imports, tabular view configuration, and basic strict checks.

The root [msml-specification.md](msml-specification.md) is the canonical human-facing specification. The installed package also includes a copy for `msml-spec`.

## License

MIT License. See [LICENSE](LICENSE).
