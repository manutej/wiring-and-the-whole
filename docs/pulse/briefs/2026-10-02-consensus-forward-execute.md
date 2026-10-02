# Implementer brief — consensus forward execution

Copy for implementer lane only. Evaluator uses `RUBRIC-EVALUATOR.md` separately.

## Forbidden

- Do not read `RUBRIC-EVALUATOR.md` during this pulse.

## Pulse metadata

| Field | Value |
|-------|--------|
| Pulse ID | R5-consensus-forward-execute |
| Branch | `cursor/ai-engineer-paris-research-8e4f` |
| Operator | cloud agent |
| Date | 2026-10-02 |

## Scope

**One primary deliverable:** Paris lane hygiene + pulse wiring + one registry adoption + one Fineract wiringmap edge.

**In:**

- `make verify-research` in pulse gate path; CONTEXT-COMPACT + implementer template updates
- Adopt `wb-covariant-evals` into `skills/systems-intake/SKILL.md`
- Fourth handler (`MarkLoanAsFraud`) on fineract-thin wiringmap with matching `// refs:`
- Paris `.gitignore`, README ingest policy

**Out:**

- TubeAlfred live ingest (credits 0)
- Explorer UI / node_modules commits
- Witness / E2 / E3 frozen JSON changes

## Done criteria

- [x] `make verify` PASS
- [x] `make verify-research` PASS (degraded ingest warn OK)
- [x] `make external-slice-check` PASS after wiringmap edge
- [x] `paris-2026.yaml` rows `wb-covariant-evals` and `pocock-pr-skills` marked `adopted` where implemented

## Claims & provenance

- Ladder: DESIGN only (skills + fixtures slice)
- Frozen artifacts: none

## Commands

```bash
make verify
make verify-research
make external-slice-check
make pulse-gate
make pulse-eval   # if programme paths touched beyond research-only docs
```

## Handoff to adversarial panel

- Diff summary, kit/data sync status, whether ingest degraded flag is visible
- Open: remaining 3 unwired Fineract handlers; Every branch separate lane

## Handoff to evaluator

- PR link + this brief + adversarial notes (operator supplies rubric separately)
