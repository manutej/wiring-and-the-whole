#!/usr/bin/env python3
"""Validate a WiringMap v0 instance against wiringmap/schema.v0.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = REPO / "wiringmap" / "schema.v0.json"
DEFAULT_INSTANCE = REPO / "wiringmap" / "examples" / "toybank-accounts.v0.json"


def main() -> int:
    schema_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SCHEMA
    instance_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_INSTANCE

    try:
        import jsonschema
        from jsonschema.exceptions import ValidationError
    except ImportError:
        print(
            "ERROR: jsonschema required — install with: python3 -m pip install jsonschema",
            file=sys.stderr,
        )
        return 1

    if not schema_path.is_file():
        print(f"ERROR: schema not found: {schema_path}", file=sys.stderr)
        return 1
    if not instance_path.is_file():
        print(f"ERROR: instance not found: {instance_path}", file=sys.stderr)
        return 1

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    instance = json.loads(instance_path.read_text(encoding="utf-8"))

    try:
        jsonschema.validate(instance, schema)
    except ValidationError as exc:
        path = " / ".join(str(p) for p in exc.absolute_path) or "(root)"
        print(f"validation failed at {path}: {exc.message}", file=sys.stderr)
        return 1

    print(f"OK: {instance_path} validates against {schema_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
