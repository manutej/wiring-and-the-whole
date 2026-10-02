#!/usr/bin/env python3
"""Parse Fineract @CommandType NewCommandSourceHandler Java for L2 CommandHandler motif rows."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

COMMAND_TYPE = re.compile(
    r"@CommandType\s*\(\s*entity\s*=\s*\"([^\"]+)\"\s*,\s*action\s*=\s*\"([^\"]+)\"\s*\)"
)
CLASS_NAME = re.compile(r"public\s+class\s+(\w+)\s+")
SERVICE_FIELD = re.compile(
    r"private\s+final\s+(\w+)\s+writePlatformService\s*;",
)
METHOD_CALL = re.compile(
    r"(?:this\.)?writePlatformService\.(\w+)\s*\(",
)


@dataclass(frozen=True)
class HandlerSpec:
    handler: str
    service: str
    method: str
    entity: str
    action: str
    source_path: str


def parse_handler_java(path: Path) -> HandlerSpec | None:
    text = path.read_text(encoding="utf-8")
    cm = CLASS_NAME.search(text)
    tm = COMMAND_TYPE.search(text)
    if not cm or not tm:
        return None
    handler = cm.group(1)
    entity, action = tm.group(1), tm.group(2)
    sm = SERVICE_FIELD.search(text)
    if not sm:
        return None
    service = sm.group(1)
    mm = METHOD_CALL.search(text)
    if not mm:
        return None
    method = mm.group(1)
    return HandlerSpec(
        handler=handler,
        service=service,
        method=method,
        entity=entity,
        action=action,
        source_path=str(path.name),
    )


def explicit_block(spec: HandlerSpec) -> list[str]:
    return [
        f"unit {spec.handler}",
        f"anno {spec.handler} @CommandType entity={spec.entity} action={spec.action}",
        f"dep {spec.handler}.writePlatformService: {spec.service}",
        f"edge {spec.handler} -> {spec.service}#{spec.method}",
    ]


def inst_row(spec: HandlerSpec) -> str:
    return (
        f"inst CommandHandler({spec.handler}, {spec.service}, "
        f"{spec.method}, {spec.entity}, {spec.action})"
    )
