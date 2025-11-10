from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from flask import render_template, url_for

from app.routes.reports import reports_blueprint


def _default_filters() -> dict[str, str]:
    today = date.today()
    six_months_ago = (today - timedelta(days=150)).strftime("%Y-%m")
    return {
        "inicio": six_months_ago,
        "fim": today.strftime("%Y-%m"),
    }


@reports_blueprint.get("/", endpoint="overview")
def overview() -> str:
    highlight_cards: list[dict[str, Any]] = [
        {
            "title": "Reservas confirmadas",
            "description": "Instalações reservadas confirmadas no mês.",
            "value": "42",
            "items": [
                {"label": "Quadras", "value": 18},
                {"label": "Piscina", "value": 9},
                {"label": "Salas multiuso", "value": 15},
            ],
            "link": url_for("reports.reservas_instalacoes"),
        },
        {
            "title": "Participação média",
            "description": "Indicador de presença das atividades esportivas.",
            "value": "78%",
            "items": [
                {"label": "Musculação", "value": "82%"},
                {"label": "Natação", "value": "74%"},
                {"label": "Ginástica", "value": "69%"},
            ],
            "link": url_for("reports.participantes_atividades"),
        },
    ]

    resumo_mensal = [
        {
            "label": "Reservas",
            "pontos": [
                {"mes": "Mai", "valor": 36},
                {"mes": "Jun", "valor": 44},
                {"mes": "Jul", "valor": 51},
            ],
        },
        {
            "label": "Atividades",
            "pontos": [
                {"mes": "Mai", "valor": 24},
                {"mes": "Jun", "valor": 28},
                {"mes": "Jul", "valor": 32},
            ],
        },
        {
            "label": "Participantes",
            "pontos": [
                {"mes": "Mai", "valor": 640},
                {"mes": "Jun", "valor": 710},
                {"mes": "Jul", "valor": 765},
            ],
        },
    ]

    context: dict[str, Any] = {
        "highlight_cards": highlight_cards,
        "filtros": _default_filters(),
        "resumo_mensal": resumo_mensal,
    }
    return render_template("reports/overview.html", **context)
