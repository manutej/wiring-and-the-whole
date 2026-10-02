#!/usr/bin/env bash
# Real-world I/O pipeline: filesystem in → subprocess tools → artifacts out → JSON report.
# Simulates how an external operator (CI, another repo) would invoke the wiring stack.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

WM="${ROOT}/wiringmap/examples/toybank-accounts.v0.json"
SCHEMA="${ROOT}/wiringmap/schema.v0.json"
REFS="${ROOT}/witness/toybank/accounts"
WORK="$(mktemp -d)"
trap 'rm -rf "${WORK}"' EXIT

fail() { echo "PIPELINE IO FAIL: $*" >&2; exit 1; }

# --- 1. Extract refs (stdout JSON captured to disk) ---
python3 "${ROOT}/scripts/extract_refs.py" "${REFS}" --example "${WM}" \
  > "${WORK}/extract.json" 2> "${WORK}/extract.stderr" \
  || fail "extract_refs exited non-zero"
REF_COUNT="$(python3 -c "import json; print(json.load(open('${WORK}/extract.json'))['ref_token_count'])")"

# --- 2. Validate wiringmap (schema I/O) ---
python3 "${ROOT}/scripts/validate_wiringmap.py" "${SCHEMA}" "${WM}" \
  > "${WORK}/validate.out" 2>&1 || fail "validate_wiringmap failed"

# --- 3. Build L2 pack directory on disk ---
python3 "${ROOT}/scripts/build_l2_pack.py" "${WM}" >/dev/null
PACK="${WM%.json}.pack"
[[ -d "${PACK}" ]] || fail "pack dir missing: ${PACK}"
cp -a "${PACK}" "${WORK}/pack/"

# --- 4. Re-expansion byte gate (reads pack files from disk) ---
python3 "${ROOT}/scripts/reexpand_gate.py" "${WORK}/pack" \
  > "${WORK}/reexpand.out" 2>&1 || fail "reexpand_gate failed"

# --- 5. Cross-check: extract ref count vs pack explicit edge lines ---
EXPLICIT_EDGES="$(grep -c '^edge ' "${WORK}/pack/pack_explicit.txt" || true)"
if [[ "${REF_COUNT}" -ne "${EXPLICIT_EDGES}" ]]; then
  fail "ref_token_count (${REF_COUNT}) != explicit pack edges (${EXPLICIT_EDGES})"
fi

# --- 6. L1 dogfood via pack I/O parsing (not question heuristics) ---
python3 "${ROOT}/scripts/grade_l1_questions.py" \
  --answer-mode io \
  --questions "${ROOT}/docs/dogfood/L1-TOYBANK-QUESTIONS.json" \
  > "${WORK}/grade.out" 2>&1 || fail "L1 I/O grade failed"

# --- 7. Fineract thin slice: validate + extract only (external fixture I/O) ---
FIN="${ROOT}/fixtures/external/fineract-handlers-thin/wiringmap.v0.json"
python3 "${ROOT}/scripts/validate_wiringmap.py" "${SCHEMA}" "${FIN}" >/dev/null \
  || fail "fineract wiringmap validate failed"
python3 "${ROOT}/scripts/extract_refs.py" \
  "${ROOT}/fixtures/external/fineract-handlers-thin" \
  --example "${FIN}" \
  > "${WORK}/fineract_extract.json" 2>/dev/null || fail "fineract extract failed"
FIN_REF_COUNT="$(python3 -c "import json; print(json.load(open('${WORK}/fineract_extract.json'))['ref_token_count'])")"

python3 "${ROOT}/scripts/build_l2_pack.py" "${FIN}" >/dev/null
FIN_PACK="${FIN%.json}.pack"
[[ -d "${FIN_PACK}" ]] || fail "fineract pack dir missing: ${FIN_PACK}"
cp -a "${FIN_PACK}" "${WORK}/fineract_pack/"

python3 "${ROOT}/scripts/reexpand_gate.py" "${WORK}/fineract_pack" \
  > "${WORK}/fineract_reexpand.out" 2>&1 || fail "fineract reexpand_gate failed"

FIN_EXPLICIT_EDGES="$(grep -c '^edge ' "${WORK}/fineract_pack/pack_explicit.txt" || true)"
if [[ "${FIN_REF_COUNT}" -ne "${FIN_EXPLICIT_EDGES}" ]]; then
  fail "fineract ref_token_count (${FIN_REF_COUNT}) != explicit pack edges (${FIN_EXPLICIT_EDGES})"
fi

python3 "${ROOT}/scripts/grade_l1_questions.py" \
  --answer-mode io \
  --questions "${ROOT}/docs/dogfood/L1-FINERACT-THIN-QUESTIONS.json" \
  > "${WORK}/fineract_grade.out" 2>&1 || fail "fineract L1 I/O grade failed"

bash "${ROOT}/scripts/fetch_slice_io_check.sh" \
  > "${WORK}/fetch_io.out" 2>&1 || fail "fetch slice I/O check failed"

# --- Report (machine-readable contract for downstream CI) ---
python3 - <<PY
import json
from pathlib import Path
work = Path("${WORK}")
report = {
    "status": "ok",
    "toybank": {
        "ref_token_count": int("${REF_COUNT}"),
        "pack_explicit_edges": int("${EXPLICIT_EDGES}"),
        "pack_dir": str(work / "pack"),
    },
    "fineract_thin": {
        "ref_token_count": int("${FIN_REF_COUNT}"),
        "pack_explicit_edges": int("${FIN_EXPLICIT_EDGES}"),
        "pack_dir": str(work / "fineract_pack"),
    },
    "artifacts": {
        "extract_json": str(work / "extract.json"),
        "grade_out": str(work / "grade.out"),
    },
}
print(json.dumps(report, indent=2))
PY

echo "PIPELINE IO PASS: toybank + fineract-thin round-trip" >&2
