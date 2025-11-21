from flask import Blueprint

admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")


def init_app() -> None:
    """
    Import only the administrative routes that are active in the system.
    """

    from . import dashboard  # noqa: F401
