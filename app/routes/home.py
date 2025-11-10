from flask import Blueprint, g, render_template

from app.routes.admin.dashboard import build_dashboard_context


home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/", methods=["GET"])
def index():
    db_session = g.get("db_session")
    database_time_iso = None
    if db_session is not None:
        with db_session.connection.cursor() as cursor:
            cursor.execute("SELECT NOW()")
            result = cursor.fetchone()
            database_time_iso = result[0].isoformat()

    return render_template(
        "admin/dashboard.html",
        **build_dashboard_context(database_time=database_time_iso),
    )


home_blueprint.add_url_rule("/", endpoint="dashboard", view_func=index)
