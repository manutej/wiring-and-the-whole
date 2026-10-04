---
name: devex-metrics-grounding
description: Ground factory and AI programs in org DevEx data — quarterly trends, not stage anecdotes. Triggers — justify agent spend, measure AI impact, prioritize factory investments across teams.
---

# DevEx metrics grounding

Platform research at scale beats conference stories. Anchor factory and long-running agent programs in **DevEx and productivity signals** you can measure.

## Progressive disclosure

**Layer 1:** Use **quarterly DevEx/productivity data**, not stage anecdotes.

**Layer 2 moves:** Frameworks · baseline · hypothesis · instrument · segment · decide.

**Layer 3:** Segment ids in **References**.

**Unified system:** Feedback / justify investment. **Downstream:** informs [`factory-operator`](../factory-operator/SKILL.md), [`eval-over-review`](../eval-over-review/SKILL.md).

## When to use

- “Is AI helping?”; prioritizing next factory capability; post-rollout review.

## When NOT to use

- No org metric access — lightweight surveys, label limitation; does not replace customer outcome metrics ([`factory-operator`](../factory-operator/SKILL.md)).

## Core moves

1. **Frameworks** — DORA / SPACE / DevX dimensions leadership already knows (`dx-frameworks-lineage`).
2. **Baseline quarter** — Before expansion: lead time, satisfaction, adoption, toil proxies.
3. **Hypothesis** — “If we embed agents in Linear+GitHub, we expect ↓ X on Y.”
4. **Instrument + segment** — Quarterly cadence; split by team maturity/repo type (`dx-quarterly-reports`).
5. **Decide** — Continue, pivot harness refresh ([`factory-harness`](../factory-harness/SKILL.md)), or pause; anecdotes labeled anecdotes in reports (`dx-catalog-400-orgs` = metadata cite).

## Quality gate

- [ ] Baseline before claiming improvement.
- [ ] Metric definitions written.
- [ ] Factory outcome metric aligned with DevEx metric.
- [ ] Vendor demos cannot drive roadmap without internal data.
- [ ] Status reports separate FACT metrics from anecdotes.

## Failure modes

| Symptom | Fix | Segment |
|---------|-----|---------|
| Demo-driven roadmap | Require baseline | `dx-quarterly-reports` |
| PR-count gaming | Pair with outcome metrics | `workos-outcome-metrics` |
| Hidden team failures | Segment cohorts | `dx-frameworks-lineage` |
| Stale skills ignored | Link to harness refresh | `warp-stale-skills` |

## References

- Index: `research/ai-engineer-paris-2026/references/index.yaml`
- L4: `dx-quarterly-reports`, `dx-frameworks-lineage`, `dx-catalog-400-orgs`
- L5: `transcript-summaries.json#Se8jHLliLXE`
