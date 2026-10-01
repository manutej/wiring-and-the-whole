#!/usr/bin/env python3
"""Backward-compatible entry: witness/toybank/accounts + toybank-accounts.v0.json."""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from extract_refs import main as extract_main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(extract_main(sys.argv[1:]))
