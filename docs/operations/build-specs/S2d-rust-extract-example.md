# Build spec S2d — Rust extract wiringmap example check

**Done when:**

1. `wiring-extract-java-refs` accepts `--example` and `--no-example-check` (parity with `extract_refs.py`).
2. `scripts/java_refs_example_parity.sh` green on toybank, fineract-thin, charter-1k.
3. `java_refs_parity.sh` passes `--no-example-check` so token parity does not default to toybank map.
