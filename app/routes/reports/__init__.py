from flask import Blueprint

reports_blueprint = Blueprint("reports", __name__, url_prefix="/reports")


def init_app() -> None:
    from . import overview  # noqa: F401
