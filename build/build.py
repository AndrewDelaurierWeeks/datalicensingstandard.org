#!/usr/bin/env python3
"""Build datalicensingstandard.org from the sealed files of The Data Licensing Standard for AI (TDLS-AI) v0.1.

    python3 build/build.py --venue PATH_TO_VENUE_CHECKOUT --out docs

The venue is https://github.com/AndrewDelaurierWeeks/data-licensing-standard at commit b1fc951. Every sealed
file is copied byte for byte and checked against the SHA-256 pinned below; the build stops on any difference.
Each Part, Requirement and Annex gets a page at https://datalicensingstandard.org/v0.1/<id>/ whose sealed block
is that section's text, and a Markdown copy at /v0.1/<id>.md that is the section's bytes. The build checks that
the Markdown copies put together give back the sealed source byte for byte, and that the words of every page's
sealed block equal the words of its section. Needs Python 3.9 or later and pandoc 3."""
import argparse, hashlib, html, json, re, shutil, subprocess, sys
from pathlib import Path

SITE = "https://datalicensingstandard.org"
VENUE = "https://github.com/AndrewDelaurierWeeks/data-licensing-standard"
VENUE_COMMIT = "b1fc9519da44f08e82a0f5727b213a084cecf46f"
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

# ------------------------------------------------------------------ the page frame
NAV = [("/", "Home"), (f"/{V}/", "Contents"), (f"/{V}/part-4/", "Questions"), (f"/{V}/part-5/", "Scoring"),
       ("/schema/", "Schema"), ("/verify/", "Verify"), ("/TDLS-AI-v0.1.pdf", "PDF")]

def page(*, title, desc, path, body, current=None, wide=False, fm):
    nav = "".join(f'<a href="{u}"{" aria-current=\"page\"" if u == current else ""}>{t}</a>' for u, t in NAV)
    canon = f"{SITE}{path}"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<link rel="stylesheet" href="/assets/site.css">
<link rel="icon" href="/assets/mark.svg" type="image/svg+xml">
<link rel="alternate" type="text/markdown" href="/{SRC}" title="The sealed source text">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:type" content="website">
</head>
<body>
<a class="skip" href="#main">Skip to the text</a>
<div class="band" aria-hidden="true"><i></i></div>
<header class="site">
<a class="brand" href="/"><span class="mk" aria-hidden="true"></span><span><b>{e(fm["title_display"])}</b><small>{e(fm["short_name"])} {V}</small></span></a>
<nav class="top" aria-label="Site">{nav}</nav>
</header>
<main id="main"{' class="wide"' if wide else ""}>
{body}
</main>
<footer class="site"><div class="in">
<p>{e(fm["capacity"])}</p>
<p>{CONFLICT_HTML}</p>
<p>{e(fm["license"])} Full terms: <a href="/{V}/part-7/">Part 7</a>.</p>
<p>The sealed files are the authority for this text: <a href="/verify/">verify them</a>. Venue: <a href="{VENUE}">{VENUE.replace("https://", "")}</a>, commit <span class="hash">{VENUE_COMMIT[:7]}</span>.</p>
</div></footer>
</body>
</html>
"""

CONFLICT_HTML = ""        # set in main(): Part 0's conflict disclosure, as sealed

# ------------------------------------------------------------------ build
def main():
    global CONFLICT_HTML
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
    CONFLICT_HTML = pandoc(conflict, "html5").strip().removeprefix("<p>").removesuffix("</p>")

    # 2. assets
    (out / "assets").mkdir()
    shutil.copytree(here / "assets" / "fonts", out / "assets" / "fonts")
    shutil.copy(here / "assets" / "site.css", out / "assets" / "site.css")
    shutil.copy(here / "assets" / "band.svg", out / "assets" / "band.svg")
    if h not in (out / "assets" / "band.svg").read_text(): die("band.svg was not drawn from this source hash")
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
        frag = heading_ids(frag, sid)
        frag = dress_tables(frag, sid)
        frag = link_refs(frag, sid)
        prev = secs[k - 1] if k else None
        nxt = secs[k + 1] if k + 1 < len(secs) else None
        pn = '<nav class="pn" aria-label="Sections">'
        if prev: pn += f'<a class="prev" href="/{V}/{prev[0]}/">Previous: {e(nav_title(prev[1], prev[2], prev[3]))}</a>'
        if nxt: pn += f'<a class="next" href="/{V}/{nxt[0]}/">Next: {e(nav_title(nxt[1], nxt[2], nxt[3]))}</a>'
        pn += "</nav>"
        addr = f"{SITE}/{V}/{sid}/"
        body = f"""<p class="kicker">{e(cite(kind, num))}</p>
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
        desc = f"{cite(kind, num)}: {t}. The Data Licensing Standard for AI, version 0.1, sealed 2026-11-24."
        (out / V / sid / "index.html").write_text(page(title=title, desc=desc, path=f"/{V}/{sid}/", body=body,
                                                        current=f"/{V}/{sid}/" if sid in ("part-4", "part-5") else None,
                                                        wide=sid in ("part-4", "part-5", "annex-a"), fm=fm))
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
    contents = f"""<p class="kicker">{e(fm["short_name"])} {V} · Contents</p>
<h1>Contents</h1>
<p>Each Part, Requirement and Annex of the sealed text has its own page and a Markdown copy. {e(fm["short_name"])} {V} R8 is at <a href="/{V}/r8/">/{V}/r8/</a>; question 10 of Part 4 is at <a href="/{V}/part-4/#q10">/{V}/part-4/#q10</a>.</p>
{toc_html()}
<p class="note">{version_line}. The whole source: <a href="/{SRC}">{SRC}</a>. The PDF: <a href="/TDLS-AI-v0.1.pdf">TDLS-AI-v0.1.pdf</a>, 83 pages.</p>"""
    (out / V / "index.html").write_text(page(title=f"Contents · {fm['short_name']} {V}", desc="The Parts, Requirements and Annexes of The Data Licensing Standard for AI, version 0.1, each at its own address.",
                                             path=f"/{V}/", body=contents, current=f"/{V}/", fm=fm))

    home = f"""<div class="hero">
<span class="mk" aria-hidden="true"></span>
<div>
<p class="serial">{e(fm["serial"])}</p>
<h1>{e(fm["title_display"])}</h1>
<p class="sub">{e(fm["subtitle"])}</p>
<p class="scope">{e(fm["scope_line"])}</p>
<p class="meta">{version_line}</p>
</div>
</div>
<div class="tiers">
<div><b>D</b><span>Declared</span><p>The vendor states it, in the schema's fields, with a named person and a date.</p></div>
<div><b>M</b><span>Measured</span><p>A measurement backs it, made by the vendor or verified by the buyer.</p></div>
<div><b>A</b><span>Attested</span><p>An independent party attests the measurement and signs it.</p></div>
</div>
<p class="note">The tiers as the document defines them, with their conditions: <a href="/{V}/part-3/">Part 3</a>.</p>
<div class="actions">
<a class="btn primary" href="/TDLS-AI-v0.1.pdf">The document, PDF, 83 pages</a>
<a class="btn" href="/{V}/part-4/">The vendor questionnaire</a>
<a class="btn" href="/{V}/part-5/">The scoring sheet</a>
<a class="btn" href="/schema/">The schema</a>
<a class="btn" href="/verify/">Verify the seal</a>
</div>
<p>Attach Part 4 to every request for proposal; keep Part 5 where the buyer's counsel directs.</p>
<h2>The text, section by section</h2>
<p>Each Part, Requirement and Annex has its own page, at /{V}/&lt;id&gt;/, with a Markdown copy of its sealed text.</p>
{toc_html()}
<h2>Cite as</h2>
<p>{inline_md(re.search(r"(?m)^\*\*Citation\.\*\* (.+)$", next(t for i, *_, t in secs if i == "part-7")).group(1))}</p>
<h2>This edition</h2>
<p>{e(re.search(r"(?m)^\*\*Version\.\*\* (v0\.1, 2026-11-24, public draft for adoption\. It supersedes the edition sealed on 2026-11-16\.)", next(t for i, *_, t in secs if i == "part-7")).group(1))} That edition's source has the SHA-256 <span class="hash">{V0_SHA}</span>, and it is archived at <a href="{V0_ARCHIVE}">{V0_ARCHIVE.replace("https://", "")}</a>.</p>"""
    if "Attach Part 4 to every request for proposal; keep Part 5 where the buyer's counsel directs." not in home:
        die("home action line")
    (out / "index.html").write_text(page(title=f"{fm['title_display']} ({fm['short_name']}) {V}",
                                         desc=f"{fm['subtitle']}. {fm['scope_line']}", path="/", body=home, current="/", fm=fm))

    sfiles = [("tdls-ai-vendor-declaration.schema.json", "The vendor declaration schema (JSON Schema 2020-12), version 0.3.0"),
              ("example-declaration.json", "An example declaration"),
              ("validate.py", "The validator, with the converter for a record in the form of OASIS Data Provenance Metadata Version 1.0, Committee Specification Draft 01"),
              ("crosswalk-0.3.0.json", "The crosswalk of Annex A, machine-readable"),
              ("LICENSE", "The MIT License of the schema, the example, the validator and the crosswalk file")]
    rows = "".join(f'<tr><td data-label="File"><a href="/{SCHEMA_DIR}/{n}">{n}</a></td><td data-label="What it is">{e(d)}</td><td data-label="SHA-256" class="hash">{sha((out / SCHEMA_DIR / n).read_bytes())}</td></tr>' for n, d in sfiles)
    schema_pg = f"""<p class="kicker">{e(fm["short_name"])} {V} · Annex A</p>
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
    for p in ("schema", SCHEMA_DIR):
        (out / p / "index.html").write_text(page(title=f"The vendor declaration schema 0.3.0 · {fm['short_name']} {V}",
                                                 desc="The machine-readable vendor declaration of The Data Licensing Standard for AI, version 0.1: schema 0.3.0, example, validator and crosswalk.",
                                                 path=f"/{p}/", body=schema_pg, current="/schema/", wide=True, fm=fm))

    vfiles = [("TDLS-AI-v0.1.pdf", "The document, 83 pages"), ("TDLS-AI-v0.1.md", "The Markdown source of the document's text"),
              ("TDLS-AI-v0.1.sha256", "The SHA-256 of the PDF and of the source text"),
              ("TDLS-AI-v0.1.tsr", "The RFC 3161 time-stamp token over the SHA-256 of the PDF"),
              ("TDLS-AI-v0.1.md.tsr", "The RFC 3161 time-stamp token over the SHA-256 of the source text")]
    vrows = "".join(f'<tr><td data-label="File"><a href="/{n}">{n}</a></td><td data-label="What it is">{e(d)}</td><td data-label="SHA-256" class="hash">{sha((out / n).read_bytes())}</td></tr>' for n, d in vfiles)
    dl = "".join(f"<pre><code>curl -O {SITE}/{n}</code></pre>" for n, _ in vfiles)
    verify = f"""<p class="kicker">{e(fm["short_name"])} {V} · The seal</p>
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
<p>The same files, with the same SHA-256 values, are published at the venue: <a href="{VENUE}">{VENUE.replace("https://", "")}</a>, commit <span class="hash">{VENUE_COMMIT}</span>.</p>"""
    (out / "verify").mkdir()
    (out / "verify" / "index.html").write_text(page(title=f"Verify the seal · {fm['short_name']} {V}",
                                                    desc="Check the SHA-256 values and the RFC 3161 time-stamp tokens of The Data Licensing Standard for AI, version 0.1.",
                                                    path="/verify/", body=verify, current="/verify/", wide=True, fm=fm))

    nf = f"""<p class="kicker">404</p>
<h1>Nothing is published at this address</h1>
<p>The text of {e(fm["short_name"])} {V} is at <a href="/{V}/">/{V}/</a>, a page for each Part, Requirement and Annex.</p>
{toc_html()}"""
    (out / "404.html").write_text(page(title=f"Not found · {fm['short_name']} {V}", desc="Nothing is published at this address.",
                                       path="/404.html", body=nf, fm=fm))

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
            f"- [Contents]({SITE}/{V}/): a page for each Part, Requirement and Annex", ""]
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
    urls = ["/", f"/{V}/"] + [f"/{V}/{s}/" for s, *_ in toc] + ["/schema/", "/verify/", f"/{SRC}", "/TDLS-AI-v0.1.pdf", f"/{SCHEMA_DIR}/tdls-ai-vendor-declaration.schema.json"]
    (out / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "".join(f"<url><loc>{SITE}{u}</loc><lastmod>2026-11-24</lastmod></url>\n" for u in urls) + "</urlset>\n")
    (out / "CNAME").write_text("datalicensingstandard.org\n")
    (out / ".nojekyll").write_text("")

    # 7. no third party: every src and href on every page is on this site, the venue, or a named source address
    for f in out.rglob("*.html"):
        t = f.read_text()
        if "<script" in t: die(f"{f}: a script")
        for tag in re.findall(r"<(?:img|link|iframe|source|video|audio|embed|object)\b[^>]*>", t):
            for u in re.findall(r'(?:src|href)="([^"]+)"', tag):
                if u.startswith("/") or u.startswith(SITE + "/"): continue
                die(f"{f}: a resource from another host: {u}")
    if re.search(r"url\((?!fonts/|band\.svg|mark\.svg)", (out / "assets" / "site.css").read_text()): die("site.css loads from elsewhere")
    print(f"built {sum(1 for _ in out.rglob('*') if _.is_file())} files into {out}; source SHA-256 {h}; {len(secs)} sections; checks passed")

if __name__ == "__main__":
    main()
