from flask import render_template

from app.routes.reports import reports_blueprint
from app.services.database import executor as sql_queries
from app.services.auth.decorators import require_auth


@reports_blueprint.get("/", endpoint="overview")
@require_auth
def overview() -> str:
    reservation_rollup = sql_queries.fetch_all(
        "queries/reports/reservations_rollup.sql"
    )
    activities_cube = sql_queries.fetch_all(
        "queries/reports/activities_cube.sql"
    )
    participants_totals = sql_queries.fetch_all(
        "queries/reports/participants_totals.sql"
    )
    installation_ranking = sql_queries.fetch_all(
        "queries/reports/installation_ranking.sql"
    )

    context = {
        "reservation_rollup": reservation_rollup,
        "activities_cube": activities_cube,
        "participants_totals": participants_totals,
        "installation_ranking": installation_ranking,
    }
    return render_template("reports/overview.html", **context)
