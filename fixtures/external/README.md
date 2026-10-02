# External repo slices (fixtures)

Thin **copies** of third-party code used for wiringmap / L1 dogfood. These paths are **not** git submodules and **do not** imply full upstream repo coverage.

## Layout (ASCII)

```
  wiring-and-the-whole (meta-repo)
  |
  +-- experiments/e3-ablation/raw/     ... vendored Fineract handler corpus (E3)
  |
  +-- fixtures/external/
        |
        +-- fineract-handlers-thin/      ... 5–8 handler files + wiringmap (THIS SLICE)
        |     *.java
        |     wiringmap.v0.json
        |     README.md  (provenance + omissions)
        |
        +-- README.md                    ... you are here

  scripts/
        extract_refs.py                  ... reads // refs: under slice dir
        fineract_slice_check.sh          ... merge gate for external slice
        fetch_fineract_slice.sh          ... PATH-LIST fetch stub (dry-run default)
        validate_wiringmap.py
```

**Reader rule:** Scripts and L1 packs under `docs/dogfood/` treat `fixtures/external/*` as the **only** Fineract surface — do not assume the rest of `experiments/e3-ablation/raw/` is wired unless a pulse explicitly expands the slice.

## Slices

| Slice | Upstream (conceptual) | In-repo source | Wired units |
|-------|----------------------|----------------|-------------|
| `fineract-handlers-thin/` | Apache Fineract command handlers | `experiments/e3-ablation/raw/` (copy) | 7 of 7 Java files (9 edges) |

## Commands

```bash
make fetch-slice-dry-run   # scripts/fetch_fineract_slice.sh (temp dir only; fixtures unchanged)
make external-slice-check
make wiringmap-stress    # includes density D4 on this slice
make dogfood-grade-fineract-thin
```

## Refreshing the thin slice (R4 fetch stub)

`scripts/fetch_fineract_slice.sh` documents **sparse-checkout**, **git archive**, and **curl raw** patterns that pull an explicit **PATH LIST** — never a full upstream tree. Defaults match basenames under `fineract-handlers-thin/`.

| Mode | Behavior |
|------|----------|
| dry-run (default) | Writes `PATH_LIST.txt` + `FETCH_PLAN.txt` under a temp dir; exits 0; fixtures untouched |
| `--apply` | Copies staged files into `fineract-handlers-thin/` and writes `MANIFEST.txt` (`source_commit=manual pin` until a live pin is recorded) |

Environment overrides: `FINERACT_UPSTREAM_REPO`, `FINERACT_UPSTREAM_REF`, `FINERACT_UPSTREAM_JAVA_PREFIX`. The current stub stages `*.java` from `experiments/e3-ablation/raw/` and keeps wiringmap/README as in-repo artifacts.

## Limitations

- `scripts/extract_refs.py` only parses `// refs:` comment lines; it does **not** infer Spring `@Autowired` / constructor injection from Java bodies.
- Handlers without `// refs:` in the slice are counted via **import-line fallback** in `fineract_slice_check.sh` (documented; not a wiringmap edge source).
