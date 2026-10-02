#!/usr/bin/env python3
"""Ensure fixtures/external/fineract-handlers-thin/MANIFEST.txt matches on-disk slice inventory."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SLICE = ROOT / "fixtures/external/fineract-handlers-thin"


def parse_manifest_paths(manifest_text: str) -> list[str]:
    lines = manifest_text.splitlines()
    try:
        idx = lines.index("# paths applied:")
    except ValueError as exc:
        raise ValueError("MANIFEST.txt missing '# paths applied:' section") from exc
    paths = [ln.strip() for ln in lines[idx + 1 :] if ln.strip() and not ln.strip().startswith("#")]
    return paths


def list_slice_files(slice_dir: Path) -> list[str]:
    return sorted(p.name for p in slice_dir.iterdir() if p.is_file() and p.name != "MANIFEST.txt")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--slice-dir", type=Path, default=DEFAULT_SLICE)
    args = p.parse_args(argv)
    slice_dir = args.slice_dir if args.slice_dir.is_absolute() else ROOT / args.slice_dir
    manifest_path = slice_dir / "MANIFEST.txt"

    if not manifest_path.is_file():
        print(f"ERROR: missing {manifest_path}", file=sys.stderr)
        return 1

    try:
        listed = parse_manifest_paths(manifest_path.read_text(encoding="utf-8"))
    except ValueError as err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 1

    on_disk = list_slice_files(slice_dir)
    if listed != on_disk:
        print("ERROR: MANIFEST path list drift", file=sys.stderr)
        print(f"  manifest: {listed}", file=sys.stderr)
        print(f"  on_disk:  {on_disk}", file=sys.stderr)
        return 1

    print(f"OK: slice MANIFEST matches {len(on_disk)} files in {slice_dir.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
