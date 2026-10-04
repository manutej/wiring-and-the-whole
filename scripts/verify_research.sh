#!/usr/bin/env bash
# Tier-1 gate for Paris research JSON: paths exist, ingest status explicit, kit data in sync.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PARIS="$ROOT/research/ai-engineer-paris-2026"

fail() { echo "verify-research: $*" >&2; exit 1; }

[[ -f "$PARIS/digest.json" ]] || fail "missing digest.json"
[[ -f "$PARIS/catalog.json" ]] || fail "missing catalog.json"

export PARIS
python3 << 'PY'
import json, os, pathlib, sys

root = pathlib.Path(os.environ["PARIS"])
digest = json.loads((root / "digest.json").read_text())
status = digest.get("last_ingest_status", "ok")
if status == "skipped_insufficient_credits":
    print("verify-research: WARN ingest degraded (skipped_insufficient_credits) — OK for merge if documented")
ingested = set(digest.get("transcripts_ingested") or [])
for vid in ingested:
    if vid not in digest.get("insights", {}):
        print(f"verify-research: WARN {vid} in transcripts_ingested but no insights entry")
kit = root / "paris-editorial-dashboard-kit/data"
if kit.is_dir():
    for name in ("catalog.json", "digest.json", "transcript-summaries.json"):
        a, b = root / name, kit / name
        if a.exists() and b.exists() and a.read_bytes() != b.read_bytes():
            sys.exit(f"verify-research: FAIL kit/data/{name} diverges from research/{name}")
print("verify-research: OK (corpus)")
PY

bash "$ROOT/scripts/verify_references_index.sh"
