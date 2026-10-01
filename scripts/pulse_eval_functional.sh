#!/usr/bin/env bash
# Functional pulse eval: exercises failure modes and cross-artifact behavior.
# Not a shallow echo of frozen JSON — expects specific pass/fail outcomes.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

pass=0
fail=0

check() {
  local name="$1"
  shift
  if "$@"; then
    echo "EVAL PASS: ${name}"
    pass=$((pass + 1))
  else
    echo "EVAL FAIL: ${name}" >&2
    fail=$((fail + 1))
  fi
}

expect_exit() {
  local expected="$1"
  shift
  set +e
  "$@" >/dev/null 2>&1
  local got=$?
  set -e
  [[ "${got}" -eq "${expected}" ]]
}

# --- Pack pipeline: happy path then deliberate breaks ---
python3 scripts/build_l2_pack.py wiringmap/examples/toybank-accounts.v0.json >/dev/null
PACK="${ROOT}/wiringmap/examples/toybank-accounts.v0.pack"

check "pack build + reexpand (canonical legend)" \
  python3 scripts/reexpand_gate.py "${PACK}"

TMP_PACK="$(mktemp -d)"
cp -a "${PACK}/." "${TMP_PACK}/"
echo "# tampered" >> "${TMP_PACK}/LEGEND.txt"
check "reexpand rejects tampered LEGEND (exit 1)" \
  expect_exit 1 python3 scripts/reexpand_gate.py "${TMP_PACK}"

cp -a "${PACK}/." "${TMP_PACK}/"
printf 'inst SliceUnit(BAD, edges=[nope])\n' >> "${TMP_PACK}/pack_factored.txt"
check "reexpand rejects broken factored inst row (exit 1)" \
  expect_exit 1 python3 scripts/reexpand_gate.py "${TMP_PACK}"
rm -rf "${TMP_PACK}"

# --- Density ladder: adversarial fixtures must fail extract/validate as designed ---
check "wiringmap-stress D0–D4 expectation matrix" \
  bash scripts/wiringmap_stress.sh

check "D1 missing-ref extract fails alone" \
  expect_exit 1 python3 scripts/extract_refs.py fixtures/density/d1-minimal \
    --example fixtures/density/d1-minimal/wiringmap.v0.json

check "D2 invalid instance fails validate alone" \
  expect_exit 1 python3 scripts/validate_wiringmap.py \
    wiringmap/schema.v0.json fixtures/density/d2-fork/invalid.v0.json

# --- External slice: wiringmap matches declared refs ---
check "external fineract slice check" bash scripts/fineract_slice_check.sh

check "fetch slice dry-run leaves fixtures untouched" \
  bash scripts/fetch_fineract_slice.sh

# --- L1 dogfood: grader matches frozen answers (navigation contract) ---
check "dogfood meta L1" \
  python3 scripts/grade_l1_questions.py
check "dogfood toybank L1" \
  python3 scripts/grade_l1_questions.py --questions docs/dogfood/L1-TOYBANK-QUESTIONS.json
check "dogfood fineract-thin L1" \
  python3 scripts/grade_l1_questions.py --questions docs/dogfood/L1-FINERACT-THIN-QUESTIONS.json

# --- Grader must fail when answers are wrong (not tautological) ---
WRONG_Q="$(mktemp)"
cat > "${WRONG_Q}" <<'JSON'
{"pack":"docs/dogfood/L1-wiring-and-the-whole.md","version":1,"questions":[{"id":"Z","text":"How many E1 witness checks does WITNESS.json define?","expected":"99"}]}
JSON
check "grade_l1 fails when expected answer is wrong (not tautology)" \
  expect_exit 1 python3 scripts/grade_l1_questions.py --questions "${WRONG_Q}"
rm -f "${WRONG_Q}"

echo ""
echo "Functional eval: ${pass} passed, ${fail} failed"
if [[ "${fail}" -gt 0 ]]; then
  exit 1
fi
exit 0
