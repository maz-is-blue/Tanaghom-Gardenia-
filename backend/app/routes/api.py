"""JSON REST API consumed by the frontend JS and available to integrators."""
import datetime as dt

from flask import Blueprint, jsonify, request, current_app

from ..db import get_db

api_bp = Blueprint("api", __name__)


@api_bp.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = current_app.config["CORS_ORIGINS"]
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


def clean(doc):
    """Drop the Mongo _id (or stringify it) for JSON responses."""
    if doc is None:
        return None
    doc = dict(doc)
    _id = doc.pop("_id", None)
    if isinstance(_id, str):
        doc.setdefault("key", _id)
    return doc


@api_bp.route("/gallery")
def gallery():
    items = [clean(m) for m in get_db().gallery.find().sort("order", 1)]
    return jsonify(items)


@api_bp.route("/events")
def events():
    items = [clean(e) for e in get_db().events.find().sort("order", 1)]
    return jsonify(items)


@api_bp.route("/choirs")
def choirs():
    items = [clean(c) for c in get_db().choirs.find().sort("order", 1)]
    return jsonify(items)


@api_bp.route("/submissions", methods=["POST", "OPTIONS"])
def create_submission():
    """Audition / contact / patron requests from the various CTAs."""
    if request.method == "OPTIONS":
        return ("", 204)

    data = request.get_json(silent=True) or request.form.to_dict()
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    if not name or not email:
        return jsonify({"ok": False, "error": "name and email are required"}), 400

    doc = {
        "name": name,
        "email": email,
        "message": (data.get("message") or "").strip(),
        "kind": (data.get("kind") or "contact").strip(),  # audition|patron|press|contact
        "created_at": dt.datetime.utcnow(),
    }
    result = get_db().submissions.insert_one(doc)
    return jsonify({"ok": True, "id": str(result.inserted_id)}), 201
