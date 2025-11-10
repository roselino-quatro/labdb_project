from __future__ import annotations

from flask import redirect, url_for

from app.routes.staff import staff_blueprint


@staff_blueprint.get("/atividades/nova", endpoint="atividade_nova")
def nova_atividade() -> str:
    return redirect(url_for("admin.atividade_create"))


@staff_blueprint.get("/equipamentos/emprestimo", endpoint="registrar_emprestimo")
def registrar_emprestimo() -> str:
    return redirect(url_for("admin.equipamento_create"))


@staff_blueprint.get("/equipamentos/manutencao", endpoint="agendar_manutencao")
def agendar_manutencao() -> str:
    return redirect(url_for("admin.aparelho_create"))
