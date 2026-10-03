# Build log — math & limitations audit (2026-10-03)

**Role:** Math/limitations agent pass (no code changes).  
**Artifacts:** [`fixtures/e3-commandhandler-wedge/token_report.json`](../../fixtures/e3-commandhandler-wedge/token_report.json), frozen [`experiments/e2-tokens/E2-RESULTS.json`](../../experiments/e2-tokens/E2-RESULTS.json), handler-count sources, breakeven / WIN wording in ops docs.

**Question answered:** Which numbers are **measured and gate-backed** vs **modeling assumptions or copy-forward constants**?

---

## 1. Accounting model (shared E2 + wedge)

Both E2 and the handler wedge use the same L2 token ledger on **cl100k_base** (tiktoken via vendored npm encoder):

| Symbol | Meaning |
|--------|---------|
| **e** | Tokens for one handler’s **explicit** wiring block (Form A: unit + anno + dep + edge) |
| **m** | Tokens for one **factored** `inst CommandHandler(...)` row |
| **F** | Fixed overhead **legend + motif** (charged once per family pack) |
| **n\*** | Break-even instance count: smallest integer **n** where **F + n·m < n·e** |

Implementation uses integer ceiling: `n* = ⌈F / (e − m)⌉` when `e > m`, else undefined / KILL.

**Decision rule (frozen E2):** **WIN** on a site when `e > m` and `n* < n_actual`. **Overall E2 WIN** when ≥1 site wins; **KILL** only if every site has `e ≤ m` or `n* > n_actual`.

This algebra is **internally consistent** and reproduced by `experiments/e2-tokens/e2_run.py` and `scripts/handler_family_token_report.py`.

---

## 2. E2-RESULTS — what is solid

Source of record: [`E2-RESULTS.json`](../../experiments/e2-tokens/E2-RESULTS.json) · narrative limits in [`E2-RESULTS.md`](../../experiments/e2-tokens/E2-RESULTS.md).

### Solid (verified by `make verify`)

| Claim | Evidence |
|-------|----------|
| **Byte-identical re-expansion** on S1, S2, S3 | `gate_byte_identical: true` per site; `gate_all_sites_byte_identical: true` |
| **Measured e, m, F** on three real Fineract files | Frozen counts; re-run must match JSON byte-for-byte on those fields |
| **e > m on all three sites** | S1: 329>216; S2: 326>209; S3: 62>27 |
| **n\* = 2, 2, 5** | S1/S2: F=148/150, margins 113/117 → n\*=2; S3: F=152, margin 35 → n\*=5 |
| **Per-site WIN** | Each site has `n* < n_actual` with frozen `n_actual` 169 / 54 / 514 |
| **Overall WIN** | Matches frozen kill rule |

### Solid but **single-site** (not family-averaged)

- **e, m, F for S3** come from **one** file: `ActivateSavingsAccountCommandHandler.java` (savings activation), not from the E3 loan-handler pool.
- The **514** in S3 is **`n_actual_repo_wide`**: a **family cardinality constant** baked into `e2_run.py` (`FAMILY_N["CommandHandler"] = 514`), not re-counted on every verify run.

### Extrapolation (E2 already labels this)

| Field | Treatment |
|-------|-----------|
| `repo_wide_savings_est_tokens` | **Order-of-magnitude only:** `(e − m) × n_actual − F` assuming **every** family member has the same **m** as the one measured site |
| Sum ≈ **43k tokens** across three families | Same assumption × three unrelated motifs; **F double-counts legend** if families co-ship (E2-RESULTS § limits item 5) |
| “514-strong handler family is fully convention-determined” | **True for the S3 motif shape** (one dep, one call) on the measured file; **not measured** across all 514 files |

**MAY / MAY NOT (frozen):** E2 **MAY** claim micro-scale token WIN with lossless gate; **MAY NOT** claim repo-scale savings or comprehension (→ E3).

---

## 3. Handler counts — three different numbers

Do not conflate these:

| Count | Value | What it measures |
|------:|------:|------------------|
| **E3 raw pool files** | **30** | `*CommandHandler.java` under `experiments/e3-ablation/raw/` |
| **Wedge pack rows** | **29** | Parser v1 + re-expand gate; [`manifest.json`](../../fixtures/e3-commandhandler-wedge/manifest.json) |
| **Skipped** | **1** | `PaymentTypeCreateCommandHandler` — orthogonal `CommandHandler<Req,Res>` API, not `@CommandType` family |
| **E2 S3 `n_actual`** | **514** | Repo-wide `@CommandType` handler **estimate** (Fineract tree / filename convention at E2 fetch); **not** the wedge pool size |

**Solid:** 29/30 parsing story, 116 explicit lines (4×29), 29 `inst` rows, byte gate on the **actual wedge pack**.

**Extrapolation:** Any sentence that equates “29 handlers in CI” with “514-handler family covered” or “Fineract-scale pack proved.” The wedge README and SCALE-PATH explicitly **disclaim** full 514 coverage.

---

## 4. `token_report.json` — solid vs extrapolation

Frozen report: [`fixtures/e3-commandhandler-wedge/token_report.json`](../../fixtures/e3-commandhandler-wedge/token_report.json).

### Solid (direct measurement on wedge pack)

| Field | Value | Notes |
|-------|------:|-------|
| `handlers_inst_rows` | 29 | Count of `inst CommandHandler(` lines |
| `tokens.explicit_full` | 1923 | Full `pack_explicit.txt` |
| `tokens.factored_full` | 947 | Full `pack_factored.txt` (motif + rows; legend counted separately in script) |
| `tokens.legend` / `motif` | 98 / 54 | Same legend as E2; S3 motif file from E2 tree |
| `tokens.fixed_overhead_legend_plus_motif` | 152 | Matches E2 S3 **F** (script **fails** if not) |
| **At n = 29** | 947 < 1923 | Factored pack wins on **measured** corpus (~976 token delta) |

### Partially solid (proxy rates, not full-pack identity)

| Field | Value | Issue |
|-------|------:|-------|
| `per_handler_explicit` | 58 | Token count of **first** handler’s 4-line block only (`AddLoanChargeCommandHandler`) |
| `per_handler_inst_row` | 26 | Token count of **first** inst row only |
| `n_star_from_per_handler_rates` | 5 | ⌈152 / (58−26)⌉ = ⌈4.75⌉ = **5** |

**Empirical spread on all 29 handlers** (same tokenizer, 2026-10-03 spot check):

- Explicit block **e:** min 50, max 85, mean **~66.3** (first row 58).
- Inst row **m:** min 22, max 43, mean **~30.8** (first row 26).
- Every handler still has **e > m**; per-handler **n\*** max **6** (worst margin 27 tokens), min **3**.

So **n\* = 5** from the first handler is **representative**, not exact; using **mean** rates gives n\* ≈ ⌈152 / 35.5⌉ = **5** as well.

**Important:** `per_handler_*` does **not** satisfy `29 × per_handler_explicit ≈ explicit_full` (29×58 = 1678 ≠ 1923). Breakeven lines in the JSON are **rate-based**, not a reconstruction of the full pack from one row.

### Extrapolation (explicit in JSON, easy to misread in demos)

| Field | Treatment |
|-------|-----------|
| `breakeven.n_actual_repo_wide_CommandHandler` | **514** copied from E2 constant (`FAMILY_N` in script) — **not** counted from wedge |
| `breakeven.verdict_at_n: "WIN"` | Means `n* < 514` using **first-row** e/m — trivial once n\* ≤ 6; **does not** mean “514 handlers tokenized” |
| `e2_S3_frozen_reference` | Display-only mirror of E2 S3 |
| `consistency_checks.*_matches_e2_S3: false` | **Correct flag:** wedge first-row **58 / 26** ≠ E2 S3 **62 / 27** (different handler, different entity/action/method string lengths) |

**Copy hygiene bug class:** [`docs/DEMO-SHOWCASE.md`](../../docs/DEMO-SHOWCASE.md) says WIN at “Fineract-scale *N* (514) using per-handler rates from the wedge pack.” The **514** part is the E2 constant; **rates** are first-row proxies; **full-pack WIN at 29** is the honest measured win on the wedge.

---

## 5. Breakeven claims — audit map

| Location | Claim | Verdict |
|----------|-------|---------|
| E2-RESULTS S3 | n\*=5 vs n_actual=514 | **Solid** for **one** measured site + frozen constant |
| E2 `repo_wide_savings_est_tokens` 17838 | (62−27)×514−152 | **Extrapolation** (constant-m assumption) |
| `token_report.json` n\*=5, WIN @ 514 | Rate proxy + constant | **Mixed:** algebra solid; **514** and “@ 514” wording **extrapolative** |
| Wedge n=29 full packs | 947 vs 1923 | **Solid measured** |
| README / HANDOFF “n* = 2–5 vs 54–514” | E2 headline | **Solid** per E2 frozen sites; **514** is not wedge count |
| Feasibility doc “breakeven math frozen at 29 rows” | [`2026-10-02-feasibility-1k-10k-loc.md`](../../reports/2026-10-02-feasibility-1k-10k-loc.md) | **Sloppy wording:** JSON is frozen with **29-row pack totals** + **first-row** rates; not “29 different n\* experiments” |
| L1 meta `e2_s3_n_star_breakeven` | 5 | **Solid** as E2 frozen fact (grading table) |
| L1 handler wedge “same legend and motif as E2 S3” | docs/dogfood | **Solid** for files; **per-handler token parity** is **not** claimed in JSON (`consistency_checks: false`) |

---

## 6. Summary table — solid vs extrapolation

| Topic | Solid | Extrapolation / do not over-read |
|-------|-------|----------------------------------|
| **Re-expand gate** | E2 3/3; wedge 29/29 pack | — |
| **Tokenizer** | cl100k_base, npm path | — |
| **e > m** | All E2 sites; all 29 wedge handlers | — |
| **n\* (E2 S3)** | 5 from measured 62/27/152 | — |
| **n\* (wedge proxy)** | 5–6 from measured rows | Using **first row only** in JSON |
| **Pack totals @ 29 handlers** | 1923 vs 947 | — |
| **514 handlers** | Constant for E2 decision rule | Wedge **does not** contain 514 files |
| **WIN @ 514** | n\* ≪ 514 (algebra) | **Not** 514-handler pack tokenization |
| **Repo-wide token savings** | — | E2 `repo_wide_savings_est_*`; constant-m |
| **S3 “convention-determined”** | Measured file + motif | All 514 members untested |
| **E2 ↔ wedge rate identity** | F = 152 | e/m per handler **differ** (58/26 vs 62/27) |

---

## 7. Recommended claim language (ops)

Use:

- “**Measured** on 29-handler wedge: factored pack **947** vs explicit **1923** tokens (cl100k).”
- “E2 **S3 micro-site** (savings handler): **e=62, m=27, n\*=5**; family size constant **514** for GA6 decision rule only.”
- “Break-even **n\* ≈ 5** CommandHandler instances amortizes legend+motif (**F=152**); wedge and E2 agree on **F** and **n\*** bucket, not on per-row **e/m** from the same source file.”

Avoid:

- “Token WIN **proved** on all **514** Fineract handlers.”
- “Wedge **confirms** E2 per-handler **62/27**” (consistency_checks are **false** by design).
- Treating **`verdict_at_n: WIN`** with **514** as a measured Fineract-scale experiment.

---

## 8. Operator re-check (no code)

```bash
make verify                                    # E2 vs frozen E2-RESULTS.json
make handler-family-pack-check                 # re-expand + parsed ≥29
python3 scripts/handler_family_token_report.py # prints token_report.json fields
```

---

*Audit complete 2026-10-03. No repository code or frozen JSON modified in this pass.*
