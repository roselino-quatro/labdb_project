from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from flask import render_template

from app.routes.staff import staff_blueprint


@staff_blueprint.get("/acessos", endpoint="acessos")
def metricas_acesso() -> str:
    hoje = date.today()
    acessos_diarios = []
    for dias in range(5):
        dia = hoje - timedelta(days=dias)
        internos = 120 - dias * 5
        externos = 32 + dias * 2
        funcionarios = 18
        acessos_diarios.append(
            {
                "data": dia.strftime("%d/%m/%Y"),
                "internos": internos,
                "externos": externos,
                "funcionarios": funcionarios,
                "total": internos + externos + funcionarios,
            }
        )

    context: dict[str, Any] = {
        "filtros": {
            "inicio": (hoje - timedelta(days=7)).isoformat(),
            "fim": hoje.isoformat(),
        },
        "acessos_diarios": list(reversed(acessos_diarios)),
        "indicadores": [
            {
                "titulo": "Média diária",
                "valor": "168",
                "descricao": "Visitantes únicos nos últimos 7 dias.",
            },
            {
                "titulo": "Pico semanal",
                "valor": "212",
                "descricao": "Maior fluxo registrado na semana anterior.",
            },
            {
                "titulo": "Externos aguardando",
                "valor": "7",
                "descricao": "Visitantes com convite pendente de validação.",
            },
        ],
    }
    return render_template("staff/acessos.html", **context)
