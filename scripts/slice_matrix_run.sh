#!/usr/bin/env bash
# Run validate → extract → pack → reexpand for each entry in fixtures/slice-matrix/manifest.v0.json.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

MANIFEST="${ROOT}/fixtures/slice-matrix/manifest.v0.json"
SCHEMA="${ROOT}/wiringmap/schema.v0.json"
WIRING_ENGINE="${WIRING_ENGINE:-rust}"
CRATE="${ROOT}/crates/wiring-core"
CANONICAL_LEGEND="${ROOT}/experiments/e2-tokens/pack_LEGEND.txt"

fail() { echo "SLICE MATRIX FAIL: $*" >&2; exit 1; }

case "${WIRING_ENGINE}" in
  rust|python) ;;
  *) fail "invalid WIRING_ENGINE=${WIRING_ENGINE} (want rust|python)" ;;
esac

ensure_engine() {
  if [[ "${WIRING_ENGINE}" == "rust" ]]; then
    if ! command -v cargo >/dev/null 2>&1; then
      fail "WIRING_ENGINE=rust but cargo not installed"
    fi
    cargo build --quiet --manifest-path "${CRATE}/Cargo.toml" --release --bins
  fi
}

validate_wm() {
  local inst="$1"
  if [[ "${WIRING_ENGINE}" == "rust" ]]; then
    "${CRATE}/target/release/wiring-validate" --schema "${SCHEMA}" --instance "${inst}"
  else
    python3 "${ROOT}/scripts/validate_wiringmap.py" "${SCHEMA}" "${inst}"
  fi
}

extract_refs() {
  local refs_dir="$1"
  local wm="$2"
  if [[ "${WIRING_ENGINE}" == "rust" ]]; then
    "${CRATE}/target/release/wiring-extract-java-refs" "${refs_dir}" --example "${wm}" >/dev/null
  else
    python3 "${ROOT}/scripts/extract_refs.py" "${refs_dir}" --example "${wm}" >/dev/null
  fi
}

build_pack() {
  local wm="$1"
  if [[ "${WIRING_ENGINE}" == "rust" ]]; then
    "${CRATE}/target/release/wiring-build-l2-pack" "${wm}" --canonical-legend "${CANONICAL_LEGEND}" >/dev/null
  else
    python3 "${ROOT}/scripts/build_l2_pack.py" "${wm}" >/dev/null
  fi
}

reexpand_pack() {
  local pack_dir="$1"
  if [[ "${WIRING_ENGINE}" == "rust" ]]; then
    "${CRATE}/target/release/wiring-reexpand" "${pack_dir}" --canonical-legend "${CANONICAL_LEGEND}" >/dev/null
  else
    python3 "${ROOT}/scripts/reexpand_gate.py" "${pack_dir}" >/dev/null
  fi
}

run_slice() {
  local sid="$1"
  local refs_rel="$2"
  local wm_rel="$3"
  local refs="${ROOT}/${refs_rel}"
  local wm="${ROOT}/${wm_rel}"
  local work
  work="$(mktemp -d)"
  validate_wm "${wm}" > "${work}/validate.out" 2>&1 || fail "${sid}: validate"
  extract_refs "${refs}" "${wm}" 2> "${work}/extract.stderr" || fail "${sid}: extract"
  build_pack "${wm}" || fail "${sid}: pack"
  local pack="${wm%.json}.pack"
  cp -a "${pack}" "${work}/pack/"
  reexpand_pack "${work}/pack" > "${work}/reexpand.out" 2>&1 || fail "${sid}: reexpand"
  rm -rf "${work}"
}

ensure_engine

SLICE_IDS=()
while read -r sid refs_rel wm_rel; do
  [[ -n "${sid}" ]] || continue
  run_slice "${sid}" "${refs_rel}" "${wm_rel}"
  SLICE_IDS+=("${sid}")
done < <(
  python3 -c "
import json
from pathlib import Path
doc = json.loads(Path('${MANIFEST}').read_text())
for s in doc['slices']:
    print(s['id'], s['refs_dir'], s['wiringmap'])
"
)

python3 -c "
import json
from pathlib import Path
doc = json.loads(Path('fixtures/slice-matrix/manifest.v0.json').read_text())
print(json.dumps({
    'status': 'ok',
    'wiring_engine': '${WIRING_ENGINE}',
    'slice_count': len(doc['slices']),
    'slices': [s['id'] for s in doc['slices']],
}, indent=2))
"

echo "SLICE MATRIX PASS: ${#SLICE_IDS[@]} slices (engine=${WIRING_ENGINE})" >&2
