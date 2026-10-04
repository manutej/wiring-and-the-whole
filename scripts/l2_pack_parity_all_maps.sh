#!/usr/bin/env bash
# Byte parity Rust vs Python for every wiringmap in slice-matrix manifest.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

python3 -c "
import json
from pathlib import Path
doc = json.loads(Path('fixtures/slice-matrix/manifest.v0.json').read_text())
for s in doc['slices']:
    print(s['wiringmap'])
" | while read -r wm; do
  [[ -n "${wm}" ]] || continue
  bash scripts/l2_pack_parity.sh "${wm}"
done

echo "OK: l2 pack parity all matrix maps"
