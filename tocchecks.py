#!/usr/bin/env python3
"""Generic sanity checks on TOC structures of a tagged PDF.

Usage: tocchecks.py file.pdf ...

Exit status: 0 if no defect, 1 if some defect (flags marked * below),
2 for a usage error, 3 if pikepdf is not available.

Structure types are compared after resolution through the role maps, so the
checks do not depend on the names chosen by LaTeX (toc, toc-item, text-block,
...).  Reported names are given as  name  or  name->Standard.

* BODY   a top-level TOC contains headings or sectioning (H, Hn, Sect,
         Title); not Part, the target of semantic-para
  EMPTY  a TOC without any TOCI descendant; not a defect for a list with
         no displayed entry (the kernel does the same)
* KID    a child of a TOC that is neither TOC nor TOCI
* MCKID  marked content (MCID) directly inside a TOC
* PAR    a TOCI whose parent is not a TOC
  PARA   a TOCI containing a paragraph (P); allowed by PDF 2.0, but the
         kernel does not produce it
* DUPMC  a marked content (page, MCID) referenced by several structure
         elements (or several times by one)
  TOCS   number of top-level TOC structures, i.e. not nested in another
         TOC (always printed; not a defect)
  NOTAGGED  the PDF has no structure tree (not a defect)

Parent-child legality itself is checked by tagpdf, not here.
"""
import collections
import re
import sys

try:
    import pikepdf
except ImportError:
    pikepdf = None

DEFECTS = ("BODY", "KID", "MCKID", "PAR", "DUPMC")

STD_NS = {"http://iso.org/pdf2/ssn", "http://iso.org/pdf/ssn",
          "http://www.w3.org/1998/Math/MathML"}
HEADING_RE = re.compile(r"H\d*|Sect|Title")


def resolve_role(name, ns, root_rolemap):
    """Standard type of (name, namespace dict) through the role maps."""
    seen = set()
    while True:
        uri = str(ns.NS) if ns is not None and "/NS" in ns else None
        if (name, uri) in seen or uri in STD_NS:
            return name
        seen.add((name, uri))
        key = "/" + name
        if ns is not None:
            rm = ns.get("/RoleMapNS")
            if rm is None or key not in rm:
                return name
            tgt = rm[key]
            if isinstance(tgt, pikepdf.Array):
                name, ns = str(tgt[0])[1:], tgt[1]
            else:
                return str(tgt)[1:]
        else:
            if root_rolemap is None or key not in root_rolemap:
                return name
            name = str(root_rolemap[key])[1:]


def duplicate_mcids(pdf, root):
    """(page number, MCID) pairs referenced more than once."""
    pages = {p.obj.objgen: i + 1 for i, p in enumerate(pdf.pages)}
    count = collections.Counter()
    seen = set()

    def walk(e, page):
        if isinstance(e, pikepdf.Dictionary):
            if e.get("/Type") == "/MCR":
                if "/Stm" not in e:
                    pg = pages.get(e.Pg.objgen) if "/Pg" in e else page
                    count[(pg, int(e.MCID))] += 1
                return
            if e.get("/Type") == "/OBJR":
                return
            if e.is_indirect:
                if e.objgen in seen:
                    return
                seen.add(e.objgen)
            if "/Pg" in e:
                page = pages.get(e.Pg.objgen)
            for k in raw_kids(e):
                walk(k, page)
        elif is_mc(e):
            count[(page, int(e))] += 1

    walk(root, None)
    return sorted(k for k, v in count.items() if v > 1)


def is_mc(x):
    if isinstance(x, int):
        return True
    if isinstance(x, pikepdf.Object) and x._type_code == pikepdf.ObjectType.integer:
        return True
    return isinstance(x, pikepdf.Dictionary) and x.get("/Type") == "/MCR"


def raw_kids(elem):
    k = elem.get("/K")
    if k is None:
        return []
    return list(k) if isinstance(k, pikepdf.Array) else [k]


def kids(elem):
    return [x for x in raw_kids(elem)
            if isinstance(x, pikepdf.Dictionary) and "/S" in x]


def check(path):
    pdf = pikepdf.open(path)
    root = pdf.Root.get("/StructTreeRoot")
    if root is None:
        return ["NOTAGGED"]
    rolemap = root.get("/RoleMap")
    std_cache = {}

    def std(e):
        if "/S" not in e:
            return "StructTreeRoot"
        key = e.objgen if e.is_indirect else id(e)
        if key not in std_cache:
            std_cache[key] = resolve_role(str(e.S)[1:], e.get("/NS"), rolemap)
        return std_cache[key]

    def label(e):
        if "/S" not in e:
            return "StructTreeRoot"
        n, s = str(e.S)[1:], std(e)
        return n if n == s else f"{n}->{s}"

    def title(e):
        return str(e["/T"]) if "/T" in e else ""

    def descendants(e, seen):
        for k in kids(e):
            if k.is_indirect:
                if k.objgen in seen:
                    continue
                seen.add(k.objgen)
            yield k
            yield from descendants(k, seen)

    msgs = []
    toplevel = 0
    visited = set()

    def visit(e, parent, in_toc):
        nonlocal toplevel
        if e.is_indirect:
            if e.objgen in visited:
                return
            visited.add(e.objgen)
        s = std(e)
        where = f"T={title(e)!r} under <{label(parent)}>"
        if s == "TOC":
            if not in_toc:
                toplevel += 1
                body = sorted({label(d) for d in descendants(e, set())
                               if HEADING_RE.fullmatch(std(d))})
                if body:
                    msgs.append(f"BODY  TOC {where} contains {', '.join(body)}")
            if not any(std(d) == "TOCI" for d in descendants(e, set())):
                msgs.append(f"EMPTY TOC {where}")
            for k in raw_kids(e):
                if is_mc(k):
                    msgs.append(f"MCKID marked content child of TOC {where}")
                elif isinstance(k, pikepdf.Dictionary) and "/S" in k \
                        and std(k) not in ("TOC", "TOCI"):
                    msgs.append(f"KID   <{label(k)}> child of TOC {where}")
        elif s == "TOCI":
            if std(parent) != "TOC":
                msgs.append(f"PAR   TOCI {where}")
            paras = sorted({label(d) for d in descendants(e, set())
                            if std(d) == "P"})
            if paras:
                msgs.append(f"PARA  TOCI {where} contains {', '.join(paras)}")
        for k in kids(e):
            visit(k, e, in_toc or s == "TOC")

    for k in kids(root):
        visit(k, root, False)
    dups = duplicate_mcids(pdf, root)
    if dups:
        shown = ", ".join(f"p{p} MCID {m}" for p, m in dups[:10])
        more = f" (and {len(dups) - 10} more)" if len(dups) > 10 else ""
        msgs.append(f"DUPMC {len(dups)} marked content(s) referenced more than"
                    f" once: {shown}{more}")
    msgs.append(f"TOCS  {toplevel} top-level TOC structure(s)")
    return msgs


def main(paths):
    if not paths:
        print(__doc__)
        return 2
    if pikepdf is None:
        print("tocchecks.py: pikepdf is not available")
        return 3
    status = 0
    for p in paths:
        print(f"=== {p}")
        for m in check(p):
            print("  " + m)
            if m.split()[0] in DEFECTS:
                status = 1
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
