"""Shared knowledge for the E2/E3/E5 experiments: how Fineract wiring is read from
source, how a unit is serialized (explicit form A / factored motif row), how a row
re-expands, and how model answers are normalized for grading.

One home for each rule. The pack LEGEND texts stay in the build scripts on purpose:
they are frozen, hash-pinned experimental artifacts at different versions (v1 / v2.1),
and the E5 lesson is precisely that the legend text is part of the experiment.
"""
import json, os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
TOKCOUNT = os.path.join(HERE, "e2-tokens", "tokcount.js")

# ---------- extraction: Java source -> unit record ----------
_CLASS = re.compile(r'public class (\w+)')
_DEP = re.compile(r'private final ([A-Z][\w<>,. ]*?)\s+(\w+);')          # constructor-injected field
_CALL = re.compile(r'(?:this\.)?(\w+)\.(\w+)\(')                          # field.method(
_ANNO = re.compile(r'@CommandType\(entity = "?([\w.-]+)"?, action = "?([\w.-]+)"?\)')
_IMPL = re.compile(r'public class \w+[\s\S]{0,200}?implements ([\w, \n]+)\{')

def extract(src):
    """Unit record: class name, @CommandType entity/action (or None), injected deps
    {field: Type}, and sorted call edges [(Type, method)] restricted to those deps."""
    cls = _CLASS.search(src).group(1)
    ann = _ANNO.search(src)
    deps = {m.group(2): m.group(1).split('<')[0].strip() for m in _DEP.finditer(src)}
    edges = sorted({(deps[m.group(1)], m.group(2)) for m in _CALL.finditer(src) if m.group(1) in deps})
    return {"cls": cls, "entity": ann.group(1) if ann else None,
            "action": ann.group(2) if ann else None, "deps": deps, "edges": edges}

def impl_of(src, cls):
    """Interface this class is the declared implementation of (E5 'impl I -> C' lines):
    the implemented interface whose name is the class name minus its Impl suffix."""
    im = _IMPL.search(src)
    if not im: return None
    base = cls.replace("JpaRepositoryImpl", "").replace("Impl", "")
    for c in (c.strip() for c in im.group(1).split(",")):
        if c == base or c.startswith(base): return c
    return None

# ---------- serialization ----------
def block_A(x):
    """Explicit form: unit / [anno] / [impl] / deps sorted by field / edges sorted."""
    L = [f"unit {x['cls']}"]
    if x.get("entity"): L.append(f"anno {x['cls']} @CommandType entity={x['entity']} action={x['action']}")
    if x.get("impl_of"): L.append(f"impl {x['impl_of']} -> {x['cls']}")
    for fld, typ in sorted(x["deps"].items()): L.append(f"dep {x['cls']}.{fld}: {typ}")
    for typ, meth in x["edges"]: L.append(f"edge {x['cls']} -> {typ}#{meth}")
    return "\n".join(L)

MOTIF = ("motif CommandHandler(H, S, f, m, entity, action):\n"
"  unit $H\n"
"  anno $H @CommandType entity=$entity action=$action\n"
"  dep $H.$f: $S\n"
"  edge $H -> $S#$m\n")

def row_B(x):
    """Factored form. Convention (exactly 1 dep, 1 edge on it) -> a pure inst row.
    Deviations -> inst on the first dep + its primary edge, then '+ line' deltas (R5).
    A '-' fill means the anno line is omitted on expansion."""
    fld, typ = sorted(x["deps"].items())[0]
    prim = next(((t, m) for (t, m) in x["edges"] if t == typ), x["edges"][0])
    row = f"inst CommandHandler({x['cls']}, {prim[0]}, {fld}, {prim[1]}, {x['entity'] or '-'}, {x['action'] or '-'})"
    deltas = [f"  + dep {x['cls']}.{f2}: {t2}" for f2, t2 in sorted(x["deps"].items()) if f2 != fld]
    deltas += [f"  + edge {x['cls']} -> {t2}#{m2}" for t2, m2 in x["edges"] if (t2, m2) != prim]
    return row + ("\n" + "\n".join(deltas) if deltas else "")

_INST = re.compile(r'inst CommandHandler\((\w+), (\w+), (\w+), (\w+), ([\w.-]+), ([\w.-]+)\)')

def expand_row(text):
    """Mechanical re-expansion of a row_B() row to block_A() text. The byte-identical
    gate in every build script is `expand_row(row_B(x)) == block_A(x)`."""
    lines = text.split("\n")
    H, S, f, meth, ent, act = _INST.match(lines[0]).groups()
    anno = [f"anno {H} @CommandType entity={ent} action={act}"] if ent != "-" else []
    deps, edges = [f"dep {H}.{f}: {S}"], [f"edge {H} -> {S}#{meth}"]
    for d in (l.strip()[2:] for l in lines[1:]):
        (deps if d.startswith("dep") else edges).append(d)
    deps = sorted(deps, key=lambda s: s.split(":")[0])
    return "\n".join([f"unit {H}"] + anno + deps + sorted(edges))

def count_tokens(texts):
    """{name: text} -> {name: cl100k_base token count}, via the vendored node tiktoken."""
    out = subprocess.run(["node", TOKCOUNT], input=json.dumps(texts),
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)

# ---------- grading ----------
def norm(s): return re.sub(r'\s+', '', s.strip().lower())

def eq(answer, gold):
    """Exact normalized match; comma lists compare as sets (order-insensitive)."""
    if norm(answer) == norm(gold): return True
    if "," in gold or "," in answer:
        return set(filter(None, map(norm, answer.split(",")))) == set(filter(None, map(norm, gold.split(","))))
    return False

def parse_answers(path):
    """Model output 'Q<n>: ...' / 'S<n>: ...' lines -> ({n: answer}, {n: sub-answer})."""
    Q, S = {}, {}
    for line in open(path):
        m = re.match(r'([QS])(\d+):\s*(.*)', line.strip())
        if m: (Q if m.group(1) == "Q" else S)[int(m.group(2))] = m.group(3).strip()
    return Q, S
