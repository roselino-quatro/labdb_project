from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.admin import admin_blueprint
from app.routes.admin.context import build_option_list, empty_model

EDUCADOR_FIELDS = (
    "nome",
    "registro_profissional",
    "modalidades",
    "email",
    "telefone",
    "disponibilidade",
)


@admin_blueprint.get("/educadores", endpoint="educador_index")
def listar_educadores() -> str:
    context: dict[str, Any] = {
        "educadores": [],
        "modalidade_options": build_option_list(
            (
                ("all", "Todas as modalidades"),
                ("natacao", "Natação"),
                ("musculacao", "Musculação"),
                ("dança", "Dança"),
            )
        ),
    }
    return render_template("admin/educador_list.html", **context)


@admin_blueprint.route(
    "/educadores/novo",
    methods=["GET", "POST"],
    endpoint="educador_create",
)
def criar_educador() -> str:
    if request.method == "POST":
        flash("Educador cadastrado com sucesso (simulação).", "success")
        return redirect(url_for("admin.educador_index"))

    context: dict[str, Any] = {
        "educador": empty_model(EDUCADOR_FIELDS),
        "modalidade_options": build_option_list(
            (
                ("natacao", "Natação"),
                ("musculacao", "Musculação"),
                ("dança", "Dança"),
                ("ginastica", "Ginástica"),
            ),
        ),
    }
    return render_template("admin/educador_form.html", **context)
