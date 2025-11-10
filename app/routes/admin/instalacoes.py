from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.admin import admin_blueprint
from app.routes.admin.context import build_option_list, empty_model

INSTALACAO_FIELDS = (
    "nome",
    "tipo",
    "capacidade",
    "descricao",
)


@admin_blueprint.get("/instalacoes", endpoint="instalacao_index")
def listar_instalacoes() -> str:
    context: dict[str, Any] = {
        "instalacoes": [],
        "tipo_options": build_option_list(
            (
                ("quadra", "Quadra"),
                ("piscina", "Piscina"),
                ("sala", "Sala multiuso"),
                ("outros", "Outros"),
            )
        ),
    }
    return render_template("admin/instalacao_list.html", **context)


@admin_blueprint.route(
    "/instalacoes/novo",
    methods=["GET", "POST"],
    endpoint="instalacao_create",
)
def criar_instalacao() -> str:
    if request.method == "POST":
        flash("Instalação cadastrada com sucesso (simulação).", "success")
        return redirect(url_for("admin.instalacao_index"))

    context: dict[str, Any] = {
        "instalacao": empty_model(INSTALACAO_FIELDS),
        "tipo_options": build_option_list(
            (
                ("quadra", "Quadra"),
                ("piscina", "Piscina"),
                ("sala", "Sala multiuso"),
                ("outros", "Outros"),
            )
        ),
        "exige_reserva": True,
        "prioridade_usp": True,
    }
    return render_template("admin/instalacao_form.html", **context)
