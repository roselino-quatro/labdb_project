from flask import Blueprint, redirect, session, url_for


auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("home.index"))
