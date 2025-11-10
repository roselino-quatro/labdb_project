from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.external import external_blueprint


@external_blueprint.get("/convites/<string:token>", endpoint="convite_confirmacao")
def convite_confirmacao(token: str) -> str:
    convite: dict[str, Any] = {
        "token": token,
        "nome": "Convidado Externo",
        "convidado_por": "Servidor USP",
        "atividade": "Aula aberta de Yoga",
        "data": "15/07/2025 às 19:30",
        "local": "Sala Multiuso 2",
    }
    return render_template("external/convite_confirmacao.html", convite=convite, form=None)


@external_blueprint.post("/convites/<string:token>", endpoint="confirmar_convite")
def confirmar_convite(token: str) -> str:
    flash("Participação confirmada! Nos vemos na atividade.", "success")
    return redirect(url_for("external.dashboard"))
