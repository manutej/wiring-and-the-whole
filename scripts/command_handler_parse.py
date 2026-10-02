#!/usr/bin/env python3
"""Parse Fineract @CommandType NewCommandSourceHandler Java for L2 CommandHandler motif rows."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

COMMAND_TYPE_QUOTED = re.compile(
    r"@CommandType\s*\(\s*entity\s*=\s*\"([^\"]+)\"\s*,\s*action\s*=\s*\"([^\"]+)\"\s*\)"
)
COMMAND_TYPE_CONST = re.compile(
    r"@CommandType\s*\(\s*entity\s*=\s*([\w.]+)\s*,\s*action\s*=\s*([\w.]+)\s*\)"
)
CLASS_NAME = re.compile(r"public\s+class\s+(\w+)\s+")
INJECTED_FIELD = re.compile(r"private\s+final\s+(\w+)\s+(\w+)\s*;")
PROCESS_COMMAND = re.compile(
    r"public\s+CommandProcessingResult\s+processCommand\s*\(",
    re.MULTILINE,
)
SERVICE_CALL = re.compile(r"(?:this\.)?(\w+)\.(\w+)\s*\(")

# Fineract CommandWrapperConstants (not vendored); pack uses resolved string labels.
CONSTANT_ENTITY = {
    "CommandWrapperConstants.ENTITY_WORKINGCAPITALLOAN": "WORKINGCAPITALLOAN",
    "ENTITY_WORKINGCAPITALLOAN": "WORKINGCAPITALLOAN",
}
CONSTANT_ACTION = {
    "CommandWrapperConstants.ACTION_RECOVERYPAYMENT": "RECOVERYPAYMENT",
    "ACTION_RECOVERYPAYMENT": "RECOVERYPAYMENT",
}


@dataclass(frozen=True)
class HandlerSpec:
    handler: str
    dep_field: str
    service: str
    method: str
    entity: str
    action: str
    source_path: str


@dataclass(frozen=True)
class ParseSkip:
    reason: str
    category: str


def _service_type(typ: str) -> bool:
    return typ.endswith("WritePlatformService") or typ.endswith("WriteService")


def _resolve_constant(token: str, table: dict[str, str]) -> str | None:
    token = token.strip()
    if token in table:
        return table[token]
    if token.startswith('"') and token.endswith('"'):
        return token[1:-1]
    return None


def parse_command_type(text: str) -> tuple[str, str] | None:
    m = COMMAND_TYPE_QUOTED.search(text)
    if m:
        return m.group(1), m.group(2)
    m = COMMAND_TYPE_CONST.search(text)
    if not m:
        return None
    ent_raw, act_raw = m.group(1), m.group(2)
    entity = _resolve_constant(ent_raw, CONSTANT_ENTITY)
    action = _resolve_constant(act_raw, CONSTANT_ACTION)
    if entity is None or action is None:
        return None
    return entity, action


def load_annotation_sidecar(sidecar_path: Path | None) -> dict[str, dict[str, str]]:
    if sidecar_path is None or not sidecar_path.is_file():
        return {}
    data = json.loads(sidecar_path.read_text(encoding="utf-8"))
    return dict(data.get("handlers") or {})


def parse_handler_java(
    path: Path,
    *,
    annotation_sidecar: dict[str, dict[str, str]] | None = None,
) -> HandlerSpec | ParseSkip | None:
    text = path.read_text(encoding="utf-8")
    sidecar = annotation_sidecar or {}

    if "implements CommandHandler<" in text and "NewCommandSourceHandler" not in text:
        return ParseSkip(
            reason="orthogonal command API (CommandHandler<Req,Res>, not @CommandType family)",
            category="orthogonal_command_api",
        )

    cm = CLASS_NAME.search(text)
    if not cm:
        return None
    handler = cm.group(1)

    ct = parse_command_type(text)
    if not ct:
        side = sidecar.get(path.name)
        if side and side.get("entity") and side.get("action"):
            ct = (side["entity"], side["action"])
        elif "NewCommandSourceHandler" in text:
            return ParseSkip(
                reason="missing or unresolved @CommandType annotation",
                category="missing_command_type",
            )
        else:
            return ParseSkip(reason="no @CommandType family match", category="unclassified")

    entity, action = ct

    fields: dict[str, str] = {}
    for typ, name in INJECTED_FIELD.findall(text):
        if _service_type(typ):
            fields[name] = typ

    if not fields:
        return ParseSkip(
            reason="no injected WritePlatformService / WriteService field",
            category="missing_service_field",
        )

    pcm = PROCESS_COMMAND.search(text)
    if not pcm:
        return ParseSkip(reason="no processCommand method", category="missing_process_command")

    body_start = pcm.end()
    next_def = re.search(r"\n\s*(?:public|private|protected|\@|\})", text[body_start:])
    body_end = body_start + next_def.start() if next_def else len(text)
    body = text[body_start:body_end]

    dep_field: str | None = None
    method: str | None = None
    service: str | None = None
    for fld, meth in SERVICE_CALL.findall(body):
        if fld in fields:
            dep_field = fld
            method = meth
            service = fields[fld]
            break

    if not dep_field or not method or not service:
        return ParseSkip(
            reason="no WritePlatformService call in processCommand body",
            category="missing_service_call",
        )

    return HandlerSpec(
        handler=handler,
        dep_field=dep_field,
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
        f"dep {spec.handler}.{spec.dep_field}: {spec.service}",
        f"edge {spec.handler} -> {spec.service}#{spec.method}",
    ]


def inst_row(spec: HandlerSpec) -> str:
    if spec.dep_field == "writePlatformService":
        return (
            f"inst CommandHandler({spec.handler}, {spec.service}, "
            f"{spec.method}, {spec.entity}, {spec.action})"
        )
    return (
        f"inst CommandHandler({spec.handler}, {spec.dep_field}, {spec.service}, "
        f"{spec.method}, {spec.entity}, {spec.action})"
    )
