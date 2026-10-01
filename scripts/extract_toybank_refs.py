#!/usr/bin/env python3
"""Parse witness/toybank/accounts // refs: lines and check coverage in wiringmap example."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ACCOUNTS_DIR = REPO / "witness" / "toybank" / "accounts"
EXAMPLE_PATH = REPO / "wiringmap" / "examples" / "toybank-accounts.v0.json"
REFS_LINE = re.compile(r"//\s*refs:\s*(.+)$")


def refs_from_java(path: Path) -> list[str]:
    for line in path.read_text(encoding="utf-8").splitlines():
        match = REFS_LINE.search(line)
        if match:
            return match.group(1).strip().split()
    return []


def evidence_pairs(example: dict) -> set[tuple[str, str]]:
    covered: set[tuple[str, str]] = set()
    for edge in example.get("edges", []):
        evidence = edge.get("evidence", "")
        if "// refs:" not in evidence:
            continue
        file_part, refs_part = evidence.split("// refs:", 1)
        fname = file_part.strip()
        for token in refs_part.strip().split():
            covered.add((fname, token))
    return covered


def main() -> int:
    if not EXAMPLE_PATH.is_file():
        print(f"ERROR: missing example instance: {EXAMPLE_PATH}", file=sys.stderr)
        return 1

    example = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
    covered = evidence_pairs(example)

    refs_by_file: dict[str, list[str]] = {}
    missing: list[str] = []

    for java_path in sorted(ACCOUNTS_DIR.glob("*.java")):
        tokens = refs_from_java(java_path)
        refs_by_file[java_path.name] = tokens
        for token in tokens:
            if (java_path.name, token) not in covered:
                missing.append(f"{java_path.name} -> {token}")

    fragment = {
        "slice": "witness/toybank/accounts",
        "refs_by_file": refs_by_file,
        "ref_token_count": sum(len(v) for v in refs_by_file.values()),
    }
    print(json.dumps(fragment, indent=2))

    if missing:
        print("refs not reflected in wiringmap example edges:", file=sys.stderr)
        for line in missing:
            print(f"  {line}", file=sys.stderr)
        return 1

    print(
        f"OK: {fragment['ref_token_count']} ref tokens covered by "
        f"{len(example.get('edges', []))} example edges",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
