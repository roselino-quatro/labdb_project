from flask import render_template

from app.routes.external import external_blueprint
from app.services.database import executor as sql_queries
from app.services.auth.decorators import require_role


@external_blueprint.get("/", endpoint="dashboard")
@require_role("external", "admin")
def dashboard() -> str:
    participations = sql_queries.fetch_all(
        "queries/external/external_participations.sql"
    )
    return render_template("external/dashboard.html", participations=participations)
