from flask import Blueprint

extension_group_blueprint = Blueprint(
    "extension_group", __name__, url_prefix="/extension_group"
)


def init_app() -> None:
    from . import dashboard, api  # noqa: F401
