#!/usr/bin/env python3
"""Structural Java extract (javalang AST) — wiring-oriented fields, not full source dump."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import javalang
except ImportError:
    print("ERROR: pip install javalang", file=sys.stderr)
    raise SystemExit(1) from None

ROOT = Path(__file__).resolve().parents[1]


def command_type_attrs(source: str) -> dict[str, str]:
    m = re.search(
        r"@CommandType\s*\(\s*entity\s*=\s*\"([^\"]+)\"\s*,\s*action\s*=\s*\"([^\"]+)\"",
        source,
    )
    if not m:
        return {}
    return {"entity": m.group(1), "action": m.group(2)}


def extract_file(path: Path) -> dict[str, object]:
    source = path.read_text(encoding="utf-8")
    tree = javalang.parse.parse(source)
    cmd = command_type_attrs(source)
    imports = [imp.path for imp in tree.imports or []]
    classes: list[dict[str, object]] = []
    for type_decl in tree.types or []:
        if not isinstance(type_decl, javalang.tree.ClassDeclaration):
            continue
        methods: list[dict[str, object]] = []
        anns: list[str] = []
        for m in type_decl.methods or []:
            if not m.name:
                continue
            invocations: list[str] = []
            if m.body:
                for _path, node in m.filter(javalang.tree.MethodInvocation):
                    if isinstance(node, javalang.tree.MethodInvocation) and node.member:
                        qual = node.qualifier or ""
                        invocations.append(f"{qual}.{node.member}" if qual else node.member)
            methods.append(
                {
                    "name": m.name,
                    "annotations": [a.name for a in m.annotations or []],
                    "invocations": sorted(set(invocations))[:40],
                }
            )
        for a in type_decl.annotations or []:
            anns.append(a.name)
        classes.append(
            {
                "name": type_decl.name,
                "annotations": anns,
                "methods": methods,
            }
        )
    return {
        "file": path.name,
        "imports": imports,
        "command_type": cmd,
        "classes": classes,
    }


def render_text(doc: dict[str, object]) -> str:
    lines: list[str] = []
    for file_doc in doc.get("files") or []:
        if not isinstance(file_doc, dict):
            continue
        lines.append(f"FILE {file_doc.get('file')}")
        ct = file_doc.get("command_type") or {}
        if isinstance(ct, dict) and ct.get("action"):
            lines.append(f"  @CommandType entity={ct.get('entity')} action={ct.get('action')}")
        for imp in file_doc.get("imports") or []:
            lines.append(f"  import {imp}")
        for cls in file_doc.get("classes") or []:
            if not isinstance(cls, dict):
                continue
            lines.append(f"  CLASS {cls.get('name')} annotations={cls.get('annotations')}")
            for m in cls.get("methods") or []:
                if not isinstance(m, dict):
                    continue
                lines.append(f"    METHOD {m.get('name')} annotations={m.get('annotations')}")
                for inv in m.get("invocations") or []:
                    lines.append(f"      CALL {inv}")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("inputs", nargs="+", type=Path, help="Java files or directories")
    p.add_argument("--out-json", type=Path, default=None)
    p.add_argument("--out-text", type=Path, default=None)
    args = p.parse_args(argv)

    paths: list[Path] = []
    for inp in args.inputs:
        inp = inp if inp.is_absolute() else ROOT / inp
        if inp.is_dir():
            paths.extend(sorted(inp.glob("*.java")))
        elif inp.is_file():
            paths.append(inp)

    files = [extract_file(p) for p in paths]
    doc = {"schema_version": "ast-struct.v0", "file_count": len(files), "files": files}
    text = render_text(doc)

    if args.out_json:
        out = args.out_json if args.out_json.is_absolute() else ROOT / args.out_json
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    if args.out_text:
        out = args.out_text if args.out_text.is_absolute() else ROOT / args.out_text
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")

    if not args.out_json and not args.out_text:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
