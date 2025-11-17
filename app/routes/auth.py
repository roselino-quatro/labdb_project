from __future__ import annotations

from typing import Any

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from psycopg2 import Error as PsycopgError

from app.services import auth_session, sql_queries


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

ERROR_MESSAGES = {
    "USER_NOT_FOUND": "We could not find a user with the provided identifier.",
    "USER_DISABLED": "The user is disabled. Contact an administrator.",
    "INVALID_CREDENTIALS": "Invalid credentials. Please try again.",
    "USER_ALREADY_EXISTS": "This CPF already has an active login.",
    "EMAIL_ALREADY_USED": "The provided email already belongs to another account.",
    "PERSON_NOT_FOUND": "CPF not found in the Pessoas registry.",
    "PASSWORD_REQUIRED": "Password is required.",
}


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if auth_session.is_authenticated() and request.method == "GET":
        return redirect(_resolve_post_login_redirect())

    form_data: dict[str, Any] = {}

    if request.method == "POST":
        form_data["login_identifier"] = (
            request.form.get("login_identifier", "").strip()
        )
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))
        params = {
            "login_identifier": form_data["login_identifier"],
            "password": password,
            "client_identifier": request.remote_addr or "unknown",
        }

        try:
            payload = sql_queries.fetch_one("queries/auth/login_user.sql", params)
        except PsycopgError as exc:
            current_app.logger.warning("Authentication failed: %s", exc, exc_info=exc)
            flash(_translate_db_error(exc), "error")
            return render_template("auth/login.html", form_data=form_data)

        if not payload:
            flash("Authentication failed. Please verify your credentials.", "error")
            return render_template("auth/login.html", form_data=form_data)

        auth_session.begin_session(payload, remember=remember)
        flash("Login successful.", "success")
        return redirect(_resolve_post_login_redirect(payload))

    return render_template("auth/login.html", form_data=form_data)


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form_data: dict[str, Any] = {}

    if request.method == "POST":
        form_data["cpf"] = request.form.get("cpf", "").strip()
        form_data["email"] = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        params = {
            "cpf": form_data["cpf"],
            "email": form_data["email"],
            "password": password,
        }

        try:
            payload = sql_queries.fetch_one("queries/auth/register_user.sql", params)
        except PsycopgError as exc:
            current_app.logger.warning("Registration failed: %s", exc, exc_info=exc)
            flash(_translate_db_error(exc), "error")
            return render_template("auth/register.html", form_data=form_data)

        if not payload:
            flash("Registration failed. Contact support.", "error")
            return render_template("auth/register.html", form_data=form_data)

        auth_session.begin_session(payload, remember=False)
        flash("Registration completed successfully.", "success")
        return redirect(payload.get("redirect_endpoint") or url_for("home.dashboard"))

    return render_template("auth/register.html", form_data=form_data)


@auth_blueprint.route("/logout", methods=["GET"])
def logout():
    auth_session.end_session()
    flash("You have been signed out.", "success")
    return redirect(url_for("auth.login"))


def _resolve_post_login_redirect(payload: dict[str, Any] | None = None) -> str:
    next_param = request.form.get("next") or request.args.get("next")
    if next_param:
        return next_param
    if payload:
        redirect_endpoint = payload.get("redirect_endpoint")
        if redirect_endpoint:
            return redirect_endpoint
    return auth_session.get_primary_endpoint()


def _translate_db_error(exc: PsycopgError) -> str:
    raw_message = ""
    if getattr(exc, "diag", None) and getattr(exc.diag, "message_primary", None):
        raw_message = exc.diag.message_primary
    else:
        raw_message = str(exc)

    for code, message in ERROR_MESSAGES.items():
        if code in raw_message:
            return message

    return "Authentication service is temporarily unavailable."
