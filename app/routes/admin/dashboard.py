from __future__ import annotations

from typing import Any

from flask import render_template

from app.routes.admin import admin_blueprint
from app.routes.admin.context import today_iso


def build_dashboard_context(database_time: str | None = None) -> dict[str, Any]:
    return {
        "internal_count": 0,
        "external_count": 0,
        "install_count": 0,
        "equipment_count": 0,
        "pending_items": [
            {
                "title": "Nenhuma pendência cadastrada",
                "description": "Cadastre novas ações para acompanhamento facilitado.",
                "action_url": "#",
            }
        ],
        "upcoming_reservas": [
            {
                "instalacao": "Ginásio Principal",
                "periodo": "Hoje - 08:00 às 10:00",
                "responsavel": "Coordenação CEFER",
                "status": "Prevista",
            }
        ],
        "database_time": database_time or today_iso(),
    }


@admin_blueprint.get("/", endpoint="dashboard")
def dashboard() -> str:
    return render_template("admin/dashboard.html", **build_dashboard_context())
