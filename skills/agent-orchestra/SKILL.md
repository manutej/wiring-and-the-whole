---
name: agent-orchestra
description: Orchestrate parallel coding agents with a conductor score — not an unbounded PR assembly line. Triggers — multiple concurrent agents, Conductor-style control, long-running parallel tasks, agent swarm coordination.
---

# Agent orchestra

Parallel long-running agents need a **score**: who plays what, when to stop, how to merge — not unlimited overlapping PRs on one epic.

## Progressive disclosure

**Layer 1:** Use a **conductor + score** before starting a second agent on related work.

**Layer 2 moves:** Write score · session caps · shared context · merge-back · stop conditions.

**Layer 3:** Segment ids in **References**.

**Unified system:** Multi-session scale. **Upstream:** [`covariant-eval-loop`](../covariant-eval-loop/SKILL.md) · **Downstream:** [`pr-pulse-discipline`](../pr-pulse-discipline/SKILL.md). Programme: [`interface-first-context`](../interface-first-context/SKILL.md).

## When to use

- >1 agent on related work; hours/days sessions that may conflict; operator drowning in run URLs.

## When NOT to use

- Single agent / single PR; fully serial batch jobs — use a queue.

## Core moves

1. **Score** — Tracks (A=API, B=tests…) with dependencies and merge order (`holtz-orchestra-thesis` — editorial).
2. **Conductor** — Human or meta-agent assigns tracks; does not implement everything (`holtz-conductor-intro`).
3. **Session caps** — Max parallel agents per repo/epic; excess waits.
4. **Shared context bundle** — Issue ID, architecture notes, interface L1 slice, eval gates — same pointer for all players.
5. **Merge-back + stops** — Integration owner on cadence; done = CI + eval + review lane; tracker embed per [`process-embedded-factory`](../process-embedded-factory/SKILL.md).

## Quality gate

- [ ] Score exists before second agent starts.
- [ ] No two agents default-edit same paths without lock.
- [ ] Integration owner named.
- [ ] Stop conditions include eval/review, not “agent said done.”
- [ ] Progress visible in system of record.

## Failure modes

| Symptom | Fix | Segment |
|---------|-----|---------|
| Duplicate PRs | Exclusive tracks | `holtz-orchestra-thesis` |
| Parallel drift | Scheduled merge-back | `holtz-conductor-intro` |
| Lost sessions | Tracker + registry | `workos-tars-webhooks` |
| Review pile | [`pr-pulse-discipline`](../pr-pulse-discipline/SKILL.md) | `pocock-pr-backlog` |

## References

- Index: `research/ai-engineer-paris-2026/references/index.yaml`
- L4: `holtz-conductor-intro`, `holtz-orchestra-thesis`
- L5: `transcript-summaries.json#TRfzFJCJ7ZE`
