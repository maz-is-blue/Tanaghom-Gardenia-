"""Flask application factory for Tanaghom Gardenia."""
import os
from flask import Flask

from .config import Config
from . import db

# backend/app/ → backend/ → tanaghom_app/
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_app(config_object=Config):
    app = Flask(
        __name__,
        template_folder=os.path.join(_project_root, "frontend", "templates"),
        static_folder=os.path.join(_project_root, "frontend", "static"),
    )
    app.config.from_object(config_object)

    app.teardown_appcontext(db.close_db)

    from .routes.pages import pages_bp
    from .routes.api import api_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
