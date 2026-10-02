# Pulse executive report — specification

Post-pulse **operator-facing** summary for the user. One report file per pulse round; plain English only in the body (no rubric scores in this artifact — those stay firewalled per [`RUBRIC-EVALUATOR.md`](RUBRIC-EVALUATOR.md)).

## When to write

After merge gate (`make verify`, `make pulse-eval` or `make pulse-loop`) and before or with PR close. Implementer may draft; operator owns accuracy.

## File location

`docs/pulse/reports/YYYY-MM-DD-<topic>.md` — copy from [`reports/TEMPLATE.md`](reports/TEMPLATE.md).

## Metadata block (required)

YAML front matter or a fixed `## Metadata` table:

| Field | Description |
|-------|-------------|
| `pulse_id` | Stable slug, e.g. `2026-10-02-pulse-meaty` |
| `started_at_utc` | Wall-clock ISO-8601 when implement scope locked |
| `ended_at_utc` | Wall-clock ISO-8601 when merge gate last passed |
| `duration_minutes` | Rounded wall-clock minutes (end − start) |
| `branch` | Feature branch name |
| `pr` | PR URL or `pending` |
| `agents` | Table: role, agent id (bcId or human), model |

### Agents table (required columns)

| role | id | model |
|------|-----|-------|
| implementer | … | … |
| adversarial panel | … | … |
| evaluator | … | optional if deferred |

## Body — exactly three sections × three bullets

Each section has **exactly three** bullet points. Short sentences; no jargon without a one-clause gloss.

### 1. Done

What shipped in this pulse (artifacts, gates, docs). Past tense.

### 2. Tested

What was executed and passed (commands, failure-mode probes). Not a re-list of `make verify` alone unless that was the scoped work.

### 3. Next

Honest follow-ups (scale gaps, deferred MUST-PROVE, next pulse topic). No fake commitments.

## Links

- Operator protocol: [`docs/PULSE.md`](../PULSE.md)
- Harness vs deep pulse: [`PULSE-DEPTH.md`](PULSE-DEPTH.md)
- Loop + Paris: [`LOOP-ENGINEERING.md`](LOOP-ENGINEERING.md)
- Agent store pointer: [`/cursor/stores/self/pulse-reporting.md`](/cursor/stores/self/pulse-reporting.md)
