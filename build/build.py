#!/usr/bin/env python3
"""Build datalicensingstandard.org from the sealed files of The Data Licensing Standard for AI (TDLS-AI) v0.1.

    python3 build/build.py --venue PATH_TO_VENUE_CHECKOUT --out docs

The venue is https://github.com/AndrewDelaurierWeeks/data-licensing-standard at commit de671fb. Every sealed
file is copied byte for byte and checked against the SHA-256 pinned below; the build stops on any difference.
Each Part, Requirement and Annex gets a page at https://datalicensingstandard.org/v0.1/<id>/ whose sealed block
is that section's text, and a Markdown copy at /v0.1/<id>.md that is the section's bytes. The build checks that
the Markdown copies put together give back the sealed source byte for byte, and that the words of every page's
sealed block equal the words of its section. Needs Python 3.9 or later and pandoc 3."""
import argparse, hashlib, html, json, re, shutil, subprocess, sys
from pathlib import Path

SITE = "https://datalicensingstandard.org"
VENUE = "https://github.com/AndrewDelaurierWeeks/data-licensing-standard"
VENUE_COMMIT = "de671fb7d37a0aff6b5c247635004bf6b41facec"
V = "v0.1"
SRC = "TDLS-AI-v0.1.md"
SCHEMA_DIR = "schema/0.3.0"                                  # the path in the schema's $id
SCHEMA_ID = f"{SITE}/{SCHEMA_DIR}/tdls-ai-vendor-declaration.schema.json"

# The sealed files, as published at the venue commit above (read 2026-11-25).
SEALED = {
    "TDLS-AI-v0.1.md":      "e2a4c2f89cb919f0757333c8b96200dd389d23674a35e627c2e5e4cc4ae29ea1",
    "TDLS-AI-v0.1.pdf":     "80bdad17c7749bd944384ebba6f148ef183626d10642c4f887aa9ed835ab1544",
    "TDLS-AI-v0.1.md.tsr":  "3d7681f997b4cccef9a57b176ce4eff5d9949960fa3e2bb6426cbaab74f205f2",
    "TDLS-AI-v0.1.tsr":     "62a46a861c67a7c1887157c9ac4a19cc62ae9c0972ab6605b45a9c42bb769a46",
    "TDLS-AI-v0.1.sha256":  None,                              # checked by content below
}
SCHEMA_FILES = {
    "tdls-ai-vendor-declaration.schema.json": "7abafb0f17069c25e3576fc80aba148976a4f061f21af1f0a91d973cc81653ba",
    "example-declaration.json":               "5fb0cdc4fe3ce1873d83be3566b96d5bd892c70302e93e4fec18d6374c4f0071",
    "crosswalk-0.3.0.json":                   "edd3995f5f400eb55a570be690797c6d4de8fd1cead145b17b7e5abf603737cc",
    "validate.py":                            None,
    "LICENSE":                                None,
}
V0_SHA = "626b49613704368ae40b17d5cbbe20dfd3559961883d25cb8a1e9366dd21bf86"
V0_ARCHIVE = f"{VENUE}/commit/9ef537703d4ef6d2fe7114da85f2dd584f31ba78"

e = html.escape
def sha(b): return hashlib.sha256(b).hexdigest()
def die(msg): sys.exit("build refused: " + msg)

# ------------------------------------------------------------------ the source, cut at its headings
def front_matter(md):
    m = re.match(r"^---\n(.*?)\n---\n", md, re.S)
    if not m: die("no front matter")
    fm = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        fm[k.strip()] = json.loads(v.strip()) if v.strip().startswith('"') else v.strip()
    return fm, m.end()

def sections(md):
    """Cut the source after its front matter at each '## ' heading, and inside Part 3 at each '### R' heading.
    Returns [(id, kind, number, title, text)], the texts in order; with the front matter they give back the source."""
    fm, start = front_matter(md)
    body = md[start:]
    cuts = [m.start() for m in re.finditer(r"(?m)^## ", body)]
    p3 = re.search(r"(?m)^## 3\. ", body).start(); p4 = re.search(r"(?m)^## 4\. ", body).start()
    cuts += [p3 + m.start() for m in re.finditer(r"(?m)^### R\d+ · ", body[p3:p4])]
    cuts = sorted(set(cuts))
    if cuts[0] != 0 and body[:cuts[0]].strip(): die("text before the first heading")
    if cuts[0] != 0: cuts[0] = 0
    out = []
    for i, c in enumerate(cuts):
        text = body[c: cuts[i + 1] if i + 1 < len(cuts) else len(body)]
        head = text.lstrip("\n").split("\n", 1)[0]
        if m := re.match(r"^## (\d)\. (.+)$", head):
            out.append((f"part-{m.group(1)}", "Part", m.group(1), m.group(2), text))
        elif m := re.match(r"^### R(\d+) · (.+)$", head):
            out.append((f"r{m.group(1)}", "R", m.group(1), m.group(2), text))
        elif m := re.match(r"^## Annex ([A-C]) · (.+)$", head):
            out.append((f"annex-{m.group(1).lower()}", "Annex", m.group(1), m.group(2), text))
        else:
            die("unexpected heading: " + head)
    if md[:start] + "".join(t for *_, t in out) != md: die("the sections do not give back the source")
    return fm, md[:start], out

def label(kind, num):        return {"Part": f"Part {num}", "R": f"R{num}", "Annex": f"Annex {num}"}[kind]
def cite(kind, num):         return f"TDLS-AI {V} {label(kind, num)}"
def nav_title(kind, num, t): return f"{label(kind, num)} · {t}"

# ------------------------------------------------------------------ Markdown to HTML
def pandoc(text, to, shift=0):
    args = ["pandoc", "-f", "markdown-smart", "-t", to, "--wrap=none"]
    if to == "html5": args += ["--no-highlight", f"--shift-heading-level-by={shift}"]
    return subprocess.run(args, input=text.encode("utf-8"), capture_output=True, check=True).stdout.decode("utf-8")

LINKABLE = re.compile(r"\b(R(1[0-2]|[1-9]))\b(?!\.\d)|\b(Part ([0-7]))\b|\b(Annex ([A-C])(?:\.(\d{1,2}))?)\b|\b(question (\d{1,2}))\b")
def link_refs(fragment, self_id):
    """Link requirement numbers, Part and Annex names and single question numbers in text, outside links,
    code and headings. The text itself is unchanged."""
    out, skip = [], 0
    for tok in re.split(r"(<[^>]+>)", fragment):
        if tok.startswith("<"):
            m = re.match(r"</?(a|code|pre|h[1-6])\b", tok)
            if m: skip += -1 if tok.startswith("</") else 1
            out.append(tok); continue
        if skip > 0 or not tok: out.append(tok); continue
        def rep(m):
            if m.group(1):   target = f"r{m.group(2)}"; anchor = ""
            elif m.group(3):
                if self_id == "annex-b": return m.group(0)        # Annex B quotes outside documents, whose own titles name their parts
                target = f"part-{m.group(4)}"; anchor = ""
            elif m.group(5):
                target = f"annex-{m.group(6).lower()}"
                anchor = f"#b{m.group(7)}" if m.group(6) == "B" and m.group(7) and 1 <= int(m.group(7)) <= 12 else ""
                if m.group(7) and not anchor: return m.group(0)
            else:
                n = int(m.group(9))
                if not 1 <= n <= 25: return m.group(0)
                target = "part-4"; anchor = f"#q{n}"
            if target == self_id and not anchor: return m.group(0)
            return f'<a href="/{V}/{target}/{anchor}">{m.group(0)}</a>'
        out.append(LINKABLE.sub(rep, tok))
    return "".join(out)

def anchor_disclosure(fragment):
    """Part 0's conflict disclosure gets an address, so every footer can link to it. Words unchanged."""
    a = "<p><strong>Conflict disclosure.</strong>"
    if fragment.count(a) != 1: die("Part 0 has no single conflict disclosure paragraph")
    return fragment.replace(a, '<p id="conflict-disclosure"><strong>Conflict disclosure.</strong>')

def instrument(fragment):
    """Part 5 below the scoring table, set as an instrument (his letter of 2026-11-25, "Part 5, V2, the instrument").
    The same words in the same order; the sealed-block check below still compares them with the section."""
    split = lambda h, pat: [x for x in re.split(pat, h) if x != ""]
    m = re.search(r'<p><strong>Scoring\.</strong> (.*?)</p>\n<p><strong>Suggested thresholds\.</strong> (.*?)</p>\n'
                  r'<p><strong>What the sheet is for\.</strong> (.*?)</p>\n<p>(From The Data Licensing Standard for AI .*?)</p>\n', fragment, re.S)
    if not m: die("Part 5: the four paragraphs below the table are not where the instrument expects them")
    sc, th, fo, ci = m.groups()
    s = split(sc, r"(?<=[.:])\s+(?=[A-Z<])")
    if len(s) != 9 or s[0] != "None = 0, D = 1, M = 2, A = 3 per requirement." or not s[5].endswith("total:"): die("Part 5: the scoring sentences changed")
    code_row = lambda i: re.sub(r'^(<a href="/v0\.1/r\d+/">R\d+</a>) (.*)$', r'<div><span class="c">\1</span> <span>\2</span></div>', i, flags=re.S)
    na = " ".join(code_row(i) for i in split(s[6], r'(?<=,)\s+(?=<a href="/v0\.1/r\d+/">R\d+</a> when)'))
    t_head, t_rest = th.split(": ", 1)
    t = re.match(r"(.*?where it applies\.) (For a purchase used in evaluation: additionally .*? at M or better\.) (A buyer may set .*)$", t_rest, re.S)
    if not t: die("Part 5: the thresholds changed")
    e_head, e_body = t.group(2).split(": ", 1)
    f = re.match(r"(.*?can check\.) (The sheet records .*)$", fo, re.S)
    if not f: die("Part 5: what the sheet is for changed")
    rows = lambda items, tag, cls: " ".join(f'<{tag} class="{cls}">{i}</{tag}>' for i in items)
    block = f"""<div class="p5i">
<section class="blk"><p class="blk-lab"><strong>Scoring.</strong></p>
<div class="keys"><span class="kn"><b>None</b> <i>= 0,</i></span> <span class="kd"><b>D</b> <i>= 1,</i></span> <span class="km"><b>M</b> <i>= 2,</i></span> <span class="ka"><b>A</b> <i>= 3</i></span> <span class="kpr">per requirement.</span></div>
<p class="met">{s[1]}</p>
<div class="cards"><p>{s[2]}</p> <p>{s[3]}</p> <p>{s[4]}</p></div>
<div class="na"><p class="head">{s[5]}</p> <div class="rows">{na}</div></div>
<div class="cards two"><p>{s[7]}</p> <p>{s[8]}</p></div>
</section>
<section class="blk"><p class="blk-lab"><strong>Suggested thresholds.</strong></p>
<div class="th"><div class="panel"><p class="ph">{t_head}:</p> {rows(split(t.group(1), r"(?<=;)\s+"), "div", "pr")}</div>
<div class="panel eval"><p class="ph">{e_head}:</p> <div class="pr">{e_body}</div></div></div>
<p class="note">{t.group(3)}</p>
</section>
<section class="blk"><p class="blk-lab"><strong>What the sheet is for.</strong></p>
<div class="for">{rows(split(f.group(1), r"(?<=;)\s+"), "p", "f")}</div>
<p>{f.group(2)}</p>
</section>
<p class="cite">{ci}</p>
</div>
"""
    return fragment[:m.start()] + block + fragment[m.end():]

TIER_CLASS = {"M": "t-m", "met": "t-m", "D": "t-k", "none": "t-k", "not met": "t-k", "N/A": "t-k", "assertion": "t-a"}

def dress_guidance(fragment):
    """Classes for the guidance colours the PDF uses: the purpose, the examples' tier words, the failure list. Words unchanged."""
    fragment = fragment.replace("<dt>Purpose</dt>\n<dd>", '<dt>Purpose</dt>\n<dd class="purpose">')
    fragment = fragment.replace("<dt>Where a check fails</dt>\n<dd>", '<dt>Where a check fails</dt>\n<dd class="fails">')
    fragment = fragment.replace("<dt>Examples, illustrative</dt>\n<dd>", '<dt>Examples, illustrative</dt>\n<dd class="examples">')
    def tier(m):
        if m.group(1) not in TIER_CLASS: die(f"unknown tier word in guidance: {m.group(1)}")
        return f'<li><strong class="{TIER_CLASS[m.group(1)]}">{m.group(1)}</strong> ·'
    return re.sub(r"<li><strong>([^<]{1,12})</strong> ·", tier, fragment)

SCORE_LABEL = {"M": "SCORE 2", "met": "SCORE 3", "D": "SCORE 1", "A": "SCORE 3", "none": "SCORE 0", "not met": "SCORE 0", "assertion": "SCORE 0", "N/A": ""}

def requirement_layout(fragment, num):
    """A requirement page as lettered on 2026-11-26 ("Requirement page V4, your combination"): the requirement on the left,
    the guidance beside it in a column held in view, set as the PDF sets its guidance. Wrappers and classes only; the
    words and their order are unchanged, and the sealed-block check below still compares them with the section."""
    m = re.match(r'(\n?<h1 [^>]*>.*?</h1>\n)(.*?)(<div class="guidance">\n.*</div>\n)$', fragment, re.S)
    if not m: die(f"R{num}: the heading, requirement and guidance are not where the page layout expects them")
    head, req, gd = m.groups()
    if re.sub(r"<p>.*?</p>\n", "", req, flags=re.S) != "": die(f"R{num}: the requirement holds something other than paragraphs")
    if gd.count("<div") != 1: die(f"R{num}: the guidance is not shaped as expected")
    labels = ["Purpose", "What the buyer checks", "Good practice", "Examples, illustrative", "Where a check fails"]
    if re.findall(r"<dt>(.*?)</dt>", gd) != labels: die(f"R{num}: the guidance's labels are not the five expected, in order")
    gd = gd.replace("<dt>Good practice</dt>\n<dd>", '<dt>Good practice</dt>\n<dd class="gp">')
    def wrap_items(block):
        if re.search(r"<li>(?:(?!</li>).)*?<(?:ul|ol|p)[ >]", block, re.S): die(f"R{num}: a nested list or a paragraph inside a guidance item")
        return re.sub(r"<li>(.*?)</li>", r'<li><span class="tx">\1</span></li>', block, flags=re.S)
    for pat in (r'(<dt>What the buyer checks</dt>\n<dd>\n<ol[^>]*>.*?</ol>)', r'(<dd class="gp">.*?</dd>)', r'(<dd class="fails">.*?</dd>)'):
        gd, n_wrap = re.subn(pat, lambda x: wrap_items(x.group(1)), gd, count=1, flags=re.S)
        if n_wrap != 1: die(f"R{num}: a guidance list is not where the page layout expects it")
    def example(x):
        word = x.group(2)
        if word not in SCORE_LABEL: die(f"R{num}: unknown tier word in an example: {word}")
        small = " small" if len(word) > 2 else ""
        return (f'<li><span class="tier{small}" data-score="{SCORE_LABEL[word]}">{x.group(1)}</span>'
                f'<span class="sep"> · </span><span class="txt">{x.group(3)}</span></li>')
    ex = re.search(r'<dd class="examples">.*?</dd>', gd, re.S)
    if not ex: die(f"R{num}: no examples in the guidance")
    exb, n_ex = re.subn(r'<li>(<strong class="t-[a-z]">([^<]{1,12})</strong>) · (.*?)</li>', example, ex.group(0), flags=re.S)
    if n_ex == 0 or n_ex != ex.group(0).count("<li>"): die(f"R{num}: an example without its tier word")
    gd = gd[:ex.start()] + exb + gd[ex.end():]
    return (f'{head}<div class="split"><div class="rqcol">{req}</div>\n'
            f'<aside class="gd" aria-label="Guidance for R{num}">{gd}</aside></div>\n')

def dress_tables(fragment, sid):
    """Give each cell its column label (for the phone layout), wrap each table, and give Part 4's rows q<n> ids."""
    def one(m):
        t = m.group(0)
        heads = [re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<th[^>]*>(.*?)</th>", t, re.S)]
        def row(rm):
            r = rm.group(0); i = [0]
            def cell(cm):
                k = i[0]; i[0] += 1
                lab = f' data-label="{e(heads[k])}"' if k < len(heads) and heads[k] else ""
                return f"<td{cm.group(1)}{lab}>"
            r = re.sub(r"<td([^>]*)>", cell, r)
            if sid == "part-4":
                q = re.search(r"<td[^>]*>(\d{1,2})</td>", r)
                if q: r = r.replace("<tr", f'<tr id="q{q.group(1)}"', 1)
            return r
        t = re.sub(r"<tr[^>]*>.*?</tr>", row, t, flags=re.S)
        return f'<div class="tbl">{t}</div>'
    return re.sub(r"<table.*?</table>", one, fragment, flags=re.S)

def heading_ids(fragment, sid):
    if sid == "annex-b":
        fragment = re.sub(r'<h2 id="[^"]*">B\.(\d+) ', lambda m: f'<h2 id="b{m.group(1)}">B.{m.group(1)} ', fragment)
    return fragment

def inline_md(text):
    return pandoc(text, "html5").strip().removeprefix("<p>").removesuffix("</p>")

def kick(t):
    """A kicker's text, escaped, with the version kept in lower case under the kicker's capitals."""
    return e(t).replace(V, f'<span class="v">{V}</span>')

def words(s):
    return re.findall(r"[\w$]+", html.unescape(s).replace(" ", " "))

# ------------------------------------------------------------------ the mark, as on the cover (design_b.mark)
def mark_svg(h, color="#000"):
    n, size = 15, 21.2; c = size / (n + 1)
    cells = "".join(f'<rect x="{0.6+i*c:.2f}" y="{0.6+j*c:.2f}" width="{c*0.95:.2f}" height="{c*0.95:.2f}"/>'
                    for i in range(n) for j in range(n) if int(h[(i * n + j) % 64], 16) % 2)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-0.2 -0.2 21.6 21.6">'
            f'<!-- The square mark of TDLS-AI v0.1, drawn from the source SHA-256 {h} as on the cover: 15 by 15 cells, '
            f'a cell filled where the hex digit at (column * 15 + row) mod 64 is odd. -->'
            f'<rect x="0" y="0" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="0.3"/>'
            f'<g fill="{color}">{cells}</g></svg>')

# ------------------------------------------------------------------ descriptions and structured data
BUILD_DATE = "2026-11-25"           # the date these pages were last built; the sealed files keep 2026-11-24
INDEXNOW_KEY = "6e8660927ac2f49e537b7f06d15d8c5d"   # public by design: it proves to search engines that a change notice comes from this site

def first_sentence(text, limit=260):
    """The section's first sentence of prose, its own words, for the page's description (a leading label such as
    'Requirement.' is skipped)."""
    paras = [re.sub(r"\s+", " ", p).strip() for p in pandoc(text, "plain").split("\n\n")]
    for p in paras[1:]:
        if not p or p[0] in "|-+*>" or re.match(r"^\d+\.\s", p) or p.isupper(): continue
        p = re.sub(r"^[A-Z][\w-]*(?: [\w-]+){0,2}\. (?=\S)", "", p)
        m = re.match(r"(.+?[.?!])(?:\s+(?=[A-Z(\"])|$)", p)
        out = m.group(1) if m else p
        if len(out.split()) < 6: continue
        if len(out) > limit:
            cut = out[:limit]
            at = max(cut.rfind("; "), cut.rfind(": "))
            out = (cut[:at] if at > limit // 2 else cut.rsplit(" ", 1)[0]) + " …"
        return out
    return ""

def ld_person(fm, full=False):
    n = {"@type": "Person", "@id": PERSON_ID, "name": fm["author"], "url": PERSON_ID}
    if full: n.update({"description": fm["credentials_full"] + " " + fm["capacity"], "sameAs": ["https://github.com/AndrewDelaurierWeeks"]})
    return n

def ld_standard(fm, full=False, parts=None, h=None):
    n = {"@type": "CreativeWork", "@id": STD_ID, "name": fm["title_display"], "alternateName": [fm["short_name"], f"{fm['short_name']} {V}"],
         "url": SITE + "/", "version": V.lstrip("v"), "datePublished": fm["date"], "author": {"@id": PERSON_ID},
         "publishingPrinciples": {"@type": "CreativeWork", "name": "Conflict disclosure", "url": f"{SITE}/{V}/part-0/#conflict-disclosure", "text": CONFLICT_TEXT}}
    if full:
        n.update({"headline": f"{fm['title_display']}: {fm['subtitle']}", "description": f"{fm['subtitle']}. {fm['scope_line']}",
                  "genre": "procurement standard", "identifier": fm["serial"], "inLanguage": "en", "creator": {"@id": PERSON_ID},
                  "license": PART7, "isAccessibleForFree": True, "keywords": ", ".join(KEYWORDS),
                  "image": {"@type": "ImageObject", "url": OG, "width": 1200, "height": 630}, "disambiguatingDescription": ONE_AUTHOR,
                  "encoding": [{"@type": "MediaObject", "name": "TDLS-AI-v0.1.pdf", "contentUrl": f"{SITE}/TDLS-AI-v0.1.pdf", "encodingFormat": "application/pdf", "sha256": SEALED["TDLS-AI-v0.1.pdf"]},
                               {"@type": "MediaObject", "name": SRC, "contentUrl": f"{SITE}/{SRC}", "encodingFormat": "text/markdown", "sha256": h}],
                  "hasPart": parts or []})
    return n

def ld_page(url, name, desc, typ="WebPage", about=None, crumbs=None):
    about = about or STD_ID
    g = [{"@type": typ, "@id": url + "#webpage", "url": url, "name": name, "description": desc, "inLanguage": "en",
          "isPartOf": {"@id": SITE_ID}, "about": {"@id": about}, "thumbnailUrl": OG, "dateModified": BUILD_DATE},
         {"@type": "WebSite", "@id": SITE_ID, "url": SITE + "/", "name": SITE_NAME[0], "alternateName": SITE_NAME[1],
          "inLanguage": "en", "publisher": {"@id": PERSON_ID}}]
    if crumbs:
        g[0]["breadcrumb"] = {"@id": url + "#breadcrumb"}
        g.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
                  "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]})
    return g

def glossary(text):
    """Annex C's entries, as sealed: '**Term.** Definition.'"""
    return [(m.group(1), re.sub(r"[*`]", "", m.group(2)).strip()) for m in re.finditer(r"(?m)^\*\*(.+?)\.\*\* (.+)$", text)]

# ------------------------------------------------------------------ the page frame
NAV = [(f"/{V}/", "Contents"), (f"/{V}/part-4/", "Questions"), (f"/{V}/part-5/", "Scoring"),
       ("/schema/", "Schema"), ("/verify/", "Verify"), ("/colophon/", "Colophon"), ("/TDLS-AI-v0.1.pdf", "PDF")]
HERO_SCRIPT = ""          # set in main(): the home page's one script, served from this site, with its integrity hash
CSS_LINK = ""             # set in main(): the stylesheet, with its integrity hash
# The page's own security policy, as a meta tag, since GitHub Pages lets a site set no headers: everything from this
# site, nothing inline but the structured data, which is not run. Only the home page runs a script or fetches data.
def csp(home):
    run = "'self'" if home else "'none'"
    return (f"default-src 'none'; script-src {run}; style-src 'self'; img-src 'self'; font-src 'self'; connect-src {run}; "
            "base-uri 'none'; form-action 'none'; object-src 'none'; "
            "require-trusted-types-for 'script'; trusted-types 'none'; upgrade-insecure-requests")
# Search and AI terms, each one the sealed text's own words (checked against the source at build time).
KEYWORDS = ["TDLS-AI", "AI training data", "training data", "data licensing", "vendor questionnaire", "scoring sheet", "procurement",
            "request for proposal", "diligence", "provenance", "chain of custody", "consent basis", "de-identification",
            "synthetic data", "human data", "sensor records", "evaluation data", "contamination", "RL environment",
            "reinforcement learning", "deletion", "evidence package", "attestation", "health data", "financial and payment data",
            "brokers", "marketplaces", "JSON Schema", "vendor declaration", "RFC 3161"]
PART7 = f"{SITE}/{V}/part-7/"        # the license, with its exclusions (quoted material, outside specifications' names)
OG = f"{SITE}/assets/og.png"
PERSON_ID = f"{SITE}/colophon/#about-the-author"
STD_ID = f"{SITE}/#standard"
SITE_ID = f"{SITE}/#website"
FONTS_PRELOAD = ("inter-latin-400-normal", "ibm-plex-mono-latin-500-normal", "eb-garamond-latin-500-normal")

def jsonld(graph):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c") + "</script>"

def page(*, title, desc, path, body, current=None, wide=False, req=False, home=False, fm, ld=None, md=None, robots="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"):
    nav = "".join(f'<a href="{u}"{" class=\"pdf\"" if t == "PDF" else ""}{" aria-current=\"page\"" if u == current else ""}>{t}</a>' for u, t in NAV)
    canon = f"{SITE}{path}"
    cls = ' class="home"' if home else (' class="wide"' if wide else (' class="rpage"' if req else ""))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{csp(home)}">
<meta name="referrer" content="no-referrer">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<meta name="author" content="{e(fm["author"])}">
<meta name="keywords" content="{e(", ".join(KEYWORDS))}">
{f'<link rel="canonical" href="{canon}">{chr(10)}' if path != "/404.html" else ""}<link rel="license" href="/{V}/part-7/">
<meta name="format-detection" content="telephone=no">
{"".join(f'<link rel="preload" href="/assets/fonts/{f}.woff2" as="font" type="font/woff2" crossorigin>{chr(10)}' for f in FONTS_PRELOAD)}{'<link rel="preload" href="/assets/device/plate.webp" as="image" fetchpriority="high">' + chr(10) if home else ""}{CSS_LINK}
<link rel="icon" href="/assets/icons/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/icons/favicon-16.png" sizes="16x16" type="image/png">
<link rel="icon" href="/assets/icons/favicon-48.png" sizes="48x48" type="image/png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="alternate" type="text/markdown" href="/{SRC}" title="The sealed source text">
{f'<link rel="alternate" type="text/markdown" href="{md}" title="This section as sealed">{chr(10)}' if md else ""}<meta property="og:site_name" content="{e(fm["title_display"])} ({e(fm["short_name"])})">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
{f'<meta property="og:url" content="{canon}">{chr(10)}' if path != "/404.html" else ""}<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="{OG}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(fm["title_display"])}: {e(fm["subtitle"])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{OG}">
<meta name="twitter:image:alt" content="{e(fm["title_display"])}: {e(fm["subtitle"])}">
{jsonld(ld) + chr(10) if ld else ""}{HERO_SCRIPT + chr(10) if home else ""}</head>
<body>
<a class="skip" href="#main">Skip to the text</a>
<header class="site">
<a class="brand" href="/" aria-label="{e(fm["short_name"])} {V}, {e(fm["title_display"])}, home"><span class="mk" aria-hidden="true"></span><span>{e(fm["short_name"])} {V}</span></a>
<nav class="top" aria-label="Site">{nav}</nav>
</header>
<main id="main"{cls}>
{body}
</main>
<footer class="site"><div class="in">
<p>{e(fm["capacity"])} {ONE_AUTHOR_HTML}</p>
<p>{e(fm["license"])} Full terms: <a href="/{V}/part-7/">Part 7</a>.</p>
<p>The sealed files are the authority for this text: <a href="/verify/">verify them</a>. Venue: <a href="{VENUE}">{VENUE.replace("https://", "")}</a>, commit <span class="hash">{VENUE_COMMIT[:7]}</span>.</p>
<p><a href="/colophon/"{' aria-current="page"' if path == "/colophon/" else ""}>Colophon</a> · <a href="/{V}/part-0/#conflict-disclosure">Conflict disclosure</a></p>
</div></footer>
</body>
</html>
"""

CONFLICT_TEXT = ""        # set in main(): Part 0's conflict disclosure, as sealed, in plain text
ONE_AUTHOR = ""           # set in main(): Part 0's sentence on whose work this is, plain
SITE_NAME = ("", "")      # set in main(): the site's name and short name
ONE_AUTHOR_HTML = ""      # set in main(): Part 0's sentence on whose work this is, as sealed

# ------------------------------------------------------------------ build
def main():
    global CONFLICT_TEXT, ONE_AUTHOR_HTML, ONE_AUTHOR, SITE_NAME, HERO_SCRIPT, CSS_LINK, OG
    ap = argparse.ArgumentParser()
    ap.add_argument("--venue", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args()
    here = Path(__file__).resolve().parent
    out = a.out
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)

    # 1. the sealed files, byte for byte
    for name, want in SEALED.items():
        b = (a.venue / name).read_bytes()
        if want and sha(b) != want: die(f"{name} has SHA-256 {sha(b)}, not the sealed {want}")
        (out / name).write_bytes(b)
    sums = (out / "TDLS-AI-v0.1.sha256").read_text()
    for name in ("TDLS-AI-v0.1.pdf", "TDLS-AI-v0.1.md"):
        if f"{SEALED[name]}  {name}" not in sums: die(f"the .sha256 file does not list {name} with its sealed value")
    (out / SCHEMA_DIR).mkdir(parents=True)
    for name, want in SCHEMA_FILES.items():
        b = (a.venue / "schema" / name).read_bytes()
        if want and sha(b) != want: die(f"schema/{name} has SHA-256 {sha(b)}, not {want}")
        (out / SCHEMA_DIR / name).write_bytes(b)
    sid_in_schema = json.loads((out / SCHEMA_DIR / "tdls-ai-vendor-declaration.schema.json").read_text())["$id"]
    if sid_in_schema != SCHEMA_ID: die(f"the schema's $id is {sid_in_schema}, not {SCHEMA_ID}")

    md_bytes = (out / SRC).read_bytes(); h = sha(md_bytes)
    md = md_bytes.decode("utf-8")
    fm, fm_text, secs = sections(md)
    part0 = next(t for i, *_, t in secs if i == "part-0")
    conflict = re.search(r"(?m)^\*\*Conflict disclosure\.\*\* .+$", part0).group(0)
    CONFLICT_TEXT = conflict.replace("**", "")
    one_author = re.search(r"(?m)^This document is one author's work\. .+$", part0)
    if not one_author: die("Part 0 has no sentence on whose work this is")
    ONE_AUTHOR = one_author.group(0)
    ONE_AUTHOR_HTML = e(ONE_AUTHOR)
    SITE_NAME = (fm["title_display"], f"{fm['short_name']} {V}")

    # 2. assets
    (out / "assets").mkdir()
    shutil.copytree(here / "assets" / "fonts", out / "assets" / "fonts")
    names = {}
    for n in ("site.css", "hero.js"):                             # content-hashed names: a cached old file can never meet new HTML
        b = (here / "assets" / n).read_bytes(); stem, ext = n.rsplit(".", 1)
        names[n] = f"{stem}.{sha(b)[:10]}.{ext}"
        (out / "assets" / names[n]).write_bytes(b)
    shutil.copytree(here / "assets" / "device", out / "assets" / "device")
    shutil.copytree(here / "assets" / "icons", out / "assets" / "icons")
    shutil.copy(here / "assets" / "icons" / "favicon.ico", out / "favicon.ico")     # the address browsers ask for unprompted
    shutil.copytree(here / "assets" / "security", out / "assets" / "security")
    shutil.copy(here / "assets" / "apple-touch-icon.png", out / "assets" / "apple-touch-icon.png")
    # the preview card under a content-hashed name, so a network that cached the old card fetches the new one
    og = (here / "assets" / "og.png").read_bytes(); og_name = f"og.{sha(og)[:10]}.png"
    (out / "assets" / og_name).write_bytes(og); OG = f"{SITE}/assets/{og_name}"
    (out / "assets" / "og.png").write_bytes(og)                # the old address serves the new card too
    sri = lambda b: "sha384-" + __import__("base64").b64encode(hashlib.sha384(b).digest()).decode()
    CSS_LINK = f'<link rel="stylesheet" href="/assets/{names["site.css"]}" integrity="{sri((out / "assets" / names["site.css"]).read_bytes())}">'
    HERO_SCRIPT = f'<script src="/assets/{names["hero.js"]}" integrity="{sri((out / "assets" / names["hero.js"]).read_bytes())}" defer></script>'
    for k in KEYWORDS:
        if k.lower() not in md.lower(): die(f"the keyword {k!r} is not in the sealed text")
    (out / "assets" / "mark.svg").write_text(mark_svg(h))

    # 3. the section pages and their Markdown copies
    order = [s[0] for s in secs]
    want_order = [f"part-{i}" for i in range(4)] + [f"r{i}" for i in range(1, 13)] + \
                 [f"part-{i}" for i in range(4, 8)] + ["annex-a", "annex-b", "annex-c"]
    if order != want_order: die("unexpected section order: " + ", ".join(order))
    toc = []
    for k, (sid, kind, num, t, text) in enumerate(secs):
        (out / V / sid).mkdir(parents=True)
        (out / V / f"{sid}.md").write_bytes(text.encode("utf-8"))
        shift = -2 if kind == "R" else -1
        frag = pandoc(text, "html5", shift)
        frag = re.sub(r'(<col)\s+style="[^"]*"', r"\1", frag)       # column widths the stylesheet overrides; no inline style
        frag = heading_ids(frag, sid)
        frag = dress_tables(frag, sid)
        frag = link_refs(frag, sid)
        frag = dress_guidance(frag)
        if sid == "part-0": frag = anchor_disclosure(frag)
        if sid == "part-5": frag = instrument(frag)
        if kind == "R": frag = requirement_layout(frag, num)
        if sid == "part-4": part4_frag = frag
        prev = secs[k - 1] if k else None
        nxt = secs[k + 1] if k + 1 < len(secs) else None
        pn = '<nav class="pn" aria-label="Sections">'
        if prev: pn += f'<a class="prev" href="/{V}/{prev[0]}/">Previous: {e(nav_title(prev[1], prev[2], prev[3]))}</a>'
        if nxt: pn += f'<a class="next" href="/{V}/{nxt[0]}/">Next: {e(nav_title(nxt[1], nxt[2], nxt[3]))}</a>'
        pn += "</nav>"
        addr = f"{SITE}/{V}/{sid}/"
        body = f"""<p class="kicker">{kick(cite(kind, num))}</p>
<div class="sealed" data-section="{sid}" data-source-sha256="{h}">
{frag}</div>
<dl class="record">
<dt>Cite as</dt><dd>{e(cite(kind, num))}</dd>
<dt>Address</dt><dd><a href="{addr}">{addr}</a></dd>
<dt>Links</dt><dd>The links on requirement, Part, Annex and question numbers are added by this site; the words of the sealed text are unchanged.</dd>
<dt>This section as sealed</dt><dd><a href="/{V}/{sid}.md">/{V}/{sid}.md</a>, its bytes in the sealed source <a href="/{SRC}">{SRC}</a>, SHA-256 <span class="hash">{h}</span></dd>
</dl>
{pn}"""
        title = f"{nav_title(kind, num, t)} · {fm['short_name']} {V}"
        lead = first_sentence(text)
        if sid == "annex-c": lead = "The terms it defines: " + ", ".join(n for n, _ in glossary(text)) + "."
        desc = f"{cite(kind, num)}: {t}." + (f" {lead}" if lead else " The Data Licensing Standard for AI, version 0.1, sealed 2026-11-24.")
        sec = {"@type": "CreativeWork", "@id": addr + "#section", "name": nav_title(kind, num, t), "alternateName": cite(kind, num),
               "url": addr, "position": k + 1, "isPartOf": {"@id": STD_ID}, "author": {"@id": PERSON_ID}, "license": PART7, "inLanguage": "en",
               "encoding": {"@type": "MediaObject", "contentUrl": f"{SITE}/{V}/{sid}.md", "encodingFormat": "text/markdown", "sha256": sha(text.encode("utf-8"))}}
        graph = ld_page(addr, title, desc, about=addr + "#section", crumbs=[("Home", SITE + "/"), ("Contents", f"{SITE}/{V}/"), (nav_title(kind, num, t), addr)])
        graph += [sec, ld_standard(fm), ld_person(fm)]
        if sid == "annex-c":
            terms = glossary(text)
            if len(terms) < 10: die("Annex C's glossary was not read")
            graph.append({"@type": "DefinedTermSet", "@id": addr + "#glossary", "name": f"{cite(kind, num)}: {t}", "url": addr,
                          "hasDefinedTerm": [{"@type": "DefinedTerm", "name": n, "description": d, "inDefinedTermSet": {"@id": addr + "#glossary"}} for n, d in terms]})
        (out / V / sid / "index.html").write_text(page(title=title, desc=desc, path=f"/{V}/{sid}/", body=body,
                                                        current=f"/{V}/{sid}/" if sid in ("part-4", "part-5") else None,
                                                        wide=sid in ("part-4", "part-5", "annex-a"), req=kind == "R", fm=fm, ld=graph, md=f"/{V}/{sid}.md"))
        toc.append((sid, kind, num, t))

    # 4. the word check: every page's sealed block against its section
    for sid, kind, num, t, text in secs:
        page_html = (out / V / sid / "index.html").read_text()
        blk = re.search(r'<div class="sealed"[^>]*>(.*)</div>\s*<dl class="record">', page_html, re.S).group(1)
        got = words(re.sub(r"<[^>]+>", " ", blk))
        plain = re.sub(r"(?m)^\s*(?:\d\.  |\d\d\. |-   )", "", pandoc(text, "plain"))   # list markers are drawn by the HTML list
        want = words(plain)
        if got != want:
            i = next((n for n, (x, y) in enumerate(zip(got, want)) if x != y), min(len(got), len(want)))
            die(f"{sid}: the page's sealed block differs from the source at word {i}: {got[i:i+6]} against {want[i:i+6]}")
    if b"".join((out / V / f"{s[0]}.md").read_bytes() for s in secs) != md_bytes[len(fm_text.encode()):]:
        die("the Markdown copies do not give back the sealed source")

    # 5. contents, home, schema, verify, 404
    def toc_html():
        rows = []
        for sid, kind, num, t in toc:
            rows.append(f'<li><a href="/{V}/{sid}/"><em>{e(label(kind, num))}</em><span>{e(t)}</span></a></li>')
        return f'<ul class="toc">{"".join(rows)}</ul>'
    version_line = f'{e(fm["version"])} · {e(fm["date"])} · {e(fm["author"])}'
    contents = f"""<p class="kicker">{kick(fm["short_name"] + " " + V)} · Contents</p>
<h1>Contents</h1>
<p>Each Part, Requirement and Annex of the sealed text has its own page and a Markdown copy. {e(fm["short_name"])} {V} R8 is at <a href="/{V}/r8/">/{V}/r8/</a>; question 10 of Part 4 is at <a href="/{V}/part-4/#q10">/{V}/part-4/#q10</a>.</p>
{toc_html()}
<p class="note">{version_line}. The whole source: <a href="/{SRC}">{SRC}</a>. The PDF: <a href="/TDLS-AI-v0.1.pdf">TDLS-AI-v0.1.pdf</a>, 83 pages.</p>"""
    cdesc = "The Parts, Requirements and Annexes of The Data Licensing Standard for AI, version 0.1, each at its own address."
    (out / V / "index.html").write_text(page(title=f"Contents · {fm['short_name']} {V}", desc=cdesc,
                                             path=f"/{V}/", body=contents, current=f"/{V}/", fm=fm,
                                             ld=ld_page(f"{SITE}/{V}/", f"Contents · {fm['short_name']} {V}", cdesc, typ="CollectionPage", crumbs=[("Home", SITE + "/"), ("Contents", f"{SITE}/{V}/")]) + [ld_standard(fm), ld_person(fm)]))

    # the home page: the cover, as a page. The plate and the black band carry the cover's words (the sealed PDF, page 1,
    # checked below), the front matter's fields and Part 4's sealed rows, with the site's links and the switch; the
    # device in motion is assets/hero.js.
    qrows = []
    for n in (1, 18, 23):
        m = re.search(rf'<tr id="q{n}"[^>]*>(.*?)</tr>', part4_frag, re.S)
        if not m: die(f"Part 4 has no row q{n}")
        r = re.sub(rf'(<td data-label="No\.">){n}(</td>)', rf'\g<1><a href="/{V}/part-4/#q{n}">{n}</a>\g<2>', m.group(1), count=1)
        if f"#q{n}" not in r: die(f"Part 4's row q{n} has no number cell")
        qrows.append(f"<tr>{r}</tr>")
    nq = len(re.findall(r'<tr id="q\d+"', part4_frag))
    if nq != 25: die(f"Part 4 has {nq} numbered rows, not 25")
    qhead = re.search(r"<thead>.*?</thead>", part4_frag, re.S).group(0)
    schema_json = json.loads((out / SCHEMA_DIR / "tdls-ai-vendor-declaration.schema.json").read_text())
    req = schema_json["required"]
    excerpt = ('{\n  "$schema": "' + schema_json["$schema"] + '",\n  "$id": "' + SCHEMA_ID + '",\n  "required": ['
               + ", ".join(f'"{x}"' for x in req[:5]) + ",\n    " + ", ".join(f'"{x}"' for x in req[5:11]) + ",\n    "
               + ", ".join(f'"{x}"' for x in req[11:16]) + ",\n    " + ", ".join(f'"{x}"' for x in req[16:]) + "],\n"
               '  "de_identification": { "claimed": true, "tier": "measured", "attacker_assumed": "...", "method": "...",\n'
               '    "measured_on": { "...": "..." }, "residual": "...", "measurement_record_hash": "..." }\n}')
    for k in ("claimed", "tier", "attacker_assumed", "method", "measured_on", "residual", "measurement_record_hash"):
        if k not in schema_json["properties"]["de_identification"]["properties"]: die(f"the cover's excerpt names de_identification.{k}, which the schema lacks")
    try:
        cover = subprocess.run(["pdftotext", "-l", "1", str(a.venue / "TDLS-AI-v0.1.pdf"), "-"], capture_output=True, check=True).stdout.decode("utf-8")
    except (OSError, subprocess.CalledProcessError): die("pdftotext (poppler) is needed to check the cover's words")
    flat = lambda t: " ".join(t.split())
    for w in ["A BUYER'S REQUIREMENT", "OPEN · CC BY 4.0 TEXT · MIT SCHEMA", f"SOURCE SHA-256 {h[:16]}", fm["serial"],
              "EMBED THE DECLARATION; EVERY TOOL THAT READS IT READS THE SAME FIELDS", excerpt,
              "validate: python3 validate.py tdls-ai-vendor-declaration.schema.json example-declaration.json · MIT",
              fm["author"], fm["credentials"], fm["capacity_cover"], f"{V} · {fm['date']} · FIRST ASSESSMENT BY 2027-02-14",
              "REPOSITORY AND SEAL TOKENS AT RELEASE"]:
        if flat(w) not in flat(cover): die(f"the cover does not carry: {w[:60]}")
    home = f"""<section class="plate" data-hero>
<div class="plate-top">
<div><p class="serial">{e(fm["serial"])}</p><p class="srchash">SOURCE SHA-256 {h[:16]}</p></div>
<div class="plate-right">
<div class="switch" role="group" aria-label="What the engraved device does" data-switch hidden><span>DATA</span><button type="button" data-mode="in" aria-pressed="true" title="Blocks stream into the device's sides">IN</button><button type="button" data-mode="out" aria-pressed="false" title="Blocks break off and fly toward the viewer">OUT</button><button type="button" data-mode="dust" aria-pressed="false" title="The engraving turns to dust where the pointer passes">DUST</button><button type="button" data-mode="matrix" aria-pressed="false" title="The whole device as a field of dust" disabled>MATRIX</button></div>
<p class="lic">OPEN · CC BY 4.0 TEXT · MIT SCHEMA</p>
</div>
</div>
<p class="req">A BUYER'S REQUIREMENT</p>
<div class="stage" data-stage role="img" aria-label="The engraved device of the cover, a carved neoclassical anthropomorphic mascaron sculpted in high relief; the device's two sides break into blocks.">
<div class="tilt" data-tilt><img class="fill" data-fallback src="/assets/device/plate.webp" alt="" width="805" height="552" fetchpriority="high" decoding="async"><canvas class="pad" data-dust aria-hidden="true"></canvas></div>
<canvas class="pad" data-matrix aria-hidden="true"></canvas>
<canvas class="wide" data-stream aria-hidden="true"></canvas>
</div>
<h1>{e(fm["title_display"])}</h1>
<p class="sub">{e(fm["subtitle"])}</p>
<p class="scope">{e(fm["scope_line"])}</p>
<p class="meta">{version_line}</p>
<div class="tiers">
<div><b>D</b><span>Declared</span><p>The vendor states it, in the schema's fields, with a named person and a date.</p></div>
<div><b>M</b><span>Measured</span><p>A measurement backs it, made by the vendor or verified by the buyer.</p></div>
<div><b>A</b><span>Attested</span><p>An independent party attests the measurement and signs it.</p></div>
</div>
<p class="note">The tiers as the document defines them, with their conditions: <a href="/{V}/part-3/">Part 3</a>.</p>
<div class="actions">
<a class="btn primary" href="/{V}/">Read the standard</a>
<a class="btn" href="/{V}/part-4/">The vendor questionnaire</a>
<a class="btn" href="/{V}/part-5/">The scoring sheet</a>
<a class="btn pdf" href="/TDLS-AI-v0.1.pdf">The PDF, 83 pages</a>
</div>
</section>
<section class="band" id="declaration">
<p class="action">Attach Part 4 to every request for proposal; keep Part 5 where the buyer's counsel directs.</p>
<p class="lab" id="decl-lab">EMBED THE DECLARATION; EVERY TOOL THAT READS IT READS THE SAME FIELDS</p>
<div class="code" tabindex="0" role="region" aria-labelledby="decl-lab"><pre>{e(excerpt)}</pre></div>
<p class="val"><a href="/schema/">validate: python3 validate.py tdls-ai-vendor-declaration.schema.json example-declaration.json · MIT</a></p>
<hr>
<div class="author">
<span class="mk" aria-hidden="true"></span>
<div class="who"><p class="name"><a href="/colophon/#about-the-author">{e(fm["author"])}</a></p><p class="cred">{e(fm["credentials"])}</p></div>
<div class="cap"><p>{e(fm["capacity_cover"])}</p><p class="ser">{e(fm["serial"])}</p></div>
</div>
<div class="foot"><a href="/TDLS-AI-v0.1.pdf#page=3">{V} · {e(fm["date"])} · FIRST ASSESSMENT BY 2027-02-14</a><a href="/verify/">REPOSITORY AND SEAL TOKENS AT RELEASE</a></div>
</section>
<section class="more" id="contents">
<p class="kicker">The text, section by section</p>
<h2>Contents</h2>
<p class="note">Each Part, Requirement and Annex has its own page, at /{V}/&lt;id&gt;/, with a Markdown copy of its sealed text.</p>
{toc_html()}
</section>
<section class="more" id="questions">
<p class="kicker">Three of the 25 questions · Part 4</p>
<h2><a href="/{V}/part-4/">The vendor questionnaire</a></h2>
<div class="tbl qs"><table>{qhead}<tbody>{"".join(qrows)}</tbody></table></div>
</section>
<section class="more" id="cite">
<h2>Cite as</h2>
<p>{inline_md(re.search(r"(?m)^\*\*Citation\.\*\* (.+)$", next(t for i, *_, t in secs if i == "part-7")).group(1))}</p>
<h2>This edition</h2>
<p>{e(re.search(r"(?m)^\*\*Version\.\*\* (v0\.1, 2026-11-24, public draft for adoption\. It supersedes the edition sealed on 2026-11-16\.)", next(t for i, *_, t in secs if i == "part-7")).group(1))} That edition's source has the SHA-256 <span class="hash">{V0_SHA}</span>, and it is archived at <a href="{V0_ARCHIVE}">{V0_ARCHIVE.replace("https://", "")}</a>.</p>
</section>"""
    if "Attach Part 4 to every request for proposal; keep Part 5 where the buyer's counsel directs." not in home:
        die("home action line")
    htitle, hdesc = f"{fm['title_display']} ({fm['short_name']}) {V}", f"{fm['subtitle']}. {fm['scope_line']}"
    parts = [{"@type": "CreativeWork", "@id": f"{SITE}/{V}/{sid}/#section", "name": nav_title(kind, num, t), "url": f"{SITE}/{V}/{sid}/", "position": i + 1}
             for i, (sid, kind, num, t) in enumerate(toc)]
    hgraph = ld_page(SITE + "/", htitle, hdesc) + [ld_standard(fm, full=True, parts=parts, h=h), ld_person(fm, full=True)]
    (out / "index.html").write_text(page(title=htitle, desc=hdesc, path="/", body=home, home=True, fm=fm, ld=hgraph))

    sfiles = [("tdls-ai-vendor-declaration.schema.json", "The vendor declaration schema (JSON Schema 2020-12), version 0.3.0"),
              ("example-declaration.json", "An example declaration"),
              ("validate.py", "The validator, with the converter for a record in the form of OASIS Data Provenance Metadata Version 1.0, Committee Specification Draft 01"),
              ("crosswalk-0.3.0.json", "The crosswalk of Annex A, machine-readable"),
              ("LICENSE", "The MIT License of the schema, the example, the validator and the crosswalk file")]
    rows = "".join(f'<tr><td data-label="File"><a href="/{SCHEMA_DIR}/{n}">{n}</a></td><td data-label="What it is">{e(d)}</td><td data-label="SHA-256" class="hash">{sha((out / SCHEMA_DIR / n).read_bytes())}</td></tr>' for n, d in sfiles)
    schema_pg = f"""<p class="kicker">{kick(fm["short_name"] + " " + V)} · Annex A</p>
<h1>The vendor declaration schema, 0.3.0</h1>
<p>The schema answers at the address in its <code>$id</code>, byte for byte as published at the venue:</p>
<p class="hash"><a href="/{SCHEMA_DIR}/tdls-ai-vendor-declaration.schema.json">{SCHEMA_ID}</a></p>
<div class="tbl files"><table><thead><tr><th>File</th><th>What it is</th><th>SHA-256</th></tr></thead><tbody>{rows}</tbody></table></div>
<p>The text that defines the fields is <a href="/{V}/annex-a/">Annex A</a>. To validate a declaration, from a folder holding these files:</p>
<pre><code>python3 -m venv .venv</code></pre>
<pre><code>.venv/bin/pip install jsonschema rfc3339-validator</code></pre>
<pre><code>.venv/bin/python validate.py tdls-ai-vendor-declaration.schema.json example-declaration.json</code></pre>
<p>The last command prints <code>valid: example-declaration.json conforms to TDLS-AI Vendor Declaration (The Data Licensing Standard for AI, v0.1) ({SCHEMA_ID})</code>. A declaration that validates has the right fields; validation scores nothing.</p>"""
    (out / "schema").mkdir(exist_ok=True)
    sdesc = "The machine-readable vendor declaration of The Data Licensing Standard for AI, version 0.1: schema 0.3.0, example, validator and crosswalk."
    for p in ("schema", SCHEMA_DIR):
        stitle = f"The vendor declaration schema 0.3.0 · {fm['short_name']} {V}"
        sg = ld_page(f"{SITE}/schema/", stitle, sdesc, about=SCHEMA_ID, crumbs=[("Home", SITE + "/"), ("Schema", f"{SITE}/schema/")])
        sg += [{"@type": "MediaObject", "@id": SCHEMA_ID, "name": schema_json.get("title", "The vendor declaration schema"), "url": SCHEMA_ID,
                "contentUrl": SCHEMA_ID, "version": "0.3.0", "encodingFormat": "application/schema+json", "license": PART7, "isPartOf": {"@id": STD_ID},
                "author": {"@id": PERSON_ID}, "sha256": sha((out / SCHEMA_DIR / "tdls-ai-vendor-declaration.schema.json").read_bytes())},
               ld_standard(fm), ld_person(fm)]
        (out / p / "index.html").write_text(page(title=stitle, desc=sdesc, path="/schema/", body=schema_pg, current="/schema/", wide=True, fm=fm, ld=sg))

    vfiles = [("TDLS-AI-v0.1.pdf", "The document, 83 pages"), ("TDLS-AI-v0.1.md", "The Markdown source of the document's text"),
              ("TDLS-AI-v0.1.sha256", "The SHA-256 of the PDF and of the source text"),
              ("TDLS-AI-v0.1.tsr", "The RFC 3161 time-stamp token over the SHA-256 of the PDF"),
              ("TDLS-AI-v0.1.md.tsr", "The RFC 3161 time-stamp token over the SHA-256 of the source text")]
    vrows = "".join(f'<tr><td data-label="File"><a href="/{n}">{n}</a></td><td data-label="What it is">{e(d)}</td><td data-label="SHA-256" class="hash">{sha((out / n).read_bytes())}</td></tr>' for n, d in vfiles)
    dl = "".join(f"<pre><code>curl -O {SITE}/{n}</code></pre>" for n, _ in vfiles)
    verify = f"""<p class="kicker">{kick(fm["short_name"] + " " + V)} · The seal</p>
<h1>Verify the seal</h1>
<p>The two tokens were issued by DigiCert's time-stamp authority, signing certificate DigiCert SHA256 RSA4096 Timestamp Responder 2026 1, policy 2.16.840.1.114412.7.1, on 2026-11-24, at 19:19:59 UTC for the PDF and at 19:21:04 UTC for the source text.</p>
<div class="tbl files"><table><thead><tr><th>File</th><th>What it is</th><th>SHA-256 of the file served here</th></tr></thead><tbody>{vrows}</tbody></table></div>
<p>Download the five files into one folder:</p>
{dl}
<p>Check both files against <code>TDLS-AI-v0.1.sha256</code>:</p>
<pre><code>sha256sum -c TDLS-AI-v0.1.sha256</code></pre>
<p>It prints <code>TDLS-AI-v0.1.pdf: OK</code> and <code>TDLS-AI-v0.1.md: OK</code>.</p>
<p>Verify each token against its file. The root certificate is the self-signed DigiCert Trusted Root G4, SHA-256 fingerprint <span class="hash">55:2F:7B:DC:F1:A7:AF:9E:6C:E6:72:01:7F:4F:12:AB:F7:72:40:C7:8E:76:1A:C2:03:D1:D9:D2:0A:C8:99:88</span>. On Debian and Ubuntu the system store holds it at the path shown:</p>
<pre><code>openssl ts -verify -data TDLS-AI-v0.1.pdf -in TDLS-AI-v0.1.tsr -CAfile /etc/ssl/certs/DigiCert_Trusted_Root_G4.pem</code></pre>
<pre><code>openssl ts -verify -data TDLS-AI-v0.1.md -in TDLS-AI-v0.1.md.tsr -CAfile /etc/ssl/certs/DigiCert_Trusted_Root_G4.pem</code></pre>
<p>Each command prints <code>Verification: OK</code>, after a line on standard error that names OpenSSL's configuration file. On another system, use a PEM file of this root certificate in place of that path; the venue's README says how to check its fingerprint and how to read each token's time.</p>
<p><a href="/security-elements/">The security elements, and what each one does</a>: page 4 of the sealed PDF, word for word.</p>
<p>The same files, with the same SHA-256 values, are published at the venue: <a href="{VENUE}">{VENUE.replace("https://", "")}</a>, commit <span class="hash">{VENUE_COMMIT}</span>.</p>"""
    (out / "verify").mkdir()
    vtitle, vdesc = f"Verify the seal · {fm['short_name']} {V}", "Check the SHA-256 values and the RFC 3161 time-stamp tokens of The Data Licensing Standard for AI, version 0.1."
    (out / "verify" / "index.html").write_text(page(title=vtitle, desc=vdesc, path="/verify/", body=verify, current="/verify/", wide=True, fm=fm,
                                                    ld=ld_page(f"{SITE}/verify/", vtitle, vdesc, crumbs=[("Home", SITE + "/"), ("Verify the seal", f"{SITE}/verify/")]) + [ld_standard(fm), ld_person(fm)]))

    # the colophon, as printed on page 3 of the sealed PDF (checked word for word below)
    lic1, lic2 = fm["license"].split(". ", 1)
    colophon = [("this-edition", "01", "This edition"), ("about-the-author", "02", "About the author"), ("seal", "03", "Seal"),
                ("next-assessment", "04", "Next assessment"), ("cite-as", "05", "Cite as")]
    seal_txt = "At publication, the SHA-256 of the published PDF and the SHA-256 of the Markdown source are time-stamped under RFC 3161. The tokens, both hashes and the verification command are published beside this document. A reader verifies the seal without trusting the author."
    next_txt = "The first quarterly assessment of training-data diligence is published by 2027-02-14; its sections and method are fixed and sealed before the first issue."
    cite_txt = "Weeks, A. D. (2026). The Data Licensing Standard for AI (TDLS-AI) v0.1. Sealed on the date in the published time-stamp token. The schema (Annex A) is cited by its $id and version."
    hash_txt = "The build script reads the parameters of the engraved elements on the cover and of the band and thread from this hash; a changed text changes them."
    try:
        p3 = subprocess.run(["pdftotext", "-raw", "-f", "3", "-l", "3", str(a.venue / "TDLS-AI-v0.1.pdf"), "-"], capture_output=True, check=True).stdout.decode("utf-8")
    except (OSError, subprocess.CalledProcessError): die("pdftotext (poppler) is needed to check the colophon's words")
    for w in ["Colophon", "THIS EDITION", f"VERSION {V}", f"PUBLISHED {fm['date']}", f"SERIAL {fm['serial']}", f"LICENSE {fm['license']}",
              f"SOURCE SHA-256 {h}", hash_txt, "ABOUT THE AUTHOR", fm["author"], fm["credentials_full"], fm["capacity"],
              "SEAL", seal_txt, "NEXT ASSESSMENT", next_txt, "CITE AS", cite_txt]:
        if flat(w) not in flat(p3): die(f"the colophon does not carry: {w[:60]}")
    sec_h = lambda sid, n, t: f'<section class="colo" id="{sid}"><p class="num">{n}</p><h2>{t}</h2>'
    colo = f"""<p class="kicker">{kick(fm["short_name"] + " " + V)} · Colophon</p>
<h1>Colophon</h1>
<p class="note">As printed on page 3 of <a href="/TDLS-AI-v0.1.pdf#page=3">the sealed PDF</a>. The link in entry 03 is added by this site; the words are as printed. Page 4: <a href="/security-elements/">the security elements, and what each one does</a>.</p>
{sec_h(*colophon[0])}
<dl class="kv"><dt>Version</dt><dd>{V}</dd><dt>Published</dt><dd>{e(fm["date"])}</dd><dt>Serial</dt><dd>{e(fm["serial"])}</dd>
<dt>License</dt><dd>{e(lic1)}.<br>{e(lic2)}</dd><dt>Source SHA-256</dt><dd class="hash">{h}</dd></dl>
<p>{e(hash_txt)}</p></section>
{sec_h(*colophon[1])}
<p class="name">{e(fm["author"])}</p>
<p>{e(fm["credentials_full"])}</p>
<p>{e(fm["capacity"])}</p></section>
{sec_h(*colophon[2])}
<p>{e(seal_txt).replace("published beside this document", '<a href="/verify/">published beside this document</a>')}</p></section>
{sec_h(*colophon[3])}
<p>{e(next_txt).replace("by 2027-02-14", "<strong>by 2027-02-14</strong>")}</p></section>
{sec_h(*colophon[4])}
<p>{e(cite_txt)}</p></section>"""
    got = words(re.sub(r"<[^>]+>", " ", colo[colo.index('<section class="colo"'):]).lower())
    seg = flat(p3)[flat(p3).index("01 THIS EDITION"):]
    seg = seg[:seg.index(cite_txt) + len(cite_txt)]
    if got != words(seg.lower()): die("the colophon page's words differ from page 3 of the sealed PDF")
    (out / "colophon").mkdir()
    ctitle = f"Colophon · {fm['short_name']} {V}"
    cdesc2 = f"The colophon of {fm['title_display']} ({fm['short_name']}) {V}: this edition, about the author, the seal, the next assessment, and how to cite it."
    (out / "colophon" / "index.html").write_text(page(title=ctitle, desc=cdesc2, path="/colophon/", body=colo, current="/colophon/", fm=fm,
                                                      ld=ld_page(f"{SITE}/colophon/", ctitle, cdesc2, typ="AboutPage", about=PERSON_ID,
                                                                 crumbs=[("Home", SITE + "/"), ("Colophon", f"{SITE}/colophon/")]) + [ld_standard(fm), ld_person(fm, full=True)]))

    # page 4 of the sealed PDF, the security elements (his letter of 2026-11-25), set as printed and checked word for word
    try:
        p4 = subprocess.run(["pdftotext", "-raw", "-f", "4", "-l", "4", str(a.venue / "TDLS-AI-v0.1.pdf"), "-"], capture_output=True, check=True).stdout.decode("utf-8")
    except (OSError, subprocess.CalledProcessError): die("pdftotext (poppler) is needed to check page 4's words")
    p4 = "\n".join(l for l in p4.splitlines() if l.split() and not set(l.split()) <= {"AI", "ML", "EVAL"})   # the border's own words
    P4 = [("look", "Look", "at the engraving", [("device", "The engraved device on the cover"), ("face", "The face of the engraved device, enlarged")],
           [("Engraved device.", "The engraved device on the cover and Plate I is drawn by the build script, created by the author, of a carved neoclassical anthropomorphic mascaron sculpted in high relief; its line angle, hatch angles and dash period are read from the source hash, so the same text always produces the same engraving and a changed text changes it. Look for the fine hatch lines across the face."),
            ("Dissolve.", "On the cover, the device's two sides break into blocks placed by a generator seeded from the same hash. Look at either side of the device to see them.")]),
          ("magnify", "Magnify", "the microprint", [("microprint", "The microprint border, enlarged"), ("thread", "The thread, enlarged")],
           [("Thread.", "The thread at the edge of the body pages carries the first sixteen characters of the source hash as microtext. Under magnification it reads TDLS-AI v0.1 and those sixteen characters."),
            ("Border.", "The margins of the colophon carry the words AI, ML and EVAL in capitals 0.76 mm high, in rows of whole words inside a 0.4 mm rule. The border is drawn without the hash and is the same for any text.")]),
          ("compare", "Compare", "the hash", [("mark", "The square mark on the cover"), ("band", "The band at the head of a body page")],
           [("Hash marks.", "The band at the head of the body pages and the square mark on the cover are drawn from the source hash by the build script."),
            ("Source hash.", "The source hash on page 3 is the SHA-256 of the Markdown source published beside this document; its first sixteen characters appear again in the thread and at the foot of every body page. Compute the SHA-256 of the source and compare.")]),
          ("verify", "Verify", "the seal", None,
           [("Time-stamp tokens.", "The tokens are issued under RFC 3161, by the authority named beside them, over both hashes at publication. A reader can verify the seal with the published tokens and the authority's certificate, on trust in that authority."),
            ("Panel.", "The panel shows the source hash and the serial of this edition. The listings in Annex A, the running lines, and parts of the cover, Plate I, the colophon and the back page are set outside the source; the PDF's hash covers them.")])]
    p4_kick, p4_h1 = "THE SECURITY ELEMENTS, AND WHAT EACH ONE DOES", "Look, Magnify, Compare, Verify"
    p4_lead = "A reader checks this edition in four steps. Looking at the engraving and magnifying the microprint show that a copy carries the elements described here; comparing the hash and verifying the seal confirm the text and its date."
    def icon(key):      # each step icon at one scale, as on page 4, where each one's box is 46 points wide
        w, h = (int.from_bytes((here / "assets" / "security" / f"icon-{key}.png").read_bytes()[i:i + 4], "big") for i in (16, 20))
        return f'<img src="/assets/security/icon-{key}.png" alt="" class="ic" width="{round(w * 86 / 369)}" height="{round(h * 86 / 369)}">'
    def quad(key, step, what, figs, paras):
        fig = ("".join(f'<img src="/assets/security/{n}.{"png" if n in ("mark", "thread") else "webp"}" alt="{e(alt)}" class="f-{n}" loading="lazy" decoding="async">' for n, alt in figs)
               if figs else f'<div class="panel"><p>SOURCE SHA-256 · SEALED AT PUBLICATION</p><p class="hx">{h[:32]}<br>{h[32:]}</p><p>{e(fm["serial"])}</p></div>')
        return (f'<section class="q" id="{key}"><div class="qh">{icon(key)}<h2>{step} <span>{what}</span></h2></div>'
                f'<div class="figs">{fig}</div>' + "".join(f"<p><strong>{e(b)}</strong> {e(t)}</p>" for b, t in paras) + "</section>")
    p4_body = (f'<p class="p4k">{p4_kick}</p><h1>{p4_h1}</h1><p class="p4l">{e(p4_lead)}</p>'
               f'<div class="grid">{"".join(quad(*q) for q in P4)}</div>')
    if words(re.sub(r"<[^>]+>", " ", p4_body).lower()) != words(flat(p4).lower()): die("the security elements page's words differ from page 4 of the sealed PDF")
    sec4 = f"""<p class="kicker">{kick(fm["short_name"] + " " + V)} · Security elements</p>
<p class="note">From page 4 of <a href="/TDLS-AI-v0.1.pdf#page=4">the sealed PDF</a>. The words are as printed.</p>
<div class="mpf"><div class="mpi p4">{p4_body}</div></div>"""
    (out / "security-elements").mkdir()
    stitle = f"The security elements, and what each one does · {fm['short_name']} {V}"
    (out / "security-elements" / "index.html").write_text(page(title=stitle, desc=p4_lead, path="/security-elements/", body=sec4, wide=True, fm=fm,
                                                               ld=ld_page(f"{SITE}/security-elements/", stitle, p4_lead,
                                                                          crumbs=[("Home", SITE + "/"), ("The security elements", f"{SITE}/security-elements/")]) + [ld_standard(fm), ld_person(fm)]))

    nf = f"""<p class="kicker">404</p>
<h1>Nothing is published at this address</h1>
<p>The text of {e(fm["short_name"])} {V} is at <a href="/{V}/">/{V}/</a>, a page for each Part, Requirement and Annex.</p>
{toc_html()}"""
    (out / "404.html").write_text(page(title=f"Not found · {fm['short_name']} {V}", desc="Nothing is published at this address.",
                                       path="/404.html", body=nf, fm=fm, robots="noindex, follow"))

    # 6. robots.txt, llms.txt, sitemap, CNAME, .nojekyll
    p7 = next(t for i, *_, t in secs if i == "part-7")
    lic = re.search(r"(?m)^\*\*License\.\*\* (.+)$", p7).group(1)
    citation = re.search(r"(?m)^\*\*Citation\.\*\* (.+)$", p7).group(1)
    (out / "robots.txt").write_text(f"""# datalicensingstandard.org: The Data Licensing Standard for AI (TDLS-AI) {V}, by {fm["author"]}.
# Every crawler is welcome on every page, crawlers that gather text for AI models included.
# Terms (Part 7, License): {lic}
# Cite as: {citation}
# The whole sealed text: {SITE}/{SRC}
# A guide for language models: {SITE}/llms.txt

# The signal below speaks for the author's material, under Part 7's license and its exclusions; material quoted from the sources named in Annex B stays with its holders.

User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=yes
Allow: /

Sitemap: {SITE}/sitemap.xml
""")
    llms = [f"# {fm['title_display']} ({fm['short_name']}) {V}", "",
            f"> {fm['subtitle']}. {fm['version']}, {fm['date']}. {fm['author']}.", "",
            fm["scope_line"], "", fm["capacity"], "", conflict, "",
            f"Cite as: {citation}", "", f"License: {lic}", "",
            "## The document", "",
            f"- [The sealed source text]({SITE}/{SRC}): the whole document in Markdown, SHA-256 {h}",
            f"- [The PDF]({SITE}/TDLS-AI-v0.1.pdf): 83 pages, SHA-256 {SEALED['TDLS-AI-v0.1.pdf']}",
            f"- [Contents]({SITE}/{V}/): a page for each Part, Requirement and Annex",
            f"- [The whole text in one file]({SITE}/llms-full.txt): the sealed source, byte for byte, SHA-256 {h}",
            f"- [Colophon]({SITE}/colophon/): this edition, about the author, the seal, the next assessment, and how to cite it",
            f"- [The security elements, and what each one does]({SITE}/security-elements/): page 4 of the PDF, word for word", ""]
    for head, kinds in (("## Requirements", ("R",)), ("## Parts", ("Part",)), ("## Annexes", ("Annex",))):
        llms += [head, ""]
        llms += [f"- [{nav_title(kind, num, t)}]({SITE}/{V}/{sid}.md): cite as {cite(kind, num)}" for sid, kind, num, t in toc if kind in kinds]
        llms += [""]
    llms += ["## Schema", "",
             f"- [The vendor declaration schema 0.3.0]({SCHEMA_ID}): JSON Schema 2020-12, its $id",
             f"- [An example declaration]({SITE}/{SCHEMA_DIR}/example-declaration.json)",
             f"- [The crosswalk]({SITE}/{SCHEMA_DIR}/crosswalk-0.3.0.json): Annex A's crosswalk, machine-readable", "",
             "## Optional", "",
             f"- [Verify the seal]({SITE}/verify/): the SHA-256 values and the RFC 3161 tokens",
             f"- [The venue]({VENUE}): the same sealed files, commit {VENUE_COMMIT}", ""]
    (out / "llms.txt").write_text("\n".join(llms))
    (out / "llms-full.txt").write_bytes(md_bytes)                    # the sealed source, byte for byte, under the name AI tools look for
    pages = ["/", f"/{V}/"] + [f"/{V}/{s}/" for s, *_ in toc] + ["/schema/", "/verify/", "/colophon/", "/security-elements/"]
    files = [f"/{SRC}", "/TDLS-AI-v0.1.pdf", f"/{SCHEMA_DIR}/tdls-ai-vendor-declaration.schema.json"]
    (out / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "".join(f"<url><loc>{SITE}{u}</loc><lastmod>{BUILD_DATE}</lastmod></url>\n" for u in pages)
                                     + "".join(f"<url><loc>{SITE}{u}</loc><lastmod>2026-11-24</lastmod></url>\n" for u in files) + "</urlset>\n")
    (out / f"{INDEXNOW_KEY}.txt").write_text(INDEXNOW_KEY)
    (out / "CNAME").write_text("datalicensingstandard.org\n")
    (out / ".nojekyll").write_text("")

    # 7. no third party: every src and href on every page is on this site, the venue, or a named source address
    for f in out.rglob("*.html"):
        t = f.read_text()
        if t.count(f'<meta http-equiv="Content-Security-Policy" content="{csp(f == out / "index.html")}">') != 1: die(f"{f}: no security policy, or the wrong one")
        if re.search(r'\sstyle="', t): die(f"{f}: an inline style")
        if re.search(r'\son[a-z]+="', t) or "javascript:" in t: die(f"{f}: an inline handler or a javascript: address")
        if t.count(CSS_LINK) != 1: die(f"{f}: the stylesheet without its integrity hash")
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
        if len(blocks) > 1: die(f"{f}: more than one block of structured data")
        for b in blocks:
            try: json.loads(b)
            except ValueError as x: die(f"{f}: structured data that does not parse: {x}")
        t = re.sub(r'<script type="application/ld\+json">.*?</script>', "", t, flags=re.S)
        n_script = t.count("<script")
        if f == out / "index.html":
            if n_script != 1 or t.count(HERO_SCRIPT) != 1: die(f"{f}: the home page carries a script other than {HERO_SCRIPT}")
        elif n_script: die(f"{f}: a script")
        for tag in re.findall(r"<(?:img|link|iframe|source|video|audio|embed|object)\b[^>]*>", t):
            for u in re.findall(r'(?:src|href)="([^"]+)"', tag):
                if u.startswith("/") or u.startswith(SITE + "/"): continue
                die(f"{f}: a resource from another host: {u}")
    if re.search(r"url\((?!fonts/|mark\.svg|security/microprint-frame\.png\))", (out / "assets" / names["site.css"]).read_text()): die("site.css loads from elsewhere")
    if re.search(r"https?://", (out / "assets" / names["hero.js"]).read_text()): die("hero.js names another host")
    print(f"built {sum(1 for _ in out.rglob('*') if _.is_file())} files into {out}; source SHA-256 {h}; {len(secs)} sections; checks passed")

if __name__ == "__main__":
    main()
