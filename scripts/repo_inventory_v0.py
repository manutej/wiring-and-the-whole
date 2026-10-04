#!/usr/bin/env python3
"""Walk a repo tree: file counts and byte totals without reading file bodies (idle-safe inventory)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def scan(root: Path, *, max_depth: int | None, ignore_dirs: set[str]) -> dict[str, object]:
    if not root.is_dir():
        raise FileNotFoundError(root)

    by_ext: dict[str, dict[str, int]] = defaultdict(lambda: {"files": 0, "bytes": 0})
    total_files = 0
    total_bytes = 0
    java_files = 0
    java_bytes = 0

    def onerror(e: OSError) -> None:
        raise e

    for dirpath, dirnames, filenames in os.walk(root, onerror=onerror):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs and not d.startswith(".")]
        rel_parts = Path(dirpath).relative_to(root).parts
        if max_depth is not None and len(rel_parts) > max_depth:
            dirnames.clear()
            continue
        for name in filenames:
            if name.startswith("."):
                continue
            p = Path(dirpath) / name
            try:
                st = p.stat()
            except OSError:
                continue
            ext = p.suffix.lower() or "(no_ext)"
            by_ext[ext]["files"] += 1
            by_ext[ext]["bytes"] += st.st_size
            total_files += 1
            total_bytes += st.st_size
            if ext == ".java":
                java_files += 1
                java_bytes += st.st_size

    return {
        "schema_version": "repo-inventory.v0",
        "root": str(root.resolve()),
        "scanned_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_files": total_files,
        "total_bytes": total_bytes,
        "java_files": java_files,
        "java_bytes": java_bytes,
        "by_extension": dict(sorted(by_ext.items())),
        "note": "Byte totals from stat() only — no file body reads.",
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=ROOT,
        help="Repository root to scan (default: wiring-and-the-whole)",
    )
    p.add_argument("--max-depth", type=int, default=None)
    p.add_argument("--out", type=Path, default=None, help="Write JSON report to path")
    args = p.parse_args(argv)

    ignore = {
        "node_modules",
        ".git",
        "target",
        "dist",
        "build",
        ".next",
        "__pycache__",
        "vendor",
    }
    root = args.root if args.root.is_absolute() else ROOT / args.root
    doc = scan(root, max_depth=args.max_depth, ignore_dirs=ignore)
    text = json.dumps(doc, indent=2) + "\n"
    if args.out:
        out = args.out if args.out.is_absolute() else ROOT / args.out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"OK: repo inventory → {out.relative_to(ROOT)}", file=sys.stderr)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
