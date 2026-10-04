---
name: factory-harness
description: Build and maintain agent factory harnesses — versioned skills, stale-skill refresh, Pareto model routing, cloud team platforms. Auto-apply when designing Warp-style harnesses, skill libraries for factories, model routers, or self-improving dev environments.
---

# Factory harness

The **harness** is everything that wraps the model: tools, skills, routing, sandboxes, telemetry, and refresh jobs. Warp (Gupta/Lloyd) treats the harness as a **living product** (~1M MAU IDE → cloud team platform), not a frozen prompt bundle.

## When to use

- Building **coding factories** for multiple repos or teams.
- Maintaining a **skill library** used by long-running agents.
- Choosing **default models** vs user-pinned models at scale.

## When NOT to use

- One-shot chat without reusable skill assets.
- Covariant bench design — pair with [`covariant-eval-loop`](../covariant-eval-loop/SKILL.md).

## Core moves (7)

1. **Harness inventory** — Tools, MCP servers, skills, sandbox shape, secrets policy — versioned together.
2. **Skill as factory asset** — Skills are **review rubrics + procedures** (Pocock alignment), not one-line prompts; store in repo with owners.
3. **Stale-skill refresh** — Schedule or event-driven revalidation (bug-repro skills, upgrade guides) — skills **decay** (Warp @ 2:28, `TN3mj92oZ8I`).
4. **Self-improvement hook** — When a run fails, capture trace → task to update skill or tool config (automatic loop possible @ 1:10 same talk).
5. **Model routing** — Prefer **Pareto defaults** (quality/cost/latency) over everyone pinning one model (@ 9:29); document override policy.
6. **Environment parity** — Dev container / cloud sandbox matches CI; harness changes trigger **`make verify`** or project equivalent before fleet rollout.
7. **Handoff to eval** — Any harness change ships with bench delta ([`covariant-eval-loop`](../covariant-eval-loop/SKILL.md), [`systems-intake`](../systems-intake/SKILL.md)).

## Quality gate

- [ ] **Skill catalog** with owner + last-validated date.
- [ ] **Refresh job** defined (calendar or “after N failures”).
- [ ] **Routing table** documented with default and escape hatches.
- [ ] Harness version string exposed to logs for incident debug.
- [ ] No silent global prompt edits without changelog entry.

## Failure modes

| Symptom | Fix | Paris cite |
|---------|-----|------------|
| Bug-repro skill wrong after upgrade | Refresh loop + regression task | Warp @ 2:28 |
| Cost explosion | Routing defaults + caps | Warp @ 9:29 |
| “Works on my machine” harness | Sandbox parity + version pin | Warp cloud platform |

## Provenance

- Suraj Gupta — *Building Self-Improving Agent Software Factories* (`TN3mj92oZ8I`)
- Zach Lloyd — *Self-Improving Software Factories* (`tUPPVhBBcoM`)
