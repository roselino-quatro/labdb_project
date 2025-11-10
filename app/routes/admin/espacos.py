from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.admin import admin_blueprint
from app.routes.admin.context import build_option_list, empty_model

ESPACO_FIELDS = (
    "nome",
    "instalacao_id",
    "capacidade",
    "disponibilidade",
    "periodicidade",
    "observacoes",
)


@admin_blueprint.get("/espacos", endpoint="espaco_index")
def listar_espacos() -> str:
    context: dict[str, Any] = {
        "espacos": [],
        "instalacao_options": build_option_list(
            (
                ("all", "Todas as instalações"),
                ("ginásio", "Ginásio"),
                ("piscina", "Piscina"),
                ("auditório", "Auditório"),
            )
        ),
        "disponibilidade_options": build_option_list(
            (
                ("livre", "Livre"),
                ("restrito", "Restrito"),
                ("indisponivel", "Indisponível"),
            )
        ),
    }
    return render_template("admin/espaco_list.html", **context)


@admin_blueprint.route(
    "/espacos/novo",
    methods=["GET", "POST"],
    endpoint="espaco_create",
)
def criar_espaco() -> str:
    if request.method == "POST":
        flash("Espaço cadastrado com sucesso (simulação).", "success")
        return redirect(url_for("admin.espaco_index"))

    context: dict[str, Any] = {
        "espaco": empty_model(ESPACO_FIELDS),
        "instalacao_options": build_option_list(
            (
                ("ginásio", "Ginásio"),
                ("piscina", "Piscina"),
                ("auditório", "Auditório"),
            )
        ),
        "disponibilidade_options": build_option_list(
            (
                ("livre", "Livre"),
                ("restrito", "Restrito"),
                ("indisponivel", "Indisponível"),
            )
        ),
    }
    return render_template("admin/espaco_form.html", **context)
