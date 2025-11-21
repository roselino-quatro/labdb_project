from flask import jsonify, request

from app.routes.staff import staff_blueprint
from app.services.database import executor as sql_queries
from app.services.auth.decorators import require_role


@staff_blueprint.get("/", endpoint="dashboard")
@require_role("staff", "admin")
def dashboard():
    filters = {
        "weekday": request.args.get("weekday") or None,
        "group_name": request.args.get("group") or None,
        "modality": request.args.get("modality") or None,
    }

    activities = sql_queries.fetch_all("queries/staff/activities.sql", filters)

    return jsonify({
        "success": True,
        "filters": filters,
        "activities": activities,
    })
