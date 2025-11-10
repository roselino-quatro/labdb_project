from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.admin import admin_blueprint
from app.routes.admin.context import (
    build_option_list,
    empty_model,
    stub_pagination,
)

INTERNO_FIELDS = (
    "nusp",
    "nome",
    "categoria",
    "email",
    "telefone",
)


@admin_blueprint.get("/internos", endpoint="interno_index")
def listar_internos() -> str:
    context: dict[str, Any] = {
        "internos": [],
        "categoria_options": build_option_list(
            (
                ("all", "Todos"),
                ("docente", "Docentes"),
                ("discente", "Discentes"),
                ("colaborador", "Colaboradores"),
            ),
            selected_value="all",
        ),
        "pagination": stub_pagination("admin.interno_index"),
    }
    return render_template("admin/interno_list.html", **context)


@admin_blueprint.route(
    "/internos/novo",
    methods=["GET", "POST"],
    endpoint="interno_create",
)
def criar_interno() -> str:
    if request.method == "POST":
        flash("Interno cadastrado com sucesso (simulação).", "success")
        return redirect(url_for("admin.interno_index"))

    context: dict[str, Any] = {
        "interno": empty_model(INTERNO_FIELDS),
        "categoria_options": build_option_list(
            (
                ("docente", "Docente"),
                ("discente", "Discente"),
                ("colaborador", "Colaborador"),
            ),
            selected_value="docente",
        ),
    }
    return render_template("admin/interno_form.html", **context)
