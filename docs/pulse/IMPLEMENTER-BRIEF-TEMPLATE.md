# Implementer brief (pulse) — template

Copy this file per pulse (e.g. `docs/pulse/briefs/YYYY-MM-DD-topic.md`). Give **only** the filled brief to the implementer subagent.

## Forbidden

- **Do not read** [`RUBRIC-EVALUATOR.md`](RUBRIC-EVALUATOR.md) or any evaluator-only brief during this pulse.
- Do not score your own work against hidden rubrics; leave that to the evaluator lane.

## Pulse metadata

| Field | Value |
|-------|--------|
| Pulse ID | |
| Branch | |
| Operator | |
| Date | |

## Scope

**One primary deliverable (Pocock small-PR rule):** pick exactly one of — Paris registry row adoption · WiringMap v0 slice edge · SKILL.md + one L1 hook · programme gate script only.

**In:**

-

**Out:**

-

## Done criteria

- [ ]
- [ ]
- [ ]

## Claims & provenance

- Ladder rung touched (if any):
- CONJECTURE / DESIGN labels needed:
- Frozen artifacts that may change (E2-RESULTS.json, E3-GRADES.json, WITNESS.json):

## Commands

- Verify: `make verify`
- Research lane (if Paris JSON or kit touched): `make verify-research`
- Pulse gate: `make pulse-gate` (verify + verify-research when Paris dir exists)
- Functional eval (wiringmap / pack / L1): `make pulse-eval`
- Witness only: `make witness`

## Handoff to adversarial panel

After implementation, stop and hand off:

- Diff summary (files + intent)
- Open questions
- What you did **not** test

## Handoff to evaluator

Implementer does **not** write the rubric. Operator provides evaluator with artifacts + PR link only.
