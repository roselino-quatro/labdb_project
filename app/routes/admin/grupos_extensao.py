from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.admin import admin_blueprint
from app.routes.admin.context import build_option_list, empty_model

GRUPO_FIELDS = (
    "nome",
    "modalidade",
    "status",
    "responsavel_interno",
    "contato",
    "descricao",
)


@admin_blueprint.get("/grupos-extensao", endpoint="grupo_extensao_index")
def listar_grupos_extensao() -> str:
    context: dict[str, Any] = {
        "grupos": [],
        "modalidade_options": build_option_list(
            (
                ("all", "Todas as modalidades"),
                ("lutas", "Lutas"),
                ("dança", "Dança"),
                ("ginastica", "Ginástica"),
            )
        ),
    }
    return render_template("admin/grupo_extensao_list.html", **context)


@admin_blueprint.route(
    "/grupos-extensao/novo",
    methods=["GET", "POST"],
    endpoint="grupo_extensao_create",
)
def criar_grupo_extensao() -> str:
    if request.method == "POST":
        flash("Grupo de extensão cadastrado com sucesso (simulação).", "success")
        return redirect(url_for("admin.grupo_extensao_index"))

    context: dict[str, Any] = {
        "grupo": empty_model(GRUPO_FIELDS),
        "modalidade_options": build_option_list(
            (
                ("lutas", "Lutas"),
                ("dança", "Dança"),
                ("ginastica", "Ginástica"),
                ("outros", "Outros"),
            )
        ),
        "status_options": build_option_list(
            (
                ("ativo", "Ativo"),
                ("inativo", "Inativo"),
                ("suspenso", "Suspenso"),
            )
        ),
    }
    return render_template("admin/grupo_extensao_form.html", **context)
