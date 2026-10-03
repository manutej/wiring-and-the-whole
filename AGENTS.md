# Agent notes — wiring-and-the-whole

## Pulse reporting (operator-facing)

After every **meaty pulse** (not a quick `make pulse-loop` only):

1. Follow [`docs/pulse/PULSE-REPORT-SPEC.md`](docs/pulse/PULSE-REPORT-SPEC.md) (**APPROVED** — entire report in plain language, no jargon).
2. Write [`docs/pulse/reports/YYYY-MM-DD-<topic>.md`](docs/pulse/reports/TEMPLATE.md) with duration (UTC), branch, PR link, and agents table.
3. Run `make verify` and `make pulse-loop`; record pass/fail in the report **Tested** section.

Cloud agents: also read [`cursor/stores/self/pulse-reporting.md`](cursor/stores/self/pulse-reporting.md) when present in the environment.

Cold start: [`docs/CONTEXT-COMPACT.md`](docs/CONTEXT-COMPACT.md) · Scale: [`docs/SCALE-PATH.md`](docs/SCALE-PATH.md) · Loop roles: [`docs/pulse/LOOP-ENGINEERING.md`](docs/pulse/LOOP-ENGINEERING.md).

Post-loop (after firewalled evaluator): `make meta-evaluator` — see [`docs/pulse/META-EVALUATOR.md`](docs/pulse/META-EVALUATOR.md) and external craft index [`docs/pulse/CRAFT-SKILLS-INTEGRATION.md`](docs/pulse/CRAFT-SKILLS-INTEGRATION.md). Implementers mid-pulse must not read [`docs/pulse/RUBRIC-EVALUATOR.md`](docs/pulse/RUBRIC-EVALUATOR.md).

## Adversarial + evaluator (mandatory separation)

- **Implementers must not** write `docs/pulse/evaluations/*` SHIP/NO-SHIP for their own PR, merge the PR based on self-review, or label their recap “adversarial.”
- **Adversarial panel** — separate agent or human; output under `docs/pulse/adversarial/` (independent filename suffix `-independent` when the implementer already shipped).
- **Evaluator** — separate from implementer and adversarial author; output under `docs/pulse/evaluations/`; merge only when this verdict is **SHIP** (or documented deferral with user consent).
- When only one agent is available: **stop after implement + gates**, then spawn a **fresh** subagent with no implementer chain-of-thought for adversarial + eval before merge.
