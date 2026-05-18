# MSML Quick Start

This guide is for using MSML inside another project, such as a software system, product architecture, research model, operational concept, or engineering design.

## 1. Install MSML

From your project root:

```bash
cd my-system
python3 -m venv .venv
source .venv/bin/activate
pip install git+https://github.com/meaningfulsystems/msml.git
```

This installs the command-line tools:

- `msml-render`
- `msml-render-all`
- `msml-validate`
- `msml-validate-all`
- `msml-spec`

## 2. Create a Modeling Folder

Recommended structure:

```text
my-system/
└── architecture/
    ├── msml-specification.md
    ├── system-model.msml
    ├── system-context.msmd
    ├── system-ibd.msmd
    └── system-sequence.msmd
```

Create the folder and copy the MSML specification into it:

```bash
mkdir -p architecture
msml-spec --copy architecture/
```

Putting `msml-specification.md` beside the MSML model (`.msml`) and MSML diagram (`.msmd`) files gives people and AI assistants local rules to read before editing the model.

## 3. Create Model and Diagram Files

Use one or more MSML model (`.msml`) files for the source model:

```text
architecture/system-model.msml
```

Use MSML diagram (`.msmd`) files for views of that model:

```text
architecture/system-context.msmd
architecture/system-ibd.msmd
architecture/system-sequence.msmd
```

Each MSML diagram (`.msmd`) file references one or more MSML model (`.msml`) files. The MSML model (`.msml`) file is the source of truth. The MSML diagram (`.msmd`) file provides layout and rendering instructions.

## 4. Validate and Render

Validate one MSML diagram (`.msmd`) file:

```bash
msml-validate architecture/system-context.msmd --strict
```

Validate every MSML model (`.msml`) and MSML diagram (`.msmd`) file in the modeling folder:

```bash
msml-validate-all architecture --strict
```

Render one MSML diagram (`.msmd`) file:

```bash
msml-render architecture/system-context.msmd
```

Render all MSML diagram (`.msmd`) files under the modeling folder:

```bash
msml-render-all architecture
```

Rendered PNG files are written next to their `.msmd` sources.

## 5. Use MSML from Python

You can also call MSML from build scripts, documentation pipelines, or CI:

```python
from pathlib import Path

from msml import render, validate

diagram = Path("architecture/system-context.msmd")

report = validate(diagram, strict=True)
if report.errors:
    raise SystemExit(1)

render(diagram)
```

## Notes

- Do not render MSML model (`.msml`) files directly. Render MSML diagram (`.msmd`) files.
- `msml-render-all` renders diagrams but does not run validation first.
- Use `msml-validate --strict` or `msml-validate-all --strict` before rendering when you want an explicit model/view consistency check.
- Use `msml-spec --path` to locate the packaged specification.
- Use `msml-spec --copy architecture/` to copy the specification into your project.
