#!/usr/bin/env python3
"""Compare extract_refs + wiringmap evidence against a frozen edge-recall sample."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = ROOT / "fixtures/edge-recall-sample/expected.v0.json"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_pairs(refs_dir: Path) -> set[tuple[str, str]]:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/extract_refs.py"),
            str(refs_dir),
            "--no-example-check",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout)
    fragment = json.loads(proc.stdout)
    pairs: set[tuple[str, str]] = set()
    for fname, tokens in (fragment.get("refs_by_file") or {}).items():
        for token in tokens:
            pairs.add((fname, token))
    return pairs


def wiringmap_pairs(wiringmap_path: Path) -> set[tuple[str, str]]:
    wm = load_json(wiringmap_path)
    if not isinstance(wm, dict):
        raise ValueError("wiringmap must be object")
    out: set[tuple[str, str]] = set()
    for edge in wm.get("edges") or []:
        evidence = edge.get("evidence", "")
        if "// refs:" not in evidence:
            continue
        file_part, refs_part = evidence.split("// refs:", 1)
        fname = file_part.strip()
        for token in refs_part.strip().split():
            out.add((fname, token))
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    args = p.parse_args(argv)

    fixture_path = args.fixture if args.fixture.is_absolute() else ROOT / args.fixture
    doc = load_json(fixture_path)
    if not isinstance(doc, dict):
        print("ERROR: fixture must be object", file=sys.stderr)
        return 1

    failures: list[str] = []
    total_pairs = 0

    for sample in doc.get("samples") or []:
        sid = sample["id"]
        expected = {tuple(pair) for pair in sample["pairs"]}
        total_pairs += len(expected)

        refs_dir = ROOT / sample["refs_dir"]
        wiringmap = ROOT / sample["wiringmap"]

        extracted = extract_pairs(refs_dir)
        from_map = wiringmap_pairs(wiringmap)

        for pair in sorted(expected - extracted):
            failures.append(f"{sid}: extract missing {pair[0]} -> {pair[1]}")
        for pair in sorted(expected - from_map):
            failures.append(f"{sid}: wiringmap missing {pair[0]} -> {pair[1]}")
        for pair in sorted(from_map - extracted):
            failures.append(f"{sid}: wiringmap cites ref not in // refs: {pair[0]} -> {pair[1]}")

    if failures:
        for line in failures:
            print(line, file=sys.stderr)
        return 1

    n_samples = len(doc.get("samples") or [])
    print(
        f"OK: edge-recall sample — {n_samples} slices, {total_pairs} frozen pairs "
        f"(extract ↔ wiringmap ↔ fixture)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
