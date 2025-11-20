from flask import Blueprint, redirect, url_for


home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/", methods=["GET"])
def index():
    return redirect(url_for("internal.dashboard"))


home_blueprint.add_url_rule("/", endpoint="dashboard", view_func=index)
