from __future__ import annotations

from typing import Any

from flask import render_template

from app.routes.internal import internal_blueprint


@internal_blueprint.get("/", endpoint="dashboard")
def dashboard() -> str:
    context: dict[str, Any] = {
        "proximas_reservas": [
            {"instalacao": "Ginásio Principal", "data": "08/07", "horario": "18:00"},
            {"instalacao": "Piscina Olímpica", "data": "10/07", "horario": "07:30"},
        ],
        "atividades_inscritas": [
            {
                "nome": "Musculação funcional",
                "periodicidade": "Seg e Qua",
                "educador": "Ana Souza",
            },
            {
                "nome": "Yoga restaurativa",
                "periodicidade": "Sex",
                "educador": "Bruno Lima",
            },
        ],
        "convites_recentes": [
            {"nome": "Carlos Pereira", "badge_color": "green", "status": "Aceito"},
            {"nome": "Fernanda Dias", "badge_color": "yellow", "status": "Pendente"},
        ],
    }
    return render_template("internal/dashboard.html", **context)
