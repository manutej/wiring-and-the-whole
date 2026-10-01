#!/usr/bin/env python3
"""Parse // refs: lines under a Java fixture dir and check wiringmap example coverage."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_REFS_DIR = Path(
    os.environ.get(
        "REFS_DIR",
        os.environ.get("TOYBANK_ACCOUNTS_DIR", REPO / "witness" / "toybank" / "accounts"),
    )
)
DEFAULT_EXAMPLE = REPO / "wiringmap" / "examples" / "toybank-accounts.v0.json"
REFS_LINE = re.compile(r"//\s*refs:\s*(.+)$")


def refs_from_java(path: Path) -> list[str]:
    for line in path.read_text(encoding="utf-8").splitlines():
        match = REFS_LINE.search(line)
        if match:
            return match.group(1).strip().split()
    return []


def file_key(java_path: Path, refs_dir: Path) -> str:
    rel = java_path.relative_to(refs_dir)
    if rel.parent == Path("."):
        return rel.name
    return rel.as_posix()


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


def run_extract(refs_dir: Path, example_path: Path | None) -> int:
    if not refs_dir.is_dir():
        print(f"ERROR: refs directory not found: {refs_dir}", file=sys.stderr)
        return 1

    refs_by_file: dict[str, list[str]] = {}
    extracted_pairs: set[tuple[str, str]] = set()

    for java_path in sorted(refs_dir.rglob("*.java")):
        key = file_key(java_path, refs_dir)
        tokens = refs_from_java(java_path)
        refs_by_file[key] = tokens
        for token in tokens:
            extracted_pairs.add((key, token))

    fragment = {
        "slice": str(refs_dir.relative_to(REPO) if refs_dir.is_relative_to(REPO) else refs_dir),
        "refs_by_file": refs_by_file,
        "ref_token_count": sum(len(v) for v in refs_by_file.values()),
    }
    print(json.dumps(fragment, indent=2))

    if example_path is None:
        print(
            f"OK: {fragment['ref_token_count']} ref tokens extracted (no wiringmap example check)",
            file=sys.stderr,
        )
        return 0

    if not example_path.is_file():
        print(f"ERROR: missing example instance: {example_path}", file=sys.stderr)
        return 1

    example = json.loads(example_path.read_text(encoding="utf-8"))
    covered = evidence_pairs(example)

    missing_in_example: list[str] = []
    for fname, token in sorted(extracted_pairs):
        if (fname, token) not in covered:
            missing_in_example.append(f"{fname} -> {token}")

    stale_in_java: list[str] = [
        f"{fname} -> {token}"
        for fname, token in sorted(covered - extracted_pairs)
    ]

    failed = False
    if missing_in_example:
        failed = True
        print("refs in witness not reflected in wiringmap example edges:", file=sys.stderr)
        for line in missing_in_example:
            print(f"  {line}", file=sys.stderr)
    if stale_in_java:
        failed = True
        print("wiringmap example cites refs missing from witness // refs: lines:", file=sys.stderr)
        for line in stale_in_java:
            print(f"  {line}", file=sys.stderr)
    if failed:
        return 1

    print(
        f"OK: {fragment['ref_token_count']} ref tokens covered by "
        f"{len(example.get('edges', []))} example edges",
        file=sys.stderr,
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "refs_dir",
        nargs="?",
        type=Path,
        default=None,
        help="Directory of *.java files with // refs: lines (default: witness/toybank/accounts)",
    )
    parser.add_argument(
        "--example",
        type=Path,
        default=None,
        help="WiringMap v0 JSON for coverage check (default: toybank-accounts example)",
    )
    parser.add_argument(
        "--no-example-check",
        action="store_true",
        help="Emit extracted refs only; skip wiringmap edge coverage",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    refs_dir = args.refs_dir or DEFAULT_REFS_DIR
    if not refs_dir.is_absolute():
        refs_dir = (REPO / refs_dir).resolve()

    example_path: Path | None
    if args.no_example_check:
        example_path = None
    elif args.example is not None:
        example_path = args.example if args.example.is_absolute() else (REPO / args.example).resolve()
    else:
        example_path = DEFAULT_EXAMPLE

    return run_extract(refs_dir, example_path)


if __name__ == "__main__":
    raise SystemExit(main())
