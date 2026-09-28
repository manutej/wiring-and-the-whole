#!/usr/bin/env python3
"""
E3 build — extract graph from 30 real Fineract handlers; emit packs A/B/C, questions, gold.
Firewall discipline: questions are generated ONLY from graph.json via templates below;
pack layout code never informs question selection. Frozen via SHA-256 before any model call.
"""
import re, os, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from wiring import extract, block_A, MOTIF, row_B, expand_row, count_tokens
files = sorted(os.listdir(os.path.join(HERE, "raw")))

# ---------- extract ----------
G = [extract(open(os.path.join(HERE, "raw", f)).read()) for f in files]
G.sort(key=lambda x: x["cls"])
json.dump(G, open(os.path.join(HERE, "graph.json"), "w"), indent=1)

# ---------- packs ----------
packA = "\n\n".join(block_A(x) for x in G) + "\n"

LEGEND = ("# WIRING PACK v1 - generator-data form\n"
"# 'motif NAME(slots): template' defines a wiring shape; template lines use $slots.\n"
"# 'inst NAME(fills)' instantiates it: expand the template with the fills.\n"
"# A following indented '+ line' is a DELTA: after expansion, add that line verbatim.\n"
"# Expansion of every inst reproduces the explicit form exactly.\n")
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
tok = count_tokens({"A": packA, "B": packB, "C": packC})
manifest["tokens"] = tok
json.dump(manifest, open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
print(json.dumps(manifest, indent=1))
