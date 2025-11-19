from flask import Blueprint

staff_blueprint = Blueprint("staff", __name__, url_prefix="/staff")


def init_app() -> None:
    from . import dashboard  # noqa: F401
