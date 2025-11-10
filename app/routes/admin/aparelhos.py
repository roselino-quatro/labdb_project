from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.admin import admin_blueprint
from app.routes.admin.context import build_option_list, empty_model

APARELHO_FIELDS = (
    "identificador",
    "nome",
    "instalacao_id",
    "estado",
    "ultima_manutencao",
    "periodicidade",
    "observacoes",
)


@admin_blueprint.get("/aparelhos", endpoint="aparelho_index")
def listar_aparelhos() -> str:
    context: dict[str, Any] = {
        "aparelhos": [],
        "localizacao_options": build_option_list(
            (
                ("all", "Todas as instalações"),
                ("gym", "Ginásio"),
                ("pool", "Piscina"),
            )
        ),
    }
    return render_template("admin/aparelho_list.html", **context)


@admin_blueprint.route("/aparelhos/novo", methods=["GET", "POST"], endpoint="aparelho_create")
def criar_aparelho() -> str:
    if request.method == "POST":
        flash("Aparelho cadastrado com sucesso (simulação).", "success")
        return redirect(url_for("admin.aparelho_index"))

    context: dict[str, Any] = {
        "aparelho": empty_model(APARELHO_FIELDS),
        "instalacao_options": build_option_list(
            (
                ("gym", "Ginásio"),
                ("pool", "Piscina Coberta"),
                ("studio", "Estúdio"),
            )
        ),
        "estado_options": build_option_list(
            (
                ("operacional", "Operacional"),
                ("manutencao", "Em manutenção"),
                ("inativo", "Inativo"),
            )
        ),
    }
    return render_template("admin/aparelho_form.html", **context)
