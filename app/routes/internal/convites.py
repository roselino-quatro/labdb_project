from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, url_for

from app.routes.internal import internal_blueprint


@internal_blueprint.get("/convites", endpoint="convites")
def listar_convites() -> str:
    context: dict[str, Any] = {
        "convites": [
            {
                "nome": "Carlos Pereira",
                "atividade": "Musculação funcional",
                "status": "Pendente",
                "badge_color": "yellow",
                "resposta": None,
                "criado_em": "02/07/2025",
                "reenviar_url": "#",
                "cancelar_url": "#",
            },
            {
                "nome": "Fernanda Dias",
                "atividade": "Yoga restaurativa",
                "status": "Aceito",
                "badge_color": "green",
                "resposta": "Confirmado em 30/06/2025",
                "criado_em": "29/06/2025",
                "reenviar_url": "#",
                "cancelar_url": "#",
            },
        ],
    }
    return render_template("internal/convites.html", **context)


@internal_blueprint.post("/convites", endpoint="novo_convite")
def criar_convite() -> str:
    flash("Convite enviado com sucesso (simulação).", "success")
    return redirect(url_for("internal.convites"))
