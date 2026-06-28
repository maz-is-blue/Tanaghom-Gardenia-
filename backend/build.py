#!/usr/bin/env python
"""
build.py — Render Flask templates to static HTML for GitHub Pages.
Run from the project root: python backend/build.py
"""
import os
import sys
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import create_app

ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR   = os.path.join(ROOT, 'docs')
STATIC_SRC = os.path.join(ROOT, 'frontend', 'static')
STATIC_DST = os.path.join(DOCS_DIR, 'static')

# GitHub Pages serves this repo at /Tanaghom-Gardenia-/
BASE = '/Tanaghom-Gardenia-'

PAGES = [
    ('/',        'index.html'),
    ('/about',   'about/index.html'),
    ('/choirs',  'choirs/index.html'),
    ('/gallery', 'gallery/index.html'),
]

REPLACEMENTS = [
    # Static asset paths (from url_for)
    ('href="/static/',   f'href="{BASE}/static/'),
    ('src="/static/',    f'src="{BASE}/static/'),
    # Navigation hrefs
    ('href="/"',         f'href="{BASE}/"'),
    ('href="/about"',    f'href="{BASE}/about/"'),
    ('href="/choirs"',   f'href="{BASE}/choirs/"'),
    ('href="/choirs#',   f'href="{BASE}/choirs/#'),
    ('href="/gallery"',  f'href="{BASE}/gallery/"'),
    ('href="/contact"',  f'href="{BASE}/contact/"'),
    ('href="/#',         f'href="{BASE}/#'),
]

def fix_paths(html):
    for old, new in REPLACEMENTS:
        html = html.replace(old, new)
    return html

def build():
    # Recreate docs/ from scratch
    if os.path.exists(DOCS_DIR):
        shutil.rmtree(DOCS_DIR)
    os.makedirs(DOCS_DIR)

    # Skip Jekyll processing
    open(os.path.join(DOCS_DIR, '.nojekyll'), 'w').close()

    # Copy static assets
    shutil.copytree(STATIC_SRC, STATIC_DST)
    print('Copied frontend/static/ -> docs/static/')

    # Render each page via Flask test client
    app = create_app()
    with app.test_client() as client:
        for url, out_path in PAGES:
            resp = client.get(url)
            html = fix_paths(resp.data.decode('utf-8'))

            dest = os.path.join(DOCS_DIR, out_path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'Built  {url:12s}  ->  docs/{out_path}')

    print('\nBuild complete.')

if __name__ == '__main__':
    build()
