# Build-out research memo — what exists and what to ship next

**Date:** 2026-10-01 · **Audience:** cold agent resuming the programme · **Sources:** `HANDOFF.md`, `options/OPTIONS.md`, `plans/ADVERSARIAL.md`, `witness/`, `experiments/`.

---

## Inventory — what we have today

### E1 witness (R8 faithfulness)

| Item | Status | Notes |
|------|--------|-------|
| `witness/run_witness.py` | **Shipped** | Monolithic generator + extractor + checks; ~300 LOC; 13 booleans. |
| `witness/WITNESS.json` | **Shipped** | Artifact of record; witnesses for steps 5–10. |
| `witness/toybank/**` | **Regenerated** | 16 Java-flavored files; deterministic on each run. |
| `experiments/PROTOCOL-E1.md` | **Shipped** | Verbatim frozen protocol. |
| `docs/witness/WITNESS-HOW-IT-WORKS.md` | **Shipped** | Architecture + check table + diagrams. |
| `FOUNDATION.md` / full **Code_X** | **Missing** | Lost in reclamation; C₀ documented as skeleton only. |
| `witness/gen_toybank.py`, `witness/extract.py` | **Not split** | Protocol mentions separate modules; implementation is inline in runner. |

### E2 token arithmetic (GA6 micro-example)

| Item | Status |
|------|--------|
| `experiments/e2-tokens/` | Packs, raw Fineract snippets, tokenizer scripts, `E2-RESULTS.md` |
| Outcome | **WIN 3/3** sites; break-even n* = 2–5; re-expansion byte-identical |

### E3 format-comprehension ablation (GA7 pilot)

| Item | Status |
|------|--------|
| `experiments/e3-ablation/` | `packA/B/C.txt`, `e3_build.py`, `e3_grade.py`, frozen responses, `E3-RESULTS.md` |
| Outcome | **B PASSES** vs A at 63% tokens; C floor 0% |
| Gap | Full protocol (50+10 q, mixed sites, firewalled minting) not run |

### E5 / E5.1 depth

| Item | Status |
|------|--------|
| `experiments/e5-depth/` | 112×10 questions, packs, v1/v2 harness fix, `E5-RESULTS.md`, grades JSON |
| Outcome | **B PASSES AT DEPTH** after legend fixes; pooled B−A = −3.7 pts |

### E4 migration chain

| Item | Status |
|------|--------|
| Protocol / harness | **Not in repo** | Referenced in OPTIONS + ADVERSARIAL early-migration milestone |

### Programme docs & plans

| Item | Status |
|------|--------|
| `plans/CONSENSUS.md`, `ADVERSARIAL.md`, `OPTIONS.md` | Restored verbatim |
| `synthesis/SYNTHESIS.md` | Crosswalk + R8 faithfulness checklist |
| `wiki/INDEX.md` | Page crosswalk (deep wiki 01–07 lost) |
| `dashboard/index.html`, `review/index.html` | Editorial status surfaces |

### Scripts & tooling gaps

| Gap | Risk (ADVERSARIAL) |
|-----|---------------------|
| No reproducible **one-command** runner for E2/E3/E5 | Hard to re-verify claims after restore |
| No **pack builder v0** as library | E2/E3 scripts are experiment-local |
| No **WiringMap v0** extractor | Option 2 blocked; L1/L2 still hand/mined |
| **SKILL.md** minting debt | GA10 — instruments described in prose only |
| Benchmark / CR@F95 harness | GA8 — explicitly out of scope until cheap artifacts done |

---

## Recommended build order (artifacts-first, unchanged from OPTIONS + HANDOFF)

1. **Document + freeze witness** (this memo + `WITNESS-HOW-IT-WORKS.md`) — done on this branch.
2. **Mint three free SKILL instruments** — zero-code ROI; unblocks dogfooding and E3 firewall narrative.
3. **Reproducible experiment runner** — thin `Makefile` or `experiments/run_all.sh` with pinned hashes; no new science.
4. **Pack builder v0** — extract L2 `(seed, marking, motif, instance table)` from one Fineract family; reuse E2 re-expansion gate.
5. **WiringMap v0** — one Spring monorepo slice: interface catalog + UWD-style edges + system cards; feeds pack builder.
6. **C₀ → Code_X witness upgrade** — split extract/pushout; exhaustive universal check within bound; MUST-PROVE 1–2 hook.
7. **Full E3 + Fineract wedge + E4 migration milestone** — after map + pack exist.

```
  E1 witness (13/13 C₀)
        │
        ├──────────────────────┬─────────────────────────┐
        v                      v                         v
  SKILL minting (3 free)   Repro runner            Code_X upgrade
        │                  E2 / E3 / E5                   │
        v                      │                         v
  Pack builder v0 (L2)         │                   WiringMap v0 (T1)
        ^                      │                         │
        └──── WiringMap v0 ────┘                         │
        │                                                │
        └──────────────────┬───────────────────────────┘
                           v
                  Full E3 + Fineract wedge + E4
```

---

## Upcoming pieces — MVP, dependencies, proof hook, risks

### 1. SKILL minting (`systems-intake`, `interface-first-context`, `symmetry-lens`)

| | |
|--|--|
| **Status** | **`interface-first-context` shipped** → [`skills/interface-first-context/SKILL.md`](../../skills/interface-first-context/SKILL.md). Remaining: `systems-intake`, `symmetry-lens`. |
| **Dependencies** | `OPTIONS.md`, `SYNTHESIS.md`, `CONSENSUS.md`; no code required. |
| **MVP scope** | One `SKILL.md` each: trigger phrases, 5–7 moves, quality checklist, failure modes, one dogfood example (Fineract handler or toybank). |
| **Proof-case hook** | E1 toybank for symmetry-lens orbit demo; E3 packs for interface-first-context. |
| **ADVERSARIAL risks** | **GA10** — prose without minted instruments; **GA7** — comprehension assumptions stay implicit unless checklist forces explicit legend/sentinel rules from E5. |

### 2. Reproducible runner

| | |
|--|--|
| **Dependencies** | Existing `e2-tokens/`, `e3-ablation/`, `e5-depth/` scripts; `package.json` in experiments if Node used. |
| **MVP scope** | Single entrypoint: run witness → assert 13/13; run E2 counts; optional E3 grade on frozen responses only (no API). |
| **Proof-case hook** | CI-style gate: fail if `WITNESS.json` or E2 numbers drift without commit. |
| **Risks** | **GA8** — runner does not substitute frozen question sets + firewall for live minting. |

### 3. Pack builder v0 (OCC L2)

| | |
|--|--|
| **Dependencies** | WiringMap or minimal hand-curated graph for one family; E2 `pack_*` format as spec; tokenizer `cl100k_base`. |
| **MVP scope** | One `@CommandType` handler family: emit pack A + pack B; **byte-identical re-expansion** test; publish F, m, e, n*. |
| **Proof-case hook** | Extends E2 WIN; prerequisite for full E3 on mixed sites. |
| **Risks** | **GA4** — motif dictionary ≠ paper restriction; label substitution soundness unproved. **GA6** — fixed legend overhead can kill wins on small n. **GA7** — pack unreadable if legend incomplete (E5 lesson). |

### 4. WiringMap v0 (Option 2 spine)

| | |
|--|--|
| **Dependencies** | Static extractors (imports, Spring annotations, DI) for one repo; optional trace CSV for recall metric later. |
| **MVP scope** | JSON schema: `interfaces[]`, `units[]`, `edges[]` (doctrine tag per edge); 30–50 file Fineract vertical slice; no runtime overlay. |
| **Proof-case hook** | Feeds pack builder; early-migration milestone needs depth ≥3 slice. |
| **Risks** | **GA1** — “derived guarantees” language forbidden until MUST-PROVE 1. **GA2** — orbit folding only on exact-iso cells. **GA10** — recall number is the honest deliverable vs Sourcegraph parity claims. |

### 5. Witness C₀ → Code_X

| | |
|--|--|
| **Dependencies** | Reconstruct or rewrite `FOUNDATION.md`; split `extract.py` / category module from runner. |
| **MVP scope** | Copresheaf-style objects; κ on quotient; universal property enumeration at protocol width; same 13 checks green. |
| **Proof-case hook** | MUST-PROVE 1 (gluing soundness) and 2 (equivariance + invariant) entry point. |
| **Risks** | **GA1** rex vs presheaf collision story; external freshening if step 5 fails → CODE-C revision, not local patch (PROTOCOL decision rules). |

---

## What not to build yet

- Full **CR@F95 benchmark** before pack + map + firewall E3 (**GA8**).
- **L3/L4** orbit folding in production packer before WiringMap + symmetry audit (**GA2**, **GA4**).
- **Migration square harness** (Option 3) before WiringMap v0 + equivalence judge design (**GA5**).

---

## Immediate next commit targets (engineering)

1. Add `experiments/README.md` with run order and expected artifacts (optional follow-up).
2. ~~Mint first SKILL: `interface-first-context`~~ **Done** — see [`skills/interface-first-context/SKILL.md`](../../skills/interface-first-context/SKILL.md).
3. Define `wiringmap/schema.v0.json` stub when starting WiringMap v0 (empty example + one Fineract edge).

---

## References

- Witness detail: [`docs/witness/WITNESS-HOW-IT-WORKS.md`](../witness/WITNESS-HOW-IT-WORKS.md)
- Sequencing: [`options/OPTIONS.md`](../../options/OPTIONS.md)
- Gaps: [`plans/ADVERSARIAL.md`](../../plans/ADVERSARIAL.md)
- Resume: [`HANDOFF.md`](../../HANDOFF.md)
