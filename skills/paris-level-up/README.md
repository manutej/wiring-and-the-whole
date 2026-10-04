# Paris 2026 level-up skills

Agent **SKILL.md** instruments distilled from **9 ingested** AI Engineer Paris talks (fact + inference separated in each skill’s Provenance). Use with programme skills (`interface-first-context`, `systems-intake`, `symmetry-lens`) and [`docs/PULSE.md`](../../docs/PULSE.md) for pulse-sized adoption.

## Curriculum (recommended order)

| Order | Skill | Primary speakers | You learn |
|-------|--------|------------------|-----------|
| 1 | [`factory-operator`](../factory-operator/SKILL.md) | WorkOS, Factory.com, Warp (Lloyd) | What counts as a factory; outcome vs output metrics |
| 2 | [`process-embedded-factory`](../process-embedded-factory/SKILL.md) | WorkOS (Cooke) | Embed agents in Slack/Linear/GitHub; progress webhooks |
| 3 | [`factory-harness`](../factory-harness/SKILL.md) | Warp (Gupta, Lloyd) | Harness, stale-skill refresh, model routing |
| 4 | [`covariant-eval-loop`](../covariant-eval-loop/SKILL.md) | W&B (Aysola) | Bench + harness + config move together; trace flywheel |
| 5 | [`agent-orchestra`](../agent-orchestra/SKILL.md) | Conductor (Holtz) | Parallel long-running agents need a conductor |
| 6 | [`pr-pulse-discipline`](../pr-pulse-discipline/SKILL.md) | Pocock | PR bottleneck; skills as review rubric; small PRs |
| 7 | [`eval-over-review`](../eval-over-review/SKILL.md) | Voss (Arize) | Evals and observability over review theater |
| 8 | [`devex-metrics-grounding`](../devex-metrics-grounding/SKILL.md) | DX (Reock) | Org data before scaling agent programs |

## Composition for coding factories

```text
factory-operator (definition + metrics)
    → process-embedded-factory (workflow integrations)
    → factory-harness (skills + routing + refresh)
    → covariant-eval-loop (prove harness changes)
    → agent-orchestra (many sessions in flight)
    → pr-pulse-discipline + eval-over-review (merge gates)
    → devex-metrics-grounding (did it help the org?)
```

Registry: [`docs/research-insights/paris-2026.yaml`](../../docs/research-insights/paris-2026.yaml).
