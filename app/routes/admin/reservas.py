from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.admin import admin_blueprint
from app.routes.admin.context import build_option_list, empty_model

RESERVA_FIELDS = (
    "instalacao",
    "responsavel",
    "inicio",
    "fim",
    "status",
    "observacoes",
)


@admin_blueprint.get("/reservas", endpoint="reserva_index")
def listar_reservas() -> str:
    context: dict[str, Any] = {
        "reservas": [],
        "status_options": build_option_list(
            (
                ("todas", "Todas"),
                ("prevista", "Prevista"),
                ("confirmada", "Confirmada"),
                ("cancelada", "Cancelada"),
            )
        ),
    }
    return render_template("admin/reserva_list.html", **context)


@admin_blueprint.route(
    "/reservas/nova",
    methods=["GET", "POST"],
    endpoint="reserva_create",
)
def criar_reserva() -> str:
    if request.method == "POST":
        flash("Reserva registrada com sucesso (simulação).", "success")
        return redirect(url_for("admin.reserva_index"))

    context: dict[str, Any] = {
        "reserva": empty_model(RESERVA_FIELDS),
        "instalacao_options": build_option_list(
            (
                ("ginásio", "Ginásio"),
                ("piscina", "Piscina"),
                ("quadra_externa", "Quadra externa"),
            )
        ),
        "status_options": build_option_list(
            (
                ("prevista", "Prevista"),
                ("confirmada", "Confirmada"),
                ("cancelada", "Cancelada"),
            )
        ),
    }
    return render_template("admin/reserva_form.html", **context)
