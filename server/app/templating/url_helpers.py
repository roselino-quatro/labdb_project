from typing import Any

from flask import Flask, url_for
from werkzeug.routing import BuildError

def register_url_helpers(app: Flask) -> None:
    @app.template_global()
    def build_url(endpoint: str, **values: Any) -> str | None:
        try:
            return url_for(endpoint, **values)
        except BuildError:
            app.logger.warning(
                "Failed to build URL for endpoint '%s' with params %s",
                endpoint,
                values,
            )
            return None
