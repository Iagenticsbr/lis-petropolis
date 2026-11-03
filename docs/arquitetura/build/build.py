#!/usr/bin/env python3
"""Monta o PDF único do LIS: HTML -> Chromium -> sumário com páginas -> rodapés -> metadados."""
import io, os, re, subprocess, sys
from html import unescape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import figs  # noqa: E402

FIG_DIR = os.path.join(HERE, "figuras")
# por padrão, o PDF final vai para docs/arquitetura/ (pasta acima de build/)
OUT_DIR = os.environ.get("OUT_DIR", os.path.abspath(os.path.join(HERE, "..")))
OUT_NAME = "LIS-arquitetura-dados-e-motor-de-analise.pdf"
TITLE = "LIS · Arquitetura, dados e motor de análise"
FOOT = "LIS · Grupo Petrópolis · IAgentics"

FONTS = "fonts/node_modules/@fontsource"
LATIN = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,"
         "U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")
GREEK = "U+0370-0377,U+037A-037F,U+0384-038A,U+038C,U+038E-03A1,U+03A3-03FF"


def fontface():
    rows = []

    def add(fam, pkg, slug, weight, style, subset, rng):
        f = f"{FONTS}/{pkg}/files/{slug}-{subset}-{weight}-{style}.woff2"
        assert os.path.exists(os.path.join(HERE, f)), f
        rows.append(f'@font-face{{font-family:"{fam}";font-style:{style};font-weight:{weight};'
                    f'font-display:block;src:url({f}) format("woff2");unicode-range:{rng}}}')

    for w in (600, 700):
        add("Bricolage Grotesque", "bricolage-grotesque", "bricolage-grotesque", w, "normal", "latin", LATIN)
    for w in (400, 600, 700):
        for st in ("normal", "italic"):
            add("Source Sans 3", "source-sans-3", "source-sans-3", w, st, "latin", LATIN)
            add("Source Sans 3", "source-sans-3", "source-sans-3", w, st, "greek", GREEK)
    for w in (400, 500):
        add("JetBrains Mono", "jetbrains-mono", "jetbrains-mono", w, "normal", "latin", LATIN)
        add("JetBrains Mono", "jetbrains-mono", "jetbrains-mono", w, "normal", "greek", GREEK)
    return "\n".join(rows)


def load_figs():
    d = {f"FIG{i}": open(os.path.join(FIG_DIR, f"fig{i}.svg"), encoding="utf-8").read() for i in (1, 2, 3)}
    for k, f in figs.FIGS.items():
        d[k] = f()
    return d


def assemble(pages):
    head = open(os.path.join(HERE, "p0_head.html"), encoding="utf-8").read()
    body = "".join(open(os.path.join(HERE, f), encoding="utf-8").read()
                   for f in ("p1_a.html", "p2_b.html", "p3_c.html", "p4_d.html"))
    html = head.replace("{{FONTFACE}}", fontface()) + body
    for k, v in load_figs().items():
        assert "{{" + k + "}}" in html, k
        html = html.replace("{{" + k + "}}", v)

    def pg(m):
        return str(pages.get(m.group(1), "00"))

    html = re.sub(r"\{\{pg:([A-Za-z0-9_-]+)\}\}", pg, html)
    left = re.findall(r"\{\{[^}]*\}\}", html)
    assert not left, left
    return html


def render(html, pdf_path):
    from playwright.sync_api import sync_playwright
    src = os.path.join(HERE, "build.html")
    open(src, "w", encoding="utf-8").write(html)
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page()
        pg.goto("file://" + src)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(400)
        pg.pdf(path=pdf_path, prefer_css_page_size=True, print_background=True,
               outline=True, tagged=True, display_header_footer=False)
        br.close()


def heading_texts(html):
    """id do sumário -> texto do título correspondente."""
    out = {}
    for m in re.finditer(r'<(section|h1|h2|h3)\b([^>]*?)\bid="([^"]+)"([^>]*)>', html):
        tag, _, ident, _ = m.groups()
        if not re.fullmatch(r"s\d+(-\d+)?|sa(-[a-d])?", ident):
            continue
        rest = html[m.end():m.end() + 600]
        if tag in ("h1", "h2", "h3"):
            t = re.match(r"(.*?)</h\d>", html[m.end():m.end() + 600], re.S)
        else:
            t = re.search(r"<h[12][^>]*>(.*?)</h[12]>", rest, re.S)
        if t:
            txt = unescape(re.sub(r"<[^>]+>", "", t.group(1)))
            out[ident] = re.sub(r"\s+", " ", txt).strip()
    return out


def outline_pages(pdf_path):
    import pikepdf
    pdf = pikepdf.open(pdf_path)
    pages = {id(p.obj.objgen): i + 1 for i, p in enumerate(pdf.pages)}
    objgen = {p.obj.objgen: i + 1 for i, p in enumerate(pdf.pages)}
    res = {}

    def walk(items):
        for it in items:
            dest = it.destination
            if dest is None and it.action is not None:
                dest = it.action.get("/D")
            pg = None
            if dest is not None and len(dest) > 0:
                try:
                    pg = objgen.get(dest[0].objgen)
                except Exception:
                    pg = None
            t = re.sub(r"\s+", " ", str(it.title)).strip()
            h = len(t) // 2
            if len(t) % 2 == 0 and t[:h] == t[h:]:  # o Chromium duplica o título em alguns casos
                t = t[:h]
            res.setdefault(t, pg)
            walk(it.children)

    with pdf.open_outline() as ol:
        walk(ol.root)
    return res, len(pdf.pages)


def font_ttf(name, woff):
    from fontTools.ttLib import TTFont
    tmp = os.path.join(HERE, f"_{name}.ttf")
    f = TTFont(os.path.join(HERE, woff))
    f.flavor = None
    f.save(tmp)
    return tmp


def stamp(src, dst):
    import pikepdf
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont as RLFont
    pdfmetrics.registerFont(RLFont("SS", font_ttf("ss", f"{FONTS}/source-sans-3/files/source-sans-3-latin-400-normal.woff")))
    pdfmetrics.registerFont(RLFont("JB", font_ttf("jb", f"{FONTS}/jetbrains-mono/files/jetbrains-mono-latin-500-normal.woff")))
    pdf = pikepdf.open(src)
    n = len(pdf.pages)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, initialFontName="SS", initialFontSize=8)
    mm = 72 / 25.4
    for i, page in enumerate(pdf.pages):
        box = [float(x) for x in page.mediabox]
        w, h = box[2] - box[0], box[3] - box[1]
        c.setPageSize((w, h))
        if i > 0:
            landscape = w > h
            mx = (14 if landscape else 17) * mm
            y = (8.5 if landscape else 10.5) * mm
            c.setStrokeColorRGB(0.682, 0.733, 0.769)
            c.setLineWidth(0.5)
            c.line(mx, y + 11, w - mx, y + 11)
            c.setFillColorRGB(0.31, 0.37, 0.42)
            c.setFont("SS", 7.8)
            c.drawString(mx, y, FOOT)
            c.setFont("JB", 7.2)
            c.drawRightString(w - mx, y, f"{i + 1} / {n}")
        c.showPage()
    c.save()
    buf.seek(0)
    ov = pikepdf.open(buf)
    for i, page in enumerate(pdf.pages):
        pikepdf.Page(page).add_overlay(pikepdf.Page(ov.pages[i]))
    # títulos do índice (marcadores): o Chromium às vezes duplica o texto do título
    def fix(items):
        for it in items:
            t = re.sub(r"\s+", " ", str(it.title)).strip()
            h = len(t) // 2
            if len(t) % 2 == 0 and t[:h] == t[h:]:
                it.title = t[:h]
            elif t.startswith("5.3 Decisões em aberto"):
                it.title = "5.3 Decisões em aberto"
            elif t.startswith("Arquitetura, dados") and t.endswith("motor de análise"):
                it.title = "Arquitetura, dados e motor de análise"
            fix(it.children)
    with pdf.open_outline() as ol:
        fix(ol.root)
    pdf.Root["/ViewerPreferences"] = pikepdf.Dictionary(DisplayDocTitle=True)
    pdf.docinfo["/Title"] = TITLE
    pdf.docinfo["/Author"] = "IAgentics Brasil"
    pdf.docinfo["/Subject"] = "Arquitetura de software, modelo de dados e motor de análise por níveis do LIS (Inteligência de Comportamento Digital)"
    pdf.docinfo["/Keywords"] = "LIS, arquitetura, modelo de dados, Jev, Claude, Apify, scraping, análise por níveis"
    pdf.Root["/Lang"] = pikepdf.String("pt-BR")
    with pdf.open_metadata() as meta:
        meta["dc:title"] = TITLE
        meta["dc:creator"] = ["IAgentics Brasil"]
        meta["dc:language"] = ["pt-BR"]
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    pdf.save(dst)
    return n


def main():
    pass1 = os.path.join(HERE, "pass1.pdf")
    pass2 = os.path.join(HERE, "pass2.pdf")
    html1 = assemble({})
    render(html1, pass1)
    titles = heading_texts(html1)
    outl, n1 = outline_pages(pass1)
    pages, missing = {}, []
    for ident, t in titles.items():
        pg = outl.get(t)
        if pg is None:
            missing.append((ident, t))
        else:
            pages[ident] = pg
    print("pass1 páginas:", n1, "| ids resolvidos:", len(pages), "| sem página:", missing)
    ids_toc = set(re.findall(r"\{\{pg:([A-Za-z0-9_-]+)\}\}", open(os.path.join(HERE, "p1_a.html"), encoding="utf-8").read()))
    still = sorted(ids_toc - set(pages))
    if still:
        print("AVISO: ids do sumário sem página:", still)
    html2 = assemble(pages)
    render(html2, pass2)
    outl2, n2 = outline_pages(pass2)
    pages2 = {i: outl2.get(t) for i, t in titles.items()}
    drift = {i: (pages[i], pages2[i]) for i in pages if pages2.get(i) != pages[i]}
    print("pass2 páginas:", n2, "| deriva do sumário:", drift)
    out = os.path.join(OUT_DIR, OUT_NAME)
    n = stamp(pass2, out)
    print("OK", out, n, "páginas")
    import json
    json.dump(pages2, open(os.path.join(HERE, "pages.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
