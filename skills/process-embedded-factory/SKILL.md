---
name: process-embedded-factory
description: Embed coding agents in eng workflow — trackers, chat, VCS, webhooks — not patch-only output. Triggers — TARS-like agents, Slack Linear GitHub factory bots, workflow integrations, long-running agents on sprint state.
---

# Process-embedded factory

Producing patches is insufficient; factories live where work is tracked. Long-running agents **read state** and **write auditable progress**.

## Progressive disclosure

**Layer 1:** Embed in **Slack/Linear/GitHub** with **webhook-driven progress**, not patch-only bots.

**Layer 2 moves:** System of record · progress agent · webhook graph · scope binding · escalation.

**Layer 3:** Segment ids in **References**.

**Unified system:** Embed in work. **Upstream:** [`factory-operator`](../factory-operator/SKILL.md) · **Downstream:** [`factory-harness`](../factory-harness/SKILL.md), [`agent-orchestra`](../agent-orchestra/SKILL.md).

## When to use

- Team coding factory (cloud/background agents); runs lasting hours/days on epics.
- Replacing “engineer runs Claude locally” with shared observable automation.

## When NOT to use

- Ad-hoc spikes with no ticket linkage; programme witness work without ticket theater.

## Core moves

1. **System of record** — One authoritative object per event (issue, PR, thread); one write path per event type.
2. **Progress agent** — Separate implementation from status; webhooks update epic state (`workos-tars-webhooks`).
3. **Webhook graph** — Inbound events → agent actions; avoid silent poll-only loops (`workos-embed-process`).
4. **Scope binding** — Every run attaches to issue ID + repo + branch policy; refuse unbounded repo autonomy.
5. **Escalation + outcomes** — Security/architecture → @human; measure cycle time after embed, not embed itself.

## Quality gate

- [ ] Agent output reachable from the tracker without email-only git.
- [ ] Webhook or event path documented (not polling alone).
- [ ] Progress updates when blocked or waiting review.
- [ ] Laptop-parity test documented — if no difference, upgrade embed (`workos-sandbox-parity`).
- [ ] Overlap policy points to [`agent-orchestra`](../agent-orchestra/SKILL.md) when >1 agent.

## Failure modes

| Symptom | Fix | Segment |
|---------|-----|---------|
| Surprise PRs | Issue state + labels | `workos-embed-process` |
| Stale epics | Progress webhooks | `workos-tars-webhooks` |
| Two agents, one ticket | Conductor / locks | `holtz-conductor-intro` |
| “Same as laptop” | Deepen embed | `workos-sandbox-parity` |

## References

- Index: `research/ai-engineer-paris-2026/references/index.yaml`
- L4: `workos-embed-process`, `workos-tars-webhooks`, `workos-sandbox-parity`
- L5: `transcript-summaries.json#HvboD89DyQ8`
