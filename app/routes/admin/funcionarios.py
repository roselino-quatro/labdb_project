from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.admin import admin_blueprint
from app.routes.admin.context import build_option_list, empty_model

FUNCIONARIO_FIELDS = (
    "nome",
    "data_nascimento",
    "formacao",
    "registro",
    "atribuicoes",
    "atividades",
    "restricoes",
)


@admin_blueprint.get("/funcionarios", endpoint="funcionario_index")
def listar_funcionarios() -> str:
    context: dict[str, Any] = {
        "funcionarios": [],
        "area_options": build_option_list(
            (
                ("all", "Todas as áreas"),
                ("administrativo", "Administrativo"),
                ("operacional", "Operacional"),
                ("educacional", "Educacional"),
            )
        ),
    }
    return render_template("admin/funcionario_list.html", **context)


@admin_blueprint.route(
    "/funcionarios/novo",
    methods=["GET", "POST"],
    endpoint="funcionario_create",
)
def criar_funcionario() -> str:
    if request.method == "POST":
        flash("Funcionário cadastrado com sucesso (simulação).", "success")
        return redirect(url_for("admin.funcionario_index"))

    context: dict[str, Any] = {
        "funcionario": empty_model(FUNCIONARIO_FIELDS),
    }
    return render_template("admin/funcionario_form.html", **context)
