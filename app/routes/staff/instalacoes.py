from __future__ import annotations

from datetime import date
from typing import Any

from flask import render_template

from app.routes.staff import staff_blueprint


@staff_blueprint.get("/instalacoes", endpoint="instalacoes")
def listar_instalacoes() -> str:
    context: dict[str, Any] = {
        "filtros": {"data": date.today().isoformat()},
        "status_options": [
            {"value": "todas", "label": "Todas", "selected": True},
            {"value": "disponivel", "label": "Disponível"},
            {"value": "uso", "label": "Em uso"},
            {"value": "manutencao", "label": "Em manutenção"},
        ],
        "instalacoes": [
            {
                "nome": "Ginásio Principal",
                "capacidade": 500,
                "responsavel": "Coordenação Esportiva",
                "status": "Em uso",
                "badge_color": "yellow",
                "proxima_reserva": "10:00 - Torneio InterUSP",
                "duracao_media": 1.8,
                "reservas_dia": 6,
                "agenda_url": "#",
                "registrar_url": "#",
            },
            {
                "nome": "Piscina Olímpica",
                "capacidade": 120,
                "responsavel": "Equipe Aquática",
                "status": "Disponível",
                "badge_color": "green",
                "proxima_reserva": "12:00 - Treino natação",
                "duracao_media": 1.2,
                "reservas_dia": 4,
                "agenda_url": "#",
                "registrar_url": "#",
            },
        ],
    }
    return render_template("staff/instalacoes.html", **context)
