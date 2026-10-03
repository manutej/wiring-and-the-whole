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
