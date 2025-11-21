from flask import Blueprint

debug_blueprint = Blueprint("debug", __name__, url_prefix="/debug")


def init_app() -> None:
    """
    Import only the debug routes that are active in the system.
    """

    from . import database  # noqa: F401
