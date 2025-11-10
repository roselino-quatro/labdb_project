from __future__ import annotations

from typing import Any

from flask import render_template

from app.routes.external import external_blueprint


@external_blueprint.get("/participacoes", endpoint="participacoes")
def listar_participacoes() -> str:
    context: dict[str, Any] = {
        "participacoes": [
            {
                "nome": "Musculação funcional",
                "data": "08/07/2025",
                "horario": "18:00",
                "status": "Confirmada",
                "badge_color": "green",
            },
            {
                "nome": "Aula aberta de Yoga",
                "data": "15/07/2025",
                "horario": "19:30",
                "status": "Aguardando confirmação",
                "badge_color": "yellow",
            },
        ]
    }
    return render_template("external/participacoes.html", **context)
