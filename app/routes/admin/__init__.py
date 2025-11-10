from flask import Blueprint

admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")


def init_app() -> None:
    """
    Importa módulos de rotas administrativas para garantir o registro
    dos endpoints associados ao blueprint `admin`.
    """

    # Imports locais para evitar dependências circulares no carregamento.
    from . import (  # noqa: F401
        aparelhos,
        atividades,
        dashboard,
        educadores,
        equipamentos,
        espacos,
        externos,
        funcionarios,
        grupos_extensao,
        instalacoes,
        internos,
        reservas,
        revisoes,
    )
