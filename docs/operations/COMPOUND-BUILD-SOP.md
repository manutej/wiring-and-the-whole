# Compound build SOP — MVP push

**Goal:** Ship **M1 Engine MVP** then **M2 1k charter** without process theater.

## Roles (segregated)

| Role | Knows | Must not | Output |
|------|--------|----------|--------|
| **Builder** | [`BUILD-SPEC-*.md`](build-specs/) only | Eval rubric, adversarial playbook, other agents' threads | Code + commits on `cursor/mvp-engine-push-cd12` |
| **Independent evaluator** | Diff + gates + build spec done-criteria | Implementer chat | `docs/pulse/evaluations/*-independent.md` SHIP/NO-SHIP |
| **Adversarial** | Same as eval + `plans/ADVERSARIAL.md` | Implement fixes | `docs/pulse/adversarial/*-independent.md` |
| **Monitoring** | Checklist + gate timestamps | Code | `docs/operations/build-log/YYYY-MM-DD.md` |
| **Math / limits** | Token reports, frozen JSON, claims | Implementation | `docs/operations/build-log/*-math.md` |
| **Senior architecture** | Architecture + craft skills | Task-level pass/fail | `docs/operations/build-log/*-arch.md` |
| **PR steward** | Branch hygiene, push | Open PR until MVP bundle green | Notes in build-log; **no PR** until checklist M1 complete |

## Per slice workflow

1. Builder implements against **build spec** → `git commit` → `git push`
2. Parallel: adversarial + math + arch review on pushed SHA
3. Independent evaluator → SHIP required to mark checklist item done
4. Monitoring appends one line to build-log

## Merge policy

- **No GitHub PR** until checklist **M1d** complete and eval SHIP on bundle.
- Then PR steward opens **one** integration PR.

## Craft

Apply [manutej/craft](https://github.com/manutej/craft): effects-and-purity, trustworthy-tests, robustness-at-boundaries, right-sized-design.
