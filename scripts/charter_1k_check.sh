#!/usr/bin/env bash
# Interface gate for fixtures/external/fineract-charter-1k (chartered ~1k LOC vertical).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLICE="${ROOT}/fixtures/external/fineract-charter-1k"
README="${SLICE}/README.md"
WIRINGMAP="${SLICE}/wiringmap.v0.json"
SCHEMA="${ROOT}/wiringmap/schema.v0.json"
MIN_JAVA="${CHARTER_1K_MIN_JAVA:-25}"
MIN_REFS="${CHARTER_1K_MIN_REFS:-60}"
MAX_IMPORT_FALLBACK="${CHARTER_1K_MAX_IMPORT_FALLBACK:-0}"

if [[ ! -f "${README}" ]]; then
  echo "ERROR: missing slice README: ${README}" >&2
  exit 1
fi

if ! grep -qi 'not.*fineract\|not a checkout' "${README}" 2>/dev/null; then
  echo "ERROR: charter README must document not full Fineract" >&2
  exit 1
fi

java_count="$(find "${SLICE}" -maxdepth 1 -name '*.java' | wc -l | tr -d ' ')"
if [[ "${java_count}" -lt "${MIN_JAVA}" ]]; then
  echo "ERROR: expected >= ${MIN_JAVA} Java handlers, found ${java_count}" >&2
  exit 1
fi

loc="$(find "${SLICE}" -maxdepth 1 -name '*.java' -exec cat {} + | wc -l | tr -d ' ')"
if [[ "${loc}" -lt 900 || "${loc}" -gt 1600 ]]; then
  echo "ERROR: charter LOC ${loc} outside expected ~1k band (900–1600)" >&2
  exit 1
fi

python3 -m pip install -q jsonschema
python3 "${ROOT}/scripts/validate_wiringmap.py" "${SCHEMA}" "${WIRINGMAP}"

extract_json="$(python3 "${ROOT}/scripts/extract_refs.py" "${SLICE}" --example "${WIRINGMAP}")"
ref_tokens="$(python3 -c "import json,sys; print(json.loads(sys.argv[1])['ref_token_count'])" "${extract_json}")"

import_fallback=0
while IFS= read -r -d '' f; do
  if grep -q '// refs:' "${f}"; then
    continue
  fi
  n="$(grep -cE '^import org\.apache\.fineract\.' "${f}" || true)"
  import_fallback=$((import_fallback + n))
done < <(find "${SLICE}" -maxdepth 1 -name '*.java' -print0)

if [[ "${import_fallback}" -gt "${MAX_IMPORT_FALLBACK}" ]]; then
  echo "ERROR: import-line fallback=${import_fallback} (max ${MAX_IMPORT_FALLBACK}); add // refs:" >&2
  exit 1
fi

if [[ "${ref_tokens}" -lt "${MIN_REFS}" ]]; then
  echo "ERROR: ref_token_count=${ref_tokens} (need >= ${MIN_REFS})" >&2
  exit 1
fi

python3 "${ROOT}/scripts/validate_slice_manifest.py" --slice-dir "${SLICE}"

echo "OK: fineract-charter-1k — ${java_count} Java files, ${loc} LOC, ${ref_tokens} ref tokens" >&2
