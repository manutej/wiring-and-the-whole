#!/usr/bin/env python3
"""
E5 build — depth-graded operadic evaluation at scale.
120 questions = 12 x 10 depth levels, every gold computed by a deterministic solver over the
merged wiring graph (30 real Fineract handlers + 8 service impls + 2 repository wrappers).
Operadic interview: 12 deep questions (D5/D6/D9/D10 x 3) carry decomposition trees — the
evaluator answers the direct question AND its sub-questions; the grader checks OC consistency
(composed sub-answers vs direct) alongside correctness [meta-operad TREE/COMPOSE/COLLAPSE/CHECK].
Packs A (explicit) and B (factored) gated byte-identical on re-expansion. Frozen via SHA-256.
"""
import re, os, json, hashlib, subprocess, random
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
E3 = os.path.join(HERE, "..", "e3-ablation")
rnd = random.Random(20260919)

# ---------------- extract new units (impls + wrappers), same regexes as E3 ----------------
def extract(path, fname):
    src = open(path).read()
    cls = re.search(r'public class (\w+)', src).group(1)
    deps = {}
    for m in re.finditer(r'private final ([A-Z][\w<>,. ]*?)\s+(\w+);', src):
        deps[m.group(2)] = m.group(1).split('<')[0].strip()
    edges = sorted({(deps[m.group(1)], m.group(2))
                    for m in re.finditer(r'(?:this\.)?(\w+)\.(\w+)\(', src) if m.group(1) in deps})
    impl_of = None
    im = re.search(r'public class \w+[\s\S]{0,200}?implements ([\w, \n]+)\{', src)
    if im:
        cands = [c.strip() for c in im.group(1).split(",")]
        base = cls.replace("JpaRepositoryImpl", "").replace("Impl", "")
        for c in cands:
            if c == base or c.startswith(base): impl_of = c; break
    return {"cls": cls, "deps": deps, "edges": edges, "impl_of": impl_of, "kind": "unit"}

H = json.load(open(os.path.join(E3, "graph.json")))
for x in H: x["kind"] = "handler"
NEW = [extract(os.path.join(HERE, "raw", f), f) for f in sorted(os.listdir(os.path.join(HERE, "raw")))]
G = H + NEW
byname = {x["cls"]: x for x in G}
impl_map = {x["impl_of"]: x["cls"] for x in NEW if x.get("impl_of")}   # iface -> impl class

# graph relations
handlers = [x for x in G if x["kind"] == "handler"]
def repo_calls(unit):   # *Repository* typed call targets of a unit
    return sorted({t for t, m in unit["edges"] if "Repository" in t})
def primary_service(x):  # the service iface a handler calls (first edge on first dep)
    return x["edges"][0][0] if x["edges"] else None

# ---------------- questions: 12 per depth, solver-backed ----------------
Q, GOLD, DEPTH, OCSUB = [], [], [], []   # OCSUB[i] = list of (subq, subgold) or []
def add(q, gold, d, subs=None):
    Q.append(q); GOLD.append(gold); DEPTH.append(d); OCSUB.append(subs or [])

annotated = [x for x in handlers if x["entity"]]
shuf = handlers[:]; rnd.shuffle(shuf)

# D1 — direct edge lookup (12)
for x in shuf[:12]:
    t, m = x["edges"][0]
    add(f"D1: Which method does {x['cls']} invoke on {t}?", m, 1)
# D2 — reverse routing (12)
ann = annotated[:]; rnd.shuffle(ann)
for x in ann[:12]:
    add(f"D2: Which handler class handles entity={x['entity']} action={x['action']}?", x["cls"], 2)
# D3 — fan-out enumeration (12): units with 2..8 edges (deviant handlers + wrappers + small impls)
fanout_units = [x for x in G if 2 <= len(x["edges"]) <= 8]
rnd.shuffle(fanout_units)
for x in fanout_units[:12]:
    add(f"D3: List every Type#method target that {x['cls']} invokes, comma-separated.",
        ",".join(f"{t}#{m}" for t, m in x["edges"]), 3)
# D4 — fan-in enumeration (12): which HANDLER classes call type T
svc_counts = Counter(t for x in handlers for t, m in x["edges"])
popular = [s for s, c in svc_counts.most_common(12)]
for s in popular[:12]:
    callers = sorted(x["cls"] for x in handlers if any(t == s for t, m in x["edges"]))
    add(f"D4: Which handler classes invoke methods on {s}? List class names, comma-separated.",
        ",".join(callers), 4)
# D5 — 2-hop via implementation (12): H -> iface -> impl -> repository types
d5pool = [x for x in handlers if primary_service(x) in impl_map
          and 1 <= len(repo_calls(byname[impl_map[primary_service(x)]])) <= 10]
rnd.shuffle(d5pool)
for i, x in enumerate(d5pool[:12]):
    s = primary_service(x); imp = impl_map[s]
    gold = ",".join(repo_calls(byname[imp]))
    subs = None
    if i < 3:
        subs = [(f"OC-a: Which service type does {x['cls']} invoke?", s),
                (f"OC-b: Which class is declared as the implementation of {s}?", imp),
                (f"OC-c: List the *Repository* types that {imp} invokes, comma-separated.", gold)]
    add(f"D5: {x['cls']} delegates to a service; via that service's declared implementation, "
        f"list the *Repository* types the implementation invokes, comma-separated. "
        f"(*Repository* = type name CONTAINS 'Repository', which INCLUDES *RepositoryWrapper types.)", gold, 5, subs)
# D6 — 3-hop through a wrapper (12): H -> iface -> impl -> Wrapper -> its repository types
wrappers = [x["cls"] for x in NEW if x["cls"].endswith("RepositoryWrapper")]
d6pool = []
for x in handlers:
    s = primary_service(x)
    if s in impl_map:
        imp = byname[impl_map[s]]
        wr = [t for t, m in imp["edges"] if t in wrappers or t.endswith("RepositoryWrapper")]
        wr_present = [w for w in wr if w in byname]
        if wr_present: d6pool.append((x, s, imp["cls"], wr_present[0]))
rnd.shuffle(d6pool)
for i, (x, s, imp, w) in enumerate(d6pool[:12]):
    gold = ",".join(repo_calls(byname[w]))
    subs = None
    if i < 3:
        subs = [(f"OC-a: Which service type does {x['cls']} invoke?", s),
                (f"OC-b: Which class implements {s}?", imp),
                (f"OC-c: Which *RepositoryWrapper* type does {imp} invoke?", w),
                (f"OC-d: List the *Repository* types {w} invokes, comma-separated.", gold)]
    add(f"D6: Starting from {x['cls']}, follow: its service, that service's implementation, "
        f"the *RepositoryWrapper* the implementation invokes. List the *Repository* types that "
        f"wrapper invokes, comma-separated.", gold, 6, subs)
# pad D6 to 12 with wrapper-direct questions if pool short
i6 = sum(1 for d in DEPTH if d == 6)
for w in wrappers * 6:
    if i6 >= 12: break
    wu = byname[w]
    nonrepo = sorted({f"{t}#{m}" for t, m in wu["edges"] if "Repository" not in t})
    add(f"D6: Which call targets of {w} are NOT *Repository*-typed? List Type#method, comma-separated; 'none' if none.",
        ",".join(nonrepo) or "none", 6); i6 += 1
# D7 — orbit shape (12)
def shape(x): return (len(x["deps"]), len(x["edges"]), bool(x["entity"]))
shapes = defaultdict(list)
for x in handlers: shapes[shape(x)].append(x["cls"])
d7pool = [x for x in handlers if len(shapes[shape(x)]) >= 2]
rnd.shuffle(d7pool)
for x in d7pool[:12]:
    others = sorted(c for c in shapes[shape(x)] if c != x["cls"])
    add(f"D7: Which handler classes have exactly the same wiring shape as {x['cls']} "
        f"(same number of deps, same number of call targets, annotation present or absent alike)? "
        f"List class names excluding {x['cls']}, comma-separated.", ",".join(others), 7)
# D8 — delta/deviation (12)
devs = sorted(x["cls"] for x in handlers if len(x["deps"]) > 1 or len(x["edges"]) > 1)
noann = sorted(x["cls"] for x in handlers if not x["entity"])
d8qs = [
 ("D8: Which handler classes deviate from the one-dep/one-call convention? List, comma-separated.", ",".join(devs)),
 ("D8: Which handler classes carry NO @CommandType annotation? List, comma-separated; 'none' if none.", ",".join(noann) or "none"),
]
for x in [byname[c] for c in devs][:5]:
    d8qs.append((f"D8: How many injected dependencies does {x['cls']} have? Answer with a number.", str(len(x["deps"]))))
    d8qs.append((f"D8: How many distinct Type#method targets does {x['cls']} invoke? Answer with a number.", str(len(x["edges"]))))
for q, g in d8qs[:12]: add(q, g, 8)
# D9 — counterfactual removal (12): remove service iface T -> which handlers lose ALL repository paths
d9svcs = [s for s in impl_map if repo_calls(byname[impl_map[s]]) and svc_counts.get(s, 0) >= 1]
rnd.shuffle(d9svcs)
for i, s in enumerate((d9svcs * 4)[:12]):
    affected = sorted(x["cls"] for x in handlers if primary_service(x) == s)
    subs = None
    if i < 3:
        subs = [(f"OC-a: Which handler classes invoke {s}? List, comma-separated.",
                 ",".join(sorted(x["cls"] for x in handlers if any(t == s for t, m in x["edges"])))),
                (f"OC-b: Does the implementation of {s} invoke at least one *Repository* type? yes/no.",
                 "yes")]
    add(f"D9: Suppose type {s} is removed from the system. Which handler classes lose their "
        f"delegation path to any *Repository* type (their primary service is {s})? List, comma-separated; 'none' if none.",
        ",".join(affected) or "none", 9, subs)
# D10 — multi-constraint + junction (12)
d10 = []
multi = sorted(s for s in impl_map
               if sum(1 for x in handlers if any(t == s for t, m in x["edges"])) >= 2
               and len(repo_calls(byname[impl_map[s]])) >= 2)
d10.append(("D10: Which service types are invoked by at least TWO handlers AND have a declared "
            "implementation that invokes at least TWO *Repository* types? List, comma-separated; 'none' if none.",
            ",".join(multi) or "none", [
              ("OC-a: Which service types are invoked by at least two handler classes? List, comma-separated.",
               ",".join(sorted(s for s in impl_map if sum(1 for x in handlers if any(t==s for t,m in x['edges'])) >= 2))),
              ("OC-b: Of the service types with declared implementations, which implementations invoke at "
               "least two *Repository* types? List the SERVICE type names, comma-separated.",
               ",".join(sorted(s for s in impl_map if len(repo_calls(byname[impl_map[s]])) >= 2)))]))
for s in list(impl_map)[:6]:
    imp = byname[impl_map[s]]
    junction = sorted(f"{t}#{m}" for t, m in imp["edges"] if t == s) or ["none"]
    # junction between iface consumers and impl: shared referenced ports = handler-called methods on s
    called = sorted({m for x in handlers for t, m in x["edges"] if t == s})
    d10.append((f"D10: Consider the units glued along {s}: list every method name that handlers "
                f"invoke on {s} (the shared junction ports), comma-separated; 'none' if none.",
                ",".join(called) or "none", None))
for x in (fanout_units * 2)[:5]:
    both = sorted({t for t, m in x["edges"]})
    d10.append((f"D10: List the distinct TYPES (not methods) that {x['cls']} invokes, comma-separated.",
                ",".join(both), None))
oc10 = 0
for q, g, subs in d10[:12]:
    if subs and oc10 < 3: add(q, g, 10, subs); oc10 += 1
    else: add(q, g, 10)

counts = Counter(DEPTH)
assert len(Q) >= 100, f"only {len(Q)} questions"

# ---------------- packs ----------------
def block_A(x):
    L = [f"unit {x['cls']}"]
    if x.get("entity"): L.append(f"anno {x['cls']} @CommandType entity={x['entity']} action={x['action']}")
    if x.get("impl_of"): L.append(f"impl {x['impl_of']} -> {x['cls']}")
    for fld, typ in sorted(x["deps"].items()): L.append(f"dep {x['cls']}.{fld}: {typ}")
    for typ, meth in x["edges"]: L.append(f"edge {x['cls']} -> {typ}#{meth}")
    return "\n".join(L)
ORDER = sorted(G, key=lambda x: x["cls"])
packA = "\n\n".join(block_A(x) for x in ORDER) + "\n"

LEGEND = ("# WIRING PACK v2.1 - generator-data form\n"
"# 'motif NAME(slots): template' defines a wiring shape; '$slot' substitutes fills.\n"
"# 'inst NAME(fills)' instantiates the template. An indented '+ line' is a DELTA: add it\n"
"# verbatim after expansion. 'impl I -> C' declares C as the implementation of interface I.\n"
"# A fill of '-' means the corresponding line is OMITTED from the expansion (e.g. entity=-\n"
"# and action=- mean the unit has NO anno line). Constants.* fills are literal values.\n"
"# Non-motif units appear explicitly (unit/dep/edge lines). Expansion of every inst\n"
"# reproduces the explicit form exactly.\n")
MOTIF = ("motif CommandHandler(H, S, f, m, entity, action):\n"
"  unit $H\n"
"  anno $H @CommandType entity=$entity action=$action\n"
"  dep $H.$f: $S\n"
"  edge $H -> $S#$m\n")

def row_B(x):
    fld, typ = sorted(x["deps"].items())[0]
    prim = next(((t, m) for (t, m) in x["edges"] if t == typ), x["edges"][0])
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
    Hc, S, f, meth, ent, act = m.groups()
    L = [f"unit {Hc}"]
    if ent != "-": L.append(f"anno {Hc} @CommandType entity={ent} action={act}")
    base_dep = [f"dep {Hc}.{f}: {S}"]; base_edge = [f"edge {Hc} -> {S}#{meth}"]
    extra_deps, extra_edges = [], []
    for d in lines[1:]:
        d = d.strip()[2:]
        (extra_deps if d.startswith("dep") else extra_edges).append(d)
    deps = sorted(base_dep + extra_deps, key=lambda s: s.split(":")[0])
    edges = sorted(base_edge + extra_edges)
    return "\n".join(L[:1] + [l for l in L[1:] if l.startswith("anno")] + deps + edges)

partsB, expA = [], []
for x in ORDER:
    if x["kind"] == "handler":
        r = row_B(x); partsB.append(r); expA.append(expand_row(r))
    else:
        b = block_A(x); partsB.append(b); expA.append(b)
packB = LEGEND + "\n" + MOTIF + "\n" + "\n\n".join(partsB) + "\n"
reexp = "\n\n".join(expA) + "\n"
GATE = (reexp == packA)

# ---------------- freeze + tokens ----------------
qs = {"questions": Q, "gold": GOLD, "depth": DEPTH,
      "oc": [[{"q": s[0], "gold": s[1]} for s in subs] for subs in OCSUB]}
json.dump(qs, open(os.path.join(HERE, "questions.json"), "w"), indent=1)
json.dump(G, open(os.path.join(HERE, "graph.json"), "w"), indent=1, default=list)
open(os.path.join(HERE, "packA.txt"), "w").write(packA)
open(os.path.join(HERE, "packB.txt"), "w").write(packB)
tok = json.loads(subprocess.run(["node", os.path.join(E3, "..", "e2-tokens", "tokcount.js")],
      input=json.dumps({"A": packA, "B": packB}), capture_output=True, text=True, check=True).stdout)
manifest = {"n_units": len(G), "n_handlers": len(handlers), "n_new_units": len(NEW),
            "n_questions": len(Q), "per_depth": dict(sorted(Counter(DEPTH).items())),
            "n_oc_trees": sum(1 for s in OCSUB if s), "n_oc_subquestions": sum(len(s) for s in OCSUB),
            "gate_byte_identical": GATE, "tokens": tok,
            "sha256": {"packA": hashlib.sha256(packA.encode()).hexdigest()[:16],
                       "packB": hashlib.sha256(packB.encode()).hexdigest()[:16],
                       "questions": hashlib.sha256(json.dumps(Q).encode()).hexdigest()[:16]}}
json.dump(manifest, open(os.path.join(HERE, "manifest.json"), "w"), indent=1)
print(json.dumps(manifest, indent=1))
