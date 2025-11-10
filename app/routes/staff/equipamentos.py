from __future__ import annotations

from typing import Any

from flask import render_template

from app.routes.staff import staff_blueprint


@staff_blueprint.get("/equipamentos", endpoint="equipamentos")
def listar_equipamentos() -> str:
    context: dict[str, Any] = {
        "equipamentos": [
            {
                "patrimonio": "EQ-1024",
                "descricao": "Bicicleta ergométrica profissional",
                "status": "Emprestado",
                "badge_color": "yellow",
                "responsavel": "Maria Silva",
                "data_devolucao": "10/07/2025",
                "devolucao_url": "#",
                "manutencao_url": "#",
            },
            {
                "patrimonio": "EQ-2048",
                "descricao": "Conjunto halteres 5kg",
                "status": "Disponível",
                "badge_color": "green",
                "responsavel": "-",
                "data_devolucao": "-",
                "devolucao_url": "#",
                "manutencao_url": "#",
            },
        ]
    }
    return render_template("staff/equipamentos.html", **context)
