#!/usr/bin/env python3
"""Gate: measured scale metrics vs frozen expected.v0.json (wiring + math honesty)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ROOT / "fixtures/scale-metrics/expected.v0.json"
MANIFEST = ROOT / "fixtures/slice-matrix/manifest.v0.json"
EDGE_RECALL = ROOT / "fixtures/edge-recall-sample/expected.v0.json"
CHARTER = ROOT / "fixtures/external/fineract-charter-1k"
E3_MANIFEST = ROOT / "fixtures/e3-commandhandler-wedge/manifest.json"
TOKEN_REPORT = ROOT / "fixtures/e3-commandhandler-wedge/token_report.json"


def java_loc_tree(dir_path: Path) -> tuple[int, int]:
    if not dir_path.is_dir():
        return 0, 0
    files = sorted(dir_path.rglob("*.java"))
    loc = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in files)
    return len(files), loc


def matrix_union_loc(manifest: dict) -> int:
    total = 0
    for sl in manifest.get("slices") or []:
        refs = ROOT / sl["refs_dir"]
        _, loc = java_loc_tree(refs)
        total += loc
    return total


def ref_token_count(refs_dir: Path, wiringmap: Path) -> int:
    import subprocess

    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/extract_refs.py"), str(refs_dir), "--example", str(wiringmap)],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    frag = json.loads(proc.stdout)
    return int(frag["ref_token_count"])


def main() -> int:
    exp = json.loads(EXPECTED.read_text(encoding="utf-8"))
    failures: list[str] = []

    c_files, c_loc = java_loc_tree(CHARTER)
    bounds = exp["charter_1k"]
    if c_files < bounds["min_java_files"]:
        failures.append(f"charter java files {c_files} < {bounds['min_java_files']}")
    if c_loc < bounds["min_loc"] or c_loc > bounds["max_loc"]:
        failures.append(f"charter LOC {c_loc} outside [{bounds['min_loc']}, {bounds['max_loc']}]")
    wm = CHARTER / "wiringmap.v0.json"
    refs = ref_token_count(CHARTER, wm)
    if refs < bounds["min_ref_tokens"]:
        failures.append(f"charter ref_tokens {refs} < {bounds['min_ref_tokens']}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    n_slices = len(manifest.get("slices") or [])
    if n_slices < exp["slice_matrix"]["min_slices"]:
        failures.append(f"slice matrix {n_slices} < {exp['slice_matrix']['min_slices']}")

    edge_doc = json.loads(EDGE_RECALL.read_text(encoding="utf-8"))
    pairs = sum(len(s["pairs"]) for s in edge_doc.get("samples") or [])
    if pairs < exp["edge_recall"]["min_total_pairs"]:
        failures.append(f"edge-recall pairs {pairs} < {exp['edge_recall']['min_total_pairs']}")

    e3 = json.loads(E3_MANIFEST.read_text(encoding="utf-8"))
    parsed = int(e3.get("parsed") or e3.get("handlers_parsed") or 0)
    if parsed < exp["handler_family"]["min_parsed"]:
        failures.append(f"handler parsed {parsed} < {exp['handler_family']['min_parsed']}")

    union_loc = matrix_union_loc(manifest)
    if union_loc < exp["union_loc_estimate"]["min_java_loc_touched_by_matrix"]:
        failures.append(
            f"matrix union LOC {union_loc} < {exp['union_loc_estimate']['min_java_loc_touched_by_matrix']}"
        )

    token_report = json.loads(TOKEN_REPORT.read_text(encoding="utf-8"))
    breakeven = token_report.get("breakeven") or {}
    verdict = breakeven.get("verdict_at_n") or token_report.get("decision")
    if verdict != "WIN":
        failures.append(f"handler token breakeven not WIN: {verdict!r}")

    report = {
        "charter": {"java_files": c_files, "loc": c_loc, "ref_tokens": refs},
        "slice_matrix_slices": n_slices,
        "edge_recall_pairs": pairs,
        "handler_parsed": parsed,
        "matrix_union_java_loc": union_loc,
        "handler_token_decision": token_report.get("decision") or token_report.get("family_decision"),
    }
    print(json.dumps(report, indent=2))

    if failures:
        for f in failures:
            print(f"ERROR: {f}", file=sys.stderr)
        return 1

    print(
        f"OK: scale metrics — charter {c_loc} LOC, {n_slices} matrix slices, "
        f"{pairs} recall pairs, ~{union_loc} LOC touched",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
