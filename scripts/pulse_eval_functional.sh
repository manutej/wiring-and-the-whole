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
check "dogfood meta L1 (pack I/O parse mode)" \
  python3 scripts/grade_l1_questions.py --answer-mode io

TMP_META_PACK="$(mktemp)"
cp docs/dogfood/L1-wiring-and-the-whole.md "${TMP_META_PACK}"
sed -i 's/| `e1_witness_check_count` | 13 |/| `e1_witness_check_count` | 12 |/' "${TMP_META_PACK}"
check "meta L1 I/O grade fails when grading fact row tampered" \
  expect_exit 1 python3 scripts/grade_l1_questions.py --answer-mode io \
    --pack "${TMP_META_PACK}"
rm -f "${TMP_META_PACK}"
check "dogfood toybank L1 (heuristic mode)" \
  python3 scripts/grade_l1_questions.py --questions docs/dogfood/L1-TOYBANK-QUESTIONS.json

check "dogfood toybank L1 (pack I/O parse mode)" \
  python3 scripts/grade_l1_questions.py --answer-mode io \
    --questions docs/dogfood/L1-TOYBANK-QUESTIONS.json

check "world I/O pipeline (extract→validate→pack→reexpand→grade)" \
  bash scripts/pipeline_world_io.sh

check "CommandHandler family wedge (29 handlers, reexpand gate)" \
  make handler-family-pack-check

TMP_HANDLER_PACK="$(mktemp -d)"
cp -r fixtures/e3-commandhandler-wedge/pack/* "${TMP_HANDLER_PACK}/"
echo "inst CommandHandler(TamperedHandler, Foo, bar, X, Y)" >> "${TMP_HANDLER_PACK}/pack_factored.txt"
check "handler wedge reexpand fails when inst row tampered" \
  expect_exit 1 python3 scripts/reexpand_gate.py "${TMP_HANDLER_PACK}"
rm -rf "${TMP_HANDLER_PACK}"

check "dogfood handler-wedge L1 (heuristic)" \
  python3 scripts/grade_l1_questions.py --questions docs/dogfood/L1-E3-COMMANDHANDLER-WEDGE-QUESTIONS.json

check "dogfood handler-wedge L1 (pack I/O parse mode)" \
  python3 scripts/grade_l1_questions.py --answer-mode io \
    --questions docs/dogfood/L1-E3-COMMANDHANDLER-WEDGE-QUESTIONS.json

TMP_PACK_MD="$(mktemp)"
cp docs/dogfood/L1-toybank-accounts.md "${TMP_PACK_MD}"
# Drop one catalog row — I/O parser must yield wrong count vs frozen questions
sed -i '/accounts.Money.*Money.java/d' "${TMP_PACK_MD}"
check "pack I/O grade fails when catalog row removed" \
  expect_exit 1 python3 scripts/grade_l1_questions.py --answer-mode io \
    --pack "${TMP_PACK_MD}" --questions docs/dogfood/L1-TOYBANK-QUESTIONS.json
rm -f "${TMP_PACK_MD}"
check "dogfood fineract-thin L1 (heuristic)" \
  python3 scripts/grade_l1_questions.py --questions docs/dogfood/L1-FINERACT-THIN-QUESTIONS.json

check "dogfood fineract-thin L1 (pack I/O parse mode)" \
  python3 scripts/grade_l1_questions.py --answer-mode io \
    --questions docs/dogfood/L1-FINERACT-THIN-QUESTIONS.json

check "fetch slice dry-run inventory I/O" \
  bash scripts/fetch_slice_io_check.sh

check "fineract slice MANIFEST matches on-disk inventory" \
  python3 scripts/validate_slice_manifest.py

check "CR@F95 harness stub (config validate + grade + tokens, no LLM)" \
  make cr-f95-stub-check

check "blind pack-only eval stub (meta + handler-wedge, no answers in bundle)" \
  make pack-blind-eval-check

check "edge-recall sample gate (toybank + fineract-thin frozen pairs)" \
  make edge-recall-sample-check

TMP_EDGE_FIX="$(mktemp)"
python3 -c "
import json
from pathlib import Path
p = Path('fixtures/edge-recall-sample/expected.v0.json')
doc = json.loads(p.read_text())
doc['samples'][0]['pairs'].append(['Ghost.java', 'missing.Service#nowhere'])
Path('${TMP_EDGE_FIX}').write_text(json.dumps(doc))
"
check "edge-recall sample fails when fixture expects missing ref pair" \
  expect_exit 1 python3 scripts/edge_recall_sample_check.py --fixture "${TMP_EDGE_FIX}"
rm -f "${TMP_EDGE_FIX}"

check "blind eval firewall rejects expected key in prompt bundle" \
  python3 -c "
import sys
sys.path.insert(0, '${ROOT}/scripts')
from pack_blind_eval_run import assert_firewall
bad = {'questions': [{'id': 'X', 'text': 'q', 'expected': 'LEAK'}]}
try:
    assert_firewall(bad)
    sys.exit(1)
except ValueError:
    sys.exit(0)
"

TMP_SLICE="$(mktemp -d)"
printf '%s\n' 'source_repo=x' '' '# paths applied:' 'only-on-manifest.txt' > "${TMP_SLICE}/MANIFEST.txt"
touch "${TMP_SLICE}/other-file.txt"
check "slice MANIFEST drift is detected" \
  expect_exit 1 python3 scripts/validate_slice_manifest.py --slice-dir "${TMP_SLICE}"
rm -rf "${TMP_SLICE}"

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
