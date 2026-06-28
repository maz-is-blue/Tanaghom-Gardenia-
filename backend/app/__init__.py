import os
from flask import Flask
from .config import Config

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_app(config_object=Config):
    app = Flask(
        __name__,
        template_folder=os.path.join(_root, 'frontend', 'templates'),
        static_folder=os.path.join(_root, 'frontend', 'static'),
    )
    app.config.from_object(config_object)
    from .routes.pages import pages_bp
    app.register_blueprint(pages_bp)
    return app
