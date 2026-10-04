#!/usr/bin/env python3
"""
L2 pack builder v0 — one family (SliceUnit) from a wiringmap.v0 JSON slice.
Emits LEGEND.txt, pack_explicit.txt, and pack_factored.txt (E2 row/motif layout).
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "wiringmap/examples/toybank-accounts.v0.json"
LEGEND_SOURCE = ROOT / "experiments/e2-tokens/pack_LEGEND.txt"

MOTIF_SLICE_UNIT = """motif SliceUnit(U, edges):
  unit $U
  foreach E in $edges -> edge $U -> $E
"""


def short_unit(unit_id: str) -> str:
    if unit_id.startswith("unit:"):
        return unit_id.removeprefix("unit:").split(".")[-1]
    return unit_id


def port_unit_symbol(port_id: str) -> tuple[str, str]:
    # port:accounts.AccountsController#list
    body = port_id.removeprefix("port:")
    unit_part, _, sym = body.partition("#")
    return unit_part.split(".")[-1], sym


def junction_target(junction: dict) -> str:
    return junction["label"]


def load_wiringmap(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def build_index(wm: dict) -> tuple[dict[str, dict], dict[str, dict]]:
    units = {u["id"]: u for u in wm["units"]}
    junctions = {j["id"]: j for j in wm.get("junctions", [])}
    return units, junctions


def edge_target(
    edge: dict,
    units: dict[str, dict],
    junctions: dict[str, dict],
) -> tuple[str, str]:
    """Return (from_unit_short, target token for 'edge U -> target')."""
    src = edge["from"]
    if src.startswith("port:"):
        from_u, _ = port_unit_symbol(src)
    elif src.startswith("unit:"):
        from_u = short_unit(src)
    else:
        raise ValueError(f"unsupported edge.from {src!r}")

    dst = edge["to"]
    if dst.startswith("port:"):
        to_u, sym = port_unit_symbol(dst)
        target = f"{to_u}#{sym}"
    elif dst.startswith("junction:"):
        target = junction_target(junctions[dst])
    elif dst.startswith("unit:"):
        target = short_unit(dst)
    else:
        raise ValueError(f"unsupported edge.to {dst!r}")

    return from_u, target


def collect_unit_edges(wm: dict) -> dict[str, list[str]]:
    units, junctions = build_index(wm)
    by_unit: dict[str, set[str]] = {short_unit(u["id"]): set() for u in wm["units"]}

    for edge in wm.get("edges", []):
        from_u, target = edge_target(edge, units, junctions)
        by_unit.setdefault(from_u, set()).add(target)

    return {u: sorted(targets) for u, targets in sorted(by_unit.items())}


def explicit_lines(unit_edges: dict[str, list[str]]) -> str:
    lines: list[str] = []
    for unit in sorted(unit_edges.keys()):
        lines.append(f"unit {unit}")
        for target in unit_edges[unit]:
            lines.append(f"edge {unit} -> {target}")
    return "\n".join(lines) + "\n"


def factored_lines(unit_edges: dict[str, list[str]]) -> str:
    parts = [MOTIF_SLICE_UNIT.rstrip(), ""]
    for unit in sorted(unit_edges.keys()):
        edges = unit_edges[unit]
        if edges:
            edge_list = ",".join(edges)
            parts.append(f"inst SliceUnit({unit}, edges=[{edge_list}])")
        else:
            parts.append(f"inst SliceUnit({unit}, edges=[])")
    return "\n".join(parts) + "\n"


def expand_inst_row(row: str) -> list[str]:
    m = re.match(r"inst SliceUnit\((\w+), edges=\[(.*)\]\)\s*$", row.strip(), re.S)
    if not m:
        raise ValueError(f"bad inst row: {row!r}")
    unit, edges_s = m.groups()
    lines = [f"unit {unit}"]
    edges = [e.strip() for e in edges_s.split(",") if e.strip()]
    for target in sorted(edges):
        lines.append(f"edge {unit} -> {target}")
    return lines


def expand_factored(factored_text: str) -> str:
    lines: list[str] = []
    for raw in factored_text.splitlines():
        line = raw.strip()
        if not line or line.startswith("motif ") or line.startswith("foreach "):
            continue
        if line.startswith("inst "):
            lines.extend(expand_inst_row(line))
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build L2 pack v0 from wiringmap JSON")
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT,
        help="wiringmap.v0 JSON path",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="output directory (default: <input stem>.pack/)",
    )
    args = parser.parse_args()
    inp: Path = args.input.resolve()
    out_dir = args.out or inp.with_suffix("")  # drop .json
    out_dir = Path(str(out_dir) + ".pack")
    out_dir.mkdir(parents=True, exist_ok=True)

    wm = load_wiringmap(inp)
    unit_edges = collect_unit_edges(wm)

    explicit = explicit_lines(unit_edges)
    factored = factored_lines(unit_edges)
    legend = LEGEND_SOURCE.read_text(encoding="utf-8")
    if not legend.endswith("\n"):
        legend += "\n"

    if expand_factored(factored) != explicit:
        raise SystemExit("internal error: expand(factored) != explicit")

    (out_dir / "LEGEND.txt").write_text(legend, encoding="utf-8")
    (out_dir / "pack_explicit.txt").write_text(explicit, encoding="utf-8")
    (out_dir / "pack_factored.txt").write_text(factored, encoding="utf-8")

    print(f"wrote {out_dir}/LEGEND.txt pack_explicit.txt pack_factored.txt")


if __name__ == "__main__":
    main()
