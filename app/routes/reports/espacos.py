from __future__ import annotations

from typing import Any

from flask import render_template

from app.routes.reports import reports_blueprint


@reports_blueprint.get("/espacos-utilizacao", endpoint="espacos_utilizacao")
def espacos_utilizacao() -> str:
    ranking_espacos = [
        {
            "tipo": "Quadra",
            "nome": "Ginásio Principal",
            "descricao": "Quadra coberta com 1.200m², utilizada para modalidades coletivas.",
            "total_reservas": 64,
            "frequencia_semana": "12 reservas",
            "duracao_media": "1.8",
        },
        {
            "tipo": "Piscina",
            "nome": "Piscina Olímpica",
            "descricao": "Piscina de 50m adaptada para treinos e aulas.",
            "total_reservas": 47,
            "frequencia_semana": "9 reservas",
            "duracao_media": "1.2",
        },
        {
            "tipo": "Sala",
            "nome": "Sala Multiuso 1",
            "descricao": "Espaço multiuso para pilates, yoga e alongamento.",
            "total_reservas": 38,
            "frequencia_semana": "7 reservas",
            "duracao_media": "1.5",
        },
    ]

    meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
    historico_uso = [
        {
            "nome": "Ginásio Principal",
            "valores": [85, 88, 90, 92, 94, 95],
        },
        {
            "nome": "Piscina Olímpica",
            "valores": [72, 75, 78, 80, 82, 84],
        },
        {
            "nome": "Sala Multiuso 1",
            "valores": [60, 63, 65, 68, 70, 72],
        },
    ]

    context: dict[str, Any] = {
        "janela_options": [
            {"value": "90d", "label": "Últimos 90 dias", "selected": True},
            {"value": "180d", "label": "Últimos 180 dias"},
            {"value": "365d", "label": "Últimos 12 meses"},
        ],
        "tipo_options": [
            {"value": "quadra", "label": "Quadras"},
            {"value": "piscina", "label": "Piscinas"},
            {"value": "sala", "label": "Salas multiuso"},
        ],
        "ranking_espacos": ranking_espacos,
        "meses": meses,
        "historico_uso": historico_uso,
    }
    return render_template("reports/espacos_utilizacao.html", **context)
