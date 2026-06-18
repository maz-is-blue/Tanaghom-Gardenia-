"""Server-rendered pages. Content is pulled from MongoDB and passed to Jinja2."""
from flask import Blueprint, render_template, abort

from ..db import get_db

pages_bp = Blueprint("pages", __name__)


def site():
    """Shared site settings (brand, nav, footer, contact). Always present."""
    return get_db().site.find_one({"_id": "settings"}) or {}


@pages_bp.route("/")
def home():
    db = get_db()
    s = site()
    return render_template(
        "index.html",
        site=s,
        stats=s.get("home_stats", []),
        choirs=list(db.choirs.find().sort("order", 1)),
        events=list(db.events.find().sort("order", 1)),
        active="home",
    )


@pages_bp.route("/about")
def about():
    db = get_db()
    s = site()
    return render_template(
        "about.html",
        site=s,
        values=list(db.values.find().sort("order", 1)),
        timeline=list(db.timeline.find().sort("order", 1)),
        stats=s.get("about_stats", []),
        leadership=list(db.leadership.find().sort("order", 1)),
        active="about",
    )


@pages_bp.route("/choirs")
def choirs():
    db = get_db()
    return render_template(
        "choirs.html",
        site=site(),
        choirs=list(db.choirs.find().sort("order", 1)),
        active="choirs",
    )


@pages_bp.route("/gallery")
def gallery():
    # Moments are loaded by the client from /api/gallery so filtering stays
    # snappy; we still pass the total for the initial server-rendered count.
    db = get_db()
    return render_template(
        "gallery.html",
        site=site(),
        moment_count=db.gallery.count_documents({}),
        active="gallery",
    )


@pages_bp.app_errorhandler(404)
def not_found(e):
    return render_template("404.html", site=site(), active=""), 404
