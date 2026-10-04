#!/usr/bin/env bash
# Gate for fixtures/external/fineract-charter-10k (~10k LOC scale charter).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLICE="${ROOT}/fixtures/external/fineract-charter-10k"
WIRINGMAP="${SLICE}/wiringmap.v0.json"
SCHEMA="${ROOT}/wiringmap/schema.v0.json"
MIN_LOC="${CHARTER_10K_MIN_LOC:-8500}"
MAX_LOC="${CHARTER_10K_MAX_LOC:-11000}"
MIN_HANDLERS="${CHARTER_10K_MIN_HANDLERS:-29}"
MIN_REFS="${CHARTER_10K_MIN_REFS:-85}"

[[ -f "${SLICE}/README.md" ]] || { echo "ERROR: missing README" >&2; exit 1; }

loc="$(find "${SLICE}" -maxdepth 1 -name '*.java' -exec cat {} + | wc -l | tr -d ' ')"
if [[ "${loc}" -lt "${MIN_LOC}" || "${loc}" -gt "${MAX_LOC}" ]]; then
  echo "ERROR: charter-10k LOC ${loc} outside [${MIN_LOC}, ${MAX_LOC}]" >&2
  exit 1
fi

handler_count="$(find "${SLICE}" -maxdepth 1 -name '*CommandHandler.java' | wc -l | tr -d ' ')"
if [[ "${handler_count}" -lt "${MIN_HANDLERS}" ]]; then
  echo "ERROR: expected >= ${MIN_HANDLERS} handlers, found ${handler_count}" >&2
  exit 1
fi

python3 -m pip install -q jsonschema
python3 "${ROOT}/scripts/validate_wiringmap.py" "${SCHEMA}" "${WIRINGMAP}"

extract_json="$(python3 "${ROOT}/scripts/extract_refs.py" "${SLICE}" --example "${WIRINGMAP}")"
ref_tokens="$(python3 -c "import json,sys; print(json.loads(sys.argv[1])['ref_token_count'])" "${extract_json}")"
if [[ "${ref_tokens}" -lt "${MIN_REFS}" ]]; then
  echo "ERROR: ref_token_count=${ref_tokens} (need >= ${MIN_REFS})" >&2
  exit 1
fi

import_fallback=0
while IFS= read -r -d '' f; do
  [[ "$(basename "$f")" == *CommandHandler.java ]] || continue
  if grep -q '// refs:' "${f}"; then
    continue
  fi
  n="$(grep -cE '^import org\.apache\.fineract\.' "${f}" || true)"
  import_fallback=$((import_fallback + n))
done < <(find "${SLICE}" -maxdepth 1 -name '*CommandHandler.java' -print0)

if [[ "${import_fallback}" -gt 0 ]]; then
  echo "ERROR: handler import-line fallback=${import_fallback}; add // refs:" >&2
  exit 1
fi

python3 "${ROOT}/scripts/validate_slice_manifest.py" --slice-dir "${SLICE}"

echo "OK: fineract-charter-10k — ${handler_count} handlers, ${loc} LOC, ${ref_tokens} ref tokens" >&2
