#!/usr/bin/env python
"""
build.py — Render Flask templates to static HTML.

Usage:
  python backend/build.py            # GitHub Pages (outputs to docs/)
  python backend/build.py --domain   # Custom domain (outputs to dist/, no prefix)
"""
import os
import sys
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import create_app

ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_SRC = os.path.join(ROOT, 'frontend', 'static')

PAGES = [
    ('/',        'index.html'),
    ('/about',   'about/index.html'),
    ('/choirs',  'choirs/index.html'),
    ('/gallery', 'gallery/index.html'),
]

def make_replacements(base):
    return [
        ('href="/static/',   f'href="{base}/static/'),
        ('src="/static/',    f'src="{base}/static/'),
        ('href="/"',         f'href="{base}/"'),
        ('href="/about"',    f'href="{base}/about/"'),
        ('href="/choirs"',   f'href="{base}/choirs/"'),
        ('href="/choirs#',   f'href="{base}/choirs/#'),
        ('href="/gallery"',  f'href="{base}/gallery/"'),
        ('href="/contact"',  f'href="{base}/contact/"'),
        ('href="/#',         f'href="{base}/#'),
    ]

def fix_paths(html, replacements):
    for old, new in replacements:
        html = html.replace(old, new)
    return html

def build(out_dir, base):
    replacements = make_replacements(base)

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    open(os.path.join(out_dir, '.nojekyll'), 'w').close()

    shutil.copytree(STATIC_SRC, os.path.join(out_dir, 'static'))
    print(f'Copied frontend/static/ -> {os.path.basename(out_dir)}/static/')

    app = create_app()
    with app.test_client() as client:
        for url, out_path in PAGES:
            resp = client.get(url)
            html = fix_paths(resp.data.decode('utf-8'), replacements)
            dest = os.path.join(out_dir, out_path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f'Built  {url:12s}  ->  {os.path.basename(out_dir)}/{out_path}')

    print('\nBuild complete.')

if __name__ == '__main__':
    if '--domain' in sys.argv:
        # For tanaghomgardenia.org — no path prefix needed
        build(os.path.join(ROOT, 'dist'), '')
    else:
        # For GitHub Pages at /Tanaghom-Gardenia-/
        build(os.path.join(ROOT, 'docs'), '/Tanaghom-Gardenia-')
