from __future__ import annotations

from datetime import date
from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.internal import internal_blueprint


@internal_blueprint.get("/equipamentos", endpoint="equipamentos")
def reservar_equipamentos_view() -> str:
    hoje = date.today()
    context: dict[str, Any] = {
        "equipamento_options": [
            {"value": "kit_musculacao", "label": "Kit musculação (halteres + colchonete)"},
            {"value": "bola_basquete", "label": "Bola de basquete oficial"},
            {"value": "corda", "label": "Corda funcional"},
        ],
        "atividade_options": [
            {"value": "atividade_1", "label": "Musculação funcional"},
            {"value": "atividade_2", "label": "Treino HIIT"},
            {"value": "atividade_3", "label": "Aula aberta"},
        ],
        "solicitacoes": [
            {
                "equipamento": "Kit musculação",
                "quantidade": 2,
                "data": "05/07/2025",
                "status": "Aprovada",
                "badge_color": "green",
                "detalhes_url": "#",
                "cancelar_url": "#",
            },
            {
                "equipamento": "Bola de basquete",
                "quantidade": 1,
                "data": "09/07/2025",
                "status": "Pendente",
                "badge_color": "yellow",
                "detalhes_url": "#",
                "cancelar_url": "#",
            },
        ],
        "hoje": hoje.isoformat(),
        "hora_padrao": "18:00",
    }
    return render_template("internal/equipamentos.html", **context)


@internal_blueprint.post("/equipamentos", endpoint="reservar_equipamento")
def reservar_equipamento_action() -> str:
    flash("Solicitação de equipamento registrada (simulação).", "success")
    return redirect(url_for("internal.equipamentos"))
