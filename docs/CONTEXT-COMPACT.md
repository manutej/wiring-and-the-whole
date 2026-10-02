# Context compact — cold-start snapshot (2026-10-02)

Single page for agents resuming on **`main`**. Detail lives in linked files; do not duplicate long inventories here.

## Mission

Map production codebases as a **module of systems** (T1), find symmetries/invariants (T2), beat naive token dumps at matched fidelity (T3). Paper: Libkind & Myers arXiv:2505.18329v2. Claims ladder in `plans/ADVERSARIAL.md` — **demonstrated ≠ proved**.

**Scale intent:** green CI is necessary, not sufficient — see [`docs/SCALE-PATH.md`](SCALE-PATH.md) (toy → Fineract wedge → CR@F95).

## On main today

| Area | Status |
|------|--------|
| E1 witness | **13/13** — `witness/` |
| E2 / E3 | WIN + B-PASSES — frozen under **`make verify`** |
| E5 depth | B-PASSES AT DEPTH — `experiments/e5-depth/` (not in verify yet) |
| Pulse | **`docs/PULSE.md`** — trigger `pulse`; **`make pulse-eval`** (24 functional checks) + **`make pulse-gate`** |
| WiringMap v0 | `wiringmap/schema.v0.json` + toybank example; **`make wiringmap-check`** |
| Density ladder | D0–D3 `fixtures/density/` + **D4** external slice — **`make wiringmap-stress`** |
| External thin slice | `fixtures/external/fineract-handlers-thin/` (7 handlers, vendored) — **`make external-slice-check`** |
| Wedge 1 CommandHandler | **29/30** → `fixtures/e3-commandhandler-wedge/` — **`make handler-family-pack-check`** |
| L1 dogfood | meta / toybank / fineract-thin / **handler-wedge** — **`make dogfood-grade*`** |
| Pack builders | toybank **`make pack-v0-check`**; handler family **`build_handler_family_pack.py`** |
| SKILL mint | **3/3:** `interface-first-context`, `systems-intake`, **`symmetry-lens`** |

## Verify & interface checks

```bash
make verify                      # witness + E2 + E3 frozen
make wiringmap-check             # toybank accounts
make wiringmap-stress            # D0–D4 expectations
make external-slice-check        # fineract-handlers-thin (+ MANIFEST when present)
make handler-family-pack-check   # e3 pool → L2 CommandHandler pack + token report
make dogfood-grade               # meta L1 questions
make dogfood-grade-toybank
make dogfood-grade-fineract-thin
make dogfood-grade-handler-wedge
make fetch-slice-dry-run         # fineract thin slice stub; temp staging only
make fetch-slice-io-check        # dry-run inventory I/O
make pack-v0-check               # L2 pack + reexpand + canonical LEGEND gate
make fetch-slice-manifest-check  # MANIFEST.txt vs slice dir
make pulse-eval                  # 24 functional negative/positive interface evals
make pipeline-io                 # E2E: files → subprocess tools → JSON report
make pulse-gate
make cr-f95-stub-check           # CR@F95 harness stub (no LLM)
```

## Honest limits (external slice)

- Extractors read **`// refs:`** only — not full Spring DI graphs.
- Fineract slice is **vendored subset**, not live `apache/fineract` checkout.
- `doctrine_tag` on edges is **v0 convention**, not proven doctrine (GA10).

## Next jumps (scale)

See [`SCALE-PATH.md`](SCALE-PATH.md): MANIFEST drift on fetch `--apply` → **CR@F95 stub** (no live LLM) → blind pack eval later.

## Pointers

- Resume: `HANDOFF.md` (history) · **Status:** this file + **`SCALE-PATH.md`**
- Build memo (historical): `docs/roadmap/BUILD-OUT-RESEARCH.md` — superseded banner at top
- Witness: `docs/witness/index.html` · L1 skill: `skills/interface-first-context/SKILL.md`
- Fixtures: `fixtures/density/README.md`, `fixtures/external/README.md`, `fixtures/e3-commandhandler-wedge/README.md`
