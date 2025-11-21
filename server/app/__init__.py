from flask import Flask

from app.config import AppConfig
from app.extensions import register_extensions
from app.routes import register_routes


def create_app(config_class: type[AppConfig] | None = None) -> Flask:
    app = Flask(__name__)

    config_object = config_class or AppConfig
    app.config.from_object(config_object)

    register_extensions(app)
    register_routes(app)

    return app
