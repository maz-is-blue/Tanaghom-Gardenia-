"""MongoDB connection helper.

A single PyMongo client is created lazily and shared across the app. Collection
accessors return live handles so routes/seed scripts stay terse.
"""
from flask import current_app, g
from pymongo import MongoClient


def get_db():
    """Return the application's MongoDB database, creating the client once."""
    if "mongo_client" not in g:
        g.mongo_client = MongoClient(current_app.config["MONGO_URI"])
        g.mongo_db = g.mongo_client[current_app.config["MONGO_DB"]]
    return g.mongo_db


def close_db(exception=None):
    client = g.pop("mongo_client", None)
    if client is not None:
        client.close()


def connect(uri, name):
    """Standalone connection (used by seed scripts outside an app context)."""
    return MongoClient(uri)[name]
