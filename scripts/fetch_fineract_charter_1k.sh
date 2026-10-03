#!/usr/bin/env bash
# Refresh fixtures/external/fineract-charter-1k from local e3 corpus (PATH LIST stub).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SLICE_DIR="${ROOT}/fixtures/external/fineract-charter-1k"
LOCAL_JAVA_CORPUS="${ROOT}/experiments/e3-ablation/raw"

APPLY=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply) APPLY=1; shift ;;
    --dry-run) APPLY=0; shift ;;
    -h|--help)
      echo "Usage: $0 [--dry-run|--apply]  # re-bootstrap charter from e3 raw + wiringmap"
      exit 0
      ;;
    *) echo "ERROR: unknown argument: $1" >&2; exit 2 ;;
  esac
done

if [[ "${APPLY}" -eq 0 ]]; then
  echo "OK: dry-run — would run scripts/bootstrap_fineract_charter_1k.py"
  exit 0
fi

python3 "${ROOT}/scripts/bootstrap_fineract_charter_1k.py"
echo "OK: charter-1k apply — see ${SLICE_DIR}/MANIFEST.txt"
