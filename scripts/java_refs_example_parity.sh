#!/usr/bin/env bash
# Rust wiring-extract-java-refs --example vs Python extract_refs.py (exit code parity).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

cargo build --quiet --manifest-path crates/wiring-core/Cargo.toml --release --bins
BIN="${ROOT}/crates/wiring-core/target/release/wiring-extract-java-refs"

run_pair() {
  local refs_dir="$1"
  local wm="$2"
  local label="$3"
  if ! python3 scripts/extract_refs.py "${refs_dir}" --example "${wm}" >/dev/null 2>&1; then
    echo "ERROR: python extract failed for ${label}" >&2
    exit 1
  fi
  if ! "${BIN}" "${refs_dir}" --example "${wm}" >/dev/null 2>&1; then
    echo "ERROR: rust extract --example failed for ${label}" >&2
    exit 1
  fi
  echo "OK: java refs example parity (${label})"
}

run_pair witness/toybank/accounts wiringmap/examples/toybank-accounts.v0.json toybank-accounts
run_pair fixtures/external/fineract-handlers-thin fixtures/external/fineract-handlers-thin/wiringmap.v0.json fineract-thin
run_pair fixtures/external/fineract-charter-1k fixtures/external/fineract-charter-1k/wiringmap.v0.json charter-1k
