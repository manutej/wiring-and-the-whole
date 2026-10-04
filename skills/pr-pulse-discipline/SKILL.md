---
name: pr-pulse-discipline
description: Fix the PR bottleneck — skills as review rubric, small diffs, separated implement/adversarial/evaluator lanes. Triggers — agent PR flood, skills for review, pulse workflows, Pocock-style process brakes.
---

# PR & pulse discipline

Agent speed increased PR supply while review bandwidth is flat. **Skills** are durable rubrics; **pulse** adds firewalled adversarial + evaluator lanes ([`docs/PULSE.md`](../../docs/PULSE.md)).

## Progressive disclosure

**Layer 1:** **Process brakes** — small PRs, skill rubrics, separated lanes.

**Layer 2 moves:** Small PR · skill rubric · risk tiers · adversarial · automated gate · evaluator SHIP.

**Layer 3:** Segment ids in **References**.

**Unified system:** Ship gates. **Upstream:** [`agent-orchestra`](../agent-orchestra/SKILL.md) · **Downstream:** [`eval-over-review`](../eval-over-review/SKILL.md).

## When to use

- Many agent PRs or giant diffs; skills for review/authoring; any pulse on factory or programme repos.

## When NOT to use

- No VCS — adapt to patch queues but keep role separation; does not replace [`eval-over-review`](../eval-over-review/SKILL.md).

## Core moves

1. **Small PR** — One primary deliverable per pulse ([`docs/pulse/IMPLEMENTER-BRIEF-TEMPLATE.md`](../../docs/pulse/IMPLEMENTER-BRIEF-TEMPLATE.md)).
2. **Skill rubric** — Reviewer runs skill checklist, not vibe scan (`pocock-skills-rubric`).
3. **Risk tiers** — Docs vs harness vs prod config → more human eyes on high tier.
4. **Lanes** — Implementer brief; adversarial gaps; implementer must not read evaluator rubric same pulse (`pulse-evaluator-firewall`).
5. **Gates** — `make verify`, `make verify-research` if Paris touched, `make pulse-eval` when wiring/pack/L1 touched; evaluator SHIP before merge.

## Quality gate

- [ ] PR description states one primary intent.
- [ ] Reviewer cites skill or brief path.
- [ ] Adversarial notes attached for pulse work.
- [ ] CI + eval commands run and referenced.
- [ ] No self-graded LGTM on pulse work.

## Failure modes

| Symptom | Fix | Segment |
|---------|-----|---------|
| PR pile | Smaller PRs + rubric | `pocock-pr-backlog` |
| Rubric ignored | Bind review to skill path | `pocock-skills-rubric` |
| Self-graded ship | Evaluator firewall | `pulse-evaluator-firewall` |
| Missing research gate | verify-research | `workos-outcome-metrics` |

## References

- Index: `research/ai-engineer-paris-2026/references/index.yaml`
- L4: `pocock-pr-backlog`, `pocock-skills-rubric`, `pulse-evaluator-firewall`
- L5: `transcript-summaries.json#LlgiOCmFG_w`
