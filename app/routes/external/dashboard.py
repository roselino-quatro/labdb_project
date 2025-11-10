from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.external import external_blueprint


@external_blueprint.get("/", endpoint="dashboard")
def dashboard() -> str:
    context: dict[str, Any] = {
        "atividades_confirmadas": [
            {
                "nome": "Musculação funcional",
                "data": "08/07",
                "horario": "18:00",
                "local": "Sala Musculação",
            }
        ]
    }
    return render_template("external/dashboard.html", **context)


@external_blueprint.post("/convite/validar", endpoint="validar_convite")
def validar_convite() -> str:
    flash("Convite validado com sucesso (simulação).", "success")
    return redirect(url_for("external.dashboard"))
