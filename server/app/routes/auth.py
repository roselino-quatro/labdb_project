from flask import Blueprint, jsonify, request, session

from app.services.database import executor as sql_queries


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route("/login", methods=["GET"])
def login():
    if session.get("user_id"):
        return jsonify({"redirect": _get_redirect_url_for_user()})
    return jsonify({"message": "Login page"})


@auth_blueprint.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email") or request.json.get("email", "").strip() if request.is_json else ""
    password = request.form.get("password") or request.json.get("password", "").strip() if request.is_json else ""
    ip_origin = request.remote_addr

    if not email or not password:
        return jsonify({"success": False, "message": "E-mail e senha são obrigatórios"}), 400

    result = sql_queries.fetch_one(
        "queries/auth/login_user.sql",
        {
            "email_or_cpf": email,
            "password": password,
            "ip_origin": ip_origin,
        },
    )

    if not result or not result.get("result"):
        return jsonify({"success": False, "message": "Credenciais inválidas"}), 401

    auth_data = result["result"]

    if not auth_data.get("success"):
        return jsonify({"success": False, "message": auth_data.get("message", "Credenciais inválidas")}), 401

    # Store user data in session
    session["user_id"] = auth_data["user_id"]
    session["user_email"] = auth_data["email"]
    session["user_nome"] = auth_data["nome"]
    session["profile_access"] = _build_profile_access(auth_data.get("roles", []))

    return jsonify({
        "success": True,
        "message": "Login realizado com sucesso",
        "redirect": _get_redirect_url_for_user(),
        "user": {
            "user_id": auth_data["user_id"],
            "email": auth_data["email"],
            "nome": auth_data["nome"],
        }
    })


@auth_blueprint.route("/register", methods=["GET"])
def register():
    if session.get("user_id"):
        return jsonify({"redirect": _get_redirect_url_for_user()})
    return jsonify({"message": "Register page"})


@auth_blueprint.route("/register", methods=["POST"])
def register_post():
    if request.is_json:
        data = request.json
        cpf = data.get("cpf", "").strip()
        nusp = data.get("nusp", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        password_confirm = data.get("password_confirm", "").strip()
    else:
        cpf = request.form.get("cpf", "").strip()
        nusp = request.form.get("nusp", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        password_confirm = request.form.get("password_confirm", "").strip()

    if not all([cpf, nusp, email, password, password_confirm]):
        return jsonify({"success": False, "message": "Todos os campos são obrigatórios"}), 400

    if password != password_confirm:
        return jsonify({"success": False, "message": "As senhas não coincidem"}), 400

    result = sql_queries.fetch_one(
        "queries/auth/request_registration.sql",
        {
            "cpf_pessoa": cpf,
            "nusp": nusp,
            "email": email,
            "password": password,
        },
    )

    if not result or not result.get("result"):
        return jsonify({"success": False, "message": "Erro ao processar solicitação de cadastro"}), 500

    registration_data = result["result"]

    if not registration_data.get("success"):
        return jsonify({"success": False, "message": registration_data.get("message", "Erro ao processar solicitação")}), 400

    return jsonify({
        "success": True,
        "message": registration_data.get("message", "Solicitação de cadastro criada com sucesso")
    })


@auth_blueprint.route("/pending-registrations", methods=["GET"])
def pending_registrations():
    if not session.get("user_id"):
        return jsonify({"success": False, "message": "Autenticação necessária"}), 401

    # Check if user is admin (simple check via session)
    profile_access = session.get("profile_access", {})
    if not profile_access.get("admin"):
        return jsonify({"success": False, "message": "Acesso de administrador necessário"}), 403

    registrations = sql_queries.fetch_all("queries/auth/list_pending_registrations.sql")

    return jsonify({
        "success": True,
        "registrations": registrations
    })


@auth_blueprint.route("/approve-registration", methods=["POST"])
def approve_registration():
    if not session.get("user_id"):
        return jsonify({"success": False, "message": "Autenticação necessária"}), 401

    profile_access = session.get("profile_access", {})
    if not profile_access.get("admin"):
        return jsonify({"success": False, "message": "Acesso de administrador necessário"}), 403

    id_solicitacao = request.form.get("id_solicitacao") or (request.json.get("id_solicitacao") if request.is_json else None)
    if not id_solicitacao:
        return jsonify({"success": False, "message": "Solicitação inválida"}), 400

    result = sql_queries.fetch_one(
        "queries/auth/approve_registration.sql",
        {
            "id_solicitacao": int(id_solicitacao),
            "cpf_admin": session["user_id"],
        },
    )

    if result and result.get("result") and result["result"].get("success"):
        return jsonify({"success": True, "message": "Cadastro aprovado com sucesso"})
    else:
        message = result.get("result", {}).get("message", "Erro ao aprovar cadastro") if result else "Erro ao processar solicitação"
        return jsonify({"success": False, "message": message}), 400


@auth_blueprint.route("/reject-registration", methods=["POST"])
def reject_registration():
    if not session.get("user_id"):
        return jsonify({"success": False, "message": "Autenticação necessária"}), 401

    profile_access = session.get("profile_access", {})
    if not profile_access.get("admin"):
        return jsonify({"success": False, "message": "Acesso de administrador necessário"}), 403

    if request.is_json:
        data = request.json
        id_solicitacao = data.get("id_solicitacao")
        observacoes = data.get("observacoes", "").strip()
    else:
        id_solicitacao = request.form.get("id_solicitacao")
        observacoes = request.form.get("observacoes", "").strip()

    if not id_solicitacao:
        return jsonify({"success": False, "message": "Solicitação inválida"}), 400

    result = sql_queries.fetch_one(
        "queries/auth/reject_registration.sql",
        {
            "id_solicitacao": int(id_solicitacao),
            "cpf_admin": session["user_id"],
            "observacoes": observacoes if observacoes else None,
        },
    )

    if result and result.get("result") and result["result"].get("success"):
        return jsonify({"success": True, "message": "Cadastro rejeitado"})
    else:
        message = result.get("result", {}).get("message", "Erro ao rejeitar cadastro") if result else "Erro ao processar solicitação"
        return jsonify({"success": False, "message": message}), 400


@auth_blueprint.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Logout realizado com sucesso"})


def _build_profile_access(roles):
    """Build profile access dictionary from roles array."""
    if not roles:
        return {}
    return {role: True for role in roles}


def _get_redirect_url_for_user():
    """Get redirect URL based on user's primary role."""
    profile_access = session.get("profile_access", {})
    if profile_access.get("admin"):
        return "/admin/dashboard"
    if profile_access.get("staff"):
        return "/staff/dashboard"
    if profile_access.get("internal"):
        return "/internal/dashboard"
    if profile_access.get("external"):
        return "/external/dashboard"
    return "/"
