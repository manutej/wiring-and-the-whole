#!/usr/bin/env bash
# Parity: Rust wiring-extract-java-refs vs Python extract_refs.py (token set only).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

REFS_DIR="${1:?refs dir required}"
SLICE="${2:-${REFS_DIR}}"

BIN="${ROOT}/crates/wiring-core/target/release/wiring-extract-java-refs"
if [[ ! -x "${BIN}" ]]; then
  cargo build --quiet --manifest-path crates/wiring-core/Cargo.toml --release
fi

TMP_PY="$(mktemp)"
TMP_RS="$(mktemp)"
trap 'rm -f "${TMP_PY}" "${TMP_RS}"' EXIT

python3 scripts/extract_refs.py "${ROOT}/${REFS_DIR}" --no-example-check >"${TMP_PY}" 2>/dev/null
"${BIN}" "${ROOT}/${REFS_DIR}" --slice "${SLICE}" >"${TMP_RS}"

python3 - <<'PY' "${TMP_PY}" "${TMP_RS}"
import json, sys
py = json.load(open(sys.argv[1]))
rs = json.load(open(sys.argv[2]))

def pairs(doc):
    out = set()
    for fname, toks in doc["refs_by_file"].items():
        for t in toks:
            out.add((fname, t))
    return out

pp, pr = pairs(py), pairs(rs)
if py["ref_token_count"] != rs["ref_token_count"] or pp != pr:
    print("parity FAIL", file=sys.stderr)
    print("py count", py["ref_token_count"], "rs count", rs["ref_token_count"], file=sys.stderr)
    print("only py", sorted(pp - pr)[:5], file=sys.stderr)
    print("only rs", sorted(pr - pp)[:5], file=sys.stderr)
    sys.exit(1)
print(f"OK: java refs parity ({py['ref_token_count']} tokens, {len(pp)} pairs)")
PY
