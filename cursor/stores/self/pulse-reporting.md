# Pulse reporting (cloud agent)

When a user or automation asks for a **post-pulse executive report**:

1. Read [`docs/pulse/PULSE-REPORT-SPEC.md`](../../../docs/pulse/PULSE-REPORT-SPEC.md) (**APPROVED 2026-10-02**).
2. Fill `docs/pulse/reports/YYYY-MM-DD-<topic>.md` from [`docs/pulse/reports/TEMPLATE.md`](../../../docs/pulse/reports/TEMPLATE.md).
3. **No jargon anywhere** in the shipped report — metadata, tables, and **3 sections × 3 bullets** (Done, Tested, Next) in plain language.
4. Record **wall-clock** UTC start/end and derived duration; link branch + PR.
5. Table **agents** (Role, Who, Notes) — include this run's cloud agent id under **Who** when known (`cursor-cloud` `run-info`).
6. Do **not** paste rubric scores into the executive report; evaluator output stays separate.
7. After merge to `main`, bump honest limits in [`docs/CONTEXT-COMPACT.md`](../../../docs/CONTEXT-COMPACT.md) if harness counts or claims changed.

Related: [`docs/PULSE.md`](../../../docs/PULSE.md), [`docs/pulse/PULSE-DEPTH.md`](../../../docs/pulse/PULSE-DEPTH.md), [`docs/pulse/LOOP-ENGINEERING.md`](../../../docs/pulse/LOOP-ENGINEERING.md), [`pulse-protocol.md`](pulse-protocol.md) (if present).
