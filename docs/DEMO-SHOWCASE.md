# Live demo script (~5 minutes)

**Audience:** stakeholders who need to see *working* harness pieces, not Fineract-scale product claims.

**Honest headline:** **Demo MVP yes** (fixtures + gates + frozen experiments). **Product MVP no** (no repo-wide map, no live CR@F95 on production Fineract).

**Deeper context:** [`docs/SCALE-PATH.md`](SCALE-PATH.md) · [`docs/PULSE.md`](PULSE.md) · vision snapshot on PR [#31](https://github.com/manutej/wiring-and-the-whole/pull/31) → `docs/reports/2026-10-02-vision-and-capabilities.md`.

---

## 0. One-liner before you type

> “We prove the *pipeline* on toy and thin real slices: extract ↔ wiring map ↔ L2 pack ↔ re-expand gate. Scale metrics are pre-registered but not discharged on whole repos.”

---

## 1. Full harness green (~90s)

```bash
make verify
```

**You should see** (tail):

```
==> E1 witness (run_witness.py)
PASS E1 witness (all_pass=true)
==> E2 tokens (npm ci + e2_run.py vs frozen E2-RESULTS.json)
PASS E2 tokens (matches frozen E2-RESULTS.json)
==> E3 grade (frozen responses only)
PASS E3 grade (matches frozen E3-GRADES.json)
==> All gates passed
```

**Point at:** frozen E1/E2/E3 under `experiments/` — reproducible, not a live LLM call in CI.

---

## 2. Wiring round-trip I/O (~30s)

```bash
make pipeline-io
```

**You should see** JSON plus a line like:

```
PIPELINE IO PASS: toybank + fineract-thin round-trip
```

Example fields:

```json
{
  "status": "ok",
  "toybank": { "ref_token_count": 8, "pack_explicit_edges": 8 },
  "fineract_thin": { "ref_token_count": 5 }
}
```

**Artifacts:** toybank map [`wiringmap/examples/toybank-accounts.v0.json`](../wiringmap/examples/toybank-accounts.v0.json) · thin slice [`fixtures/external/fineract-handlers-thin/`](../fixtures/external/fineract-handlers-thin/).

---

## 3. Real-handler wedge + token math (~45s)

```bash
make handler-family-pack-check
python3 scripts/handler_family_token_report.py | python3 -m json.tool
```

**You should see:** re-expand gate pass, `parsed >= 29`, then token JSON with **WIN** at Fineract-scale *N* (514 handlers) using per-handler rates from the wedge pack:

```json
"tokens": {
  "explicit_full": 1923,
  "factored_full": 947
},
"breakeven": { "n_actual_repo_wide_CommandHandler": 514, "verdict_at_n": "WIN" }
```

**Fixture:** [`fixtures/e3-commandhandler-wedge/`](../fixtures/e3-commandhandler-wedge/) (29/30 vendored `@CommandType` handlers, not full Fineract).

Optional L1 navigation (table parse, no LLM):

```bash
make dogfood-grade-handler-wedge
# OK: 7 questions graded for docs/dogfood/L1-e3-commandhandler-wedge.md
```

---

## Bonus slides (if time)

| Demo | Command | What it shows |
|------|---------|----------------|
| Density / failure modes | `make wiringmap-stress` | D0–D4: pass + *expected* extract/validate failures |
| Thin external slice gate | `make external-slice-check` | 7 Java files, manifest drift gate, ref coverage |
| Category witness JSON | `make witness` | `"all_pass": true` + named diagram checks |
| Post-pulse operator bundle | `make meta-evaluator \| python3 -m json.tool \| head -60` | Programme pointers + craft skill resolution (not a product UI) |
| Witness ASCII (browser) | open [`docs/witness/index.html`](witness/index.html) | E1 pushout / system-map diagrams |

---

## Fixture & report index

| Artifact | Path |
|----------|------|
| Toybank wiring map | `wiringmap/examples/toybank-accounts.v0.json` |
| Fineract thin (7 handlers) | `fixtures/external/fineract-handlers-thin/` |
| Handler family wedge | `fixtures/e3-commandhandler-wedge/pack/` |
| Density ladder manifest | `fixtures/density/stress_manifest.json` |
| Adversarial pre-registration | `plans/ADVERSARIAL.md` |
| Vision progress report (2026-10-02) | `docs/reports/2026-10-02-vision-and-capabilities.md` (on branch `cursor/vision-progress-report-cd12`, PR #31) |

---

## What **not** to demo

- **“We mapped Fineract.”** Only a **7-handler thin slice** + **30-file handler pool** (29 parsed). No repo-wide WiringMap emitter.
- **“Agents navigate production today.”** L1 grades use **frozen packs + parsed tables** (`grade_l1_questions.py --answer-mode io`), not live agent sessions on a clone.
- **“CR@F95 is solved.”** E2 is **3 frozen Fineract sites**; unified/blind pack evals are **check targets** in `make verify`, not customer-facing benchmarks.
- **“Sparse checkout of full Fineract works here.”** `fetch_fineract_slice.sh` is manifest/stub discipline until network/credentials; demo `external-slice-check` on vendored files instead.
- **PULSE as magic word.** It is an **operator protocol** ([`docs/PULSE.md`](PULSE.md)) — merge gate + firewalled evaluator — not a shipped SaaS loop.

---

## MVP definitions (use these words)

| Label | Status |
|-------|--------|
| **Demo MVP** | **Yes** — `make verify`, `make pipeline-io`, handler wedge + witness HTML/JSON in &lt;5 min, honest SCALE-PATH narrative. |
| **Product MVP** | **No** — missing automated WiringMap v1 at scale, staff-engineer edge-recall on real traces, firewalled E3 at 50+10 mixed sites, migration squares (GA5), production agent SKU. |
