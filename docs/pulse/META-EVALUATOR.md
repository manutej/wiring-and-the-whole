# Meta-evaluator hook (post-loop)

**Lane:** operator / next-pulse planner — **not** the implementer during an open pulse.

After `make pulse-loop` (or verify + `pulse-eval`) and a **firewalled** evaluator SHIP|NO-SHIP, operators may attach a **meta-evaluator bundle** so the next agent gets architecture and external craft guardrails without breaking the implementer ↔ evaluator firewall in [`LOOP-ENGINEERING.md`](LOOP-ENGINEERING.md).

## What it is

| Piece | Path |
|-------|------|
| JSON bundle generator | [`scripts/meta_evaluator_hook.py`](../../scripts/meta_evaluator_hook.py) |
| Craft upstream index | [`CRAFT-SKILLS-INTEGRATION.md`](CRAFT-SKILLS-INTEGRATION.md) |
| Programme cold-start | [`docs/CONTEXT-COMPACT.md`](../CONTEXT-COMPACT.md) |

Run:

```bash
make meta-evaluator          # pretty-print JSON to stdout
make meta-evaluator-check    # sanity gate (also in make pulse-eval)
```

Environment:

- `CRAFT_SKILLS_ROOT` — optional path to a `manutej/craft` checkout (default: sibling `craft/` if present).

## Firewall (non-negotiable)

1. **Implementers** must not read [`RUBRIC-EVALUATOR.md`](RUBRIC-EVALUATOR.md) during the same pulse ([`docs/PULSE.md`](../PULSE.md)).
2. The meta-evaluator hook **must not** embed rubric text, dimension labels (D1–D7), or evaluator scorecards.
3. Craft skills are **code-quality guardrails** (router + member skills). They do **not** replace the programme evaluator rubric or adversarial register.
4. Store evaluator output under `docs/pulse/evaluations/` — meta bundle only **names** that directory as forbidden for implementers.

## When to run

| Phase | Meta-evaluator |
|-------|----------------|
| Mid-implement | **No** — use implementer brief + in-repo skills only |
| Post-evaluator SHIP | **Yes** — attach bundle to handoff / next pulse brief |
| Doc-only pulse | Optional — operator discretion |

## Related

- [`LOOP-ENGINEERING.md`](LOOP-ENGINEERING.md) — three clocks and harness table
- [`PULSE-REPORT-SPEC.md`](PULSE-REPORT-SPEC.md) — executive report (no rubric scores)
