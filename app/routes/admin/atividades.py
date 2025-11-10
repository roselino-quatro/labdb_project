from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.admin import admin_blueprint
from app.routes.admin.context import build_option_list, empty_model

ATIVIDADE_FIELDS = (
    "nome",
    "educador",
    "modalidade",
    "periodo",
    "vagas_totais",
    "descricao",
)


@admin_blueprint.get("/atividades", endpoint="atividade_index")
def listar_atividades() -> str:
    context: dict[str, Any] = {
        "atividades": [],
        "status_options": build_option_list(
            (
                ("todas", "Todas"),
                ("andamento", "Em andamento"),
                ("concluida", "Concluída"),
            )
        ),
    }
    return render_template("admin/atividade_list.html", **context)


@admin_blueprint.route(
    "/atividades/nova",
    methods=["GET", "POST"],
    endpoint="atividade_create",
)
def criar_atividade() -> str:
    if request.method == "POST":
        flash("Atividade cadastrada com sucesso (simulação).", "success")
        return redirect(url_for("admin.atividade_index"))

    context: dict[str, Any] = {
        "atividade": empty_model(ATIVIDADE_FIELDS),
        "modalidade_options": build_option_list(
            (
                ("natacao", "Natação"),
                ("musculacao", "Musculação"),
                ("dança", "Dança"),
                ("ginastica", "Ginástica"),
            )
        ),
    }
    return render_template("admin/atividade_form.html", **context)
