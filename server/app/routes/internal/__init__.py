from flask import Blueprint

internal_blueprint = Blueprint("internal", __name__, url_prefix="/internal")


def init_app() -> None:
    from . import dashboard  # noqa: F401
