---
name: interface-first-context
description: Build L1 interface-only LLM context packs (catalog, system cards, wiring edges, omissions log). Auto-apply when mapping repos, wiring summaries, Fineract/Spring slices, manual OCC L1 before L2 factoring, or when user asks for interface-first / repo-map / ports-only context.
---

# Interface-first context (L1)

Manual **T3-L1** projection: exported surfaces + typed wiring, no implementation bodies unless explicitly requested. Aligns with Option 1 L1 in [`options/OPTIONS.md`](../../options/OPTIONS.md); interface axiom in [`synthesis/SYNTHESIS.md`](../../synthesis/SYNTHESIS.md).

## When to use

- Bootstrapping context for a monorepo slice (Spring MVC, handlers, services) before deeper compression.
- Producing a **WiringMap feedstock** catalog (units + edges) without motif factoring yet.
- Capping tokens under a hard budget while preserving cross-file navigation (CONSENSUS R4: interface-only baseline vs aider repo-map).
- Dogfooding witness-scale repos ([`witness/toybank/`](../../witness/toybank/)) before Fineract-scale packs.
- Any task where the user says "ports only", "interface catalog", "L1 pack", or "wiring summary".

## When NOT to use

- Implementation-local bug hunt (needs method bodies, tests, or stack traces — L1 will miss; see R4 predicted losses in [`plans/CONSENSUS.md`](../../plans/CONSENSUS.md)).
- Replacing a **factored L2 pack** when redundancy is high and legend is ready — run L1 first, then L2 per [`experiments/e2-tokens/pack_LEGEND.txt`](../../experiments/e2-tokens/pack_LEGEND.txt).
- Claiming doctrine-derived guarantees on extraction (GA10 — demonstrated on witness only until MUST-PROVE 1).
- Orbit folding / symmetry diffs (use symmetry-lens when minted; not this skill).

## Quick procedure

1. **Scope** — Name repo, commit/ref, vertical slice (e.g. `accounts/` MVC chain), and token budget if any.
2. **Ports** — For each compilation unit, list **exported** symbols only (public API, schemas, topics). Source: [`docs/witness/WITNESS-HOW-IT-WORKS.md`](../../docs/witness/WITNESS-HOW-IT-WORKS.md) — ports = exported symbols; refs from `// refs:` or static import/call edges.
3. **System cards** — One card per unit: role, ports table (symbol → kind/signature stub), internal symbols **omitted** unless user asked.
4. **Wiring edges** — Explicit `Unit → Target#symbol` (call/DI/import/link); tag junction nodes (DTO, table, topic) when shared.
5. **Parallel product boundary** — Mark unrelated modules with `‖` (no edges) per SYNTHESIS crosswalk — safe truncation line.
6. **Omissions log** — Every elided file/symbol with reason (`impl-local`, `out-of-slice`, `duplicate-of-savings-orbit`, etc.).
7. **Quality gate** — Run checklist below; fix before delivery. Optional L2: only after gate passes.

## Output template

```markdown
# L1 — {repo} · {slice} · {ref}

## Interface catalog
| unit_id | path | role | port_count |
|---------|------|------|------------|
| ...     | ...  | ...  | n          |

## Per-unit cards
### {unit_id} (`{path}`)
**Ports (exported only)**
- `{symbol}` — {kind}: `{signature_stub}`

**Wiring (outbound)**
- → `{Target}#{symbol}` ({edge_kind: call|ref|import|di})

## Wiring edges (flat)
- `{Source}` → `{Target}#{symbol}`

## Omissions log
- `{path}` — {reason}

## Legend stub (only if shorthand used)
- `-` — omit optional annotation line (E5 sentinel; MUST define if used)
- `*Foo*` — glob rule: {suffix|substring|path} (define explicitly)
```

## Quality gate

- [ ] **Ports only** — No method bodies, private fields, or full AST dumps unless user requested.
- [ ] **Every edge endpoint is a named port or junction** — DTO/table/topic nodes listed in catalog when they glue units.
- [ ] **Reader-spec-equivalent** — Any shorthand, sentinel, or glob has a **Legend stub** matching E5: pack readable by the model, not only re-expandable by the builder ([`experiments/e5-depth/E5-RESULTS.md`](../../experiments/e5-depth/E5-RESULTS.md)).
- [ ] **Sentinel `-`** — If used: documented as "omit this anno line" (E5.1 fix).
- [ ] **Globs** — Suffix vs substring stated (E5 `*Repository*` lesson).
- [ ] **No silent collisions** — Same simple name on incompatible signatures (witness Money case) called out, not merged.
- [ ] **Claims discipline** — No "canonical minimal motif" (GA4); L1 is not L2 restriction seed vocabulary.

## After L1 (L2 hook)

When the quality gate passes and redundancy warrants it, emit **factored** packs: `motif` + `inst(...)` + delta lines per [`experiments/e2-tokens/pack_LEGEND.txt`](../../experiments/e2-tokens/pack_LEGEND.txt). Require byte-identical re-expansion vs explicit `dep`/`edge` rows (E2 gate). GA7: incomplete legend = comprehension tax — never ship L2 without legend parity to E5 rules.

## Failure modes

| Symptom | Fix | Ref |
|---------|-----|-----|
| Model misses cross-file links | Add flat **Wiring edges** + port signatures on both ends | [`synthesis/SYNTHESIS.md`](../../synthesis/SYNTHESIS.md) Interface row |
| Pack "equivalent" but model fails | Legend missing `-`, Constants fills, or glob gloss | [`experiments/e5-depth/E5-RESULTS.md`](../../experiments/e5-depth/E5-RESULTS.md) |
| Token budget blown | Drop impl bodies (default), then non-exported symbols; keep catalog + edges | [`plans/CONSENSUS.md`](../../plans/CONSENSUS.md) R4 baselines |
| Confused restriction vs motif | L1 lists all explicit edges; L2 motif dict is engineering add-on, not paper restriction | [`plans/ADVERSARIAL.md`](../../plans/ADVERSARIAL.md) GA4 |
| Over-claimed extraction | Label as manual/partial; cite witness demo scale | [`HANDOFF.md`](../../HANDOFF.md) §3 |
| DI/reflection invisible | Note R6 gap in omissions; do not invent edges | [`plans/CONSENSUS.md`](../../plans/CONSENSUS.md) R6 |

## Dogfood example (toybank · Accounts vertical)

Witness source: [`witness/toybank/accounts/`](../../witness/toybank/accounts/). Ports = `public` methods; wiring from `// refs:` comments ([`docs/witness/WITNESS-HOW-IT-WORKS.md`](../../docs/witness/WITNESS-HOW-IT-WORKS.md)).

```markdown
# L1 — toybank · accounts MVC · witness generated

## Interface catalog
| unit_id | path | role | port_count |
|---------|------|------|------------|
| accounts.Ctrl | accounts/AccountsController.java | HTTP adapter | 2 |
| accounts.Svc | accounts/AccountsService.java | domain | 2 |
| accounts.Repo | accounts/AccountsRepository.java | persistence | 2 |

## Per-unit cards
### accounts.Ctrl
**Ports:** `list(int)→Page`, `get(long)→Dto`
**Wiring:** → `accounts.AccountsService#fetchPage`, `#fetchOne`; → `shared.PageDto#of`; → `shared.AuditDto#log`

### accounts.Svc
**Ports:** `fetchPage(int)→Page`, `fetchOne(long)→Dto`
**Wiring:** → `accounts.AccountsRepository#findPage`, `#findOne`; → `shared.EventTopics#EVT`

### accounts.Repo
**Ports:** `findPage(int)→Page`, `findOne(long)→Dto`
**Wiring:** → `shared.PageDto#of`

## Wiring edges (flat)
- AccountsController → AccountsService#fetchPage
- AccountsController → AccountsService#fetchOne
- AccountsService → AccountsRepository#findPage
- AccountsService → AccountsRepository#findOne

## Omissions log
- `void log(...)` on each unit — non-exported / internal
- `accounts/Money.java` — out of vertical slice (collision pair with loans documented in witness step 9)

## Legend stub
(none — fully explicit L1)
```

## References

- [options/OPTIONS.md — Option 1 L1 / OCC wedge](../../options/OPTIONS.md)
- [synthesis/SYNTHESIS.md — interface axiom & crosswalk](../../synthesis/SYNTHESIS.md)
- [plans/CONSENSUS.md — R4 compression, interface-first baseline](../../plans/CONSENSUS.md)
- [plans/ADVERSARIAL.md — GA7 comprehension, GA4 restriction vs motif](../../plans/ADVERSARIAL.md)
- [experiments/e5-depth/E5-RESULTS.md — sentinel & glob rules](../../experiments/e5-depth/E5-RESULTS.md)
- [experiments/e2-tokens/pack_LEGEND.txt — L2 pack format](../../experiments/e2-tokens/pack_LEGEND.txt)
- [docs/witness/WITNESS-HOW-IT-WORKS.md — ports & toybank graph](../../docs/witness/WITNESS-HOW-IT-WORKS.md)
- [HANDOFF.md — claims & minting status](../../HANDOFF.md)
