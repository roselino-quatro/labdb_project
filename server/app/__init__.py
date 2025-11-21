from flask import Flask

from app.config import AppConfig
from app.extensions import register_extensions
from app.routes import register_routes
from app.templating.context_processors import register_context_processors
from app.templating.url_helpers import register_url_helpers


def create_app(config_class: type[AppConfig] | None = None) -> Flask:
    app = Flask(__name__)

    config_object = config_class or AppConfig
    app.config.from_object(config_object)

    register_extensions(app)
    register_routes(app)
    register_context_processors(app)
    register_url_helpers(app)

    return app
