# Scale path — from harness to the envisioned programme

This repo is **not** done when `make verify` is green. The bet (see [`README.md`](../README.md)): production codebases are **modules of systems**; you can ship **wiring** to an LLM cheaper than the **whole**, at matched fidelity, on **high-redundancy** real code.

**Demonstrated today ≠ proved at scale.** This page maps what the harness proves, what scale requires, and the next engineering jumps that stay honest.

---

## Vision at scale (what “solved” looks like)

```
  PRODUCTION REPO (e.g. Fineract-scale)
        │
        │  sparse path list / family detector — NOT full-tree read
        v
  WiringMap v1  ──►  interface catalog + typed edges + system cards
        │
        ├── L1 context (ports only) ──► agent navigation
        ├── L2 factored packs ──► token $ at matched CR@F95
        ├── L3 exact-iso orbits ──► fold only where sound (GA2)
        └── migration squares ──► capstone (GA5), after map exists
```

Success metrics we are allowed to chase (pre-registered in [`plans/ADVERSARIAL.md`](../plans/ADVERSARIAL.md)):

- **CR@F95** — tokens to reach ≥95% of full-context accuracy vs open baselines; headline is **marginal gain of L2–L4 over L1**, not raw byte deletion.
- **Edge recall** on a staff-engineer slice (trace or hand-audit), not “we parsed imports once.”
- **Comprehension** — B arm within ≤5 pts of A at mixed sites (E3 full protocol), with **reader-spec-equivalent** legends (E5 lesson).

Category language is **spec** until MUST-PROVE 1–5 land; empirics lead.

---

## What the current harness actually proves

| Layer | Scale claim | What we have | Honest limit |
|-------|-------------|--------------|--------------|
| Faithfulness | Code = module of systems | E1 witness 13/13 toybank | C₀ not Code_X; toy only |
| Token math | L2 cheaper than explicit | E2 WIN 3 Fineract sites | Not repo-wide |
| Comprehension | No ≥5 pt tax | E3 pilot + E5 depth | One family / frozen arms |
| Wiring I/O | Extract ↔ map ↔ pack | `make pipeline-io`, density D0–D4, thin external slice | `// refs:` only; 7 handlers |
| Instruments | Repeatable agent moves | 3 SKILL.md + pulse protocol | **Pack I/O** on toybank, fineract-thin, handler-wedge; meta L1 still heuristic |

The **density ladder** and **thin external slice** exist so we can **stress scripts and packs** without loading million-file trees — that is the bridge mechanism, not the finish line.

---

## Ladder: toy → wedge → scale (artifacts-first)

```
  NOW          WEDGE (next)              SCALE (programme)
  ───          ────────────              ─────────────────
  D0–D4        Fineract handler FAMILY   CR@F95 benchmark
  toybank      (514 @CommandType)        firewall + mixed sites
  7-handler    sparse fetch + L2 pack    orbit stats (U1)
  thin slice   re-expand gate on real      WiringMap v1 + traces
               pack_LEGEND motifs
```

### Wedge 1 — One real motif family at Fineract density

- **Input:** `experiments/e3-ablation/raw/` pool (already vendored), not live clone of entire repo.
- **Output:** L2 CommandHandler pack via [`scripts/build_handler_family_pack.py`](../scripts/build_handler_family_pack.py) — **29/30** handlers (parser v1 + [`annotation_sidecar.v0.json`](../fixtures/e3-commandhandler-wedge/annotation_sidecar.v0.json)); one **orthogonal** `CommandHandler<Req,Res>` skipped; [`fixtures/e3-commandhandler-wedge/`](../fixtures/e3-commandhandler-wedge/).
- **Proof:** `make handler-family-pack-check` (reexpand byte gate + parsed ≥29).
- **Also:** [`scripts/handler_family_token_report.py`](../scripts/handler_family_token_report.py) + frozen [`token_report.json`](../fixtures/e3-commandhandler-wedge/token_report.json); L1 dogfood [`L1-e3-commandhandler-wedge.md`](dogfood/L1-e3-commandhandler-wedge.md).
- **Next:** blind pack-only LLM eval; extend sidecar / wiringmap for annotation-less handlers at scale.

### Wedge 2 — Scoped extract without whole-tree read

- **Input:** PATH LIST from [`scripts/fetch_fineract_slice.sh`](../scripts/fetch_fineract_slice.sh) → real `git sparse-checkout` or archive when credentials/network allow; until then **local corpus stub** with manifest pin.
- **Output:** wiringmap JSON validated + extract coverage gate (same contract as toybank).
- **Proof:** `make external-slice-check` (includes **`MANIFEST.txt` drift gate** via `validate_slice_manifest.py`); `make fetch-slice-manifest-check`; **`make edge-recall-sample-check`** (13 frozen ref pairs on toybank + thin slice).

### Wedge 3 — Full E3 + Fineract map statistics

- After wedge 1–2: 50+10 questions, mixed sites, firewalled minting, pinned models ([`HANDOFF.md`](../HANDOFF.md)).
- Discharges GA6/GA7 at **meso** scale — still not “all of Fineract.”

---

## What we deliberately do not pretend

- Full Spring DI / reflection wiring from static analysis alone (GA2, OPTIONS Option 2).
- “Derived guarantees” from doctrine tags on edges (GA10) — v0 convention only.
- Beating closed commercial tools without reproducible baselines (GA9).

---

## Operator commands (scale-oriented I/O today)

```bash
make pipeline-io                # toybank + fineract-thin round-trip JSON
make wiringmap-stress           # adversarial density D0–D4
make external-slice-check       # thin slice contract (+ MANIFEST drift)
make handler-family-pack-check  # e3 CommandHandler L2 pack + token report
make dogfood-grade-handler-wedge
make fetch-slice-dry-run        # PATH LIST staging (no full tree)
make fetch-slice-io-check
make pulse-eval                 # 31 functional pass/fail incl. negative cases
make pulse-unified-eval-check   # one JSON: pack-blind + cr-f95 stub (optional PACK_EVAL_LLM=1)
make pack-blind-eval-check      # L1 prompt bundles + I/O stub (optional LLM lane)
make edge-recall-sample-check   # frozen extract ↔ wiringmap pairs
make cr-f95-stub-check          # question firewall + tokens; no LLM/API
```

---

## Next pulse targets (aligned with scale, not repo hygiene)

1. ~~**Parser v1** (e3 pool 29/30)~~ — done; PaymentType remains orthogonal family.
2. ~~**Wire fetch `--apply` + MANIFEST** into slice check~~ — `MANIFEST.txt` + `validate_slice_manifest.py` in `external-slice-check`.
3. ~~**Meta L1 I/O parser**~~ — Grading facts table + `--answer-mode io` on meta pack.
4. ~~**Blind pack-only eval stub**~~ — [`experiments/pack-blind-eval/`](../experiments/pack-blind-eval/) + `make pack-blind-eval-check` (meta + handler-wedge; optional `PACK_EVAL_LLM=1`).
5. ~~**CR@F95 harness stub**~~ — [`experiments/cr-f95-stub/`](../experiments/cr-f95-stub/) + `make cr-f95-stub-check` (firewall + token + **`accuracy_column: null`** schema).
6. ~~**Pulse unified eval report**~~ — [`experiments/pulse-unified-eval/`](../experiments/pulse-unified-eval/) + `make pulse-unified-eval-check`. **Next:** Pareto curve vs baselines + live LLM fill in unified JSON.

See also [`docs/CONTEXT-COMPACT.md`](CONTEXT-COMPACT.md) for cold-start status.
