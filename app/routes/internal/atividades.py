from __future__ import annotations

from datetime import date
from typing import Any

from flask import render_template

from app.routes.internal import internal_blueprint


@internal_blueprint.get("/atividades", endpoint="atividades")
def listar_atividades() -> str:
    context: dict[str, Any] = {
        "filtros": {"data": date.today().isoformat()},
        "periodicidade_options": [
            {"value": "todos", "label": "Todas", "selected": True},
            {"value": "semanal", "label": "Semanal"},
            {"value": "mensal", "label": "Mensal"},
        ],
        "grupo_options": [
            {"value": "todos", "label": "Todos os grupos", "selected": True},
            {"value": "ginastica", "label": "Ginástica"},
            {"value": "natacao", "label": "Natação"},
        ],
        "modalidade_options": [
            {"value": "todas", "label": "Todas", "selected": True},
            {"value": "musculacao", "label": "Musculação"},
            {"value": "yoga", "label": "Yoga"},
        ],
        "atividades": [
            {
                "nome": "Musculação funcional",
                "modalidade": "Musculação",
                "periodicidade": "Seg e Qua · 07:00",
                "status": "Com vagas",
                "badge_color": "green",
                "descricao": "Treino supervisionado com foco em fortalecimento e mobilidade.",
                "educador": "Ana Souza",
                "local": "Sala Musculação",
                "vagas_ocupadas": 18,
                "vagas_totais": 25,
                "detalhes_url": "#",
                "inscricao_url": "#",
            },
            {
                "nome": "Yoga restaurativa",
                "modalidade": "Yoga",
                "periodicidade": "Sex · 18:00",
                "status": "Lista de espera",
                "badge_color": "yellow",
                "descricao": "Aula voltada para alongamento e respiração.",
                "educador": "Bruno Lima",
                "local": "Sala Multiuso 2",
                "vagas_ocupadas": 20,
                "vagas_totais": 20,
                "detalhes_url": "#",
                "inscricao_url": "#",
            },
        ],
    }
    return render_template("internal/atividades.html", **context)
