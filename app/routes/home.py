from flask import Blueprint, redirect, url_for

from app.services import auth_session

home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/", methods=["GET"])
def index():
    if auth_session.is_authenticated():
        return redirect(auth_session.get_primary_endpoint())
    return redirect(url_for("auth.login"))


home_blueprint.add_url_rule("/", endpoint="dashboard", view_func=index)
