#!/usr/bin/env bash
# Pulse merge gate: repro harness + operator reminders (not a substitute for evaluator).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Pulse gate: running make verify"
make verify

cat <<'EOF'

==> Pulse reminders (process gates — not automated here)
  - Adversarial panel: separate subagents; output gaps before merge.
  - Evaluator: score using docs/pulse/RUBRIC-EVALUATOR.md
    Implementer must NOT receive that rubric during the same pulse.
  - Interface tests: failure modes and reader navigation — not frozen-json echo.
  - See docs/PULSE.md for the full loop.

EOF

echo "PASS pulse-gate (verify + reminders)"
