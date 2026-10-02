# Pulse executive report — specification

> **APPROVED** — 2026-10-02 — Operator rule: the **entire** executive report — metadata tables, agent table, and all three body sections — must use **plain language with no jargon**. If a term is repo-internal (gate names, artifact slugs, rubric labels), rewrite it for a reader who only sees this one file. Rubric scores stay out of this artifact per [`RUBRIC-EVALUATOR.md`](RUBRIC-EVALUATOR.md).

Post-pulse **operator-facing** summary for the user. One report file per pulse round.

## When to write

After merge gate (`make verify`, `make pulse-eval` or `make pulse-loop`) and before or with PR close. Implementer may draft; operator owns accuracy.

## File location

`docs/pulse/reports/YYYY-MM-DD-<topic>.md` — copy from [`reports/TEMPLATE.md`](reports/TEMPLATE.md).

## Metadata block (required)

Use a `## Metadata` table. **Plain-language row labels** in the shipped report (examples below). ISO-8601 times stay in UTC.

| Row label (plain) | What to record |
|-------------------|----------------|
| Pulse round name | Stable slug, e.g. `2026-10-02-pulse-meaty` |
| Start time (UTC) | When implement scope locked |
| End time (UTC) | When merge gate last passed |
| How long (minutes) | Rounded wall-clock minutes (end − start) |
| Working branch | Feature branch name |
| Pull request | URL or `pending` |

Optional **gate timing** table (plain labels): name each check in everyday words (e.g. “Full repo witness check”, “Automated pulse test battery run 1”) and elapsed wall time.

### Agents table (required)

| Role | Who | Notes |
|------|-----|-------|
| Builder | cloud agent id or human | model or “human” |
| Challenge reviewers | … | separate panel when used |
| Independent scorer | … | optional if deferred |

Use the **Role / Who / Notes** column headers in the report file (not internal ids like bcId unless listed under **Who**).

## Body — exactly three sections × three bullets

Each section has **exactly three** bullet points. Short sentences; **no jargon** (same rule as metadata).

### 1. Done

What shipped in this pulse (artifacts, gates, docs). Past tense.

### 2. Tested

What was executed and passed (checks, deliberate failure probes). Not a re-list of the default repo check alone unless that was the scoped work.

### 3. Next

Honest follow-ups (scale gaps, deferred proof items, next pulse topic). No fake commitments.

## Links

- Operator protocol: [`docs/PULSE.md`](../PULSE.md)
- Harness vs deep pulse: [`PULSE-DEPTH.md`](PULSE-DEPTH.md)
- Loop + Paris: [`LOOP-ENGINEERING.md`](LOOP-ENGINEERING.md)
- Compact status index: [`docs/CONTEXT-COMPACT.md`](../CONTEXT-COMPACT.md)
- Agent store pointer: [`/cursor/stores/self/pulse-reporting.md`](/cursor/stores/self/pulse-reporting.md)

## Example

First approved sample: [`reports/2026-10-02-pulse-meaty.md`](reports/2026-10-02-pulse-meaty.md).
