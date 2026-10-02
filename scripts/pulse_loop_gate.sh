#!/usr/bin/env bash
# Pulse loop engineering gate: verify + pulse-eval + role-separation checklist.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Pulse loop: make verify"
make verify

echo "==> Pulse loop: make pulse-eval"
make pulse-eval

cat <<'EOF'

==> Pulse loop checklist (human gates — see docs/pulse/LOOP-ENGINEERING.md)
  [ ] Implementer brief filed; implementer did NOT read RUBRIC-EVALUATOR.md
  [ ] Adversarial panel (separate subagents) — gaps listed, not implementer recap
  [ ] Interface tests — failure modes / cold navigation, not frozen-json echo
  [ ] Evaluator lane — firewalled SHIP | NO-SHIP stored outside implementer context
  [ ] Paris/Every research edits stayed on research lanes; no silent E2/E3/witness drift

EOF

echo "PASS pulse-loop (verify + pulse-eval + checklist)"
