---
name: eval-over-review
description: Shift from ritual code review to eval discipline — observability, tests-as-gates, measured AI change. Triggers — review bottleneck, Arize-style LLM evals, agent-generated code quality gates.
---

# Eval over review

Human diff review does not scale with agent speed. Replace theater with **measurement** — evals, observability — and reserve humans for **high-risk** judgment (pairs with PR discipline and covariant loops).

## Progressive disclosure

**Layer 1:** **Evals + observability** first; humans on high-risk gaps.

**Layer 2 moves:** Review map · agent eval suite · observability · human-on-risk · covariant ship.

**Layer 3:** Segment ids in **References**.

**Unified system:** Ship gates (measurement). **Upstream:** [`pr-pulse-discipline`](../pr-pulse-discipline/SKILL.md) · **Downstream:** [`devex-metrics-grounding`](../devex-metrics-grounding/SKILL.md). Cross-talk composition with Pocock/W&B is **CONJECTURE** unless cited.

## When to use

- Agent-generated paths; quality gates for factories; artifact-backed ship criteria vs LGTM culture.

## When NOT to use

- Zero automated checks — add evals first; eval ≠ formal correctness without scope label.

## Core moves

1. **Review map** — What review caught → automatable vs human-only (`voss-test-ai-framing`).
2. **Agent eval suite** — Tasks from real failures; JSON/log artifacts (`voss-agent-speed`).
3. **Observability** — Prod signals on AI-touched code: errors, latency, flags.
4. **Human on risk** — Tier-1 architecture/security and eval gaps only (`voss-review-bandwidth`).
5. **Covariant + small PRs** — Ship eval/harness together ([`covariant-eval-loop`](../covariant-eval-loop/SKILL.md)); keep diffs tractable ([`pr-pulse-discipline`](../pr-pulse-discipline/SKILL.md)); loop metrics via [`devex-metrics-grounding`](../devex-metrics-grounding/SKILL.md).

## Quality gate

- [ ] ≥1 automated check blocks merge on agent-touched paths.
- [ ] Eval artifacts stored, not CI-green-only.
- [ ] Human review scope documented.
- [ ] New capability → new or updated eval task.
- [ ] Smoke on PR, full suite on schedule documented.

## Failure modes

| Symptom | Fix | Segment |
|---------|-----|---------|
| Review theater | Drop steps covered by eval | `voss-review-bandwidth` |
| Eval green, users hurt | Prod observability | `voss-agent-speed` |
| Slow eval | Tier smoke vs nightly | `wb-covariant-triple` |
| Giant diffs | Small PR rule | `pocock-pr-backlog` |

## References

- Index: `research/ai-engineer-paris-2026/references/index.yaml`
- L4: `voss-agent-speed`, `voss-review-bandwidth`, `voss-test-ai-framing`
- L5: `transcript-summaries.json#_mi3alkqy4s`
