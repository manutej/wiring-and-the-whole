#!/usr/bin/env python3
"""Export wiringmap.v0 JSON to a stalks-and-sections SheafGraph (stdout). Stdlib only."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

RESIDUAL_MEANING = (
    "Structural wiring only: no residual was computed, and every map stays unverified "
    "until a quantizer exists (j2)."
)

LEVELS = [
    {"id": 0, "label": "units"},
    {"id": 1, "label": "junctions"},
]

RESTRICT_BY_KIND = {
    "call": "projection",
    "ref": "embed",
    "di": "identity",
    "import": "identity",
    "link": "identity",
}

# Last segment of a source path (e.g. bolt_386.go), not Java package.class names.
_SOURCE_FILE_EXT = frozenset(
    {"c", "cpp", "go", "h", "java", "js", "jsx", "kt", "py", "rb", "rs", "swift", "ts", "tsx"}
)


def slugify_ref(ref: str) -> str:
    tail = ref.rstrip("/").split("/")[-1]
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", tail).strip("-").lower()
    return slug or "wiringmap"


def unit_title(unit_id: str) -> str:
    body = unit_id.split(":", 1)[-1] if ":" in unit_id else unit_id
    if "." in body:
        stem, suffix = body.rsplit(".", 1)
        if suffix.lower() in _SOURCE_FILE_EXT and stem:
            return Path(body).stem
        return suffix
    if ":" in body:
        return body.rsplit(":", 1)[-1]
    return body


def load_wiringmap(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def build_port_owner(wm: dict[str, Any]) -> dict[str, str]:
    owners: dict[str, str] = {}
    for unit in wm.get("units") or []:
        uid = unit["id"]
        for port in unit.get("ports") or []:
            owners[port["id"]] = uid
    return owners


def resolve_endpoint(endpoint: str, port_owner: dict[str, str], junction_ids: set[str]) -> str:
    if endpoint.startswith("port:"):
        owner = port_owner.get(endpoint)
        if not owner:
            raise SystemExit(f"unresolvable endpoint: {endpoint}")
        return owner
    if endpoint.startswith("unit:"):
        return endpoint
    if endpoint in junction_ids:
        return endpoint
    raise SystemExit(f"unresolvable endpoint: {endpoint}")


def export_wiringmap(wm: dict[str, Any]) -> dict[str, Any]:
    meta = wm.get("meta") or {}
    graph_id = slugify_ref(str(meta.get("ref", "wiringmap")))
    title = meta.get("slice") or graph_id

    junction_ids = {j["id"] for j in (wm.get("junctions") or [])}
    port_owner = build_port_owner(wm)

    nodes: list[dict[str, Any]] = []
    for unit in wm.get("units") or []:
        ports = unit.get("ports") or []
        dim = max(1, min(64, len(ports)))
        nodes.append(
            {
                "id": unit["id"],
                "title": unit_title(unit["id"]),
                "kind": "module",
                "level": 0,
                "dim": dim,
                "summary": unit.get("role", ""),
                "sources": [unit.get("path", "")],
                "known": False,
            }
        )
    for junction in wm.get("junctions") or []:
        nodes.append(
            {
                "id": junction["id"],
                "title": junction.get("label", junction["id"]),
                "kind": "api",
                "level": 1,
                "dim": 1,
                "known": False,
            }
        )

    merged: dict[tuple[str, str], dict[str, Any]] = defaultdict(
        lambda: {"kinds": set(), "count": 0}
    )
    for edge in wm.get("edges") or []:
        src = resolve_endpoint(edge["from"], port_owner, junction_ids)
        tgt = resolve_endpoint(edge["to"], port_owner, junction_ids)
        if src == tgt:
            continue
        key = (src, tgt)
        merged[key]["count"] += 1
        merged[key]["kinds"].add(edge.get("edge_kind", "link"))

    x_swarm_edge = {"residualMeaning": RESIDUAL_MEANING}
    edges: list[dict[str, Any]] = []
    for (src, tgt), info in sorted(merged.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        kinds = sorted(info["kinds"])
        relation = kinds[0] if len(kinds) == 1 else "+".join(kinds)
        restrict_kind = RESTRICT_BY_KIND.get(kinds[0], "identity")
        if len(kinds) > 1:
            restrict_kind = "identity"
        count = info["count"]
        note = f"merged {count} wiring edge" + ("s" if count != 1 else "")
        edges.append(
            {
                "source": src,
                "target": tgt,
                "relation": relation,
                "restrictKind": restrict_kind,
                "note": note,
                "x-swarm": dict(x_swarm_edge),
            }
        )

    return {
        "id": graph_id,
        "title": title,
        "residualMeaning": RESIDUAL_MEANING,
        "levels": LEVELS,
        "nodes": nodes,
        "edges": edges,
    }


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: wiringmap_to_sheaf.py <wiringmap.v0.json>", file=sys.stderr)
        raise SystemExit(2)
    path = Path(sys.argv[1])
    wm = load_wiringmap(path)
    out = export_wiringmap(wm)
    sys.stdout.write(json.dumps(out, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
