#!/usr/bin/env bash
# Parity: Rust wiring-build-l2-pack vs Python build_l2_pack.py (byte-identical artifacts).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

WM="${1:-wiringmap/examples/toybank-accounts.v0.json}"
WM_ABS="${ROOT}/${WM}"
LEGEND="${ROOT}/experiments/e2-tokens/pack_LEGEND.txt"

BIN="${ROOT}/crates/wiring-core/target/release/wiring-build-l2-pack"
if [[ ! -x "${BIN}" ]]; then
  cargo build --quiet --manifest-path crates/wiring-core/Cargo.toml --release
fi

TMP_PY="$(mktemp -d)"
TMP_RS="$(mktemp -d)"
trap 'rm -rf "${TMP_PY}" "${TMP_RS}"' EXIT

python3 scripts/build_l2_pack.py "${WM_ABS}" --out "${TMP_PY}/out" >/dev/null
"${BIN}" "${WM_ABS}" --out "${TMP_RS}/out" --canonical-legend "${LEGEND}" >/dev/null

for name in LEGEND.txt pack_explicit.txt pack_factored.txt; do
  if ! cmp -s "${TMP_PY}/out.pack/${name}" "${TMP_RS}/out.pack/${name}"; then
    echo "parity FAIL: ${name}" >&2
    diff -u "${TMP_PY}/out.pack/${name}" "${TMP_RS}/out.pack/${name}" >&2 || true
    exit 1
  fi
done

echo "OK: l2 pack parity (toybank, Rust ≡ Python build_l2_pack.py)"
