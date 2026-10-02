#!/usr/bin/env bash
# Pulse merge gate: repro harness + operator reminders (not a substitute for evaluator).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Pulse gate: running make verify"
make verify

if [[ -d "${ROOT}/research/ai-engineer-paris-2026" ]]; then
  echo "==> Pulse gate: running make verify-research (Paris lane present)"
  make verify-research
fi

cat <<'EOF'

==> Pulse reminders (process gates — not automated here)
  - Small PR discipline (Pocock): one registry adoption OR one wiringmap slice OR one SKILL+L1 pair per pulse.
  - Adversarial panel: separate subagents; output gaps before merge.
  - Evaluator: score using docs/pulse/RUBRIC-EVALUATOR.md
    Implementer must NOT receive that rubric during the same pulse.
  - Interface tests: run make pulse-eval when scope touches wiringmap, pack, or L1 dogfood.
  - Merge blocked until adversarial notes + pulse-eval (if applicable) + evaluator SHIP.
  - See docs/PULSE.md and docs/roadmap/CONSENSUS-FORWARD.md for the full loop.

EOF

echo "PASS pulse-gate (verify + research sync + reminders)"
