#!/usr/bin/env bash
# Phase 1: Rust wiring-validate parity gate on frozen WiringMap instances.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

SCHEMA="${ROOT}/wiringmap/schema.v0.json"
CRATE="${ROOT}/crates/wiring-core"

if ! command -v cargo >/dev/null 2>&1; then
  echo "SKIP: cargo not installed" >&2
  exit 0
fi

cargo build --quiet --manifest-path "${CRATE}/Cargo.toml" --release
BIN="${CRATE}/target/release/wiring-validate"

INSTANCES=(
  "wiringmap/examples/toybank-accounts.v0.json"
  "wiringmap/examples/repo-rust-spine.v0.json"
  "fixtures/external/fineract-handlers-thin/wiringmap.v0.json"
)

for rel in "${INSTANCES[@]}"; do
  inst="${ROOT}/${rel}"
  if [[ ! -f "${inst}" ]]; then
    echo "ERROR: missing instance ${rel}" >&2
    exit 1
  fi
  "${BIN}" --schema "${SCHEMA}" --instance "${inst}"
  python3 -m pip install -q jsonschema 2>/dev/null || true
  python3 scripts/validate_wiringmap.py "${SCHEMA}" "${inst}" >/dev/null
done

echo "OK: wiring-core validate parity (${#INSTANCES[@]} instances, Rust + Python)"

bash scripts/java_refs_parity.sh witness/toybank/accounts witness/toybank/accounts
bash scripts/java_refs_parity.sh fixtures/external/fineract-handlers-thin fixtures/external/fineract-handlers-thin

REEXPAND_BIN="${CRATE}/target/release/wiring-reexpand"
PACK="${ROOT}/wiringmap/examples/toybank-accounts.v0.pack"
CANONICAL_LEGEND="${ROOT}/experiments/e2-tokens/pack_LEGEND.txt"
if [[ ! -f "${PACK}/pack_explicit.txt" ]]; then
  echo "ERROR: missing toybank pack at ${PACK}" >&2
  exit 1
fi
"${REEXPAND_BIN}" "${PACK}" --canonical-legend "${CANONICAL_LEGEND}"
echo "OK: wiring-core reexpand gate (toybank pack, Rust parity with reexpand_gate.py)"
