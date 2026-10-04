#!/usr/bin/env python3
"""Refresh fineract charter slices in fixtures/edge-recall-sample/expected.v0.json."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures/edge-recall-sample/expected.v0.json"

CHARTERS: list[tuple[str, Path, Path]] = [
    (
        "fineract-charter-1k",
        ROOT / "fixtures/external/fineract-charter-1k",
        ROOT / "fixtures/external/fineract-charter-1k/wiringmap.v0.json",
    ),
    (
        "fineract-charter-10k",
        ROOT / "fixtures/external/fineract-charter-10k",
        ROOT / "fixtures/external/fineract-charter-10k/wiringmap.v0.json",
    ),
]


def extract_pairs(refs_dir: Path) -> list[list[str]]:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/extract_refs.py"),
            str(refs_dir),
            "--no-example-check",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    fragment = json.loads(proc.stdout)
    pairs: list[list[str]] = []
    for fname, tokens in sorted((fragment.get("refs_by_file") or {}).items()):
        for token in tokens:
            pairs.append([fname, token])
    return pairs


def main() -> int:
    doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    samples = doc.setdefault("samples", [])
    charter_ids = {cid for cid, _, _ in CHARTERS}
    samples = [s for s in samples if s.get("id") not in charter_ids]

    one_k_pairs: set[tuple[str, str]] = set()
    charter_1k_dir = CHARTERS[0][1]
    if charter_1k_dir.is_dir():
        for pair in extract_pairs(charter_1k_dir):
            one_k_pairs.add((pair[0], pair[1]))

    for cid, refs_dir, wiringmap in CHARTERS:
        if not refs_dir.is_dir():
            print(f"SKIP: missing {refs_dir}", file=sys.stderr)
            continue
        pairs = extract_pairs(refs_dir)
        if cid == "fineract-charter-10k":
            pairs = [p for p in pairs if (p[0], p[1]) not in one_k_pairs]
        entry: dict[str, object] = {
            "id": cid,
            "refs_dir": str(refs_dir.relative_to(ROOT)),
            "wiringmap": str(wiringmap.relative_to(ROOT)),
            "pairs": pairs,
        }
        if cid == "fineract-charter-10k":
            entry["allow_extract_surplus"] = True
        samples.append(entry)

    doc["samples"] = samples
    doc["description"] = (
        "Frozen (file, ref_token) pairs for wedge-2 edge recall sample gate "
        "(toybank + fineract thin + charter 1k + charter 10k scale vertical)"
    )
    FIXTURE.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    total = sum(len(s["pairs"]) for s in samples)
    print(f"OK: edge-recall fixture — {len(samples)} slices, {total} pairs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
