"""Andrew / SysML2d hard rule: IBD connectors never pass over boxes.

Hop-overs may jump a *line*. They must not travel through another part's
interior. Endpoint boxes are excluded because the connector is allowed to
meet a port on that box edge.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from msml.io import read_json_file


REPO = Path(__file__).resolve().parents[1]
EBIKE = REPO / "projects/e-bike"
APOLLO = REPO / "projects/apollo"

# Shrink each part so a port sitting on the box edge is not a hit.
EDGE_SHRINK_PX = 6

OBSTACLE_TYPES = ("part", "comment", "note", "block", "actor")


def _xy(point: object) -> tuple[float, float]:
    if isinstance(point, dict):
        return float(point["x"]), float(point["y"])
    seq = list(point)  # type: ignore[arg-type]
    return float(seq[0]), float(seq[1])


def _shrink(rect: tuple[float, float, float, float]) -> tuple[float, float, float, float] | None:
    rx, ry, rw, rh = rect
    rx += EDGE_SHRINK_PX
    ry += EDGE_SHRINK_PX
    rw -= 2 * EDGE_SHRINK_PX
    rh -= 2 * EDGE_SHRINK_PX
    if rw <= 0 or rh <= 0:
        return None
    return rx, ry, rw, rh


def _point_in_rect(x: float, y: float, rect: tuple[float, float, float, float]) -> bool:
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh


def _segments_intersect(
    x1: float, y1: float, x2: float, y2: float,
    x3: float, y3: float, x4: float, y4: float,
) -> bool:
    def orient(ax: float, ay: float, bx: float, by: float, cx: float, cy: float) -> float:
        return (by - ay) * (cx - bx) - (bx - ax) * (cy - by)

    o1 = orient(x1, y1, x2, y2, x3, y3)
    o2 = orient(x1, y1, x2, y2, x4, y4)
    o3 = orient(x3, y3, x4, y4, x1, y1)
    o4 = orient(x3, y3, x4, y4, x2, y2)
    return (o1 == 0 or o2 == 0 or (o1 > 0) != (o2 > 0)) and (
        o3 == 0 or o4 == 0 or (o3 > 0) != (o4 > 0)
    )


def _segment_hits_rect(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    rect: tuple[float, float, float, float],
) -> bool:
    shrunk = _shrink(rect)
    if shrunk is None:
        return False
    rx, ry, rw, rh = shrunk
    if _point_in_rect(x1, y1, shrunk) or _point_in_rect(x2, y2, shrunk):
        return True
    minx, maxx = (x1, x2) if x1 <= x2 else (x2, x1)
    miny, maxy = (y1, y2) if y1 <= y2 else (y2, y1)
    if maxx < rx or minx > rx + rw or maxy < ry or miny > ry + rh:
        return False
    edges = (
        (rx, ry, rx + rw, ry),
        (rx + rw, ry, rx + rw, ry + rh),
        (rx + rw, ry + rh, rx, ry + rh),
        (rx, ry + rh, rx, ry),
    )
    return any(_segments_intersect(x1, y1, x2, y2, *edge) for edge in edges)


def _box_hits(diagram_path: Path) -> list[str]:
    diagram_doc = read_json_file(diagram_path)
    model_name = diagram_doc["model_files"][0]
    model_doc = read_json_file(diagram_path.parent / model_name)
    diagram = diagram_doc["diagram"]

    boxes: dict[str, dict] = {}
    port_owner: dict[str, str] = {}
    for element in diagram["elements"]:
        kind = element.get("type")
        if kind in OBSTACLE_TYPES:
            layout = element["layout"]
            boxes[element["id"]] = {
                "ref": element.get("model_ref", element["id"]),
                "rect": (
                    float(layout["x"]),
                    float(layout["y"]),
                    float(layout["width"]),
                    float(layout["height"]),
                ),
            }
        if kind == "port":
            port_owner[element["model_ref"]] = element["owner_ref"]

    model_rels = {
        rel["id"]: rel for rel in model_doc["model"]["relationships"]
    }

    hits: list[str] = []
    for rel in diagram.get("relationships") or []:
        if rel.get("type") != "connector":
            continue
        waypoints = rel.get("waypoints") or []
        if len(waypoints) < 2:
            continue
        model_rel = model_rels[rel["relationship_ref"]]
        endpoints = {
            port_owner.get(model_rel["source"]),
            port_owner.get(model_rel["target"]),
        }
        forbidden = {
            pid: info
            for pid, info in boxes.items()
            if pid not in endpoints
        }
        for start, end in zip(waypoints, waypoints[1:]):
            x1, y1 = _xy(start)
            x2, y2 = _xy(end)
            for pid, info in forbidden.items():
                if _segment_hits_rect(x1, y1, x2, y2, info["rect"]):
                    hits.append(
                        f"{diagram_path.name} {rel['id']} "
                        f"segment ({x1},{y1})->({x2},{y2}) "
                        f"crosses {pid} ({info['ref']})"
                    )
    return hits


class IbdNoLineThroughBoxTests(unittest.TestCase):
    def test_e_bike_ibd_connectors_miss_foreign_boxes(self) -> None:
        self.assertEqual(
            _box_hits(EBIKE / "e-bike-ibd.msmd"),
            [],
            "IBD connectors must not pass through boxes",
        )

    def test_e_bike_context_connectors_miss_foreign_boxes(self) -> None:
        self.assertEqual(
            _box_hits(EBIKE / "e-bike-ctx.msmd"),
            [],
            "Context IBD connectors must not pass through boxes",
        )

    def test_apollo_ibd_connectors_miss_foreign_boxes(self) -> None:
        self.assertEqual(
            _box_hits(APOLLO / "apollo-ibd.msmd"),
            [],
            "Apollo IBD connectors must not pass through boxes",
        )

    def test_apollo_context_connectors_miss_foreign_boxes(self) -> None:
        self.assertEqual(
            _box_hits(APOLLO / "apollo-ctx.msmd"),
            [],
            "Apollo context connectors must not pass through boxes",
        )

    def test_apollo_csm_connectors_miss_foreign_boxes(self) -> None:
        self.assertEqual(
            _box_hits(APOLLO / "apollo-csm.msmd"),
            [],
            "Apollo CSM connectors must not pass through boxes",
        )

    def test_apollo_saturn_ibd_connectors_miss_foreign_boxes(self) -> None:
        self.assertEqual(
            _box_hits(APOLLO / "apollo-sat-ibd.msmd"),
            [],
            "Apollo Saturn IBD connectors must not pass through boxes",
        )

    def test_apollo_lm_connectors_miss_foreign_boxes(self) -> None:
        self.assertEqual(
            _box_hits(APOLLO / "apollo-lm.msmd"),
            [],
            "Apollo LM connectors must not pass through boxes",
        )

    def test_apollo_ground_connectors_miss_foreign_boxes(self) -> None:
        self.assertEqual(
            _box_hits(APOLLO / "apollo-gnd.msmd"),
            [],
            "Apollo ground connectors must not pass through boxes",
        )
