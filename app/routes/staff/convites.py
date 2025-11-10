from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.staff import staff_blueprint


@staff_blueprint.get("/convites", endpoint="convites")
def listar_convites() -> str:
    context: dict[str, Any] = {
        "atividade_options": [
            {"value": "musculacao", "label": "Musculação Funcional"},
            {"value": "natacao", "label": "Natação Intermediária"},
            {"value": "pilates", "label": "Pilates Avançado"},
        ],
        "convites": [
            {
                "nome": "Carlos Pereira",
                "atividade": "Musculação Funcional",
                "status": "Aguardando aceite",
                "badge_color": "yellow",
                "emitido_em": "02/07/2025",
                "reenviar_url": "#",
                "cancelar_url": "#",
            },
            {
                "nome": "Fernanda Dias",
                "atividade": "Pilates Avançado",
                "status": "Aceito",
                "badge_color": "green",
                "emitido_em": "29/06/2025",
                "reenviar_url": "#",
                "cancelar_url": "#",
            },
        ],
    }
    return render_template("staff/convites.html", **context)


@staff_blueprint.post("/convites", endpoint="convite_externo")
def criar_convite() -> str:
    flash("Convite externo emitido com sucesso (simulação).", "success")
    return redirect(url_for("staff.convites"))
