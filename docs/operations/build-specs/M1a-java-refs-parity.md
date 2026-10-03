# Build spec M1a — Java refs parity (builders only)

## Done when

1. `refs_from_java_source` matches Python `REFS_LINE = re.compile(r"//\s*refs:\s*(.+)$")` per line (multiline: first matching line wins like Python loop).
2. Unit tests: `// refs:`, `//  refs:`, `//refs:` forms.
3. `scripts/java_refs_parity.sh` unchanged contract; passes toybank + fineract-thin.
4. `make wiring-core-check` and `make pulse-loop` green.

## Out of scope

- wiringmap `--example` in Rust
- pipeline-io switch
- PR creation
