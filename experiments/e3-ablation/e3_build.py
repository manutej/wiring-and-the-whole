#!/usr/bin/env python3
"""
E3 build — extract graph from 30 real Fineract handlers; emit packs A/B/C, questions, gold.
Firewall discipline: questions are generated ONLY from graph.json via templates below;
pack layout code never informs question selection. Frozen via SHA-256 before any model call.
"""
import re, os, json, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
files = sorted(os.listdir(os.path.join(HERE, "raw")))

# ---------- extract ----------
G = []
for f in files:
    src = open(os.path.join(HERE, "raw", f)).read()
    cls = re.search(r'public class (\w+)', src).group(1)
    ann = re.search(r'@CommandType\(entity = "?([\w.-]+)"?, action = "?([\w.-]+)"?\)', src)
    deps = {}
    for m in re.finditer(r'private final ([A-Z][\w<>,. ]*?)\s+(\w+);', src):
        deps[m.group(2)] = m.group(1).split('<')[0].strip()
    edges = sorted({(deps[m.group(1)], m.group(2))
                    for m in re.finditer(r'(?:this\.)?(\w+)\.(\w+)\(', src) if m.group(1) in deps})
    G.append({"cls": cls, "entity": ann.group(1) if ann else None,
              "action": ann.group(2) if ann else None, "deps": deps, "edges": edges})
G.sort(key=lambda x: x["cls"])
json.dump(G, open(os.path.join(HERE, "graph.json"), "w"), indent=1)

# ---------- packs ----------
def block_A(x):
    L = [f"unit {x['cls']}"]
    if x["entity"]: L.append(f"anno {x['cls']} @CommandType entity={x['entity']} action={x['action']}")
    for fld, typ in sorted(x["deps"].items()): L.append(f"dep {x['cls']}.{fld}: {typ}")
    for typ, meth in x["edges"]: L.append(f"edge {x['cls']} -> {typ}#{meth}")
    return "\n".join(L)
packA = "\n\n".join(block_A(x) for x in G) + "\n"

LEGEND = ("# WIRING PACK v1 - generator-data form\n"
"# 'motif NAME(slots): template' defines a wiring shape; template lines use $slots.\n"
"# 'inst NAME(fills)' instantiates it: expand the template with the fills.\n"
"# A following indented '+ line' is a DELTA: after expansion, add that line verbatim.\n"
"# Expansion of every inst reproduces the explicit form exactly.\n")
MOTIF = ("motif CommandHandler(H, S, f, m, entity, action):\n"
"  unit $H\n"
"  anno $H @CommandType entity=$entity action=$action\n"
"  dep $H.$f: $S\n"
"  edge $H -> $S#$m\n")

def row_B(x):
    """Convention: exactly 1 dep and 1 edge on that dep -> pure inst row.
       Deviations -> inst on the first dep/edge + delta lines (R5 discipline)."""
    fld, typ = sorted(x["deps"].items())[0]
    prim = next(((t, m) for (t, m) in x["edges"] if t == typ), x["edges"][0] if x["edges"] else (typ, "UNKNOWN"))
    row = f"inst CommandHandler({x['cls']}, {prim[0]}, {fld}, {prim[1]}, {x['entity'] or '-'}, {x['action'] or '-'})"
    deltas = []
    for f2, t2 in sorted(x["deps"].items()):
        if f2 != fld: deltas.append(f"  + dep {x['cls']}.{f2}: {t2}")
    for t2, m2 in x["edges"]:
        if (t2, m2) != prim: deltas.append(f"  + edge {x['cls']} -> {t2}#{m2}")
    return row + ("\n" + "\n".join(deltas) if deltas else "")

def expand_row(text):
    lines = text.split("\n")
    m = re.match(r'inst CommandHandler\((\w+), (\w+), (\w+), (\w+), ([\w.-]+), ([\w.-]+)\)', lines[0])
    H, S, f, meth, ent, act = m.groups()
    L = [f"unit {H}"]
    if ent != "-": L.append(f"anno {H} @CommandType entity={ent} action={act}")
    L += [f"dep {H}.{f}: {S}", f"edge {H} -> {S}#{meth}"]
    extra_deps, extra_edges = [], []
    for d in lines[1:]:
        d = d.strip()[2:]
        (extra_deps if d.startswith("dep") else extra_edges).append(d)
    # reproduce block_A ordering: unit, [anno], all deps sorted by field, then edges sorted
    unit = L[0]
    anno = [l for l in L[1:] if l.startswith("anno")]
    base_dep = [l for l in L[1:] if l.startswith("dep")]
    base_edge = [l for l in L[1:] if l.startswith("edge")]
    deps = sorted(base_dep + extra_deps, key=lambda s: s.split(":")[0])
    edges = sorted(base_edge + extra_edges)
    return "\n".join([unit] + anno + deps + edges)

rows = [row_B(x) for x in G]
packB = LEGEND + "\n" + MOTIF + "\n" + "\n".join(rows) + "\n"
reexp = "\n\n".join(expand_row(r) for r in rows) + "\n"
GATE = (reexp == packA)

def block_C(x):
    L = [f"unit {x['cls']}"]
    for fld, typ in sorted(x["deps"].items()): L.append(f"dep {x['cls']}.{fld}: {typ}")
    return "\n".join(L)
packC = "\n\n".join(block_C(x) for x in G) + "\n"

# ---------- questions (graph-only templates) ----------
import random
rnd = random.Random(20260916)
Q, GOLD, QTYPE = [], [], []
def add(q, a, t): Q.append(q); GOLD.append(a); QTYPE.append(t)
sample = rnd.sample(G, len(G))
# T2: method called (wiring-only) x8
for x in sample[:8]:
    prim = row_B(x).split("\n")[0]
    meth = re.match(r'inst CommandHandler\(\w+, \w+, \w+, (\w+),', prim).group(1)
    add(f"Which method does {x['cls']} invoke on its injected service?", meth, "T2-method")
# T3: entity/action -> handler (wiring-only) x6 — annotated handlers only
annotated = [x for x in sample[8:] if x["entity"]]
for x in annotated[:6]:
    add(f"Which handler class handles entity={x['entity']} action={x['action']}?", x["cls"], "T3-route")
# T4: fan-in counts x3
from collections import Counter
svc_count = Counter(t for x in G for (t, m) in x["edges"])
top = [s for s, c in svc_count.most_common(3)]
for s in top:
    add(f"How many handlers in the pack call methods on {s}? Answer with a number.", str(svc_count[s]), "T4-count")
# T1: dep type (answerable from interface-only — arm-C audit probes) x4
for x in sample[14:18]:
    typ = sorted(x["deps"].items())[0][1]
    add(f"What is the type of the service injected into {x['cls']}?", typ, "T1-deptype")
# Delta questions (natural deviants from the 1-dep/1-edge convention) x4
devs = [x for x in G if len(x["deps"]) > 1 or len(x["edges"]) > 1]
add("Which handler classes have MORE than one injected dependency? List class names, comma-separated; answer 'none' if none.",
    ",".join(sorted(x["cls"] for x in G if len(x["deps"]) > 1)) or "none", "T5-delta")
add("Which handler classes invoke MORE than one distinct Type#method target? List class names, comma-separated; answer 'none' if none.",
    ",".join(sorted(x["cls"] for x in G if len(x["edges"]) > 1)) or "none", "T5-delta")
if devs:
    d = devs[0]
    add(f"List every Type#method target that {d['cls']} invokes, comma-separated.",
        ",".join(f"{t}#{m}" for t, m in d["edges"]), "T5-delta")
    d2 = devs[-1]
    add(f"How many injected dependencies does {d2['cls']} have? Answer with a number.",
        str(len(d2["deps"])), "T5-delta")

manifest = {"n_handlers": len(G), "n_questions": len(Q), "gate_byte_identical": GATE,
            "deviants": sorted(x["cls"] for x in devs),
            "sha256": {"packA": hashlib.sha256(packA.encode()).hexdigest(),
                       "packB": hashlib.sha256(packB.encode()).hexdigest(),
                       "packC": hashlib.sha256(packC.encode()).hexdigest(),
                       "questions": hashlib.sha256(json.dumps(Q).encode()).hexdigest()}}
for name, txt in [("packA.txt", packA), ("packB.txt", packB), ("packC.txt", packC)]:
    open(os.path.join(HERE, name), "w").write(txt)
json.dump({"questions": Q, "gold": GOLD, "qtype": QTYPE}, open(os.path.join(HERE, "questions.json"), "w"), indent=1)
json.dump(manifest, open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
# token counts
tok = json.loads(subprocess.run(["node", os.path.join(HERE, "..", "e2-tokens", "tokcount.js")],
      input=json.dumps({"A": packA, "B": packB, "C": packC}), capture_output=True, text=True, check=True).stdout)
manifest["tokens"] = tok
json.dump(manifest, open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
print(json.dumps(manifest, indent=1))
