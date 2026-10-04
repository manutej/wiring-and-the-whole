---
name: process-embedded-factory
description: Embed coding agents in eng workflow — issue trackers, chat, VCS, webhooks, progress agents — not code-only output. Auto-apply when designing TARS-like agents, Slack/Linear/GitHub bots, factory integrations, or long-running agents that must follow sprint state.
---

# Process-embedded factory

WorkOS’s lesson: **producing patches is insufficient**; factories must live where work is tracked and discussed. Design integrations so long-running agents **read state** and **write auditable progress**, not only open PRs.

## When to use

- Standing up a **team coding factory** (cloud agents, background workers).
- Agents that run **hours or days** on a feature branch or epic.
- Replacing “engineer runs Claude locally” with **shared, observable** automation.

## When NOT to use

- Pure research spikes with no ticket/epic linkage (document as ad-hoc).
- Programme witness/E2/E3 work — no ticket theater required.

## Core moves (7)

1. **System of record** — Pick authoritative objects: Linear/Jira issues, GitHub PRs, Slack threads; one write path per event type.
2. **Progress agent** — Separate **implementation** from **status** (WorkOS Horizon/TARS pattern @ 4:10, `HvboD89DyQ8`): webhooks update “where is this epic?”
3. **Chat embed** — Agents answer in Slack (or equivalent) with links to diffs, CI, and scope — humans intervene without cloning repos.
4. **Webhook graph** — List inbound events (issue moved, review requested, CI failed) and agent actions; no silent polling-only loops.
5. **Scope binding** — Every long run attaches to **issue ID + repo + branch policy**; refuse unbounded repo-wide autonomy by default.
6. **Human escalation** — Defined triggers: security paths, dependency majors, architecture flags → @human, not auto-merge.
7. **Outcome check** — After embed, measure feature cycle time — not embed itself (see [`factory-operator`](../factory-operator/SKILL.md)).

## Output template

```markdown
# Process embed — {team} · {factory name}

## Systems of record
| System | Read | Write | Webhooks |
|--------|------|-------|----------|
| ... | issues, comments | status, links | ... |

## Agent roles
| Role | Trigger | Stops when |
|------|---------|------------|
| Implementer | issue labeled `agent-ok` | PR open + CI green |
| Progress (TARS-like) | any issue/PR event | epic closed |

## Long-running session policy
- Max duration / cost cap:
- Refresh context from: issue body, last N comments, CI logs

## Not automated (explicit)
- ...
```

## Quality gate

- [ ] Agent output is **reachable from the tracker** without opening only email/git.
- [ ] **Webhook or event** path documented (not “agent polls git every 5m” alone).
- [ ] **Progress** updates even when no new code (blocked, waiting review).
- [ ] Parity test documented: “Would this differ from laptop Claude?” → if no, upgrade embed.

## Failure modes

| Symptom | Fix |
|---------|-----|
| Agents open PRs nobody asked for | Bind to issue state + label policy |
| Stale epic for days | Progress agent + webhook on stall |
| Two agents same ticket | Lock or conductor assignment ([`agent-orchestra`](../agent-orchestra/SKILL.md)) |

## Provenance

- Ryan Cooke — *No, That’s Not a Software Factory* (`HvboD89DyQ8`, @ 3:56, 4:10)
