# Paris 2026 factory skill plugin (portable v1)

Self-contained **Cursor skill bundle** — 8 factory OS skills distilled from **9 ingested** AI Engineer Paris talks. Programme boundary skills (`interface-first-context`, `systems-intake`, `symmetry-lens`) are optional peers, not bundled.

**Spec:** [`docs/specs/software-factory-skill-plugin.v1.md`](../../docs/specs/software-factory-skill-plugin.v1.md) · **Progress:** [`docs/specs/software-factory-skills-PROGRESS.md`](../../docs/specs/software-factory-skills-PROGRESS.md)

## Package layout

```text
skills/paris-level-up/
├── README.md
├── plugin-manifest.json
└── assets/
    ├── factory-os-diagram.mmd
    ├── reference-tier-cheatsheet.md
    └── references-index.yaml      # slim L4 index for satellite repos

skills/{factory-operator,…}/SKILL.md   # eight skills (siblings in monorepo)
```

**Reference source of truth (monorepo):** `research/ai-engineer-paris-2026/references/index.yaml`  
**L5 transcripts:** `research/ai-engineer-paris-2026/transcript-summaries.json` (do not copy full corpus into the plugin)

Captions: English **auto-generated** YouTube — see spec § Caption limitation.

## Copy to another repo (3 steps)

1. **Copy paths** — `skills/paris-level-up/` (manifest + assets) and the eight skill folders listed in `plugin-manifest.json` → same relative paths under the target repo’s `skills/`.
2. **References** — Either copy `research/ai-engineer-paris-2026/references/index.yaml` + `transcript-summaries.json` (subset) **or** ship only `assets/references-index.yaml` and accept L3 segment ids without L5 quotes until you sync research.
3. **Discover** — Point Cursor at `skills/**/SKILL.md`; optional: register trigger phrases from `plugin-manifest.json`. Programme skills and `make verify-research` are **optional** (monorepo governance only).

### Optional install modes

| Mode | Command / action |
|------|------------------|
| **Subtree copy** | `rsync -a skills/paris-level-up skills/factory-operator … $TARGET/skills/` |
| **Submodule** | Add this repo submodule at `vendor/wiring-paris`; symlink or copy skills into `skills/` |
| **Symlink index** | `ln -s ../../research/ai-engineer-paris-2026/references/index.yaml skills/paris-level-up/assets/references-full.yaml` |

## Trigger phrases (plugin-level)

`software factory`, `coding factory`, `agent factory`, `long-running agents`, `factory harness`, `PR bottleneck`, `covariant eval`, `orchestra not factory`, `eval over code review`, `DevEx metrics AI`

## Curriculum (order)

| # | Skill | Primary talks |
|---|--------|----------------|
| 1 | [`factory-operator`](../factory-operator/SKILL.md) | WorkOS, Factory.com, Warp Lloyd |
| 2 | [`process-embedded-factory`](../process-embedded-factory/SKILL.md) | WorkOS embed |
| 3 | [`factory-harness`](../factory-harness/SKILL.md) | Warp Gupta/Lloyd |
| 4 | [`covariant-eval-loop`](../covariant-eval-loop/SKILL.md) | W&B |
| 5 | [`agent-orchestra`](../agent-orchestra/SKILL.md) | Conductor |
| 6 | [`pr-pulse-discipline`](../pr-pulse-discipline/SKILL.md) | Pocock |
| 7 | [`eval-over-review`](../eval-over-review/SKILL.md) | Voss |
| 8 | [`devex-metrics-grounding`](../devex-metrics-grounding/SKILL.md) | DX |

OS diagram: [`assets/factory-os-diagram.mmd`](assets/factory-os-diagram.mmd) · Tier cheatsheet: [`assets/reference-tier-cheatsheet.md`](assets/reference-tier-cheatsheet.md)

Registry (monorepo): [`docs/research-insights/paris-2026.yaml`](../../docs/research-insights/paris-2026.yaml)
