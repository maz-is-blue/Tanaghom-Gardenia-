# Tanaghom Gardenia — Choral Society

A bilingual (English / Arabic) website for the Tanaghom Gardenia choral society,
rebuilt from static HTML into a deployable **Python (Flask) + MongoDB** application
with a clean separation of frontend and backend.

The original design — fonts, layout, animations, the custom cursor, the gallery
lightbox, the choir audio-player visualisations — is preserved exactly. The
content (events, choirs, gallery, timeline, leadership, site settings) now lives
in MongoDB and is served through the backend.

## Architecture

```
Browser ──▶ Flask
            ├─ Server-rendered pages (Jinja2)         /  /about  /choirs  /gallery
            │    content pulled from MongoDB
            ├─ JSON REST API                          /api/gallery /api/events
            │    consumed by frontend JS               /api/choirs  /api/submissions
            └─ Static assets (CSS / JS / fonts / img)
                       │
                       ▼
                   MongoDB   (site, events, choirs, gallery,
                              values, timeline, leadership, submissions)
```

- **Backend** — `app/` (Flask application factory, Mongo connection, page +
  API blueprints).
- **Frontend** — `app/templates/` (Jinja2) and `app/static/`
  (`css/fonts.css`, `css/theme.css`, `css/custom.css`, shared `js/app.js`, and
  per-page scripts). All the original inline CSS and JS were extracted into these
  files.
- **Data** — `seed.py` populates MongoDB with all site content.

## Project layout

```
tanaghom_app/
├─ app/
│  ├─ __init__.py          app factory
│  ├─ config.py            env-driven config
│  ├─ db.py                MongoDB connection
│  ├─ routes/
│  │  ├─ pages.py          server-rendered pages
│  │  └─ api.py            JSON REST API + form submissions
│  ├─ templates/           base.html + index/about/choirs/gallery/404
│  └─ static/              css, js, fonts, img
├─ seed.py                 load content into MongoDB
├─ run.py                  dev server entrypoint
├─ wsgi.py                 gunicorn entrypoint
├─ requirements.txt
├─ Dockerfile
└─ docker-compose.yml
```

## Run with Docker (recommended)

```bash
cp .env.example .env            # edit SECRET_KEY
docker compose up -d --build    # starts mongo + web
docker compose run --rm seed    # one-time: load content
# open http://localhost:8000
```

## Run locally (without Docker)

Requires Python 3.10+ and a MongoDB instance (local or Atlas).

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # set MONGO_URI if not localhost

python seed.py                  # load content into MongoDB
python run.py                   # http://localhost:5000
```

For production:

```bash
# Linux / macOS / Docker
gunicorn --bind 0.0.0.0:8000 --workers 3 wsgi:app

# Windows (gunicorn has no Windows support)
waitress-serve --listen=0.0.0.0:8000 wsgi:app
```

## API

| Method | Endpoint            | Description                                   |
|--------|---------------------|-----------------------------------------------|
| GET    | `/api/gallery`      | Gallery moments (drives the gallery grid).    |
| GET    | `/api/events`       | Upcoming season events.                        |
| GET    | `/api/choirs`       | Both ensembles with full detail.               |
| POST   | `/api/submissions`  | Audition / patron / contact form submissions.  |

`POST /api/submissions` body (JSON):

```json
{ "name": "Jane Doe", "email": "jane@example.com", "message": "Soprano…", "kind": "audition" }
```

Submissions are stored in the `submissions` collection with a timestamp.

## Editing content

All content lives in MongoDB. Edit `seed.py` and re-run `python seed.py`, or update
documents directly (e.g. with `mongosh` or MongoDB Compass). Collections:
`site`, `events`, `choirs`, `gallery`, `values`, `timeline`, `leadership`.

## Notes

- The gallery photographs are stylised SVG placeholders (as in the original
  design). To use real images, add an `image` URL to each `gallery` document and
  extend `bgFor()` in `app/static/js/gallery.page.js`.
- Fonts (Inter, Playfair Display, Noto Naskh Arabic) are self-hosted in
  `app/static/fonts/` — no external font CDN calls.
```
