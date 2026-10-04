# Corpus provenance — what repo did we use?

## Short answer

| Charter | Real upstream? | What we actually ship |
|---------|----------------|------------------------|
| **fineract-charter-1k** | Fineract **PATH LIST** (pinned fetch scripts) | Subset of Apache Fineract Java, wired with `// refs:` |
| **fineract-charter-10k** | **Not** a Fineract checkout | **42 files** copied from **this repo’s experiment corpora** |

Charter 10k is **not vibe-coded** and **not a random synthetic app**: the Java is the same family of **real Fineract-derived sources** already used in e3/e5/e2 experiments. We **did not** clone all of [apache/fineract](https://github.com/apache/fineract) at ~10k LOC for CI.

## Charter 10k sources (in-repo)

| Pool | Path | Role |
|------|------|------|
| Handlers | `experiments/e3-ablation/raw/*CommandHandler.java` | `@CommandType` wedge (parser v1) |
| Services depth | `experiments/e5-depth/raw/*.java` | Extra LOC / realism |
| Tokens corpus | `experiments/e2-tokens/raw/*.java` | Additional Java mass |

Bootstrap: `python3 scripts/bootstrap_fineract_charter_10k.py` → `fixtures/external/fineract-charter-10k/`.

- **MANIFEST** states `fetch_mode=stub` and `source_commit=unpinned-experiments-corpus`.
- **PATH_LIST.txt** lists every `.java` file in the charter directory.
- Orthogonal `CommandHandler<Req,Res>` APIs (e.g. payment type create) are **removed**, same policy as charter 1k.

## What “wired” means here

- **30 handlers** have injected `// refs:` and a **WiringMap v0** with units + example edges.
- **Service / repository** files add ~86% of LOC but are **not** fully mapped (Spring DI out of scope).
- Gates: `make charter-10k-check`, shard `fineract-charter-10k` in `make slice-matrix-check`.

## This monorepo

All scale fixtures live in **[manutej/wiring-and-the-whole](https://github.com/manutej/wiring-and-the-whole)** — witness toybank, Fineract thin slice, charters, Rust `wiring-core`, preview app.

See also: [`SCALE-REPORT-LATEST.md`](reports/SCALE-REPORT-LATEST.md) and [`scale-dashboard/index.html`](scale-dashboard/index.html).
