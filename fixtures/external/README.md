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
        validate_wiringmap.py
```

**Reader rule:** Scripts and L1 packs under `docs/dogfood/` treat `fixtures/external/*` as the **only** Fineract surface — do not assume the rest of `experiments/e3-ablation/raw/` is wired unless a pulse explicitly expands the slice.

## Slices

| Slice | Upstream (conceptual) | In-repo source | Wired units |
|-------|----------------------|----------------|-------------|
| `fineract-handlers-thin/` | Apache Fineract command handlers | `experiments/e3-ablation/raw/` (copy) | 3 of 7 Java files |

## Commands

```bash
make external-slice-check
make wiringmap-stress    # includes density D4 on this slice
make dogfood-grade-fineract-thin
```

## Limitations

- `scripts/extract_refs.py` only parses `// refs:` comment lines; it does **not** infer Spring `@Autowired` / constructor injection from Java bodies.
- Handlers without `// refs:` in the slice are counted via **import-line fallback** in `fineract_slice_check.sh` (documented; not a wiringmap edge source).
