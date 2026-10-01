# The Wiring & the Whole

Research corpus for a simple bet:

> A large codebase is not a pile of files. It is a **module of systems** — units known only through interfaces, glued by typed interaction patterns. If that algebra is real, you should be able to ship the *wiring* to an LLM instead of the *whole*, cheaper and without a comprehension tax.

This repo is the recovered working record of that program: paper digestion, consensus repairs, adversarial gaps, a toy faithfulness witness, and three experiments on real [Apache Fineract](https://github.com/apache/fineract) Java.

**Start here:** [`HANDOFF.md`](HANDOFF.md) · recovery ledger: [`RECOVERY.md`](RECOVERY.md)

Paper in the background: Libkind & Myers, *[Towards a Double Operadic Theory of Systems](https://arxiv.org/abs/2505.18329)* (arXiv:2505.18329v2, 80pp).

---

## What was discovered

Four empirical results, in the order they were required to exist.

| Experiment | Question | Result | What it is allowed to mean |
|---|---|---|---|
| **E1** witness | Can "codebase = module of systems" be *demonstrated* on a real gluing, not just asserted? | **13/13** checks on a 16-file toybank | Demonstrated at toy scale on `C₀` SymTab. Not a proof of `Code_X`. |
| **E2** tokens | Is the factored `(seed, marking, motif)` form actually cheaper than explicit edge lists? | **WIN on 3/3** Fineract sites. Break-even `n* = 2–5` vs family sizes 54–514. Re-expansion gate **byte-identical**. | L2 token arithmetic is live at micro-scale. Not repo-scale savings. |
| **E3** ablation | Do models *read* the factored form, or do you pay a comprehension tax? | **B PASSES.** A 93.8% vs B 95.3% vs C 0% on the wiring pool. B uses **63%** of A's tokens. | No ≥5-pt tax at pilot scale on one convention-heavy family. |
| **E5 / E5.1** depth | Does that parity survive multi-hop / depth? | **B PASSES AT DEPTH.** Pooled B−A = **−3.7 pts**. Sonnet **100% at every depth in both arms**. Raw −10.2 pts was ~80% harness artifact. | Information-equivalence must be **spec-equivalence for the reader**, not just re-expandable by the builder. |

The binding lesson from E5 is the one that travels: a pack can be lossless under the builder's private expansion function and still be unreadable, if the legend forgets to define a sentinel. After two spec fixes (document the `-` omit-marker; disambiguate `*Repository*`), the depth collapse disappeared.

---

## The bet, layered

Compression is not "delete tokens." It is a 4-layer pipeline:

1. **L1** — interface-only projection (aider's repo-map is already roughly this)
2. **L2** — pattern dictionary: ship `(seed, marking, motif, instance table)`, not spelled-out graphs
3. **L3** — ε-orbit folding (representative + structured deltas; exact-iso cells only)
4. **L4** — doctrine-annotated elision

The headline that is allowed: **marginal gain of L2–L4 over interface-only**, measured as CR@F95 (tokens to reach ≥95% of full-context accuracy). That full benchmark is **not in this repo**. E2 and E3/E5 are the cheap precursors the adversarial panel demanded before any benchmark code.

---

## E2 numbers (real Fineract files, 2026-09-16)

| Site | Family (repo-wide n) | explicit e | factored m | legend+motif F | break-even n\* | verdict |
|---|---|---|---|---|---|---|
| `SavingsAccountsApiResource` | ApiResource (169) | 329 | 216 | 148 | **2** | WIN |
| `SavingsAccountRepositoryWrapper` | RepositoryWrapper (54) | 326 | 209 | 150 | **2** | WIN |
| `ActivateSavingsAccountCommandHandler` | `@CommandType` handler (514) | 62 | 27 | 152 | **5** | WIN |

S3 is the real story: a 514-member family that is almost fully convention-determined. One `inst CommandHandler(...)` row (27 tokens) replaces a 62-token explicit block. Tokenizer: `cl100k_base`.

Naive order-of-magnitude extrapolation across just these three families: ~43k tokens of wiring description, before any L3 orbit folding. Family variation is unmeasured; treat the 43k as a sketch, not a claim.

---

## What's in the repo

```
HANDOFF.md            resume document for a cold agent
RECOVERY.md           what was restored verbatim vs lost to container reclamation
plans/
  IDEATION.md         original framing
  META-PLAN.md        typed work units + OC gates
  CONSENSUS.md        R1–R8 binding repairs (4-fable round)
  ADVERSARIAL.md      GA1–GA10 + MUST-PROVE 1–5 ("category theory is costume until…")
  SOLUTIONS-METAPROMPT.md · PANEL-METAPROMPT.md
wiki/INDEX.md         page-tagged crosswalk of the 80pp paper (deep wiki 01–07 lost)
ynthesis/SYNTHESIS.md  paper construct → codebase construct
options/OPTIONS.md    five build options, sequenced artifacts-first
witness/              E1: run_witness.py + WITNESS.json (13/13) + toybank/
experiments/
  PROTOCOL-E1.md
  PROTOCOLS-E2-E3-RECONSTRUCTED.md
  e2-tokens/          packs, tokenizer, E2-RESULTS
  e3-ablation/        A/B/C packs, frozen hashes, grades
  e5-depth/           112q × 10 depths, QA-panel audit, E5.1 rerun
```

Original session: 2026-07-24 → 07-30. Workspace reclaimed. Corpus rebuilt 2026-09-16 from artifacts held in context + re-execution. E5 run 2026-09-19. Operator: CETI `<cetiaiservices@gmail.com>`.

---

## How to read it

1. [`HANDOFF.md`](HANDOFF.md) — mission, current state of truth, next actions.
2. [`synthesis/SYNTHESIS.md`](synthesis/SYNTHESIS.md) — the one-paragraph thesis and the paper→code crosswalk.
3. [`plans/CONSENSUS.md`](plans/CONSENSUS.md) then [`plans/ADVERSARIAL.md`](plans/ADVERSARIAL.md) — what the program is *allowed* to claim.
4. [`docs/witness/WITNESS-HOW-IT-WORKS.md`](docs/witness/WITNESS-HOW-IT-WORKS.md) — E1 architecture, diagrams, and the 13 checks (artifact: [`witness/WITNESS.json`](witness/WITNESS.json)).
5. [`experiments/e2-tokens/E2-RESULTS.md`](experiments/e2-tokens/E2-RESULTS.md) → [`e3-ablation/E3-RESULTS.md`](experiments/e3-ablation/E3-RESULTS.md) → [`e5-depth/E5-RESULTS.md`](experiments/e5-depth/E5-RESULTS.md).

Method note from the handoff, still binding: every generative phase has an adversarial phase; consistency ≠ correctness; demonstrated ≠ proved; models ≠ measurements. Treat every "strengthened" check as unverified until an independent reader re-derives it. That rule caught two real bugs in E1 and the E5 harness artifacts.

---

## Claims discipline

**MAY**

- E1 demonstrated the cospan-doctrine shapes (pushout, system-map square, wiring automorphism ⇒ composite iso, a named functorial invariant constant on a planted orbit, κ firing on a Money collision) on a 16-file toy.
- E2: factored serialization is cheaper than explicit edge lists at micro-scale on real Spring code, losslessly.
- E3: no ≥5-point comprehension tax at pilot scale on one `@CommandType` family.
- E5.1: after the pack legend is complete, a strong model reads both forms at exact parity through depth 10; pooled gap stays inside the 5-pt rule.

**MAY NOT**

- Noether's theorem applies.
- Canonical minimal presentations from freeness.
- Rex-ness of Code-C in general.
- "Beats Headroom" (market comparison, not a benchmark arm).
- CR@F95, L3/L4, repo-scale savings, cross-corpus generality.
- That E5's operadic-interview v1 validated *model* reasoning. It validated the harness. 4/10 trees were decomposition theater, caught label-free by universal inconsistency.

MUST-PROVE 1–5 are still open: gluing soundness for Code-C; well-typed equivariance + a named nontrivial invariant; ε-theorem or exact-hull; substitution-soundness; migration-square semantics + pasting.

---

## Standing debt

From the handoff and options list, still unshipped:

- Mint `systems-intake`, `interface-first-context`, `symmetry-lens` (and later `doctrine-typer`, `wiring-mapper`, `migration-square-checker`) as `SKILL.md` files.
- Full-protocol E3 (50+10 questions, mixed sites, firewalled minting, pinned models).
- Upgrade witness `C₀` → full `Code_X`.
- Fineract wedge with orbit statistics (U1) and the E4 migration chain folded in.

Lost to reclamation and **not** in this bundle (see [`RECOVERY.md`](RECOVERY.md)): `FOUNDATION.md`, `EXPERIMENTS.md`, `PATH-FORWARD.md`, wiki pages 01–07, dashboards, `NOETHER.md`, `COMPRESSION.md`, the source PDF. `wiki/INDEX.md` preserves the page-tagged crosswalk.

This GitHub copy was reconstituted from the original `wiring-and-the-whole.bundle` (6 commits on `master`, tip `93876a5`). Commit history of the bundle is recorded in the original pack; the GitHub default branch is `main`.

---

## Nearby work

Same operator's applied-operad / sheaf line:

- [`manutej/jev`](https://github.com/manutej/jev) — applied double-operadic type system (same Libkind–Myers paper)
- [`manutej/ceti-explainer`](https://github.com/manutej/ceti-explainer) — short-course explainers for sheaves, operads, cohomology
- [`manutej/sheaf-port`](https://github.com/manutej/sheaf-port) · [`manutej/cell-sheaf`](https://github.com/manutej/cell-sheaf)

This repo is the empirical wedge: *does a wiring pack actually compress, and can a model still read it?*
