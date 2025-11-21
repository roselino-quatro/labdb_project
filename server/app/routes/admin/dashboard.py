from flask import render_template

from app.routes.admin import admin_blueprint
from app.services.database import executor as sql_queries
from app.services.auth.decorators import require_role


@admin_blueprint.get("/", endpoint="dashboard")
@require_role("admin")
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
