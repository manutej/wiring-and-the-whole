#!/usr/bin/env python3
"""Append-only wiring discovery records (JSONL) for batch workers / incremental analysis."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STORE = ROOT / "fixtures/wiring-index/discoveries.jsonl"

REQUIRED_KEYS = frozenset({"schema_version", "repo_root", "path", "kind", "recorded_at_utc"})


def validate_record(rec: dict[str, Any]) -> None:
    missing = REQUIRED_KEYS - set(rec.keys())
    if missing:
        raise ValueError(f"missing keys: {sorted(missing)}")
    if rec["schema_version"] != "wiring-index-record.v0":
        raise ValueError("schema_version must be wiring-index-record.v0")


def append_record(store: Path, rec: dict[str, Any]) -> None:
    validate_record(rec)
    store.parent.mkdir(parents=True, exist_ok=True)
    with store.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")


def cmd_append(args: argparse.Namespace) -> int:
    payload = json.loads(args.json)
    if not isinstance(payload, dict):
        print("ERROR: --json must be object", file=sys.stderr)
        return 1
    payload.setdefault("recorded_at_utc", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    payload.setdefault("schema_version", "wiring-index-record.v0")
    store = args.store if args.store.is_absolute() else ROOT / args.store
    append_record(store, payload)
    print(f"OK: appended to {store.relative_to(ROOT)}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    store = args.store if args.store.is_absolute() else ROOT / args.store
    if not store.is_file():
        print(json.dumps({"records": 0}))
        return 0
    kinds: dict[str, int] = {}
    n = 0
    for line in store.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        n += 1
        k = str(rec.get("kind") or "unknown")
        kinds[k] = kinds.get(k, 0) + 1
    print(json.dumps({"records": n, "by_kind": kinds}, indent=2))
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--store", type=Path, default=DEFAULT_STORE)
    sub = p.add_subparsers(dest="cmd", required=True)

    ap = sub.add_parser("append", help="Append one JSON record")
    ap.add_argument("--json", required=True, help="Record object as JSON string")
    ap.set_defaults(func=cmd_append)

    st = sub.add_parser("stats", help="Count records in store")
    st.set_defaults(func=cmd_stats)

    args = p.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
