"""
Generate a static site in /docs for GitHub Pages deployment.

    python build.py

Renders all pages using seed data directly (no MongoDB needed), copies
static assets, and writes api/gallery.json for the gallery JS to fetch.
"""
import json
import os
import shutil

# ── paths ────────────────────────────────────────────────────────────────────
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)          # Tanaghom Gardenia/
DOCS = os.path.join(ROOT, "docs")
STATIC_SRC = os.path.join(ROOT, "frontend", "static")

# ── import seed data directly (no DB needed) ─────────────────────────────────
from seed import SITE, EVENTS, CHOIRS, VALUES, TIMELINE, LEADERSHIP, GALLERY

# ── create Flask app (templates only, no DB routes called) ───────────────────
from app import create_app

flask_app = create_app()


def fix_paths(html):
    """Rewrite server-absolute paths to relative for static hosting."""
    html = html.replace('href="/static/', 'href="static/')
    html = html.replace('src="/static/',  'src="static/')
    html = html.replace('href="/"',       'href="index.html"')
    html = html.replace('href="/about"',  'href="about.html"')
    html = html.replace('href="/choirs"', 'href="choirs.html"')
    html = html.replace('href="/gallery"','href="gallery.html"')
    return html


os.makedirs(DOCS, exist_ok=True)

# ── render pages ─────────────────────────────────────────────────────────────
with flask_app.test_request_context():
    from flask import render_template

    pages = [
        ("index.html",  "index.html",  "home",    dict(
            site=SITE,
            stats=SITE.get("home_stats", []),
            choirs=sorted(CHOIRS, key=lambda c: c["order"]),
            events=sorted(EVENTS, key=lambda e: e["order"]),
        )),
        ("about.html",  "about.html",  "about",   dict(
            site=SITE,
            values=sorted(VALUES,    key=lambda v: v["order"]),
            timeline=sorted(TIMELINE, key=lambda t: t["order"]),
            stats=SITE.get("about_stats", []),
            leadership=sorted(LEADERSHIP, key=lambda l: l["order"]),
        )),
        ("choirs.html", "choirs.html", "choirs",  dict(
            site=SITE,
            choirs=sorted(CHOIRS, key=lambda c: c["order"]),
        )),
        ("gallery.html","gallery.html","gallery", dict(
            site=SITE,
            moment_count=len(GALLERY),
        )),
    ]

    for template, outfile, active, ctx in pages:
        html = render_template(template, active=active, **ctx)
        with open(os.path.join(DOCS, outfile), "w", encoding="utf-8") as f:
            f.write(fix_paths(html))
        print(f"  {outfile}")

# ── copy static assets ────────────────────────────────────────────────────────
dst_static = os.path.join(DOCS, "static")
if os.path.exists(dst_static):
    shutil.rmtree(dst_static)
shutil.copytree(STATIC_SRC, dst_static)
print("  static/")

# ── patch gallery.page.js to fetch the static JSON instead of /api/gallery ───
gallery_js = os.path.join(dst_static, "js", "gallery.page.js")
with open(gallery_js, encoding="utf-8") as f:
    js = f.read()
js = js.replace("fetch('/api/gallery')", "fetch('api/gallery.json')")
with open(gallery_js, "w", encoding="utf-8") as f:
    f.write(js)

# ── write gallery JSON (replaces the /api/gallery endpoint) ──────────────────
def clean(doc):
    d = dict(doc)
    d.pop("_id", None)
    return d

api_dir = os.path.join(DOCS, "api")
os.makedirs(api_dir, exist_ok=True)
with open(os.path.join(api_dir, "gallery.json"), "w", encoding="utf-8") as f:
    json.dump(
        [clean(m) for m in sorted(GALLERY, key=lambda g: g["order"])],
        f, ensure_ascii=False, indent=2,
    )
print("  api/gallery.json")

print(f"\nDone — static site in: {DOCS}")
