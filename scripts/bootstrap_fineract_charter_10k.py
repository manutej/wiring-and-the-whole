#!/usr/bin/env python3
"""Bootstrap fixtures/external/fineract-charter-10k — ~10k LOC chartered PATH LIST (experiments corpus)."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

# Reuse 1k bootstrap logic for handlers + wiringmap
import bootstrap_fineract_charter_1k as b1k  # noqa: E402

CHARTER = ROOT / "fixtures/external/fineract-charter-10k"

SOURCE_GLOBS: list[tuple[Path, str]] = [
    (ROOT / "experiments/e3-ablation/raw", "*CommandHandler.java"),
    (ROOT / "experiments/e5-depth/raw", "*.java"),
    (ROOT / "experiments/e2-tokens/raw", "*.java"),
]

UPSTREAM_REF = "develop"
UPSTREAM_REPO = "https://github.com/apache/fineract.git"


def collect_sources() -> list[tuple[Path, str]]:
    """Return (src_path, dest_basename) deduped by basename (first source wins)."""
    seen: set[str] = set()
    out: list[tuple[Path, str]] = []
    for base, pattern in SOURCE_GLOBS:
        if not base.is_dir():
            continue
        for src in sorted(base.glob(pattern)):
            if src.name in seen:
                continue
            seen.add(src.name)
            out.append((src, src.name))
    return out


def main() -> int:
    sidecar = b1k.load_sidecar()
    if CHARTER.exists():
        shutil.rmtree(CHARTER)
    CHARTER.mkdir(parents=True)

    copied: list[str] = []
    for src, name in collect_sources():
        shutil.copy2(src, CHARTER / name)
        copied.append(name)

    specs: list[tuple[str, b1k.HandlerSpec, list[str]]] = []
    skipped_orthogonal: list[str] = []

    for path in sorted(CHARTER.glob("*CommandHandler.java")):
        parsed_probe = b1k.parse_handler_java(path, annotation_sidecar=sidecar)
        if isinstance(parsed_probe, b1k.ParseSkip) and parsed_probe.category == "orthogonal_command_api":
            skipped_orthogonal.append(path.name)
            path.unlink()
            continue
        parsed = b1k.parse_handler_java(path, annotation_sidecar=sidecar)
        if not isinstance(parsed, b1k.HandlerSpec):
            continue
        text = path.read_text(encoding="utf-8")
        imports = b1k.service_imports(text)
        short_svc = parsed.service.split(".")[-1]
        tokens: list[str] = [f"{short_svc}#{parsed.method}"]
        fq = b1k.fq_token_for_service(parsed.service, imports.get(short_svc), parsed.method)
        if fq and fq not in tokens:
            tokens.append(fq)
        if "DataIntegrityErrorHandler" in text and b1k.DATA_INTEGRITY_TOKEN not in tokens:
            tokens.append(b1k.DATA_INTEGRITY_TOKEN)
        if "getLoanId()" in text and b1k.JSON_COMMAND_LOAN_ID not in tokens:
            tokens.append(b1k.JSON_COMMAND_LOAN_ID)
        if "entityId()" in text and b1k.JSON_COMMAND_ENTITY_ID not in tokens:
            tokens.append(b1k.JSON_COMMAND_ENTITY_ID)
        b1k.inject_refs(path, tokens)
        specs.append((path.name, parsed, tokens))

    slice_ref = "fixtures/external/fineract-charter-10k"
    wm = b1k.build_wiringmap(specs)
    wm["meta"]["slice"] = (
        f"{len(copied)} Java files (~10k LOC experiments PATH LIST); "
        f"{len(specs)} wired handlers; service bodies co-packaged for scale test"
    )
    wm["meta"]["ref"] = slice_ref
    wm["meta"]["notes"] = (
        "Experiments PATH LIST (e3-ablation handlers, e5-depth + e2-tokens services); "
        "// refs: injected from parser v1 — not a live Fineract checkout."
    )
    for u in wm["units"]:
        u["path"] = u["path"].replace("fineract-charter-1k", "fineract-charter-10k")

    (CHARTER / "wiringmap.v0.json").write_text(json.dumps(wm, indent=2) + "\n", encoding="utf-8")

    readme = f"""# fineract-charter-10k — experiments PATH LIST (~10k LOC)

**Not a Fineract checkout.** This charter copies **{len(copied)}** Java files from in-repo
experiments (`e3-ablation`, `e5-depth`, `e2-tokens`) for **scale honesty** — validate → extract → pack → reexpand
at ~10k LOC without claiming repo-wide wiring.

## Wiring discipline

- **{len(specs)}** `@CommandType` handlers carry `// refs:` and full map units (same family as charter-1k).
- **Service / repository** files add LOC and realism; they are **not** fully mapped (Spring DI out of scope).

Orthogonal handlers excluded: {", ".join(skipped_orthogonal) or "none"}.

## Gates

```bash
make charter-10k-check
make slice-matrix-check   # includes this shard when listed in manifest
```

Bootstrap: `python3 scripts/bootstrap_fineract_charter_10k.py`
"""
    (CHARTER / "README.md").write_text(readme, encoding="utf-8")

    java_names = sorted(p.name for p in CHARTER.glob("*.java"))
    (CHARTER / "PATH_LIST.txt").write_text("\n".join(java_names) + "\n", encoding="utf-8")

    paths = sorted(p.name for p in CHARTER.iterdir() if p.is_file() and p.name != "MANIFEST.txt")
    manifest = "\n".join(
        [
            f"source_repo={UPSTREAM_REPO}",
            "source_commit=unpinned-experiments-corpus",
            f"source_ref={UPSTREAM_REF}",
            "fetched_at=2026-10-04T00:00:00Z",
            "fetch_mode=stub (experiments PATH LIST; handlers wired; services context-only; no upstream SHA pinned)",
            "path_list_file=PATH_LIST.txt",
            "",
            "# paths applied:",
            *paths,
            "",
        ]
    )
    (CHARTER / "MANIFEST.txt").write_text(manifest, encoding="utf-8")

    loc = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in CHARTER.glob("*.java"))
    pairs = sum(len(b1k.refs_from_java(p)) for p in CHARTER.glob("*.java"))
    print(
        f"OK: charter-10k — {len(copied)} files, {loc} LOC, {len(specs)} wired handlers, {pairs} ref tokens",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
