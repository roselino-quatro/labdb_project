from flask import jsonify, request, session

from app.routes.external import external_blueprint
from app.services.database import executor as sql_queries
from app.services.auth.decorators import require_external_auth


@external_blueprint.get("/", endpoint="dashboard")
@require_external_auth()
def dashboard():
    """Get invite information and related data for external user."""
    invite_id = session.get("invite_id")
    if not invite_id:
        return jsonify({"success": False, "message": "Sessão inválida"}), 401

    # Get invite information
    invite = sql_queries.fetch_one(
        "queries/external/get_invite_by_token.sql",
        {"token": session.get("external_token")},
    )

    if not invite:
        return jsonify({"success": False, "message": "Convite não encontrado"}), 404

    # Get participation if invite is accepted
    participation = None
    if session.get("invite_status") == "ACEITO":
        participation = sql_queries.fetch_one(
            "queries/external/get_invite_participation.sql",
            {"invite_id": invite_id},
        )

    return jsonify({
        "success": True,
        "invite": invite,
        "participation": participation,
    })


@external_blueprint.post("/accept", endpoint="accept_invite")
@require_external_auth()
def accept_invite():
    """Accept an external invite."""
    invite_id = session.get("invite_id")
    if not invite_id:
        return jsonify({"success": False, "message": "Sessão inválida"}), 401

    if session.get("invite_status") != "PENDENTE":
        return jsonify({"success": False, "message": "Convite não está pendente"}), 400

    result = sql_queries.fetch_one(
        "queries/external/accept_invite.sql",
        {"invite_id": invite_id},
    )

    if not result or not result.get("result"):
        return jsonify({"success": False, "message": "Erro ao processar aceitação"}), 500

    accept_data = result["result"]

    if not accept_data.get("success"):
        return jsonify({"success": False, "message": accept_data.get("message", "Erro ao aceitar convite")}), 400

    # Update session
    session["invite_status"] = "ACEITO"

    return jsonify({
        "success": True,
        "message": accept_data.get("message", "Convite aceito com sucesso"),
    })


@external_blueprint.post("/reject", endpoint="reject_invite")
@require_external_auth()
def reject_invite():
    """Reject an external invite."""
    invite_id = session.get("invite_id")
    if not invite_id:
        return jsonify({"success": False, "message": "Sessão inválida"}), 401

    if session.get("invite_status") != "PENDENTE":
        return jsonify({"success": False, "message": "Convite não está pendente"}), 400

    result = sql_queries.fetch_one(
        "queries/external/reject_invite.sql",
        {"invite_id": invite_id},
    )

    if not result or not result.get("result"):
        return jsonify({"success": False, "message": "Erro ao processar recusa"}), 500

    reject_data = result["result"]

    if not reject_data.get("success"):
        return jsonify({"success": False, "message": reject_data.get("message", "Erro ao recusar convite")}), 400

    # Update session
    session["invite_status"] = "RECUSADO"

    return jsonify({
        "success": True,
        "message": reject_data.get("message", "Convite recusado"),
    })
