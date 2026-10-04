# Wiring index store (incremental discoveries)

Append-only **JSONL** for batch workers analyzing large repos without re-reading everything each run.

- **Schema per line:** `wiring-index-record.v0` — see [`record.schema.v0.json`](record.schema.v0.json)
- **CLI:** `python3 scripts/wiring_index_store.py append --json '{...}'`
- **Stats:** `python3 scripts/wiring_index_store.py stats`

Designed for S5 large-repo leap (e.g. [OpenRig](https://github.com/mvschwarz/openrig)): inventory first (`repo_inventory_v0.py`), then targeted extract passes that append facts here.
