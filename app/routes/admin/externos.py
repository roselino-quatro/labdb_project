from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.admin import admin_blueprint
from app.routes.admin.context import (
    build_option_list,
    empty_model,
    stub_pagination,
)

EXTERNO_FIELDS = (
    "nome",
    "documento",
    "email",
    "telefone",
    "convidado_por",
    "status",
    "autorizacao",
)


@admin_blueprint.get("/externos", endpoint="externo_index")
def listar_externos() -> str:
    context: dict[str, Any] = {
        "externos": [],
        "status_options": build_option_list(
            (
                ("pendente", "Pendente"),
                ("aprovado", "Aprovado"),
                ("expirado", "Expirado"),
            ),
            selected_value="pendente",
        ),
        "pagination": stub_pagination("admin.externo_index"),
    }
    return render_template("admin/externo_list.html", **context)


@admin_blueprint.route(
    "/externos/novo",
    methods=["GET", "POST"],
    endpoint="externo_create",
)
def criar_externo() -> str:
    if request.method == "POST":
        flash("Externo cadastrado com sucesso (simulação).", "success")
        return redirect(url_for("admin.externo_index"))

    context: dict[str, Any] = {
        "externo": empty_model(EXTERNO_FIELDS),
        "status_options": build_option_list(
            (
                ("pendente", "Pendente"),
                ("aprovado", "Aprovado"),
                ("expirado", "Expirado"),
            )
        ),
    }
    return render_template("admin/externo_form.html", **context)
