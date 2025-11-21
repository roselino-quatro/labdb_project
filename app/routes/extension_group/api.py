from flask import flash, redirect, render_template, request, url_for

from app.routes.extension_group import extension_group_blueprint
from app.services.auth.decorators import require_role
from app.services.database import executor as sql_queries


@require_role("admin")
@extension_group_blueprint.route("/create", methods=["POST"])
def create_extension_group():
    name = request.form.get("group_name", "").strip()
    description = request.form.get("description", "").strip()
    cpf_responsible = request.form.get("cpf_responsible", "").strip()

    if not name or not description or not cpf_responsible:
        flash("Grupo de extensão precisa de nome, descrição e responsável", "error")
        return render_template("admin/dashboard.html"), 400

    sql_queries.execute_statement(
        "queries/extension_group/criar_grupo_extensao.sql",
        {
            "nome_grupo": name,
            "descricao": description,
            "cpf_responsavel": cpf_responsible,
        },
    )

    return redirect(url_for("admin.dashboard", _method="GET"))


@require_role("admin")
@extension_group_blueprint.route("/update", methods=["POST"])
def update_extension_group():
    old_name = request.form.get("old_group_name", "").strip()

    group = sql_queries.fetch_one(
        "queries/extension_group/buscar_grupo.sql", {"nome_grupo": old_name}
    )

    if not group:
        flash("Grupo de extensão não encontrado", "error")
        return render_template("admin/dashboard.html"), 400

    new_name = request.form.get("new_group_name", group["nome_grupo"]).strip()
    description = request.form.get("description", group["descricao"]).strip()
    cpf_responsible = request.form.get(
        "cpf_responsible", group["cpf_responsavel_interno"]
    ).strip()

    sql_queries.execute_statement(
        "queries/extension_group/atualizar_grupo_extensao.sql",
        {
            "nome_grupo_antigo": old_name,
            "nome_grupo_novo": new_name,
            "descricao": description,
            "cpf_responsavel": cpf_responsible,
        },
    )

    return redirect(url_for("admin.dashboard", _method="GET"))


@require_role("admin")
@extension_group_blueprint.route("/delete", methods=["DELETE"])
def delete_extension_group():
    name = request.form.get("group_name", "").strip()

    if not name:
        flash("É necessário passar o nome de um grupo", "error")
        return render_template("admin/dashboard.html"), 400

    sql_queries.execute_statement(
        "queries/extension_group/deletar_grupo_extensao.sql",
        {
            "nome_grupo": name,
        },
    )

    return redirect(url_for("admin.dashboard", _method="GET"))
