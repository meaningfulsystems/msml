"""Shared MSML file loading helpers."""

import json
from pathlib import Path
from typing import Optional, Set


def read_json_file(path: Path) -> dict:
    """Read a JSON file from disk."""
    with open(path) as f:
        return json.load(f)


def load_model_documents(model_path: Path, seen: Optional[Set[Path]] = None) -> list[tuple[Path, dict]]:
    """Load a model file and imported model files in import-first order."""
    seen = seen or set()
    model_path = model_path.resolve()
    if model_path in seen:
        return []
    seen.add(model_path)

    data = read_json_file(model_path)
    if "model" not in data:
        raise ValueError(f"{model_path} is not an MSML model file")

    documents = []
    model = data["model"]
    imports = model.get("imports", [])
    if isinstance(imports, str):
        imports = [imports]
    for import_path in imports:
        documents.extend(load_model_documents(model_path.parent / import_path, seen))
    documents.append((model_path, data))
    return documents
