#!/usr/bin/env python3
"""Validate MSML model and diagram files."""

import argparse
import re
import sys
from pathlib import Path

from .io import load_model_documents, read_json_file


HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$")
POSITIONED_TYPES = {
    "block",
    "part",
    "port",
    "lifeline",
    "execution_occurrence",
    "state",
    "initial_node",
    "initial_pseudostate",
    "activity_final_node",
    "flow_final_node",
    "final_state",
    "fork_node",
    "join_node",
    "decision_node",
    "merge_node",
    "partition",
    "action",
    "call_behavior_action",
    "object_node",
    "actor",
    "use_case",
    "system_boundary",
    "requirement",
    "test_case",
    "constraint_property",
    "value_property",
    "package",
    "model",
    "class",
    "comment",
    "annotation",
    "table_row",
    "matrix_row",
    "matrix_column",
}


class Reporter:
    def __init__(self):
        self.errors = 0
        self.warnings = 0

    def error(self, path, scope, code, message):
        self.errors += 1
        print(f"ERROR  {path}  {scope}  {code}: {message}")

    def warn(self, path, scope, code, message):
        self.warnings += 1
        print(f"WARN   {path}  {scope}  {code}: {message}")

    def merge(self, other: "Reporter"):
        self.errors += other.errors
        self.warnings += other.warnings


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def read_json(path: Path, reporter: Reporter):
    try:
        return read_json_file(path)
    except Exception as exc:
        reporter.error(relpath(path), "file", "MSML-SCHEMA-001", str(exc))
        return None


def load_model(model_path: Path, reporter: Reporter, seen=None):
    try:
        documents = load_model_documents(model_path, seen)
    except Exception as exc:
        reporter.error(relpath(model_path), "file", "MSML-SCHEMA-001", str(exc))
        return {"definitions": {}, "relationships": {}}

    definitions = {}
    relationships = {}
    for loaded_path, data in documents:
        model = data["model"]
        for definition in model.get("definitions", []):
            did = definition.get("id")
            if not did:
                reporter.error(relpath(loaded_path), "model", "MSML-SCHEMA-002", "definition missing id")
                continue
            if did in definitions:
                reporter.error(relpath(loaded_path), f"definition[{did}]", "MSML-SCHEMA-004", "duplicate definition id")
            definitions[did] = definition

        for relationship in model.get("relationships", []):
            rid = relationship.get("id")
            if not rid:
                reporter.error(relpath(loaded_path), "model", "MSML-SCHEMA-002", "relationship missing id")
                continue
            if rid in relationships:
                reporter.error(relpath(loaded_path), f"relationship[{rid}]", "MSML-SCHEMA-004", "duplicate relationship id")
            relationships[rid] = relationship

    return {"definitions": definitions, "relationships": relationships}


def walk_values(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_values(child)


def validate_colors(path: Path, data, reporter: Reporter):
    for obj in walk_values(data):
        for key, value in obj.items():
            if key.endswith("_color") and isinstance(value, str) and not HEX_COLOR.match(value):
                reporter.error(relpath(path), "file", "MSML-SCHEMA-003", f"invalid color {key}={value!r}")


def validate_model_file(path: Path, data, reporter: Reporter):
    if "msml_version" not in data:
        reporter.error(relpath(path), "file", "MSML-SCHEMA-002", "missing msml_version")
    if "model" not in data:
        reporter.error(relpath(path), "file", "MSML-SCHEMA-002", "missing model object")
        return
    seen_defs = set()
    seen_rels = set()
    for definition in data["model"].get("definitions", []):
        did = definition.get("id")
        if not did:
            reporter.error(relpath(path), "model", "MSML-SCHEMA-002", "definition missing id")
        elif did in seen_defs:
            reporter.error(relpath(path), f"definition[{did}]", "MSML-SCHEMA-004", "duplicate definition id")
        seen_defs.add(did)
    for relationship in data["model"].get("relationships", []):
        rid = relationship.get("id")
        if not rid:
            reporter.error(relpath(path), "model", "MSML-SCHEMA-002", "relationship missing id")
        elif rid in seen_rels:
            reporter.error(relpath(path), f"relationship[{rid}]", "MSML-SCHEMA-004", "duplicate relationship id")
        seen_rels.add(rid)


def collect_related_diagram_usage(path: Path, model_files: list[str]):
    model_paths = {(path.parent / model_file).resolve() for model_file in model_files}
    used_model_refs = set()
    used_relationship_refs = set()

    for candidate in sorted(path.parent.glob("*.msmd")):
        try:
            data = read_json_file(candidate)
        except Exception:
            continue
        candidate_model_files = data.get("model_files")
        if not isinstance(candidate_model_files, list):
            continue
        candidate_model_paths = {
            (candidate.parent / model_file).resolve()
            for model_file in candidate_model_files
        }
        if model_paths and model_paths.isdisjoint(candidate_model_paths):
            continue

        diagram = data.get("diagram", {})
        if diagram.get("subject_ref"):
            used_model_refs.add(diagram["subject_ref"])
        used_model_refs.update(
            element.get("model_ref")
            for element in diagram.get("elements", [])
            if element.get("model_ref")
        )
        used_relationship_refs.update(
            relationship.get("relationship_ref")
            for relationship in diagram.get("relationships", [])
            if relationship.get("relationship_ref")
        )

    return used_model_refs, used_relationship_refs


def validate_diagram_file(path: Path, data, reporter: Reporter, strict=False, lint=False):
    if "msml_version" not in data:
        reporter.error(relpath(path), "file", "MSML-SCHEMA-002", "missing msml_version")
    if "diagram" not in data:
        reporter.error(relpath(path), "file", "MSML-SCHEMA-002", "missing diagram object")
        return
    if "model_file" in data:
        reporter.error(relpath(path), "file", "MSML-SCHEMA-009", "model_file is invalid; use model_files")

    model_files = data.get("model_files")
    model_load_errors = False
    if not isinstance(model_files, list) or not model_files:
        reporter.error(relpath(path), "file", "MSML-SCHEMA-007", "missing non-empty model_files array")
        model = {"definitions": {}, "relationships": {}}
        model_load_errors = True
    else:
        model = {"definitions": {}, "relationships": {}}
        for model_file in model_files:
            model_path = path.parent / model_file
            if not model_path.exists():
                reporter.error(relpath(path), "file", "MSML-SCHEMA-007", f"model file not found: {model_file}")
                model_load_errors = True
                continue
            loaded = load_model(model_path, reporter)
            model["definitions"].update(loaded["definitions"])
            model["relationships"].update(loaded["relationships"])

    diagram = data["diagram"]
    element_ids = set()
    model_ref_to_element = {}
    for element in diagram.get("elements", []):
        eid = element.get("id")
        scope = f"element[{eid}]"
        if not eid:
            reporter.error(relpath(path), "diagram", "MSML-SCHEMA-002", "element missing id")
            continue
        if eid in element_ids:
            reporter.error(relpath(path), scope, "MSML-SCHEMA-004", "duplicate element id")
        element_ids.add(eid)

        model_ref = element.get("model_ref")
        if not model_ref:
            reporter.error(relpath(path), scope, "MSML-SCHEMA-005", "missing model_ref")
        elif not model_load_errors and model_ref not in model["definitions"]:
            reporter.error(relpath(path), scope, "MSML-SCHEMA-005", f"model_ref not found: {model_ref}")
        else:
            model_ref_to_element.setdefault(model_ref, []).append(eid)

        if element.get("type") in POSITIONED_TYPES:
            layout = element.get("layout", {})
            for key in ("x", "y", "width", "height"):
                if key not in layout:
                    reporter.error(relpath(path), scope, "MSML-SCHEMA-008", f"missing layout.{key}")

        if lint:
            font = element.get("style", {}).get("font", {})
            size = font.get("size")
            if isinstance(size, (int, float)) and size < 9:
                reporter.warn(relpath(path), scope, "MSML-LINT-001", f"font size {size} below 9pt")

    relationship_ids = set()
    used_relationship_refs = set()
    for relationship in diagram.get("relationships", []):
        rid = relationship.get("id")
        scope = f"relationship[{rid}]"
        if not rid:
            reporter.error(relpath(path), "diagram", "MSML-SCHEMA-002", "relationship missing id")
            continue
        if rid in relationship_ids:
            reporter.error(relpath(path), scope, "MSML-SCHEMA-004", "duplicate relationship id")
        relationship_ids.add(rid)

        relationship_ref = relationship.get("relationship_ref")
        if not relationship_ref:
            reporter.error(relpath(path), scope, "MSML-SCHEMA-006", "missing relationship_ref")
        elif not model_load_errors and relationship_ref not in model["relationships"]:
            reporter.error(relpath(path), scope, "MSML-SCHEMA-006", f"relationship_ref not found: {relationship_ref}")
        else:
            used_relationship_refs.add(relationship_ref)

    if strict and not model_load_errors:
        for rid, relationship in model["relationships"].items():
            if relationship.get("type") == "message":
                for field in ("source_lifeline", "target_lifeline"):
                    ref = relationship.get(field)
                    definition = model["definitions"].get(ref)
                    if definition and definition.get("type") not in ("block", "actor"):
                        reporter.error(
                            relpath(path),
                            f"relationship[{rid}]",
                            "MSML-STRICT-004",
                            f"{field} references non-block/actor definition {ref}",
                        )
        if diagram.get("type") in ("ibd", "parametric"):
            subject_ref = diagram.get("subject_ref")
            definition = model["definitions"].get(subject_ref)
            if not subject_ref or not definition or definition.get("type") != "block":
                reporter.error(
                    relpath(path),
                    "diagram",
                    "MSML-STRICT-005",
                    "subject_ref missing or not a block definition",
                )
        if diagram.get("type") == "requirement_table" and not diagram.get("table", {}).get("columns"):
            reporter.error(
                relpath(path),
                "diagram",
                "MSML-STRICT-006",
                "requirement_table requires diagram.table.columns",
            )
        if diagram.get("type") == "allocation_table" and not diagram.get("table", {}).get("columns"):
            reporter.error(
                relpath(path),
                "diagram",
                "MSML-STRICT-006",
                "allocation_table requires diagram.table.columns",
            )
        if diagram.get("type") == "allocation_matrix":
            if not diagram.get("matrix"):
                reporter.error(
                    relpath(path),
                    "diagram",
                    "MSML-STRICT-006",
                    "allocation_matrix requires diagram.matrix",
                )
            roles = {el.get("matrix_role") for el in diagram.get("elements", [])}
            if "row" not in roles or "column" not in roles:
                reporter.error(
                    relpath(path),
                    "diagram",
                    "MSML-STRICT-006",
                    "allocation_matrix requires elements with matrix_role row and column",
                )

    if lint and not model_load_errors:
        if isinstance(model_files, list):
            used_model_refs, used_relationship_refs = collect_related_diagram_usage(path, model_files)
        else:
            used_model_refs = {e.get("model_ref") for e in diagram.get("elements", []) if e.get("model_ref")}
            if diagram.get("subject_ref"):
                used_model_refs.add(diagram["subject_ref"])
        for did in sorted(set(model["definitions"]) - used_model_refs):
            reporter.warn(relpath(path), f"definition[{did}]", "MSML-LINT-004", "definition has no element in related diagrams")
        for rid in sorted(set(model["relationships"]) - used_relationship_refs):
            reporter.warn(relpath(path), f"relationship[{rid}]", "MSML-LINT-005", "relationship has no view in related diagrams")


def validate(path: Path, strict=False, lint=False) -> Reporter:
    reporter = Reporter()
    data = read_json(path, reporter)
    if not data:
        return reporter
    validate_colors(path, data, reporter)
    if path.suffix == ".msml":
        validate_model_file(path, data, reporter)
    elif path.suffix == ".msmd":
        validate_diagram_file(path, data, reporter, strict=strict or lint, lint=lint)
    else:
        reporter.error(relpath(path), "file", "MSML-SCHEMA-002", "file must be .msml or .msmd")
    return reporter


def validate_all(root: Path, strict=False, lint=False) -> Reporter:
    """Validate all MSML model and diagram files under a directory."""
    reporter = Reporter()
    files = sorted(
        path
        for suffix in ("*.msml", "*.msmd")
        for path in root.rglob(suffix)
    )
    if not files:
        reporter.error(relpath(root), "file", "MSML-SCHEMA-002", "no .msml or .msmd files found")
        return reporter

    for path in files:
        reporter.merge(validate(path, strict=strict, lint=lint))
    return reporter


def main():
    parser = argparse.ArgumentParser(description="Validate MSML model and diagram files.")
    parser.add_argument("path")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--lint", action="store_true")
    args = parser.parse_args()

    reporter = validate(Path(args.path), strict=args.strict, lint=args.lint)
    print(f"{reporter.errors} errors, {reporter.warnings} warnings.")
    sys.exit(1 if reporter.errors else 0)


if __name__ == "__main__":
    main()
