from __future__ import annotations

from typing import Any

from flask import flash, redirect, render_template, request, url_for

from app.routes.admin import admin_blueprint


@admin_blueprint.get("/revisoes", endpoint="revisao_index")
def listar_revisoes() -> str:
    context: dict[str, Any] = {
        "revisoes": [],
    }
    return render_template("admin/revisao_list.html", **context)


@admin_blueprint.post("/revisoes/<string:review_id>/aprovar", endpoint="revisao_aprovar")
def aprovar_revisao(review_id: str) -> str:
    flash(f"Revisão {review_id} aprovada (simulação).", "success")
    return redirect(url_for("admin.revisao_index"))


@admin_blueprint.post("/revisoes/<string:review_id>/rejeitar", endpoint="revisao_rejeitar")
def rejeitar_revisao(review_id: str) -> str:
    flash(f"Revisão {review_id} rejeitada (simulação).", "info")
    return redirect(url_for("admin.revisao_index"))
