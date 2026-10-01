#!/usr/bin/env bash
# Repro harness: E1 witness + E2 token counts + optional E3 grade (frozen responses only).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

log() { printf '==> %s\n' "$*"; }
fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }

command -v python3 >/dev/null || fail "python3 required"
command -v node >/dev/null || fail "node required (for E2 tiktoken)"

# --- Gate 1: E1 witness ---
log "E1 witness (run_witness.py)"
python3 witness/run_witness.py | python3 -c 'import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get("all_pass") else 1)' \
  || fail "witness: all_pass is not true"
echo "PASS E1 witness (all_pass=true)"

# --- Gate 2: E2 token micro-example ---
log "E2 tokens (npm ci + e2_run.py vs frozen E2-RESULTS.json)"
(
  cd "$ROOT/experiments"
  if [[ -f package-lock.json ]]; then npm ci --silent; else npm install --silent; fi
)
E2_DIR="$ROOT/experiments/e2-tokens"
FROZEN_E2="$E2_DIR/E2-RESULTS.json"
[[ -f "$FROZEN_E2" ]] || fail "missing $FROZEN_E2"

E2_OUT="$(cd "$E2_DIR" && python3 e2_run.py)"
python3 - "$FROZEN_E2" "$E2_OUT" <<'PY'
import json, sys

frozen_path, fresh_json = sys.argv[1], sys.argv[2]
frozen = json.load(open(frozen_path))
fresh = json.loads(fresh_json)

def site_diff(sid):
    diffs = []
    for key in (
        "gate_byte_identical", "e_explicit_tokens", "m_factored_row_tokens",
        "F_fixed_overhead_tokens", "n_star_breakeven", "verdict",
    ):
        a, b = frozen["sites"][sid].get(key), fresh["sites"][sid].get(key)
        if a != b:
            diffs.append(f"  {sid}.{key}: frozen={a!r} fresh={b!r}")
    return diffs

errors = []
for key in ("gate_all_sites_byte_identical", "overall", "legend_tokens"):
    if frozen.get(key) != fresh.get(key):
        errors.append(f"  {key}: frozen={frozen.get(key)!r} fresh={fresh.get(key)!r}")
for sid in ("S1", "S2", "S3"):
    errors.extend(site_diff(sid))

if errors:
    print("E2 mismatch vs frozen E2-RESULTS.json:", file=sys.stderr)
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
PY
echo "PASS E2 tokens (matches frozen E2-RESULTS.json)"

# --- Gate 3: E3 grade on frozen responses (optional; skip if script missing) ---
E3_GRADE="$ROOT/experiments/e3-ablation/e3_grade.py"
if [[ ! -f "$E3_GRADE" ]]; then
  echo "SKIP E3: e3_grade.py not found"
  exit 0
fi

log "E3 grade (frozen responses only)"
FROZEN_E3="$ROOT/experiments/e3-ablation/E3-GRADES.json"
[[ -f "$FROZEN_E3" ]] || fail "missing $FROZEN_E3"

E3_OUT="$(cd "$ROOT/experiments/e3-ablation" && python3 e3_grade.py)"
python3 - "$FROZEN_E3" "$E3_OUT" <<'PY'
import json, sys

frozen = json.load(open(sys.argv[1]))
fresh = json.loads(sys.argv[2])
keys = (
    "verdict", "pooled_A_wiring_strict", "pooled_B_wiring_strict",
    "pooled_C_wiring_strict", "A_minus_B_pts_strict", "wiring_pool_size",
)
errors = []
for key in keys:
    if frozen.get(key) != fresh.get(key):
        errors.append(f"  {key}: frozen={frozen.get(key)!r} fresh={fresh.get(key)!r}")
if errors:
    print("E3 mismatch vs frozen E3-GRADES.json:", file=sys.stderr)
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
PY
echo "PASS E3 grade (matches frozen E3-GRADES.json)"

log "All gates passed"
