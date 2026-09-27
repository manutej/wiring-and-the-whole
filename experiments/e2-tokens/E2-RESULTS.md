# E2-RESULTS — Token micro-example (GA6 discharged at micro-scale)
Run 2026-09-16 · protocol: EXPERIMENTS.md §E2 (frozen; operative reconstruction in
../PROTOCOLS-E2-E3-RECONSTRUCTED.md) · artifact of record: `E2-RESULTS.json` ·
serializations persisted as `pack_*.txt` for audit · tokenizer: cl100k_base (real BPE,
tiktoken npm vendored encoder — the frozen §0.1 fallback chain's python path was
proxy-blocked; npm path used; same encoding).

## Headline
**WIN on all three sites.** The information-equivalence gate passed everywhere (mechanical
re-expansion of the factored form reproduces the explicit form **byte-identically**), the
factored form is marginally cheaper at every site (e > m), and break-even n\* is 2–5
instances against repo-wide family sizes of 54–514. Per the frozen decision rule
(WIN: e > m and n\* < n_actual on ≥1 site) the L2 token arithmetic is **live at micro-scale**.

## The table (real Fineract files, develop branch, fetched 2026-09-16)
| Site | Family (repo-wide n) | e = explicit | m = factored row | F = legend+motif | n\* = F/(e−m) | verdict |
|---|---|---|---|---|---|---|
| S1 `SavingsAccountsApiResource` | ApiResource (169) | 329 tok | 216 tok | 148 tok | **2** | WIN |
| S2 `SavingsAccountRepositoryWrapper` | RepositoryWrapper (54) | 326 tok | 209 tok | 150 tok | **2** | WIN |
| S3 `ActivateSavingsAccountCommandHandler` | @CommandType handler (514) | 62 tok | 27 tok | 152 tok | **5** | WIN |

Naive repo-wide extrapolation at constant m (order-of-magnitude only): ≈ 19.0k (S1 family) +
6.2k (S2) + 17.8k (S3) ≈ **43k tokens saved on wiring description across just these three
families** — before any L3 orbit folding.

## Reading the mechanism honestly
- **S3 is the real story.** The 514-strong handler family is fully convention-determined:
  one `inst CommandHandler(H, S, m, entity, action)` row (27 tok) replaces a 62-tok explicit
  block — a 56% marginal saving from genuine shape-capture, with n\*=5 amortizing 100× over.
- **S1/S2 savings are shallower** (~35%): their motif mostly factors serialization syntax
  (repeated keywords + the unit's own name), while the per-site `deps=/calls=` lists ride
  along verbatim. Deeper convention-capture (e.g., standard ApiResource dep bundles as named
  sub-motifs) is available upside, untested.

## Recorded deviations & limits (per program discipline)
1. Python tiktoken vocab download proxy-blocked → npm tiktoken (same cl100k encoding). No
   measurement impact.
2. n_actual per family counted from the git tree (filename convention); other members' rows
   assumed comparable to the measured site's m — **order-of-magnitude claim only**, as the
   frozen protocol scopes it. Real family variation will add delta lines to rows (R5),
   raising m; unmeasured beyond these 3 sites.
3. Extraction is regex-level (constructor-injected `private final` fields + `field.method(`
   calls): a deliberate subset of true wiring (no static/config/reflective edges). E2 measures
   token arithmetic of the serializations, not extractor recall (that is Option-2/R6 territory).
4. No delta lines were needed at these 3 sites (S3 fully convention-determined; S1/S2 carry
   full lists) — the delta-cost term of the accounting is therefore exercised only in E3's
   planted-delta packs, not here.
5. F charges the shared legend (98 tok) to every family separately — conservative
   (overcounts total F when families co-ship).

## MAY / MAY-NOT claim (frozen)
MAY: the (seed, marking) serialization is cheaper than explicit edge lists at micro-scale on
real Spring code, losslessly (gate-verified), with n\* ≪ n_actual for all three families.
MAY NOT: repo-scale savings (unmeasured), comprehension parity (→ E3), anything about L3/L4,
extractor completeness.

## Next per sequence
E3 format-comprehension ablation — E2's WIN authorizes it (tokens(B) < tokens(A) branch).
