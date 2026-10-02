#!/usr/bin/env bash
# I/O check: dry-run fetch reports one staged file per slice inventory entry.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SLICE="${ROOT}/fixtures/external/fineract-handlers-thin"

on_disk="$(find "${SLICE}" -maxdepth 1 -type f -printf '%f\n' | sort | wc -l | tr -d ' ')"

capture="$(mktemp)"
trap 'rm -f "${capture}"' EXIT
bash "${ROOT}/scripts/fetch_fineract_slice.sh" > "${capture}" 2>&1

staged_lines="$(grep -cE '^\s+staged \(' "${capture}" || true)"
if [[ "${staged_lines}" -eq 0 ]]; then
  echo "FAIL fetch I/O: no staged lines in fetch output" >&2
  cat "${capture}" >&2
  exit 1
fi

if [[ "${on_disk}" -ne "${staged_lines}" ]]; then
  echo "FAIL fetch I/O: on_disk=${on_disk} staged_lines=${staged_lines}" >&2
  exit 1
fi

echo "OK: fetch dry-run staged ${staged_lines} files (matches slice inventory ${on_disk})" >&2
exit 0
