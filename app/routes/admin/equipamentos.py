from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.admin import admin_blueprint
from app.routes.admin.context import build_option_list, empty_model

EQUIPAMENTO_FIELDS = (
    "patrimonio",
    "categoria",
    "descricao",
    "quantidade",
    "situacao",
    "data_aquisicao",
    "valor_aquisicao",
    "origem",
)


@admin_blueprint.get("/equipamentos", endpoint="equipamento_index")
def listar_equipamentos() -> str:
    context: dict[str, Any] = {
        "equipamentos": [],
        "situacao_options": build_option_list(
            (
                ("disponivel", "Disponível"),
                ("manutencao", "Em manutenção"),
                ("baixado", "Baixado"),
            )
        ),
    }
    return render_template("admin/equipamento_list.html", **context)


@admin_blueprint.route(
    "/equipamentos/novo",
    methods=["GET", "POST"],
    endpoint="equipamento_create",
)
def criar_equipamento() -> str:
    if request.method == "POST":
        flash("Equipamento cadastrado com sucesso (simulação).", "success")
        return redirect(url_for("admin.equipamento_index"))

    context: dict[str, Any] = {
        "equipamento": empty_model(EQUIPAMENTO_FIELDS),
        "categoria_options": build_option_list(
            (
                ("musculacao", "Musculação"),
                ("natacao", "Natação"),
                ("ginastica", "Ginástica"),
                ("outros", "Outros"),
            )
        ),
        "situacao_options": build_option_list(
            (
                ("disponivel", "Disponível"),
                ("manutencao", "Em manutenção"),
                ("baixado", "Baixado"),
            )
        ),
    }
    return render_template("admin/equipamento_form.html", **context)
