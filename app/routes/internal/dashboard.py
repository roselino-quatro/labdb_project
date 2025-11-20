from flask import render_template, request

from app.routes.internal import internal_blueprint
from app.services.database import executor as sql_queries
from app.services.auth.decorators import require_role


@internal_blueprint.get("/", endpoint="dashboard")
@require_role("internal", "admin")
def dashboard() -> str:
    cpf = request.args.get("cpf") or ""
    reservas = []
    if cpf:
        reservas = sql_queries.fetch_all(
            "queries/internal/reservas_por_interno.sql",
            {"cpf": cpf},
        )

    date_param = request.args.get("date") or None
    start_param = request.args.get("start") or None
    end_param = request.args.get("end") or None

    available_installs: list[dict[str, str]] = []
    if date_param and start_param and end_param:
        available_installs = sql_queries.fetch_all(
            "queries/internal/instalacoes_disponiveis.sql",
            {
                "date": date_param,
                "start": start_param,
                "end": end_param,
            },
        )

    context = {
        "cpf": cpf,
        "reservas": reservas,
        "date_filter": date_param,
        "start_filter": start_param,
        "end_filter": end_param,
        "available_installs": available_installs,
    }
    return render_template("internal/dashboard.html", **context)
