# Production retroactive ledger (merged PRs)

**Purpose:** After each merge to `main`, record what shipped, what was verified, and **small optimizations** applied retroactively — no silent drift from compound-loop rigor.

| PR | Merged | Scope | Retro status |
|----|--------|-------|--------------|
| [#42](https://github.com/manutej/wiring-and-the-whole/pull/42) | yes | M1 Rust engine + M2 charter-1k | **verified** — `make pulse-loop` on `main`; independent evals on branch preserved in `docs/pulse/evaluations/` |
| [#43](https://github.com/manutej/wiring-and-the-whole/pull/43) | yes | S2 slice matrix + S3 metrics + `/scale` | **verified** — dual-engine matrix + B1 `short_unit` fix; preview `/scale` live after deploy |

## Rigor checks (run on `main` after every merge)

```bash
make verify
make pulse-loop
make scale-metrics-check
make slice-matrix-check
WIRING_ENGINE=python bash scripts/slice_matrix_run.sh
```

## Optimizations applied (retroactive)

| Item | Before | After | Rationale |
|------|--------|-------|-----------|
| Preview nav | `/charter` not in SiteNav | Charter 1k/10k + Scale in [`SiteNav.tsx`](../../preview/graph/src/components/SiteNav.tsx) | Discoverability |
| Python oracle | `toybank-report` crash on dotless `unit:` | `removeprefix("unit:")` in [`build_l2_pack.py`](../../scripts/build_l2_pack.py) | Dual-engine honesty |
| Parity sweep | toybank-only L2 parity in wiring-core-check | [`l2_pack_parity_all_maps.sh`](../../scripts/l2_pack_parity_all_maps.sh) + pulse | Scale regression |
| Metrics WIN | extrapolated n@514 only | measured factored vs explicit in [`scale_metrics_check.py`](../../scripts/scale_metrics_check.py) | Math limits alignment |
| Java refs parity | Rust CLI defaulted to `--example` | [`java_refs_parity.sh`](../../scripts/java_refs_parity.sh) passes `--no-example-check` | Pure token parity |

## Open ledger items (non-blocking, next compound loops)

| ID | Item | Owner lane |
|----|------|------------|
| L1 | `wiring_core_check` SKIP when cargo missing — prefer fail-closed in CI images with Rust | architecture |
| L2 | Rust structural validate vs Python jsonschema — document or dual-run both everywhere | engine |
| L3 | Slice matrix diagram says “parallel”; runner is sequential — optional `SLICE_MATRIX_PARALLEL` | infra |
| L4 | `repo-rust-spine` map still fails L2 build (known); exclude from matrix or fix expand | engine |

## Teamwork lanes (every compound loop)

See [`skills/compound-build-loop/SKILL.md`](../../skills/compound-build-loop/SKILL.md): builder → gates → adversarial + math + arch (parallel) → independent eval → PR steward.
