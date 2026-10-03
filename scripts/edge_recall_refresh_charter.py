#!/usr/bin/env python3
"""Append fineract-charter-1k pairs to fixtures/edge-recall-sample/expected.v0.json."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures/edge-recall-sample/expected.v0.json"
CHARTER_DIR = ROOT / "fixtures/external/fineract-charter-1k"
CHARTER_MAP = CHARTER_DIR / "wiringmap.v0.json"


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
    samples = [s for s in samples if s.get("id") != "fineract-charter-1k"]
    pairs = extract_pairs(CHARTER_DIR)
    samples.append(
        {
            "id": "fineract-charter-1k",
            "refs_dir": "fixtures/external/fineract-charter-1k",
            "wiringmap": "fixtures/external/fineract-charter-1k/wiringmap.v0.json",
            "pairs": pairs,
        }
    )
    doc["samples"] = samples
    doc["description"] = (
        "Frozen (file, ref_token) pairs for wedge-2 edge recall sample gate "
        "(toybank + fineract thin + ~1k charter vertical)"
    )
    FIXTURE.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    total = sum(len(s["pairs"]) for s in samples)
    print(f"OK: edge-recall fixture — {len(samples)} slices, {total} pairs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
