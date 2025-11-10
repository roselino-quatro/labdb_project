from flask import Blueprint

staff_blueprint = Blueprint("staff", __name__, url_prefix="/staff")


def init_app() -> None:
    from . import (  # noqa: F401
        acessos,
        atividades,
        convites,
        dashboard,
        equipamentos,
        instalacoes,
        shortcuts,
    )
