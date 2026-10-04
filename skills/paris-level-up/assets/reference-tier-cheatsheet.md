# Reference tiers (Paris factory plugin)

| Tier | Where | Use when |
|------|--------|----------|
| **L1** | SKILL.md `Layer 1` | Quick auto-apply / operator one-liner |
| **L2** | SKILL.md core moves | Executing a factory change |
| **L3** | SKILL.md `References` segment ids | Audit trail without pasting quotes |
| **L4** | `references/index.yaml` segments | MM:SS, label FACT/CONJECTURE, summary |
| **L5** | `transcript-summaries.json` + captions | Faithfulness review, evaluator pass |

**Monorepo:** `research/ai-engineer-paris-2026/references/index.yaml`  
**Portable copy:** `skills/paris-level-up/assets/references-index.yaml`

**Default tier in manifest:** `referenceTierDefault: L3` — agents stay on moves unless user asks for cites.
