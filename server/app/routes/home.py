from flask import Blueprint, jsonify


home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/", methods=["GET"])
def index():
    return jsonify({"message": "CEFER API", "redirect": "/admin/dashboard"})


home_blueprint.add_url_rule("/", endpoint="dashboard", view_func=index)
