# Craft skills integration (external guardrails)

Programme repo **wiring-and-the-whole** keeps pulse rubrics and witness harness on `main`. [**craft**](https://github.com/manutej/craft) supplies composable **code-quality** skills (production-grade router + member skills + `RULES.md` constitution). Pull craft in for **maintainability** checks; keep **pulse closure** on programme artifacts.

## Resolution order

1. **Local checkout** — `CRAFT_SKILLS_ROOT` or repo sibling `craft/` (cloud agents: clone to `/workspace/craft`).
2. **Upstream raw** — bundle JSON includes `raw_url` per skill under `https://raw.githubusercontent.com/manutej/craft/main/…`.
3. **No vendor copy on `main`** — do not subtree-merge craft into `skills/`; index only (see `make meta-evaluator`).

## Mapping to pulse lanes

| Lane | Use craft? | Use programme rubric? |
|------|------------|------------------------|
| Implementer | Optional member skill when editing application code; prefer smallest diff | **Must not** read rubric |
| Adversarial panel | Findings may cite craft principles as cheap checks | Independent of rubric scoring |
| Evaluator (firewalled) | May note slop patterns; scores only via [`RUBRIC-EVALUATOR.md`](RUBRIC-EVALUATOR.md) | **Yes** |
| Meta-evaluator (post-loop) | **`make meta-evaluator`** skill index + `RULES.md` link | **No rubric text** in bundle |

## Operator commands

```bash
git clone https://github.com/manutej/craft ../craft   # or export CRAFT_SKILLS_ROOT=/path/to/craft
make meta-evaluator-check
make meta-evaluator | jq '.craft.skills[].name'
```

## Router entrypoint

- Skill: `production-grade` — generative guard before writing; critique mode on diffs.
- Constitution: [`RULES.md`](https://github.com/manutej/craft/blob/main/RULES.md) (13 always-on rules).

Member skills indexed by [`scripts/meta_evaluator_hook.py`](../../scripts/meta_evaluator_hook.py) at generation time.

## Related programme skills (in-repo)

- [`skills/interface-first-context/SKILL.md`](../../skills/interface-first-context/SKILL.md) — navigation / L1 contract
- [`skills/systems-intake/SKILL.md`](../../skills/systems-intake/SKILL.md) — slice questionnaire stub
- [`skills/symmetry-lens/SKILL.md`](../../skills/symmetry-lens/SKILL.md) — symmetry framing

These stay on `main`; craft remains an external index unless a future pulse charters a submodule pin.
