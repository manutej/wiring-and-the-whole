#!/usr/bin/env python3
"""Validate fixtures/scale-report/latest.v0.json structure and timing presence."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "fixtures/scale-report/latest.v0.json"


def main() -> int:
    if not REPORT.is_file():
        print(f"ERROR: missing {REPORT} — run make scale-report", file=sys.stderr)
        return 1
    doc = json.loads(REPORT.read_text(encoding="utf-8"))
    if doc.get("schema_version") != "scale-report.v0":
        print("ERROR: schema_version", file=sys.stderr)
        return 1
    timing = doc.get("slice_matrix_timing") or {}
    rust = timing.get("rust") or {}
    if not rust.get("slices"):
        print("ERROR: missing rust slice timings", file=sys.stderr)
        return 1
    if float(rust.get("total_ms") or 0) <= 0:
        print("ERROR: rust total_ms must be > 0", file=sys.stderr)
        return 1
    print(f"OK: scale report check — {len(rust['slices'])} timed shards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
