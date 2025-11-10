from __future__ import annotations

from typing import Any

from flask import render_template

from app.routes.staff import staff_blueprint


@staff_blueprint.get("/", endpoint="dashboard")
def dashboard() -> str:
    context: dict[str, Any] = {
        "stats": {
            "atividades_ativas": 12,
            "reservas_hoje": 7,
            "equipamentos_emprestados": 15,
            "externos_aguardando": 4,
        },
        "atividades_hoje": [
            {"nome": "Musculação Funcional", "horario": "07:00", "educador": "Ana Souza", "local": "Sala Musculação"},
            {"nome": "Pilates Avançado", "horario": "09:00", "educador": "Bruno Lima", "local": "Sala Multiuso"},
        ],
        "instalacoes_monitoradas": [
            {"nome": "Ginásio Principal", "proxima_reserva": "10:00 - Torneio InterUSP", "status": "Em uso"},
            {"nome": "Piscina Olímpica", "proxima_reserva": "12:00 - Treino Natação", "status": "Disponível"},
        ],
        "alertas_equipamentos": [
            {"descricao": "Bicicleta ergométrica #24", "status": "Manutenção agendada", "acao": "Confirmar manutenção", "link": "#"},
            {"descricao": "Peso livre 12kg", "status": "Baixo estoque", "acao": "Repor inventário", "link": "#"},
        ],
    }
    return render_template("staff/dashboard.html", **context)
