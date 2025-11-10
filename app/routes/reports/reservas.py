from __future__ import annotations

from typing import Any

from flask import render_template

from app.routes.reports import reports_blueprint


@reports_blueprint.get("/reservas", endpoint="reservas_instalacoes")
def reservas_instalacoes() -> str:
    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
    reservas_por_mes = [
        {
            "instalacao": "Ginásio Principal",
            "mensal": [8, 10, 11, 9, 12, 14],
            "total": 64,
        },
        {
            "instalacao": "Piscina Olímpica",
            "mensal": [6, 7, 9, 7, 8, 10],
            "total": 47,
        },
    ]
    totais_por_instalacao = [
        {"nome": "Ginásio Principal", "total": 64, "ultima_reserva": "08/07"},
        {"nome": "Piscina Olímpica", "total": 47, "ultima_reserva": "05/07"},
        {"nome": "Quadra Externa", "total": 35, "ultima_reserva": "03/07"},
    ]
    instalacoes_loop = [
        {"nome": "Sala Multiuso 1", "total": 18},
        {"nome": "Sala Multiuso 2", "total": 22},
        {"nome": "Auditório CEFER", "total": 15},
    ]

    context: dict[str, Any] = {
        "instalacao_options": [
            {"value": "all", "label": "Todas as instalações", "selected": True},
            {"value": "ginásio", "label": "Ginásio Principal", "selected": False},
            {"value": "piscina", "label": "Piscina Olímpica", "selected": False},
        ],
        "ano_options": [
            {"value": "2025", "label": "2025", "selected": True},
            {"value": "2024", "label": "2024", "selected": False},
            {"value": "2023", "label": "2023", "selected": False},
        ],
        "meses": meses,
        "reservas_por_mes": reservas_por_mes,
        "total_reservas": sum(item["total"] for item in reservas_por_mes),
        "totais_por_instalacao": totais_por_instalacao,
        "instalacoes_loop": instalacoes_loop,
    }
    return render_template("reports/reservas_instalacoes.html", **context)
