from flask import render_template, request

from app.routes.decorators import require_roles
from app.routes.staff import staff_blueprint
from app.services import sql_queries


@staff_blueprint.get("/", endpoint="dashboard")
@require_roles("staff", "admin")
def dashboard() -> str:
    filters = {
        "weekday": request.args.get("weekday") or None,
        "group_name": request.args.get("group") or None,
        "modality": request.args.get("modality") or None,
    }

    activities = sql_queries.fetch_all("queries/staff/activities.sql", filters)

    context = {
        "filters": filters,
        "activities": activities,
    }
    return render_template("staff/dashboard.html", **context)
