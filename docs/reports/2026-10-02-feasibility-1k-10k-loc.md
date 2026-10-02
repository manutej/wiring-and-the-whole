# Feasibility — 1k and 10k line chartered slices (2026-10-02)

**Audience:** anyone planning the next scale jumps · **Baseline:** `origin/main` · **Sources:** [`SCALE-PATH.md`](../SCALE-PATH.md), [`2026-10-02-vision-and-capabilities.md`](2026-10-02-vision-and-capabilities.md) (on branch `cursor/vision-progress-report-cd12`), [`HANDOFF.md`](../../HANDOFF.md), [`fixtures/external/fineract-handlers-thin/MANIFEST.txt`](../../fixtures/external/fineract-handlers-thin/MANIFEST.txt), [`plans/ADVERSARIAL.md`](../../plans/ADVERSARIAL.md), pulse gates in [`scripts/pulse_eval_functional.sh`](../../scripts/pulse_eval_functional.sh).

**Chartered slice** = a fixed list of paths (not a full repo checkout), pinned in a manifest, with automated extract → map → pack → re-expand checks and frozen evaluation fixtures.

---

## Where we are now (lines of code under test)

Counts are **Java source lines** in fixtures the harness actually runs against (file counts in parentheses). Overlap is noted so numbers stay honest.

| Corpus | Java lines | Files | What CI uses it for |
|--------|----------:|------:|---------------------|
| Toy witness (`witness/toybank/`) | **79** | 16 | E1 witness (13 checks), `// refs:` extract, L2 pack, L1 dogfood |
| Density adversarial (`fixtures/density/` D1–D2 only) | **~20** | 4 | Deliberate extract/validate failures in `make pulse-eval` |
| E3 handler pool (`experiments/e3-ablation/raw/`) | **1,342** | 30 | CommandHandler parser + L2 pack (`make handler-family-pack-check`, 29/30 parsed) |
| Fineract thin slice (`fixtures/external/fineract-handlers-thin/`) | **322** | 7 | Same seven handlers as a subset of the E3 pool — **do not add to union** |
| Density D3 orbit | **~30** | 10 | Toybank-shaped stress; overlaps witness pattern |

**Effective union under test today (no double-counting thin slice):** about **1,440 Java lines** across **~50 files**, plus hand-curated wiring maps and frozen JSON for historical E2/E3/E5 claims on `make verify`.

**What “under test” does *not* mean yet:**

- Only **29 frozen** `(file, ref token)` pairs for edge recall — not staff-audited wiring on hundreds of handlers ([`fixtures/edge-recall-sample/README.md`](../../fixtures/edge-recall-sample/README.md)).
- Wiring maps are **hand-built**; extractors only understand `// refs:` comments and the **CommandHandler** regex parser — not arbitrary Spring wiring ([vision report § “Element extraction”](2026-10-02-vision-and-capabilities.md)).
- **3 of 7** thin-slice handlers have `// refs:`; the rest rely on import-line heuristics in slice check only ([`fixtures/external/fineract-handlers-thin/README.md`](../../fixtures/external/fineract-handlers-thin/README.md)).
- **CR@F95** (compression ratio at 95% fidelity) harness records tokens and blocks answer leaks; **accuracy is intentionally null** on default continuous integration — no live language-model score ([`experiments/cr-f95-stub/`](../../experiments/cr-f95-stub/)).

**Automation surface (for trust, not production LOC):** `make verify` + `make pulse-eval` (**34** functional checks), including pipeline I/O, manifest drift, unified eval stub, pack-blind firewall, and meta-evaluator hook.

---

## 1k LOC — feasible? what it takes

**Verdict: yes — mostly a curation and charter problem, not a parser line-count problem.** The E3 handler pool is already **~1.3k lines** in one motif family; the gap is **trusted wiring coverage**, not raw bytes.

### What breaks or strains at ~1k lines

- **Manual `// refs:` and map editing** — does not scale linearly; at 1k lines across ~25–40 files, expect most edges to be missing from the wiring map unless automation improves.
- **Parser coverage** — today: one family, **29/30** files, **1** orthogonal API skipped, **1** sidecar for unresolved annotation constants ([`fixtures/e3-commandhandler-wedge/`](../../fixtures/e3-commandhandler-wedge/)). Adding non-handler Java (services, resources) hits **no parser**.
- **Map curation** — partial maps pass some gates via heuristics; that weakens the “extract matches map evidence” story adversarial reviewers care about (gap **GA4** in [`ADVERSARIAL.md`](../../plans/ADVERSARIAL.md)).
- **Edge recall** — 29 pairs will miss most real edges in a 1k-line vertical slice; sampling must grow or the gate becomes cosmetic.
- **Preview / graph UX** — toy witness HTML exists; there is **no** auto-generated graph for the 1k slice — agents rely on L1 markdown packs.
- **Continuous integration time** — still **small** at 1k (seconds to low minutes); not the bottleneck.

### What already helps

- **Re-expand byte gate** — factored L2 packs must match explicit wiring ([`scripts/reexpand_gate.py`](../../scripts/reexpand_gate.py)).
- **Pipeline I/O** — one command round-trips extract, validate, pack, grade ([`make pipeline-io`](../../Makefile)).
- **Manifest drift gate** — slice inventory cannot silently rot ([`validate_slice_manifest.py`](../../scripts/validate_slice_manifest.py)).
- **Density ladder D0–D4** — adversarial fixtures prove failure modes, not only happy paths.
- **Frozen evals** — E2/E3/E5 JSON on `make verify`; pulse checks tamper and negative cases.
- **Sparse fetch script** — path-list discipline staged ([`scripts/fetch_fineract_slice.sh`](../../scripts/fetch_fineract_slice.sh)); `--apply` + upstream pin ready for wedge 2.
- **Handler wedge token report** — breakeven math frozen at 29 rows ([`token_report.json`](../../fixtures/e3-commandhandler-wedge/token_report.json)).

### What must be built (1k charter)

| Workstream | Size | Outcome |
|------------|------|---------|
| **Charter ~25–35 files / ~1k lines** one vertical (e.g. loan command handlers + 2–3 services they call) | Medium | `PATH_LIST` + `MANIFEST.txt` pin; no full Fineract tree |
| **Grow edge-recall sample** to ~100–200 frozen pairs on that charter | Medium | Statistical spot-check, still not full recall |
| **Parser → map bridge (v1.1)** for CommandHandler rows | Medium | Auto `ref`/`call` edges where pattern is unambiguous; sidecar only for constant gaps |
| **`fetch_fineract_slice.sh --apply`** with real upstream commit pin | Small–medium | Replace “stub” manifest story with reproducible fetch |
| **Optional:** fill pack-blind / unified eval with live model on charter L1 only | Medium | First honest comprehension signal on wedge (keep default CI model-off) |

**Effort shape:** one **medium** integration workstream (charter + manifest + fetch), one **medium** quality workstream (recall sample + map bridge), one **small** optional eval workstream.

---

## 10k LOC — feasible? what it takes

**Verdict: feasible as a staged programme, not as a single “turn on parser for whole module” step.** Ten thousand lines is roughly **3–8×** the handler pool density **plus** surrounding services, configuration, and tests — multiple motif families and incomplete static visibility (Spring injection, reflection).

### What breaks

- **Single-family parser** — CommandHandler regex covers a thin strip of Fineract; 10k lines need **MVC controllers**, repositories, jobs, or config — none have shippers today.
- **Manual maps** — impractical at 10k; without emitters, maps lag code and edge recall collapses.
- **Edge recall** — staff-engineer traces (hand-audit or run logs) become mandatory for credible claims; frozen pairs in the hundreds are still a sample, not proof.
- **Comprehension (GA7)** — format A/B/C ablation at 10k context sizes needs firewalled question sets mined from issues/pull requests, not in-repo trivia — adversarial gap **GA8**.
- **Token economics (GA6)** — fixed legend overhead and per-pack schema tax must be re-measured per family; 10k lines may add **multiple** L2 packs.
- **Preview graphs** — wiring map JSON validates, but human/agent navigation at 10k needs **scoped views** (by system card / slice), not one giant graph.
- **CI time** — likely still **medium** if slices stay sparse; risk rises if every push re-tokenizes 10k lines with external tokenizer calls.
- **Wiring holes** — full Spring dependency injection and reflection remain **out of scope** per [`SCALE-PATH.md`](../SCALE-PATH.md); at 10k, omitted edges dominate recall unless scope is declared narrowly.

### What already helps (same as 1k, plus)

- **Wedge ladder** — proves real Fineract syntax at 29 handlers; E2 frozen WIN at three sites; E3 pilot B-pass story gives a template for mixed-site eval.
- **Pulse unified eval** — one JSON merges pack-blind stub and CR@F95 stub — ready to attach Pareto columns when accuracy is filled.
- **Skills (3/3)** — agent workflow instruments exist; dogfood gates prove L1 I/O parsing, not field deployment.

### What must be built (10k charter)

| Workstream | Size | Outcome |
|------------|------|---------|
| **Multi-family parser roadmap** (handler + MVC + one persistence motif) | Large | Each family: parse → L2 pack + optional map emit; explicit skip categories |
| **Sparse checkout automation** in CI | Medium | Cone sparse-checkout or archive path list; credential-safe dry-run on default CI |
| **Sampling strategy for edge recall** | Large | Stratified frozen pairs + periodic staff trace subset; publish recall **rate**, not “100% parsed once” |
| **Staff traces or hand-audit protocol** | Large | Pre-registered slice; aligns with ADVERSARIAL “staff-engineer slice” |
| **Scoped L1 / graph previews** | Medium | System cards + slice-filtered dashboard or docs; avoid whole-repo graph |
| **E3-scale comprehension battery** | Large | 50+10 questions on wedge packs, mixed sites, pinned models — GA7 at **meso** scale |
| **External question mint + firewall** | Medium | Before any published CR@F95 number (pulse adversarial **G1**) |

**Effort shape:** **large** parser/map automation, **large** measurement (recall + comprehension), **medium** infra (sparse fetch, scoped UX), **medium** eval harness (live LLM lane off by default).

---

## Testing plan (simple bullets)

- Keep **`make verify`** as the non-negotiable core (witness + frozen E2/E3/E5 JSON).
- Keep **`make pulse-eval`** as the functional battery (tamper tests, manifest drift, unified eval shape, firewall leaks) — extend with charter-specific negative cases when slices grow.
- For each new chartered slice: **`make external-slice-check`** or successor gate — validate map, extract coverage, manifest pin.
- **`make handler-family-pack-check`** (or per-family analogue) — re-expand byte identity + minimum parsed count.
- **`make edge-recall-sample-check`** — grow frozen pairs with the slice; fail CI if extract ↔ map evidence regresses.
- **`make pipeline-io`** — one JSON report per slice for operator audits.
- **`make pulse-unified-eval-check`** — stay model-off on default CI; optional job with API key for comprehension fills.
- **`make cr-f95-stub-check`** — keep `accuracy_column: null` until questions are externally minted; then fill under firewall.
- **Dogfood L1** — `--answer-mode io` on every new L1 pack; add frozen question JSON.
- **Adversarial pulse note** per scale jump — record gaps vs GA6–GA8 so scale claims stay honest.
- **Do not** treat import-line heuristics as permanent substitutes for `// refs:` or parsed edges on chartered slices.

---

## Risks and honest timeline shape

(No calendar dates — only effort shape.)

| Risk | Why it hurts | Mitigation shape |
|------|--------------|------------------|
| Maps fall behind code | False green extract gates | Parser emit + sidecar shrink; charter bounded |
| Recall looks good on a tiny sample | Over-claim wiring fidelity | Publish sample size; add staff traces |
| Comprehension eval designed in-repo | CR@F95 circularity (GA8) | Issue/PR-mined questions + firewall |
| Spring/reflection edges missing | Recall ceiling | Narrow charter scope; document omissions |
| Live LLM eval flakiness | Noisy Pareto | Pin models; optional CI job; frozen stub default |
| Programme hygiene mistaken for capstone | GA10 | Keep CONTEXT-COMPACT “measure vs spec” rows updated |

**Overall effort shape**

- **1k LOC chartered slice with trusted gates:** **medium** — mostly wiring discipline and sample growth on top of existing ~1.3k handler pool tools.
- **10k LOC with defensible recall + comprehension samples:** **large** — multi-family extraction, trace protocol, and eval harness fill — multiple parallel workstreams before the programme thesis is **proved** (still **demonstrated** on fixtures until then).

**Bottom line:** The repo already **exercises ~1.4k lines** of real Java in continuous integration, but **proves** fidelity mainly on **toy + one handler family**. A **1k charter** is **near-term feasible** by tightening manifest, map emit, and recall sampling on one vertical. A **10k charter** is **feasible only with new automation and measurement workstreams** — not by vendoring more files alone.
