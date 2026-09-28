#!/usr/bin/env sh
# Reproducibility gate: rebuild every generated artifact and fail if anything
# committed under witness/ or experiments/ changes. This is the frozen-hash
# discipline as a mechanical check instead of prose. Requires node + `npm ci`
# in experiments/ (for the cl100k tokenizer); everything else is stdlib Python.
set -eu
cd "$(dirname "$0")/.."
python3 witness/run_witness.py            > /dev/null
python3 experiments/e2-tokens/e2_run.py   > /dev/null
python3 experiments/e3-ablation/e3_build.py > /dev/null
python3 experiments/e3-ablation/e3_grade.py > /dev/null
python3 experiments/e5-depth/e5_build.py  > /dev/null
python3 experiments/e5-depth/e5_grade.py  > /dev/null
python3 experiments/e5-depth/e5_grade2.py > /dev/null
changed=$(git status --porcelain -- witness experiments)
if [ -n "$changed" ]; then
  echo "REPRODUCIBILITY GATE FAILED: regenerated artifacts differ from committed:" >&2
  echo "$changed" >&2
  git --no-pager diff --stat -- witness experiments >&2
  exit 1
fi
echo "reproducibility gate: OK (witness 13 checks, E2/E3/E5 packs, E3/E5 grades unchanged)"
