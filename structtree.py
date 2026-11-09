#!/usr/bin/env python3
"""Print the structure tree of a tagged PDF, with the text of each MCID.

Usage: structtree.py file.pdf [--no-text] [--no-role]

Each element is printed as
    <name> [namespace] -> Standard   /T=... /Alt=...
where "-> Standard" is the standard type obtained through the role maps
(/RoleMapNS of PDF 2.0 namespaces, /RoleMap of the StructTreeRoot); it is
omitted when equal to the name or with --no-role.

Text is decoded byte-wise (latin-1), which is enough for T1/OT1 ASCII text.
A space is inserted for a TJ kern below -200 and for each text positioning
operator (Td, TD, T*, Tm) or new BT after some text.
"""
import sys
import pikepdf

STD_NS = {
    "http://iso.org/pdf2/ssn": "pdf2",
    "http://iso.org/pdf/ssn": "pdf",
    "http://www.w3.org/1998/Math/MathML": "mathml",
}


def ns_short(uri):
    if uri is None:
        return ""
    return STD_NS.get(uri) or uri.rstrip("/").rsplit("/", 1)[-1]


def resolve_role(name, ns, root_rolemap):
    """Follow the role maps from (name, namespace dict) to a standard type.

    Returns (standard name, namespace uri); the uri is None for elements
    without namespace mapped through the PDF 1.7 /RoleMap.
    """
    seen = set()
    while True:
        uri = str(ns.NS) if ns is not None and "/NS" in ns else None
        if (name, uri) in seen:          # cycle in the role map
            return name, uri
        seen.add((name, uri))
        if uri in STD_NS:
            return name, uri
        key = "/" + name
        if ns is not None:
            rm = ns.get("/RoleMapNS")
            if rm is None or key not in rm:
                return name, uri         # unmapped non-standard name
            tgt = rm[key]
            if isinstance(tgt, pikepdf.Array):
                name, ns = str(tgt[0])[1:], tgt[1]
            else:                        # a bare name: PDF 1.7 standard type
                name, ns = str(tgt)[1:], None
                return name, None
        else:
            if root_rolemap is None or key not in root_rolemap:
                return name, None
            name = str(root_rolemap[key])[1:]


def page_mcid_text(pdf):
    """Map (page objgen, mcid) -> text shown inside that marked content."""
    result = {}
    for page in pdf.pages:
        key = page.obj.objgen
        stack = []  # list of mcid or None, one per open BDC/BMC
        for operands, op in pikepdf.parse_content_stream(page):
            name = str(op)
            if name in ("BDC", "BMC"):
                mcid = None
                if name == "BDC" and len(operands) == 2:
                    props = operands[1]
                    if isinstance(props, pikepdf.Dictionary) and "/MCID" in props:
                        mcid = int(props.MCID)
                stack.append(mcid)
                if mcid is not None:
                    result.setdefault((key, mcid), "")
                continue
            if name == "EMC":
                if stack:
                    stack.pop()
                continue
            cur = next((m for m in reversed(stack) if m is not None), None)
            if cur is None:
                continue
            if name in ("Td", "TD", "T*", "Tm", "BT"):
                txt = result[(key, cur)]
                if txt and not txt.endswith(" "):
                    result[(key, cur)] = txt + " "
            elif name in ("Tj", "TJ", "'", '"'):
                arg = operands[-1]
                parts = []
                if isinstance(arg, pikepdf.Array):
                    for x in arg:
                        if isinstance(x, pikepdf.String):
                            parts.append(bytes(x).decode("latin-1"))
                        elif float(x) < -200:
                            parts.append(" ")
                else:
                    parts.append(bytes(arg).decode("latin-1"))
                result[(key, cur)] += "".join(parts)
    return result


class Walker:
    def __init__(self, pdf, show_text, show_role):
        self.root = pdf.Root.StructTreeRoot
        self.rolemap = self.root.get("/RoleMap")
        self.texts = page_mcid_text(pdf) if show_text else {}
        self.show_text = show_text
        self.show_role = show_role
        self.out = []
        self.seen = set()

    def mcid_line(self, ind, mcid, page):
        txt = self.texts.get((page, mcid), "?") if page else "?"
        self.out.append(ind + f"MCID {mcid}"
                        + (f" {txt.strip()!r}" if self.show_text else ""))

    def walk(self, elem, depth, page):
        ind = "  " * depth
        if isinstance(elem, int) or (isinstance(elem, pikepdf.Object)
                                     and elem._type_code == pikepdf.ObjectType.integer):
            self.mcid_line(ind, int(elem), page)
            return
        if not isinstance(elem, pikepdf.Dictionary):
            return
        typ = elem.get("/Type")
        if typ == "/MCR":
            pg = elem.Pg.objgen if "/Pg" in elem else page
            if "/Stm" in elem:
                self.out.append(ind + f"MCID {int(elem.MCID)} (in XObject)")
            else:
                self.mcid_line(ind, int(elem.MCID), pg)
            return
        if typ == "/OBJR":
            self.out.append(ind + f"OBJR {elem.Obj.get('/Subtype')}")
            return
        s = elem.get("/S")
        if s is None:
            return
        if elem.is_indirect:
            if elem.objgen in self.seen:
                self.out.append(ind + f"<{str(s)[1:]}> (cycle!)")
                return
            self.seen.add(elem.objgen)
        if "/Pg" in elem:
            page = elem.Pg.objgen
        name = str(s)[1:]
        ns = elem.get("/NS")
        line = ind + f"<{name}>"
        uri = str(ns.NS) if ns is not None and "/NS" in ns else None
        if uri is not None:
            line += f" [{ns_short(uri)}]"
        if self.show_role:
            std, _ = resolve_role(name, ns, self.rolemap)
            if std != name:
                line += f" -> {std}"
        for key in ("/T", "/Alt", "/ActualText", "/E", "/Lang"):
            if key in elem:
                line += f" {key}={str(elem[key])!r}"
        self.out.append(line)
        kids = elem.get("/K")
        if kids is None:
            return
        for k in (kids if isinstance(kids, pikepdf.Array) else [kids]):
            self.walk(k, depth + 1, page)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    pdf = pikepdf.open(args[0])
    if "/StructTreeRoot" not in pdf.Root:
        print("No StructTreeRoot: PDF is not tagged")
        return 1
    w = Walker(pdf, "--no-text" not in argv, "--no-role" not in argv)
    kids = w.root.get("/K")
    if kids is not None:
        for k in (kids if isinstance(kids, pikepdf.Array) else [kids]):
            w.walk(k, 0, None)
    print("\n".join(w.out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
