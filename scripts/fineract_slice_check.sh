#!/usr/bin/env bash
# Interface gate for fixtures/external/fineract-handlers-thin (partial wiringmap).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLICE="${ROOT}/fixtures/external/fineract-handlers-thin"
README="${SLICE}/README.md"
WIRINGMAP="${SLICE}/wiringmap.v0.json"
SCHEMA="${ROOT}/wiringmap/schema.v0.json"
MIN_JAVA="${FINERACT_SLICE_MIN_JAVA:-5}"
MIN_REFS="${FINERACT_SLICE_MIN_REFS:-9}"

if [[ ! -f "${README}" ]]; then
  echo "ERROR: missing slice README: ${README}" >&2
  exit 1
fi

if ! grep -qi 'not.*full fineract\|not a checkout' "${README}" 2>/dev/null; then
  if ! grep -qi 'What is \*\*not\*\* included' "${README}"; then
    echo "ERROR: slice README must document omissions / not full Fineract" >&2
    exit 1
  fi
fi

java_count="$(find "${SLICE}" -maxdepth 1 -name '*.java' | wc -l | tr -d ' ')"
if [[ "${java_count}" -lt "${MIN_JAVA}" ]]; then
  echo "ERROR: expected >= ${MIN_JAVA} Java handlers, found ${java_count}" >&2
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

if [[ "${ref_tokens}" -lt "${MIN_REFS}" ]]; then
  echo "ERROR: ref_token_count=${ref_tokens} (need >= ${MIN_REFS})" >&2
  exit 1
fi

python3 "${ROOT}/scripts/validate_slice_manifest.py" --slice-dir "${SLICE}"

echo "OK: fineract-handlers-thin — ${java_count} Java files, ${ref_tokens} ref tokens, ${import_fallback} import-line fallback (unwired handlers)" >&2
