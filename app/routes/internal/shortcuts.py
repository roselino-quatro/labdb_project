from __future__ import annotations

from flask import redirect, url_for

from app.routes.internal import internal_blueprint


@internal_blueprint.get("/convites/novo", endpoint="novo_convite_redirect")
def novo_convite_redirect() -> str:
    return redirect(url_for("staff.convites"))


@internal_blueprint.get("/reservas/nova", endpoint="reservar_instalacao")
def reservar_instalacao_redirect() -> str:
    return redirect(url_for("admin.reserva_create"))
