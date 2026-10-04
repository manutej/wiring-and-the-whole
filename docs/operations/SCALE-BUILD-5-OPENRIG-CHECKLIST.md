# Scale build 5 — OpenRig large repo (prep)

**Spec:** [`build-specs/S5-openrig-large-repo.md`](build-specs/S5-openrig-large-repo.md)

| ID | Item | Gate | Status |
|----|------|------|--------|
| S5a | Repo inventory (stat-only) | `make repo-inventory-check` | **done** (this monorepo baseline) |
| S5b | Wiring index JSONL store | `wiring_index_store.py stats` | **scaffold** |
| S5c | Pin + inventory OpenRig clone | `fixtures/repo-inventory/openrig.v0.json` | pending |
| S5d | RigSpec edge → index records | eval doc | pending |
| S5× | Independent SHIP | — | pending |
