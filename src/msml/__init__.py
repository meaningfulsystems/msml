"""Meaningful Systems Modeling Language tools."""

from pathlib import Path

__version__ = "0.1.0"


def load_model(model_path):
    """Load an MSML model (.msml) and its imports."""
    from .model import load_model as _load_model

    return _load_model(Path(model_path))


def load_diagram(diagram_path):
    """Load an MSML diagram (.msmd) and its referenced models."""
    from .model import load_diagram as _load_diagram

    return _load_diagram(Path(diagram_path))


def render(diagram_path, output_path=None):
    """Render an MSML diagram (.msmd) to PNG."""
    from .render import render as _render

    return _render(diagram_path, output_path)


def validate(path, strict=False, lint=False):
    """Validate an MSML model (.msml) or diagram (.msmd) file."""
    from .validate import validate as _validate

    return _validate(Path(path), strict=strict, lint=lint)


def validate_all(root, strict=False, lint=False):
    """Validate all MSML model (.msml) and diagram (.msmd) files under a directory."""
    from .validate import validate_all as _validate_all

    return _validate_all(Path(root), strict=strict, lint=lint)


def spec_path() -> Path:
    """Return the installed MSML specification path."""
    from .spec import spec_path as _spec_path

    return _spec_path()
