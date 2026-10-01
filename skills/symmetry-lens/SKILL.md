---
name: symmetry-lens
description: T2a symmetry audit over WiringMap slices — exact-iso orbit cells, σ/φ transport, invariant checklists, symmetry-breaking diffs. Auto-apply when folding duplicate MVC verticals, accounts‖savings orbits, density D3, refactor equivariance review, or user asks symmetry-lens / orbit audit / Option 4.
---

# Symmetry-lens (T2a audit)

**Design-review protocol** for wiring equivariance and orbit representatives — Option 4 in [`options/OPTIONS.md`](../../options/OPTIONS.md). Formal claims stay on **exact-isomorphism cells** only ([`plans/ADVERSARIAL.md`](../../plans/ADVERSARIAL.md) **GA2**); name and compute at least one **nontrivial interface invariant** constant on the orbit ([**GA3**]). No **"Noether"** in formal claims or checklist titles ([`plans/CONSENSUS.md`](../../plans/CONSENSUS.md) R2); prose may say "after Noether" as analogy only.

Witness anchor: **step 7** wiring automorphism ⇒ composite iso ([`docs/witness/WITNESS-HOW-IT-WORKS.md`](../../docs/witness/WITNESS-HOW-IT-WORKS.md), [`experiments/PROTOCOL-E1.md`](../../experiments/PROTOCOL-E1.md)).

## When to use

- Two or more vertical slices look like **rename duplicates** (e.g. `accounts/` vs `savings/` MVC triples) before L3 orbit folding or token factoring.
- Reviewing whether a refactor **preserves wiring symmetry** (system map + tier swap σ still composes).
- Producing **symmetry-breaking diffs** — the one controller that differs from its orbit mates is the review item (Option 4c).
- Dogfood / stress: [`fixtures/density/d3-orbit/`](../../fixtures/density/d3-orbit/) or [`witness/toybank/`](../../witness/toybank/) with `accounts/ ‖ savings/` boundary.
- User asks "orbit table", "equivariance check", "invariant checklist", or "symmetry auditor".

## When NOT to use

- **Interface-only L1** catalog with no orbit hypothesis — use [`skills/interface-first-context/SKILL.md`](../interface-first-context/SKILL.md) first.
- **Approximate / ε>0 symmetry** as a licensed fold — GA2: no approximate equivariance theorem in repo; treat ε-orbits as *heuristic flags* only, never as sound compression claims.
- **Conserved quantities along trajectories** (Petri P-invariants, runtime flows) — that is T2b research, not this prompt instrument.
- **Theorem-derived guarantees** — checklists are engineering audit, not MUST-PROVE 2 discharge ([`plans/ADVERSARIAL.md`](../../plans/ADVERSARIAL.md) GA10).
- **Motif dictionary / L2 restriction seed** without substitution proof — GA4; symmetry-lens does not replace E2 legend work.

## Quick procedure

1. **Inputs** — WiringMap v0 or L1 pack: units, exported ports, edges; mark parallel product `‖` between unrelated verticals ([`synthesis/SYNTHESIS.md`](../../synthesis/SYNTHESIS.md) crosswalk).
2. **Orbit hypothesis** — Name tiers (e.g. `A` = accounts, `S` = savings). Define **component iso** φ: kind + **signature_stub** bijection on matched units (namespace rename only at witness scale — no search).
3. **Composite glue** — For each tier, record MVC chain composite (Controller→Service→Repository) as finite port/edge structure.
4. **Automorphism σ** — Tier swap on parallel product `W = A ‖ S` (prescribed σ, not discovered). **Step 7 pattern:** glue-then-swap vs swap-then-glue; construct induced map; verify bijection + inverse on finite composite (construct-then-verify).
5. **Exact-iso gate (GA2)** — Orbit fold / representative selection allowed **only** if every matched cell is exact-iso under φ (ports, stubs, edge kinds). If any delta remains, **do not fold** — emit **symmetry-breaking diff** with file:line or port id.
6. **Invariant B (GA3)** — Define finite relation on exported wiring (witness: directed `(port_a, port_b)` where `a` exports and `b` is in `refs` and exported elsewhere). Verify: `B_A` transported along φ equals `B_S`; system maps from refactor leave B unchanged on fixed ports (steps 8–8a pattern).
7. **Outputs** — Orbit table, one named invariant summary, checklist for refactor, anomalies list, claims footnote (demonstrated on witness/D3 only until MUST-PROVE 2).
8. **Quality gate** — Run checklist below before recommending L3 fold or token savings.

## Output template

```markdown
# Symmetry audit — {repo} · {slice} · {ref}

## Parallel product boundary
- `{pathA}/` ‖ `{pathB}/` — {edge_policy: no cross-tier edges | list exceptions}

## Orbit hypothesis
| tier | units | role |
|------|-------|------|
| A | ... | ... |
| S | ... | orbit twin |

## Component iso φ (exact-iso cells only)
| A unit#port | S unit#port | stub match |
|-------------|-------------|------------|
| ... | ... | yes / **BREAK** |

## Step 7 — σ swap on W = A ‖ S
- Prescribed σ: ...
- Composite check: glue(A)↔glue(S) induced iso: **pass | fail**
- Notes: construct-then-verify (no iso search)

## Invariant B (GA3 — named)
- Definition: ...
- B_A vs transport(φ, B_S): **equal | diff**
- System-map stability (if applicable): ...

## Orbit table (exact-iso representatives)
| orbit_id | representative | members | fold_ok |
|----------|----------------|---------|---------|
| ... | ... | ... | yes / **no — delta** |

## Symmetry-breaking diffs (review flags)
- `{unit}#{port}` — delta: {what differs} — triage: bug | debt | intentional

## Refactor checklist (interface-level, not theorem-derived)
- [ ] Every exported port key/signature unchanged under declared system map
- [ ] σ ∘ glue equals glue ∘ σ on checked composite (step 7 pattern)
- [ ] Invariant B preserved on orbit members
- [ ] No fold claim where GA2 exact-iso fails

## Claims discipline
- Demonstrated: {witness | D3 | manual slice} — not MUST-PROVE 2/3
- No Noether in formal claims; no ε-fold soundness without audit
```

## Quality gate

- [ ] **GA2 exact-iso** — Every `fold_ok: yes` row has byte-level stub/port/edge-kind match under φ; otherwise `fold_ok: no` + diff.
- [ ] **GA3 nontrivial invariant** — One named finite invariant computed on both orbit members; "constant on orbits" stated only with shown equality or explicit diff.
- [ ] **Step 7 explicit** — σ and φ prescribed; composite iso check described (pass/fail), not hand-waved.
- [ ] **No Noether branding** — Checklist titles use "invariant" / "equivariance" / "symmetry audit", not "Noether law" or "conservation theorem".
- [ ] **Parallel product honest** — Cross-tier edges absent or listed; `‖` boundary matches L1 omissions.
- [ ] **No silent κ** — Colliding simple names with incompatible signatures (witness `Money`) flagged, not merged ([`witness/run_witness.py`](../../witness/run_witness.py) step 9 lesson, GA1).
- [ ] **Claims ladder** — Label scale (toybank, D3, Fineract TBD); cite ADVERSARIAL GA2/GA3/GA10 where relevant.

## After audit (L3 hook)

When exact-iso orbits dominate and redundancy metrics exceed pre-registered thresholds ([`plans/CONSENSUS.md`](../../plans/CONSENSUS.md) R4–R5), **candidate** L3 fold: one representative + structured deltas per orbit — only after this gate passes. Symmetry-soundness error budget **<2%** is a program metric, not satisfied by prompt alone. ε-orbits: audit every delta; the differing service is the review item (Option 4c).

## Failure modes

| Symptom | Fix | Ref |
|---------|-----|-----|
| Fold claimed with renamed internals only | Require port-key + **signature_stub** match under φ | GA2 exact-iso |
| "Invariant constant on orbits" with no definition | Instantiates **GA3 vacuity** — define B (or other finite relation) and show transport | PROTOCOL-E1 step 8 |
| Iso "found" by search narrative | Witness uses **construct-then-verify** on prescribed σ, φ | Step 7 |
| ε-symmetry folded into pack | Heuristic flag only; separate anomalies list; no soundness claim | GA2, R5 |
| Confused with L2 motif | Orbit fold ≠ motif dictionary; restriction seed separate | GA4 |
| Noether in checklist title | Rename to symmetry / invariant transfer | R2, GA10 |
| accounts/savings edges invented | Respect `‖`; extract only `// refs:` evidence | R6, density D3 |

## Dogfood example (toybank · accounts ‖ savings)

**Sources:** [`witness/toybank/accounts/`](../../witness/toybank/accounts/), [`witness/toybank/savings/`](../../witness/toybank/savings/) — parallel product, no cross-tier refs in E1 vertical. Machine mirror for orbit stress: [`fixtures/density/d3-orbit/wiringmap.v0.json`](../../fixtures/density/d3-orbit/wiringmap.v0.json) (D3 ladder, [`fixtures/density/README.md`](../../fixtures/density/README.md)).

```markdown
# Symmetry audit — toybank · accounts ‖ savings · witness / D3

## Parallel product boundary
- `witness/toybank/accounts/` ‖ `witness/toybank/savings/` — no edges between tiers (E1 slice)

## Orbit hypothesis
| tier | units | role |
|------|-------|------|
| A | AccountsController, AccountsService, AccountsRepository | MVC |
| S | SavingsController, SavingsService, SavingsRepository | orbit twin (namespace rename) |

## Component iso φ (exact-iso cells only)
| A | S | stub match |
|---|----|------------|
| AccountsController#list | SavingsController#list | yes |
| AccountsService#fetchPage | SavingsService#fetchPage | yes |
| AccountsRepository#findPage | SavingsRepository#findPage | yes |

## Step 7 — σ swap on W = A ‖ S
- Prescribed σ: swap tier tags on glued composites; φ renames Accounts* ↔ Savings*
- Composite check: **pass** at witness scale (`step7_automorphism_composite_iso` in WITNESS.json)
- Method: construct induced map; verify inverse on finite comp — no search

## Invariant B (GA3 — named)
- Definition: exported-port reachability along `refs` (step 8)
- B_accounts vs transport(φ, B_savings): **equal** (`step8_invariant_constant_on_orbit`)

## Orbit table (exact-iso representatives)
| orbit_id | representative | members | fold_ok |
|----------|----------------|---------|---------|
| mvc-page | accounts.* chain | savings.* chain | yes (stubs match; audit internal `#log` only on system-map step 6) |

## Symmetry-breaking diffs
- (none in clean witness — plant a delta in a fork to exercise Option 4c triage)

## Refactor checklist
- [x] Step 7 composite iso documented
- [x] Invariant B named and compared
- [x] GA2: fold_ok only where stub match yes

## Claims discipline
- Demonstrated: E1 witness 13/13 — not general Fineract or MUST-PROVE 2
```

**D3-only probe:** `python3 scripts/extract_refs.py fixtures/density/d3-orbit/accounts --example fixtures/density/d3-orbit/wiringmap.v0.json` (expect exit 0 per density README).

## References

- [options/OPTIONS.md — Option 4 Symmetry Auditor](../../options/OPTIONS.md)
- [plans/ADVERSARIAL.md — GA2 exact-iso, GA3 invariant, GA10 claims](../../plans/ADVERSARIAL.md)
- [plans/CONSENSUS.md — R2 T2a/T2c split, R5 approximate orbits](../../plans/CONSENSUS.md)
- [docs/witness/WITNESS-HOW-IT-WORKS.md — step 7 diagram, steps 8–8a](../../docs/witness/WITNESS-HOW-IT-WORKS.md)
- [experiments/PROTOCOL-E1.md — steps 7–8 GA3 discharge](../../experiments/PROTOCOL-E1.md)
- [fixtures/density/d3-orbit/ — orbit stress fixture](../../fixtures/density/d3-orbit/)
- [skills/interface-first-context/SKILL.md — L1 prerequisite](../interface-first-context/SKILL.md)
- [wiringmap/schema.v0.json — unit/port/edge ids](../../wiringmap/schema.v0.json)
- [HANDOFF.md — minting status & claims](../../HANDOFF.md)
