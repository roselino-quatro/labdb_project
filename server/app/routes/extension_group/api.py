from flask import jsonify, request

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
        return jsonify(
            {
                "success": False,
                "message": "Grupo de extensão precisa de nome, descrição e responsável.",
            }
        ), 400

    sql_queries.execute_statement(
        "queries/extension_group/criar_grupo_extensao.sql",
        {
            "nome_grupo": name,
            "descricao": description,
            "cpf_responsavel": cpf_responsible,
        },
    )

    return jsonify(
        {
            "success": True,
            "message": "Grupo de extensão criado com sucesso!",
        }
    ), 200


@require_role("admin")
@extension_group_blueprint.route("/update", methods=["POST"])
def update_extension_group():
    old_name = request.form.get("old_group_name", "").strip()

    new_name = request.form.get("new_group_name", None)
    description = request.form.get("description", None)
    cpf_responsible = request.form.get("cpf_responsible", None)

    sql_queries.execute_statement(
        "queries/extension_group/atualizar_grupo_extensao.sql",
        {
            "nome_grupo_antigo": old_name,
            "nome_grupo_novo": new_name,
            "descricao": description,
            "cpf_responsavel": cpf_responsible,
        },
    )

    return jsonify(
        {
            "success": True,
            "message": "Grupo atualizado!",
        }
    ), 200


@require_role("admin")
@extension_group_blueprint.route("/delete", methods=["DELETE"])
def delete_extension_group():
    name = request.form.get("group_name", "").strip()

    if not name:
        return jsonify(
            {
                "success": False,
                "message": "Grupo não encontrado.",
            }
        ), 400

    sql_queries.execute_statement(
        "queries/extension_group/deletar_grupo_extensao.sql",
        {
            "nome_grupo": name,
        },
    )

    return jsonify(
        {
            "success": True,
            "message": "Grupo deletado!",
        }
    ), 200
