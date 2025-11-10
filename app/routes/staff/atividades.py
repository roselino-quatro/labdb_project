from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.staff import staff_blueprint


@staff_blueprint.get("/atividades", endpoint="atividades")
def listar_atividades() -> str:
    context: dict[str, Any] = {
        "status_options": [
            {"value": "todas", "label": "Todas", "selected": True},
            {"value": "aberta", "label": "Abertas"},
            {"value": "andamento", "label": "Em andamento"},
            {"value": "concluida", "label": "Concluídas"},
        ],
        "educador_options": [
            {"value": "todos", "label": "Todos os educadores", "selected": True},
            {"value": "ana", "label": "Ana Souza"},
            {"value": "bruno", "label": "Bruno Lima"},
        ],
        "atividades": [
            {
                "nome": "Musculação funcional",
                "periodicidade": "Seg e Qua · 07:00",
                "educador": "Ana Souza",
                "inscritos": 24,
                "capacidade": 30,
                "proxima_sessao": "Hoje · 07:00",
                "presenca_url": "#",
                "editar_url": "#",
            },
            {
                "nome": "Natação adultos",
                "periodicidade": "Ter e Qui · 19:00",
                "educador": "Bruno Lima",
                "inscritos": 18,
                "capacidade": 20,
                "proxima_sessao": "Amanhã · 19:00",
                "presenca_url": "#",
                "editar_url": "#",
            },
        ],
    }
    return render_template("staff/atividades.html", **context)


@staff_blueprint.get("/atividades/exportar", endpoint="planilha_presenca")
def exportar_planilha_presenca() -> str:
    flash("Exportação de presença simulada com sucesso.", "success")
    return redirect(request.referrer or url_for("staff.atividades"))
