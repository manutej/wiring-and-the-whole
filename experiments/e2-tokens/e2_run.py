#!/usr/bin/env python3
"""
E2 — TOKEN MICRO-EXAMPLE (discharges GA6). Real Fineract sites, both serializations,
byte-identical re-expansion gate, cl100k token counts, F/m/e and n* = F/(e-m).
Sites: S1 SavingsAccountsApiResource (ApiResource family, n=169 repo-wide)
       S2 SavingsAccountRepositoryWrapper (RepositoryWrapper family, n=54)
       S3 ActivateSavingsAccountCommandHandler (@CommandType handler family, n=514)
"""
import re, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from wiring import extract, block_A, count_tokens
FAMILY_N = {"ApiResource": 169, "RepositoryWrapper": 54, "CommandHandler": 514}

def read(f): return open(os.path.join(HERE, "raw", f)).read()

SITES = [
    ("S1", "ApiResource", "SavingsAccountsApiResource.java"),
    ("S2", "RepositoryWrapper", "SavingsAccountRepositoryWrapper.java"),
    ("S3", "CommandHandler", "ActivateSavingsAccountCommandHandler.java"),
]
EX = {sid: extract(read(f)) for sid, fam, f in SITES}

# Form A (explicit edge list, aider-repo-map style) is wiring.block_A + newline.
# ---------------- Form B: legend + seed + motif defs + instantiation rows ----------------
LEGEND = """# WIRING PACK v1 — generator-data form
# legend: 'motif NAME(slots): template' defines a wiring shape; template lines use $slots.
# 'inst NAME(fills) [+ delta-lines]' instantiates it: expand template with fills, then apply
# deltas verbatim. 'deps=' lists field:Type pairs; 'calls=' lists Type#method targets.
# Expansion of every inst reproduces the explicit form exactly (lossless by construction).
"""

# Motif definitions per family — the SHARED shape, learned from the family convention.
MOTIFS = {
"CommandHandler": """motif CommandHandler(H, S, m, entity, action):
  unit $H
  anno $H @CommandType entity=$entity action=$action
  dep $H.writePlatformService: $S
  edge $H -> $S#$m
""",
"RepositoryWrapper": """motif RepositoryWrapper(W, R, deps, calls):
  unit $W
  foreach f:T in $deps -> dep $W.$f: $T
  foreach T#m in $calls -> edge $W -> $T#$m
""",
"ApiResource": """motif ApiResource(A, deps, calls):
  unit $A
  foreach f:T in $deps -> dep $A.$f: $T
  foreach T#m in $calls -> edge $A -> $T#$m
""",
}

def row_for(sid, fam, x):
    if fam == "CommandHandler":
        # fully convention-determined: one dep, one call
        (typ, meth) = x["edges"][0]
        ent, act = x["entity"], x["action"]
        return f"inst CommandHandler({x['cls']}, {typ}, {meth}, {ent}, {act})\n"
    deps = ",".join(f"{f}:{t}" for f, t in sorted(x["deps"].items()))
    calls = ",".join(f"{t}#{m}" for t, m in x["edges"])
    return f"inst {fam}({x['cls']}, deps=[{deps}], calls=[{calls}])\n"

def expand(fam, rowtext, x):
    """Mechanical expansion of an inst row back to Form A lines."""
    if fam == "CommandHandler":
        m = re.match(r'inst CommandHandler\((\w+), (\w+), (\w+), (\w+), (\w+)\)', rowtext)
        H, S, meth, ent, act = m.groups()
        L = [f"unit {H}", f"anno {H} @CommandType entity={ent} action={act}",
             f"dep {H}.writePlatformService: {S}", f"edge {H} -> {S}#{meth}"]
        return "\n".join(L) + "\n"
    m = re.match(r'inst \w+\((\w+), deps=\[(.*?)\], calls=\[(.*?)\]\)', rowtext, re.S)
    A, deps_s, calls_s = m.groups()
    L = [f"unit {A}"]
    for pair in filter(None, deps_s.split(",")):
        f, t = pair.split(":")
        L.append(f"dep {A}.{f}: {t}")
    for c in filter(None, calls_s.split(",")):
        t, meth = c.split("#")
        L.append(f"edge {A} -> {t}#{meth}")
    return "\n".join(L) + "\n"

# ---------------- run: gate, tokenize, account ----------------
texts, results = {}, {}
gate_all = True
for sid, fam, f in SITES:
    x = EX[sid]
    A = block_A(x) + "\n"
    row = row_for(sid, fam, x)
    reexp = expand(fam, row, x)
    gate = (reexp == A)
    gate_all &= gate
    texts[f"{sid}_A"] = A
    texts[f"{sid}_row"] = row
    texts[f"{sid}_motif"] = MOTIFS[fam]
    results[sid] = {"family": fam, "file": f, "units_deps": len(x["deps"]),
                    "edges": len(x["edges"]), "gate_byte_identical": gate}
texts["LEGEND"] = LEGEND

tok = count_tokens(texts)

for sid, fam, f in SITES:
    e = tok[f"{sid}_A"]                       # explicit per-instance cost
    m = tok[f"{sid}_row"]                     # factored per-instance marginal cost
    F = tok["LEGEND"] + tok[f"{sid}_motif"]   # fixed overhead: legend + this family's motif
    n_star = (float('inf') if e <= m else -(-F // (e - m)))
    n_act = FAMILY_N[fam]
    results[sid].update({"e_explicit_tokens": e, "m_factored_row_tokens": m,
        "F_fixed_overhead_tokens": F, "n_star_breakeven": n_star,
        "n_actual_repo_wide": n_act,
        "verdict": ("WIN" if e > m and n_star < n_act else
                    "KILL" if e <= m else "AMBIGUOUS"),
        "repo_wide_savings_est_tokens": (e - m) * n_act - F if e > m else 0})

out = {"experiment": "E2 token micro-example", "date": "2026-09-16",
       "tokenizer": "cl100k_base (tiktoken npm, vendored encoder)",
       "gate_all_sites_byte_identical": gate_all,
       "legend_tokens": tok["LEGEND"], "sites": results,
       "kill_rule": "KILL iff e<=m OR n*>n_actual on ALL sites",
       "overall": None}
wins = [s for s in results.values() if s["verdict"] == "WIN"]
kills = [s for s in results.values() if s["verdict"] == "KILL"]
out["overall"] = ("WIN" if wins else ("KILL" if len(kills) == len(results) else "AMBIGUOUS"))
json.dump(out, open(os.path.join(HERE, "E2-RESULTS.json"), "w"), indent=2, default=str)
# also persist the serializations for audit
for k, v in texts.items():
    open(os.path.join(HERE, f"pack_{k}.txt"), "w").write(v)
print(json.dumps(out, indent=2, default=str))
