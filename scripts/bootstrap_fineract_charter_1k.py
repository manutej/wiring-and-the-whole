#!/usr/bin/env python3
"""Bootstrap fixtures/external/fineract-charter-1k from e3-ablation raw + parser-derived refs."""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from command_handler_parse import HandlerSpec, ParseSkip, parse_handler_java  # noqa: E402
from extract_refs import refs_from_java  # noqa: E402

RAW = ROOT / "experiments/e3-ablation/raw"
CHARTER = ROOT / "fixtures/external/fineract-charter-1k"
SIDECAR = ROOT / "fixtures/e3-commandhandler-wedge/annotation_sidecar.v0.json"
UPSTREAM_REF = "develop"
UPSTREAM_REPO = "https://github.com/apache/fineract.git"

REFS_INJECT = re.compile(r"^(package\s+[^;]+;\s*)", re.MULTILINE)
IMPORT_SERVICE = re.compile(
    r"^import\s+(org\.apache\.fineract\.(?:[\w.]+\.)?([\w.]+Write(?:Platform)?Service));\s*$",
    re.MULTILINE,
)
DATA_INTEGRITY_TOKEN = "infrastructure.DataIntegrityErrorHandler#handleDataIntegrityIssues"
JSON_COMMAND_LOAN_ID = "infrastructure.core.api.JsonCommand#getLoanId"
JSON_COMMAND_ENTITY_ID = "infrastructure.core.api.JsonCommand#entityId"


def load_sidecar() -> dict[str, dict[str, str]]:
    if not SIDECAR.is_file():
        return {}
    data = json.loads(SIDECAR.read_text(encoding="utf-8"))
    return dict(data.get("handlers") or {})


def fq_token_for_service(service_class: str, import_line: str | None, method: str) -> str | None:
    """Second recall token: package-relative service#method (distinct from bare class name)."""
    if import_line:
        prefix = "org.apache.fineract."
        if import_line.startswith(prefix):
            rel = import_line[len(prefix) :]
            return f"{rel}#{method}"
    return None


def service_imports(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in IMPORT_SERVICE.finditer(text):
        fq, simple = m.group(1), m.group(2)
        out[simple.split(".")[-1]] = fq
    return out


def inject_refs(path: Path, tokens: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if "// refs:" in text:
        return
    line = "  // refs: " + " ".join(tokens) + "\n"
    if REFS_INJECT.search(text):
        text = REFS_INJECT.sub(r"\1\n" + line, text, count=1)
    else:
        text = line + text
    path.write_text(text, encoding="utf-8")


def junction_id(service_label: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", service_label)
    return f"junction:{safe}"


def build_wiringmap(specs: list[tuple[str, HandlerSpec, list[str]]]) -> dict:
    slice_ref = "fixtures/external/fineract-charter-1k"
    junctions: dict[str, dict] = {}
    units: list[dict] = []
    edges: list[dict] = []

    def ensure_junction(label: str) -> str:
        jid = junction_id(label)
        if jid not in junctions:
            junctions[jid] = {
                "id": jid,
                "label": label,
                "junction_kind": "other",
            }
        return jid

    ensure_junction("infrastructure.DataIntegrityErrorHandler")
    ensure_junction("infrastructure.core.api.JsonCommand")

    for fname, spec, tokens in specs:
        rel_path = f"{slice_ref}/{fname}"
        uid = f"unit:handler.{spec.handler}"
        units.append(
            {
                "id": uid,
                "path": rel_path,
                "role": f"Command handler — {spec.entity} {spec.action}",
                "ports": [
                    {
                        "id": f"port:handler.{spec.handler}#processCommand",
                        "symbol": "processCommand",
                        "kind": "method",
                        "signature_stub": "CommandProcessingResult processCommand(JsonCommand command)",
                        "exported": True,
                    }
                ],
            }
        )
        port_from = f"port:handler.{spec.handler}#processCommand"
        for i, token in enumerate(tokens):
            if "#" not in token:
                continue
            svc_part = token.split("#", 1)[0]
            label = svc_part
            if svc_part.startswith("infrastructure.core.api.JsonCommand"):
                to_j = ensure_junction("infrastructure.core.api.JsonCommand")
            elif svc_part == "infrastructure.DataIntegrityErrorHandler":
                to_j = ensure_junction("infrastructure.DataIntegrityErrorHandler")
            else:
                label = svc_part.split(".")[-1] if "." not in svc_part else svc_part
                to_j = ensure_junction(
                    label if label.endswith("Service") or "ErrorHandler" in label else svc_part
                )
            edge_id = f"edge:{spec.handler.lower()}-{i}"
            edges.append(
                {
                    "id": edge_id,
                    "from": port_from,
                    "to": to_j,
                    "edge_kind": "di",
                    "doctrine_tag": "system_map",
                    "evidence": f"{fname} // refs: {token}",
                }
            )

    return {
        "schema_version": "wiringmap.v0",
        "meta": {
            "repo": "wiring-and-the-whole",
            "ref": slice_ref,
            "slice": f"{len(units)} @CommandType handlers (~1k LOC chartered vertical)",
            "notes": "Pinned PATH LIST from e3-ablation raw; // refs: injected from parser v1 (not live Fineract checkout).",
        },
        "junctions": list(junctions.values()),
        "units": units,
        "edges": edges,
    }


def write_manifest(_java_names: list[str]) -> None:
    paths = sorted(
        p.name
        for p in CHARTER.iterdir()
        if p.is_file() and p.name != "MANIFEST.txt"
    )
    lines = [
        f"source_repo={UPSTREAM_REPO}",
        "source_commit=e3-ablation-local-corpus",
        f"source_ref={UPSTREAM_REF}",
        "fetched_at=2026-10-03T00:00:00Z",
        "fetch_mode=stub (local corpus for *.java; in-repo wiringmap/README)",
        "path_list_file=PATH_LIST.txt",
        "",
        "# paths applied:",
        *paths,
    ]
    (CHARTER / "MANIFEST.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    sidecar = load_sidecar()
    if CHARTER.exists():
        shutil.rmtree(CHARTER)
    CHARTER.mkdir(parents=True)

    specs: list[tuple[str, HandlerSpec, list[str]]] = []
    java_names: list[str] = []

    skipped_orthogonal: list[str] = []

    for src in sorted(RAW.glob("*CommandHandler.java")):
        parsed_probe = parse_handler_java(src, annotation_sidecar=sidecar)
        if isinstance(parsed_probe, ParseSkip) and parsed_probe.category == "orthogonal_command_api":
            skipped_orthogonal.append(src.name)
            continue

        dest = CHARTER / src.name
        shutil.copy2(src, dest)
        java_names.append(src.name)

        parsed = parse_handler_java(dest, annotation_sidecar=sidecar)
        if not isinstance(parsed, HandlerSpec):
            continue

        text = dest.read_text(encoding="utf-8")
        imports = service_imports(text)
        short_svc = parsed.service.split(".")[-1]
        tokens: list[str] = [f"{short_svc}#{parsed.method}"]
        fq = fq_token_for_service(parsed.service, imports.get(short_svc), parsed.method)
        if fq and fq not in tokens:
            tokens.append(fq)
        if "DataIntegrityErrorHandler" in text and DATA_INTEGRITY_TOKEN not in tokens:
            tokens.append(DATA_INTEGRITY_TOKEN)
        if "getLoanId()" in text and JSON_COMMAND_LOAN_ID not in tokens:
            tokens.append(JSON_COMMAND_LOAN_ID)
        if "entityId()" in text and JSON_COMMAND_ENTITY_ID not in tokens:
            tokens.append(JSON_COMMAND_ENTITY_ID)

        inject_refs(dest, tokens)
        specs.append((src.name, parsed, tokens))

    wm = build_wiringmap(specs)
    (CHARTER / "wiringmap.v0.json").write_text(
        json.dumps(wm, indent=2) + "\n", encoding="utf-8"
    )

    readme = f"""# fineract-charter-1k — pinned handler vertical (~1k LOC)

**Not a Fineract checkout.** {len(java_names)} Java files copied from
(excludes orthogonal `CommandHandler<Req,Res>` APIs: {", ".join(skipped_orthogonal) or "none"})
[`experiments/e3-ablation/raw/`](../../experiments/e3-ablation/raw/) with hand-maintained
[`wiringmap.v0.json`](wiringmap.v0.json) and parser-injected `// refs:` on
{len(specs)} wired handlers.

## What is **not** included

- Full Fineract tree, runtime, or staff traces
- Auto WiringMap from production DI

## Gates

```bash
make charter-1k-check
python3 scripts/extract_refs.py fixtures/external/fineract-charter-1k \\
  --example fixtures/external/fineract-charter-1k/wiringmap.v0.json
```

Refresh stub fetch plan: `./scripts/fetch_fineract_charter_1k.sh --apply`
"""
    (CHARTER / "README.md").write_text(readme, encoding="utf-8")
    write_manifest([])

    loc = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in CHARTER.glob("*.java"))
    pairs = sum(len(refs_from_java(p)) for p in CHARTER.glob("*.java"))
    print(
        f"OK: charter-1k — {len(java_names)} java files, {len(specs)} wired, "
        f"{loc} LOC, {pairs} ref tokens",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
