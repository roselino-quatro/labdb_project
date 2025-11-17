from flask import render_template

from app.routes.admin import admin_blueprint
from app.routes.decorators import require_roles
from app.services import sql_queries


@admin_blueprint.get("/", endpoint="dashboard")
@require_roles("admin")
def dashboard() -> str:
    stats = sql_queries.fetch_all("queries/admin/dashboard_stats.sql")
    upcoming_reservations = sql_queries.fetch_all(
        "queries/admin/upcoming_reservations.sql"
    )
    activity_enrollment = sql_queries.fetch_all(
        "queries/admin/activity_enrollment.sql"
    )

    context = {
        "stats": stats,
        "upcoming_reservations": upcoming_reservations,
        "activity_enrollment": activity_enrollment,
    }
    return render_template("admin/dashboard.html", **context)
