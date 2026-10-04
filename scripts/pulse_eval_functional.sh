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

check "fineract charter-1k slice (~1k LOC, manifest + refs)" make charter-1k-check

check "fineract charter-10k slice (~10k LOC experiments PATH LIST)" make charter-10k-check

check "slice matrix (7 shards, rust engine validate→extract→pack→reexpand)" make slice-matrix-check

check "slice matrix (7 shards, python engine dual-stack)" \
  env WIRING_ENGINE=python bash scripts/slice_matrix_run.sh

check "scale metrics (charter LOC, recall pairs, handler WIN, matrix union LOC)" make scale-metrics-check

check "l2 pack parity all slice-matrix wiringmaps (Rust vs Python)" \
  bash scripts/l2_pack_parity_all_maps.sh

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

check "pipeline-io rejects invalid WIRING_ENGINE" \
  expect_exit 1 env WIRING_ENGINE=bogus bash scripts/pipeline_world_io.sh

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

check "CR@F95 harness stub (config validate + grade + tokens, unfilled accuracy_column)" \
  make cr-f95-stub-check

check "CR@F95 stub rejects non-null accuracy_column in run config" \
  python3 -c "
import json, subprocess, sys, tempfile, os
from pathlib import Path
ROOT = Path('${ROOT}')
cfg = json.loads((ROOT / 'experiments/cr-f95-stub/run_config.meta-l1.v0.json').read_text())
cfg['accuracy_column'] = {'accuracy': 0.99, 'fidelity_target': 0.95, 'reference_arm': 'fake', 'filled_at': '2026-01-01T00:00:00Z'}
bad = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
json.dump(cfg, bad)
bad.close()
proc = subprocess.run([sys.executable, str(ROOT / 'scripts/cr_f95_stub_run.py'), '--config', bad.name], capture_output=True)
os.unlink(bad.name)
sys.exit(0 if proc.returncode != 0 else 1)
"

check "blind pack-only eval stub (meta + handler-wedge, no answers in bundle)" \
  make pack-blind-eval-check

check "archived pack-blind results match schema and live stub grades" \
  make pack-blind-results-check

check "pack-blind results check fails when archived case count drifts" \
  python3 -c "
import json, subprocess, sys, tempfile, os
from pathlib import Path
ROOT = Path('${ROOT}')
art = json.loads((ROOT / 'experiments/pack-blind-eval/results/stub.report.v0.json').read_text())
art['cases'][0]['questions_count'] = 999
bad = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
json.dump(art, bad)
bad.close()
proc = subprocess.run(
    [sys.executable, str(ROOT / 'scripts/validate_pack_blind_results.py'), '--artifact', bad.name, '--compare-live'],
    capture_output=True, text=True, cwd=str(ROOT),
)
os.unlink(bad.name)
sys.exit(0 if proc.returncode != 0 else 1)
"

check "pulse unified eval (pack-blind + cr-f95 stub, llm_invoked false by default)" \
  python3 -c "
import json, subprocess, sys
from pathlib import Path
ROOT = Path('${ROOT}')
proc = subprocess.run(
    [sys.executable, str(ROOT / 'scripts/pulse_unified_eval_run.py')],
    capture_output=True, text=True, cwd=str(ROOT),
)
if proc.returncode != 0:
    sys.stderr.write(proc.stderr)
    sys.exit(1)
doc = json.loads(proc.stdout)
if doc.get('llm_invoked') is not False:
    sys.exit(1)
if doc.get('pack_blind_eval', {}).get('status') != 'ok':
    sys.exit(1)
if doc.get('cr_f95_stub', {}).get('status') != 'ok':
    sys.exit(1)
if len(doc.get('pack_blind_eval', {}).get('cases') or []) < 2:
    sys.exit(1)
"

check "edge-recall sample gate (toybank + thin + charter 1k/10k delta, 120+ frozen pairs)" \
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

check "meta-evaluator hook (craft index + rubric firewall)" \
  python3 scripts/meta_evaluator_hook.py --check

check "wiring-core Rust validate + java refs parity" \
  bash scripts/wiring_core_check.sh

echo ""
echo "Functional eval: ${pass} passed, ${fail} failed"
if [[ "${fail}" -gt 0 ]]; then
  exit 1
fi
exit 0
