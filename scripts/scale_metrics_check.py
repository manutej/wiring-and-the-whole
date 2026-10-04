#!/usr/bin/env python3
"""Gate: measured scale metrics vs frozen expected.v0.json (wiring + math honesty)."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ROOT / "fixtures/scale-metrics/expected.v0.json"
MANIFEST = ROOT / "fixtures/slice-matrix/manifest.v0.json"
EDGE_RECALL = ROOT / "fixtures/edge-recall-sample/expected.v0.json"
CHARTER = ROOT / "fixtures/external/fineract-charter-1k"
CHARTER_10K = ROOT / "fixtures/external/fineract-charter-10k"
E3_MANIFEST = ROOT / "fixtures/e3-commandhandler-wedge/manifest.json"
TOKEN_REPORT = ROOT / "fixtures/e3-commandhandler-wedge/token_report.json"


def java_loc_tree(dir_path: Path) -> tuple[int, int]:
    if not dir_path.is_dir():
        return 0, 0
    files = sorted(dir_path.rglob("*.java"))
    loc = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in files)
    return len(files), loc


def _content_key(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix_unique_loc(manifest: dict) -> tuple[int, int]:
    """Unique Java bodies across shards (content hash — no double-count charter-1k vs 10k copies)."""
    seen_hashes: set[str] = set()
    loc = 0
    for sl in manifest.get("slices") or []:
        refs = ROOT / sl["refs_dir"]
        if not refs.is_dir():
            continue
        for p in refs.rglob("*.java"):
            digest = _content_key(p)
            if digest in seen_hashes:
                continue
            seen_hashes.add(digest)
            loc += len(p.read_text(encoding="utf-8").splitlines())
    return len(seen_hashes), loc


def edge_recall_totals(edge_doc: dict) -> tuple[int, int]:
    frozen = 0
    distinct: set[tuple[str, str]] = set()
    for sample in edge_doc.get("samples") or []:
        for pair in sample.get("pairs") or []:
            frozen += 1
            distinct.add((pair[0], pair[1]))
    return frozen, len(distinct)


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

    if CHARTER_10K.is_dir() and "charter_10k" in exp:
        c10_files, c10_loc = java_loc_tree(CHARTER_10K)
        b10 = exp["charter_10k"]
        if c10_files < b10["min_java_files"]:
            failures.append(f"charter-10k java files {c10_files} < {b10['min_java_files']}")
        if c10_loc < b10["min_loc"] or c10_loc > b10["max_loc"]:
            failures.append(f"charter-10k LOC {c10_loc} outside [{b10['min_loc']}, {b10['max_loc']}]")
        wm10 = CHARTER_10K / "wiringmap.v0.json"
        if wm10.is_file():
            refs10 = ref_token_count(CHARTER_10K, wm10)
            if refs10 < b10["min_ref_tokens"]:
                failures.append(f"charter-10k ref_tokens {refs10} < {b10['min_ref_tokens']}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    n_slices = len(manifest.get("slices") or [])
    if n_slices < exp["slice_matrix"]["min_slices"]:
        failures.append(f"slice matrix {n_slices} < {exp['slice_matrix']['min_slices']}")

    edge_doc = json.loads(EDGE_RECALL.read_text(encoding="utf-8"))
    pairs, distinct_pairs = edge_recall_totals(edge_doc)
    if pairs < exp["edge_recall"]["min_total_pairs"]:
        failures.append(f"edge-recall pairs {pairs} < {exp['edge_recall']['min_total_pairs']}")
    min_distinct = exp["edge_recall"].get("min_distinct_pairs")
    if min_distinct is not None and distinct_pairs < min_distinct:
        failures.append(f"edge-recall distinct pairs {distinct_pairs} < {min_distinct}")

    e3 = json.loads(E3_MANIFEST.read_text(encoding="utf-8"))
    parsed = int(e3.get("parsed") or e3.get("handlers_parsed") or 0)
    if parsed < exp["handler_family"]["min_parsed"]:
        failures.append(f"handler parsed {parsed} < {exp['handler_family']['min_parsed']}")

    unique_files, unique_loc = matrix_unique_loc(manifest)
    min_unique = exp["union_loc_estimate"].get(
        "min_unique_java_loc", exp["union_loc_estimate"]["min_java_loc_touched_by_matrix"]
    )
    if unique_loc < min_unique:
        failures.append(f"matrix unique LOC {unique_loc} < {min_unique}")

    token_report = json.loads(TOKEN_REPORT.read_text(encoding="utf-8"))
    tokens = token_report.get("tokens") or {}
    explicit_full = int(tokens.get("explicit_full") or 0)
    factored_full = int(tokens.get("factored_full") or 0)
    # Measured pack sizes on 29-handler wedge (not repo-wide 514 extrapolation).
    if factored_full >= explicit_full or explicit_full == 0:
        failures.append(
            f"handler wedge measured factored {factored_full} >= explicit {explicit_full}"
        )
    breakeven = token_report.get("breakeven") or {}
    verdict = breakeven.get("verdict_at_n")

    report: dict[str, object] = {
        "charter_1k": {"java_files": c_files, "loc": c_loc, "ref_tokens": refs},
        "slice_matrix_slices": n_slices,
        "edge_recall_frozen_pairs": pairs,
        "edge_recall_distinct_pairs": distinct_pairs,
        "handler_parsed": parsed,
        "matrix_unique_java_bodies": unique_files,
        "matrix_unique_java_loc": unique_loc,
        "handler_measured_explicit_tokens": explicit_full,
        "handler_measured_factored_tokens": factored_full,
        "handler_breakeven_verdict_at_n514": verdict,
    }
    if CHARTER_10K.is_dir():
        c10_files, c10_loc = java_loc_tree(CHARTER_10K)
        wm10 = CHARTER_10K / "wiringmap.v0.json"
        refs10 = ref_token_count(CHARTER_10K, wm10) if wm10.is_file() else 0
        report["charter_10k"] = {"java_files": c10_files, "loc": c10_loc, "ref_tokens": refs10}
    print(json.dumps(report, indent=2))

    if failures:
        for f in failures:
            print(f"ERROR: {f}", file=sys.stderr)
        return 1

    print(
        f"OK: scale metrics — charter {c_loc} LOC, {n_slices} matrix slices, "
        f"{pairs} frozen / {distinct_pairs} distinct recall pairs, "
        f"{unique_loc} unique Java LOC ({unique_files} bodies)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
