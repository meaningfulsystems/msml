"""Load MSML model and diagram files."""

from pathlib import Path
from typing import Optional, Set, Tuple

from .io import load_model_documents, read_json_file


def load_model(model_path: Path, seen: Optional[Set[Path]] = None) -> dict:
    """Load a model file and its imports into a flat model graph."""
    definitions = {}
    relationships = []
    for loaded_path, data in load_model_documents(model_path, seen):
        model = data["model"]
        for definition in model.get("definitions", []):
            if "id" not in definition:
                raise ValueError(f"Definition without id in {loaded_path}")
            definitions[definition["id"]] = definition
        relationships.extend(model.get("relationships", []))
    return {"definitions": definitions, "relationships": relationships}


def load_diagram(diagram_path: Path) -> Tuple[dict, dict]:
    """Load a diagram file and all referenced model files."""
    data = read_json_file(diagram_path)
    if "diagram" not in data:
        raise ValueError(f"{diagram_path} is not an MSMD diagram file")

    if "model_file" in data:
        raise ValueError(
            f"MSML-SCHEMA-009: {diagram_path} uses model_file; use model_files array"
        )
    model_files = data.get("model_files")
    if not isinstance(model_files, list) or not model_files:
        raise ValueError(
            f"MSML-SCHEMA-007: {diagram_path} must declare non-empty model_files array"
        )

    model = {"definitions": {}, "relationships": []}
    for model_file in model_files:
        loaded = load_model(diagram_path.parent / model_file)
        model["definitions"].update(loaded["definitions"])
        model["relationships"].extend(loaded["relationships"])
    return data, model
