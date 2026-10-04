---
name: agent-orchestra
description: Orchestrate parallel coding agents — conductor score, session limits, merge-back, not factory assembly-line only. Auto-apply when running multiple concurrent agents, Conductor-style desktop control, long-running parallel tasks, or swarm without coordination plan.
---

# Agent orchestra

**Metaphor** (Charlie Holtz, Conductor @ `TRfzFJCJ7ZE`): many agents in parallel need a **score** — who plays what, when to stop, how to combine — not an unbounded factory line of PRs. Essential for **long-running** programs where several sessions touch the same epic.

## When to use

- **>1 agent** active on related work (features, migrations, refactors).
- **Long-running** sessions (hours/days) that might overlap or conflict.
- Operator drowning in agent tabs / cloud run URLs.

## When NOT to use

- Single agent, single PR, single issue — overhead not worth it.
- Fully serial batch jobs with no shared state — use queue instead.

## Core moves (7)

1. **Score** — Written plan: tracks (Agent A = API, B = tests, C = docs) with **dependencies** and merge order.
2. **Conductor role** — Human or dedicated meta-agent assigns tracks, **does not** implement everything.
3. **Session caps** — Max parallel agents per repo/epic; excess waits (avoid git/CI thundering herd).
4. **Shared context bundle** — Issue ID, architecture notes, [`interface-first-context`](../interface-first-context/SKILL.md) L1 slice, eval gates — same pointer for all players.
5. **Merge-back cadence** — Rebase/integrate on schedule; one **integration owner** resolves conflicts.
6. **Stop conditions** — Per track: done = CI green + eval pass + review lane; orchestra stops when score complete.
7. **Embed alignment** — Progress visible in tracker ([`process-embedded-factory`](../process-embedded-factory/SKILL.md)).

## Output template

```markdown
# Orchestra score — {epic}

## Tracks
| Track | Agent/session | Scope | Blocked by | Done when |
|-------|---------------|-------|------------|-----------|
| A | ... | ... | — | PR merged |

## Integration
- Owner:
- Merge window:
- Conflict policy:

## Forbidden overlap
- Files/dirs exclusively owned by track ...
```

## Quality gate

- [ ] No two agents **default-edit same paths** without lock.
- [ ] **Score exists** before second agent starts.
- [ ] Integration owner named.
- [ ] Stop conditions include **eval/review**, not “agent said done.”

## Failure modes

| Symptom | Fix |
|---------|-----|
| Duplicate PRs same fix | Conductor assigns exclusive tracks |
| Endless parallel drift | Scheduled merge-back |
| Lost sessions | Embed + session registry in tracker |

## Provenance

- Charlie Holtz — *Orchestras, Not Factories* (`TRfzFJCJ7ZE`)
