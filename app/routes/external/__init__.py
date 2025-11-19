from flask import Blueprint

external_blueprint = Blueprint("external", __name__, url_prefix="/external")


def init_app() -> None:
    from . import dashboard  # noqa: F401
