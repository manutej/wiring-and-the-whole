# Pulse reporting (cloud agent)

When a user or automation asks for a **post-pulse executive report**:

1. Read [`docs/pulse/PULSE-REPORT-SPEC.md`](../../../docs/pulse/PULSE-REPORT-SPEC.md).
2. Fill `docs/pulse/reports/YYYY-MM-DD-<topic>.md` from [`docs/pulse/reports/TEMPLATE.md`](../../../docs/pulse/reports/TEMPLATE.md).
3. Use **3 sections × 3 bullets** (Done, Tested, Next) in plain English.
4. Record **wall-clock** UTC start/end and derived duration; link branch + PR.
5. Table **agents** (role, id, model) — include this run's bcId when known (`cursor-cloud` `run-info`).
6. Do **not** paste rubric scores into the executive report; evaluator output stays separate.
7. After merge to `main`, bump honest limits in [`docs/CONTEXT-COMPACT.md`](../../../docs/CONTEXT-COMPACT.md) if harness counts or claims changed.

Related: [`docs/PULSE.md`](../../../docs/PULSE.md), [`pulse-protocol.md`](pulse-protocol.md) (if present).
