---
name: devex-metrics-grounding
description: Ground AI and factory programs in org DevEx data — DX-style platform research, quarterly trends, not stage anecdotes. Auto-apply when justifying agent spend, measuring AI impact, or prioritizing factory investments across teams.
---

# DevEx metrics grounding

Justin Reock (DX @ `Se8jHLliLXE`): **400+ org** platform data beats conference stories. Before scaling **coding factories** or **long-running agents**, anchor claims in **developer experience and productivity signals** your organization can actually measure.

## When to use

- Executive or platform team asks **“Is AI helping?”**
- Prioritizing **which factory capability** to build next.
- Post-rollout review of agent/factory programs.

## When NOT to use

- Pure local dev ergonomics with no org metric access — use lightweight surveys instead, label limitation.
- Replacing product/customer outcome metrics ([`factory-operator`](../factory-operator/SKILL.md)) — combine both.

## Core moves (6)

1. **Pick frameworks** — DORA / SPACE / DevX-style dimensions already familiar to leadership (DX platform lineage in talk).
2. **Baseline quarter** — Snapshot before factory/agent expansion: lead time, satisfaction, AI tool adoption, toil proxies.
3. **Hypothesis** — One sentence: “If we embed agents in Linear+GitHub, we expect ↓ X on dimension Y.”
4. **Instrument** — Platform or survey cadence (quarterly); avoid one-off hero projects as proof.
5. **Segment** — Team maturity, repo type, language — aggregate hides failures.
6. **Decide** — Continue, pivot harness, or pause spend — link to [`factory-harness`](../factory-harness/SKILL.md) refresh if skills stale.

## Quality gate

- [ ] **Baseline exists** before claiming improvement.
- [ ] Metric definitions **written** (not “productivity feels up”).
- [ ] Factory outcome metric **aligned** with DevEx metric (no contradiction).
- [ ] Anecdotes labeled **anecdotes** in status reports.

## Failure modes

| Symptom | Fix |
|---------|-----|
| Vendor demo drives roadmap | Require internal baseline |
| Metrics gaming (PR count) | Use outcome + DevEx pair |
| No data access | Pilot with one team instrumented |

## Provenance

- Justin Reock — *State of AI in Software Development* (`Se8jHLliLXE`)
