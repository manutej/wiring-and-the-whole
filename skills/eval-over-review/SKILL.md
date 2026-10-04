---
name: eval-over-review
description: Replace ritual code review with eval discipline — observability, tests-as-gates, AI change measurement. Auto-apply when code review is bottleneck, Arize-style LLM evals, or agent-generated code quality gates.
---

# Eval over review

Laurie Voss (`_mi3alkqy4s`): agent speed broke the assumption that **human diff review** scales. The replacement is not “no humans” but **measurement** — evals, observability, and targeted human judgment on **high-risk** deltas (pairs with Pocock PR discipline and W&B covariant loops).

## When to use

- **Agent-generated** or **agent-assisted** code paths.
- Designing **quality gates** for factories and long-running agents.
- Moving from “LGTM culture” to **artifact-backed** ship criteria.

## When NOT to use

- Sole gate with zero automated checks — add evals first.
- Claiming eval proves formal correctness — label demonstrated scope.

## Core moves (7)

1. **Review map** — List what review used to catch; mark each **automatable** (test, lint, eval harness) vs **human-only** (architecture, security judgment).
2. **Eval suite for agents** — Tasks derived from real failures (regression style); store results as JSON/logs.
3. **Observability** — Production signals for AI-touched code: errors, latency, feature flags — Arize-adjacent mindset.
4. **Human on risk** — Humans review **tier-1** changes and eval gaps, not every line.
5. **Pair with PR discipline** — Small diffs make evals tractable ([`pr-pulse-discipline`](../pr-pulse-discipline/SKILL.md)).
6. **Covariant changes** — Eval/harness bumps ship together ([`covariant-eval-loop`](../covariant-eval-loop/SKILL.md)).
7. **DevEx feedback** — Did eval investment reduce incidents or cycle time? ([`devex-metrics-grounding`](../devex-metrics-grounding/SKILL.md)).

## Quality gate

- [ ] **≥1 automated check** blocks merge for agent-touched paths.
- [ ] Eval artifacts **stored**, not only CI green without logs.
- [ ] Human review scope **documented** (what humans still do).
- [ ] New agent capability → **new or updated eval task**.

## Failure modes

| Symptom | Fix |
|---------|-----|
| Review theater continues | Remove redundant human steps covered by eval |
| Eval green, users suffer | Add prod observability + trace tasks |
| Eval too slow | Tier: smoke on PR, full nightly |

## Provenance

- Laurie Voss — *The Death of the Code Review* (`_mi3alkqy4s`)
