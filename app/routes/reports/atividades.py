from __future__ import annotations

from typing import Any

from flask import render_template

from app.routes.reports import reports_blueprint


@reports_blueprint.get("/atividades-educador", endpoint="atividades_educador")
def atividades_por_educador() -> str:
    context: dict[str, Any] = {
        "modalidade_options": [
            {"value": "natacao", "label": "Natação"},
            {"value": "musculacao", "label": "Musculação"},
            {"value": "ginastica", "label": "Ginástica"},
        ],
        "periodo_options": [
            {"value": "ultimos_3", "label": "Últimos 3 meses", "selected": True},
            {"value": "ultimos_6", "label": "Últimos 6 meses"},
            {"value": "ano_corrente", "label": "Ano corrente"},
        ],
        "resumo_educadores": [
            {
                "nome": "Ana Souza",
                "modalidades": ["Musculação", "HIIT"],
                "total_atividades": 18,
                "total_participantes": 220,
            },
            {
                "nome": "Bruno Lima",
                "modalidades": ["Natação"],
                "total_atividades": 14,
                "total_participantes": 180,
            },
        ],
        "categorias": [
            {
                "nome": "Tempo integral",
                "total_atividades": 32,
                "total_participantes": 400,
                "detalhes": [
                    {"modalidade": "Musculação", "qtd": 12},
                    {"modalidade": "HIIT", "qtd": 8},
                    {"modalidade": "Alongamento", "qtd": 12},
                ],
            },
            {
                "nome": "Parcial",
                "total_atividades": 18,
                "total_participantes": 210,
                "detalhes": [
                    {"modalidade": "Natação", "qtd": 10},
                    {"modalidade": "Ginástica", "qtd": 8},
                ],
            },
        ],
    }
    return render_template("reports/atividades_educador.html", **context)
