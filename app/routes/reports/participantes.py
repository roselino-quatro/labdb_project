from __future__ import annotations

from typing import Any

from flask import render_template

from app.routes.reports import reports_blueprint


@reports_blueprint.get("/participantes-atividades", endpoint="participantes_atividades")
def participantes_por_atividade() -> str:
    atividades = [
        {
            "nome": "Musculação Funcional",
            "educador": "Ana Souza",
            "capacidade": 30,
            "inscritos": 28,
            "comparecimento": "25 (83%)",
        },
        {
            "nome": "Natação Intermediária",
            "educador": "Bruno Lima",
            "capacidade": 20,
            "inscritos": 18,
            "comparecimento": "16 (80%)",
        },
    ]

    context: dict[str, Any] = {
        "periodo_options": [
            {"value": "30d", "label": "Últimos 30 dias", "selected": True},
            {"value": "90d", "label": "Últimos 90 dias"},
            {"value": "365d", "label": "Último ano"},
        ],
        "status_options": [
            {"value": "prevista", "label": "Prevista"},
            {"value": "ativa", "label": "Ativa"},
            {"value": "concluida", "label": "Concluída"},
        ],
        "total_participantes": sum(item["inscritos"] for item in atividades),
        "media_por_atividade": round(
            sum(item["inscritos"] for item in atividades) / len(atividades), 1
        ),
        "percentual_ocupacao": 81,
        "participantes_por_atividade": atividades,
    }
    return render_template("reports/participantes_atividades.html", **context)
