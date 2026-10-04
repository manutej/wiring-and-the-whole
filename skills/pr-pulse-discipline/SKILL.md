---
name: pr-pulse-discipline
description: Fix the PR bottleneck — Agent Skills as review rubric, small diffs, separated implement/adversarial/evaluator lanes. Auto-apply when agent output floods PRs, designing skills for review, pulse workflows, or Pocock-style process brakes.
---

# PR & pulse discipline

Matt Pocock’s frame (`LlgiOCmFG_w`): AI **increased PR supply** while human review bandwidth is flat — the bottleneck is **review and process**, not raw generation. **Skills** are durable rubrics for authoring and reviewing; this repo’s **pulse** adds firewalled adversarial + evaluator lanes ([`docs/PULSE.md`](../../docs/PULSE.md)).

## When to use

- Agents opening **many PRs** or giant diffs.
- Minting **skills** meant for review/authoring (not only codegen).
- Any **pulse** on programme or factory repos.

## When NOT to use

- No VCS / no PR culture — adapt to patch queues but keep separation of roles.
- Replacing [`eval-over-review`](../eval-over-review/SKILL.md) — use both.

## Core moves (7)

1. **Small PR rule** — One primary deliverable per pulse: one skill adoption, one wiringmap slice, one harness bump ([`docs/pulse/IMPLEMENTER-BRIEF-TEMPLATE.md`](../../docs/pulse/IMPLEMENTER-BRIEF-TEMPLATE.md)).
2. **Skill as rubric** — Review skill lists moves, checklists, forbidden merges — reviewer runs skill, not vibe scan.
3. **Risk tiers** — Blast radius labels (docs-only vs harness vs prod config); higher tier → more human eyes.
4. **Implementer brief** — Scope in/out, commands, handoff; implementer **must not** read evaluator rubric same pulse.
5. **Adversarial lane** — Separate subagent/person lists gaps before merge.
6. **Automated gate** — `make verify`, `make verify-research` (if Paris touched), `make pulse-eval` when wiring/pack/L1 touched.
7. **Evaluator SHIP** — Merge blocked until firewalled evaluator signs ([`docs/roadmap/CONSENSUS-FORWARD.md`](../../docs/roadmap/CONSENSUS-FORWARD.md)).

## Quality gate

- [ ] PR description states **one primary intent**.
- [ ] Reviewer can point to **skill or brief** used.
- [ ] Adversarial notes attached for pulse work.
- [ ] CI + eval commands run and referenced in PR.

## Failure modes

| Symptom | Fix | Paris cite |
|---------|-----|------------|
| PR pile, no reviews | Tier + skill-based review; reduce PR size | Pocock |
| Self-graded “LGTM” | Evaluator firewall | Programme pulse |
| Skills unused | Bind review checklist to skill file path | Pocock |

## Provenance

- Matt Pocock — *Fixing the PR Bottleneck* (`LlgiOCmFG_w`)
