from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from flask import render_template

from app.routes.internal import internal_blueprint


@internal_blueprint.get("/reservas", endpoint="reservas")
def listar_reservas() -> str:
    hoje = date.today()
    context: dict[str, Any] = {
        "filtros": {
            "inicio": hoje.isoformat(),
            "fim": (hoje + timedelta(days=30)).isoformat(),
        },
        "status_options": [
            {"value": "todas", "label": "Todas", "selected": True},
            {"value": "confirmada", "label": "Confirmada"},
            {"value": "pendente", "label": "Pendente"},
            {"value": "cancelada", "label": "Cancelada"},
        ],
        "reservas": [
            {
                "instalacao": "Ginásio Principal",
                "data": "08/07/2025",
                "horario": "18:00 - 20:00",
                "status": "Confirmada",
                "badge_color": "green",
                "comprovante_url": "#",
                "cancelar_url": "#",
            },
            {
                "instalacao": "Piscina Olímpica",
                "data": "12/07/2025",
                "horario": "07:30 - 09:00",
                "status": "Pendente",
                "badge_color": "yellow",
                "comprovante_url": "#",
                "cancelar_url": "#",
            },
        ],
    }
    return render_template("internal/reservas.html", **context)
