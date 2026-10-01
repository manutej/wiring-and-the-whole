#!/usr/bin/env bash
# fetch_fineract_slice.sh — Refresh fixtures/external/fineract-handlers-thin without a full-tree checkout.
#
# PATH LIST only (no sparse clone of the entire upstream tree). Supported patterns:
#
#   1. git sparse-checkout (throwaway worktree)
#        git clone --filter=blob:none --no-checkout "${FINERACT_UPSTREAM_REPO}" "${WORKDIR}"
#        cd "${WORKDIR}" && git sparse-checkout init --cone
#        git sparse-checkout set "${UPSTREAM_PATH_1}" "${UPSTREAM_PATH_2}" ...
#        git checkout "${FINERACT_UPSTREAM_REF}"
#
#   2. git archive (explicit path list; server must support upload-archive)
#        git archive --remote="${FINERACT_UPSTREAM_REPO}" "${FINERACT_UPSTREAM_REF}" \
#          -- "${UPSTREAM_PATH_1}" "${UPSTREAM_PATH_2}" | tar -x -C "${STAGING}"
#
#   3. curl raw (GitHub-style; one request per path — still no full tree)
#        curl -fsSL "https://raw.githubusercontent.com/apache/fineract/${REF}/${UPSTREAM_PATH}" \
#          -o "${STAGING}/$(basename "${UPSTREAM_PATH}")"
#
# Default PATH LIST = basenames currently under fixtures/external/fineract-handlers-thin/.
# Upstream path mapping for *.java is optional (FINERACT_UPSTREAM_JAVA_PREFIX); wiringmap and
# README are in-repo curated artifacts and are not fetched from upstream in this stub.
#
# Usage:
#   ./scripts/fetch_fineract_slice.sh              # dry-run (default): stage plan under temp dir
#   ./scripts/fetch_fineract_slice.sh --apply      # copy staged slice into fixtures + MANIFEST.txt
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SLICE_DIR="${ROOT}/fixtures/external/fineract-handlers-thin"
LOCAL_JAVA_CORPUS="${ROOT}/experiments/e3-ablation/raw"

FINERACT_UPSTREAM_REPO="${FINERACT_UPSTREAM_REPO:-https://github.com/apache/fineract.git}"
FINERACT_UPSTREAM_REF="${FINERACT_UPSTREAM_REF:-develop}"
# Example Fineract layout for command handlers (override per pulse when pinning paths).
FINERACT_UPSTREAM_JAVA_PREFIX="${FINERACT_UPSTREAM_JAVA_PREFIX:-fineract-provider/src/main/java/org/apache/fineract/portfolio}"

APPLY=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply) APPLY=1; shift ;;
    --dry-run) APPLY=0; shift ;;
    -h|--help)
      sed -n '2,30p' "$0"
      exit 0
      ;;
    *)
      echo "ERROR: unknown argument: $1 (use --dry-run or --apply)" >&2
      exit 2
      ;;
  esac
done

if [[ ! -d "${SLICE_DIR}" ]]; then
  echo "ERROR: slice directory missing: ${SLICE_DIR}" >&2
  exit 1
fi

mapfile -t DEFAULT_PATHS < <(
  find "${SLICE_DIR}" -maxdepth 1 -type f -printf '%f\n' | sort
)

if [[ ${#DEFAULT_PATHS[@]} -eq 0 ]]; then
  echo "ERROR: no files in ${SLICE_DIR}" >&2
  exit 1
fi

STAGING="$(mktemp -d "${TMPDIR:-/tmp}/fineract-slice.XXXXXX")"
cleanup() { rm -rf "${STAGING}"; }
if [[ "${APPLY}" -eq 0 ]]; then
  trap cleanup EXIT
fi

PATH_LIST_FILE="${STAGING}/PATH_LIST.txt"
printf '%s\n' "${DEFAULT_PATHS[@]}" > "${PATH_LIST_FILE}"

upstream_java_path() {
  local base="$1"
  printf '%s/**/handler/%s' "${FINERACT_UPSTREAM_JAVA_PREFIX}" "${base}"
}

PLAN_FILE="${STAGING}/FETCH_PLAN.txt"
{
  echo "mode=$([[ "${APPLY}" -eq 1 ]] && echo apply || echo dry-run)"
  echo "upstream_repo=${FINERACT_UPSTREAM_REPO}"
  echo "upstream_ref=${FINERACT_UPSTREAM_REF}"
  echo "staging=${STAGING}"
  echo "slice_dir=${SLICE_DIR}"
  echo ""
  echo "# sparse-checkout path set (upstream paths for *.java only):"
  for name in "${DEFAULT_PATHS[@]}"; do
    case "${name}" in
      *.java) echo "$(upstream_java_path "${name}")" ;;
      *) echo "# skip upstream fetch (in-repo): ${name}" ;;
    esac
  done
  echo ""
  echo "# git archive example (requires upload-archive support on remote):"
  echo "# git archive --remote=\"${FINERACT_UPSTREAM_REPO}\" \"${FINERACT_UPSTREAM_REF}\" \\"
  for name in "${DEFAULT_PATHS[@]}"; do
    case "${name}" in
      *.java) echo "#   -- \"$(upstream_java_path "${name}")\" \\" ;;
    esac
  done
  echo "#   | tar -x -C \"${STAGING}\""
} > "${PLAN_FILE}"

stage_java_from_local_corpus() {
  local name="$1"
  local src="${LOCAL_JAVA_CORPUS}/${name}"
  if [[ ! -f "${src}" ]]; then
    echo "ERROR: missing local corpus file for stub staging: ${src}" >&2
    return 1
  fi
  cp "${src}" "${STAGING}/${name}"
}

stage_in_repo_artifact() {
  local name="$1"
  cp "${SLICE_DIR}/${name}" "${STAGING}/${name}"
}

echo "==> fetch_fineract_slice ($([[ "${APPLY}" -eq 1 ]] && echo apply || echo dry-run))"
echo "    staging: ${STAGING}"
echo "    path list: ${PATH_LIST_FILE}"
echo "    plan: ${PLAN_FILE}"

for name in "${DEFAULT_PATHS[@]}"; do
  case "${name}" in
    *.java)
      stage_java_from_local_corpus "${name}"
      echo "    staged (local corpus stub): ${name}"
      ;;
    *)
      stage_in_repo_artifact "${name}"
      echo "    staged (in-repo artifact): ${name}"
      ;;
  esac
done

if [[ "${APPLY}" -eq 0 ]]; then
  echo "OK: dry-run — staged under temp dir only; fixtures unchanged"
  echo "    re-run with --apply to copy into ${SLICE_DIR}"
  exit 0
fi

MANIFEST="${SLICE_DIR}/MANIFEST.txt"
FETCHED_AT="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

for name in "${DEFAULT_PATHS[@]}"; do
  cp "${STAGING}/${name}" "${SLICE_DIR}/${name}"
done

{
  echo "source_repo=${FINERACT_UPSTREAM_REPO}"
  echo "source_commit=manual pin"
  echo "source_ref=${FINERACT_UPSTREAM_REF}"
  echo "fetched_at=${FETCHED_AT}"
  echo "fetch_mode=stub (local corpus for *.java; in-repo wiringmap/README)"
  echo "path_list_file=PATH_LIST.txt"
  echo ""
  echo "# paths applied:"
  printf '%s\n' "${DEFAULT_PATHS[@]}"
} > "${MANIFEST}"

echo "OK: apply — updated ${SLICE_DIR} (${#DEFAULT_PATHS[@]} files)"
echo "    manifest: ${MANIFEST}"
rm -rf "${STAGING}"
exit 0
