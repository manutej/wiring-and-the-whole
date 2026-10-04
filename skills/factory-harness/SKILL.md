---
name: factory-harness
description: Maintain factory harnesses — versioned skills, stale-skill refresh, Pareto routing, team platforms. Triggers — Warp-style harness, skill libraries for factories, model routers, self-improving dev environments.
---

# Factory harness

The harness wraps the model: tools, skills, routing, sandboxes, telemetry, refresh jobs. Treat it as a **living product**, not a frozen prompt bundle.

## Progressive disclosure

**Layer 1:** Version the harness; **refresh stale skills**; route models; hook self-improvement.

**Layer 2 moves:** Inventory · skill assets · refresh · routing · eval handoff.

**Layer 3:** Segment ids in **References**.

**Unified system:** Platform loop. **Upstream:** [`process-embedded-factory`](../process-embedded-factory/SKILL.md) · **Downstream:** [`covariant-eval-loop`](../covariant-eval-loop/SKILL.md).

## When to use

- Multi-repo/team coding factories; shared skill libraries for long-running agents; default vs pinned models at scale.

## When NOT to use

- One-shot chat without reusable skills; bench design → [`covariant-eval-loop`](../covariant-eval-loop/SKILL.md).

## Core moves

1. **Harness inventory** — Tools, MCP, skills, sandbox, secrets — versioned together.
2. **Skills as assets** — Review rubrics + procedures with owners (align [`pr-pulse-discipline`](../pr-pulse-discipline/SKILL.md)).
3. **Stale-skill refresh** — Calendar or failure-driven revalidation (`warp-stale-skills`, `warp-self-improve-loop`).
4. **Pareto routing** — Quality/cost/latency defaults; document overrides (`warp-pareto-routing`).
5. **Covariant handoff** — Harness change ships with bench delta ([`covariant-eval-loop`](../covariant-eval-loop/SKILL.md)); CI parity before fleet rollout.

## Quality gate

- [ ] Skill catalog with owner + last-validated date.
- [ ] Refresh job defined (calendar or after N failures).
- [ ] Routing table with defaults and escape hatches.
- [ ] Harness version in logs for incidents.
- [ ] No silent global prompt edits without changelog.

## Failure modes

| Symptom | Fix | Segment |
|---------|-----|---------|
| Skills wrong after upgrade | Refresh + regression | `warp-stale-skills` |
| Cost explosion | Routing defaults + caps | `warp-pareto-routing` |
| Works locally only | Sandbox parity + pin | `warp-lloyd-environment` |
| Bench drift | Same PR as harness | `wb-covariant-triple` |

## References

- Index: `research/ai-engineer-paris-2026/references/index.yaml`
- L4: `warp-scale-maus`, `warp-self-improve-loop`, `warp-stale-skills`, `warp-pareto-routing`, `warp-lloyd-environment`
- L5: `transcript-summaries.json#TN3mj92oZ8I`, `#tUPPVhBBcoM`
