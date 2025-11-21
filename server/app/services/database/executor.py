from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from flask import current_app, g
from psycopg2.extras import RealDictCursor


DEFAULT_SQL_ROOT = Path(__file__).resolve().parents[3] / "sql"


class SQLExecutionError(RuntimeError):
    """Raised when a SQL asset cannot be executed."""


def _get_sql_root() -> Path:
    configured_root = current_app.config.get("SQL_ROOT_PATH")
    if configured_root:
        return Path(configured_root)
    return DEFAULT_SQL_ROOT


def _load_sql(relative_path: str) -> str:
    sql_root = _get_sql_root()
    sql_path = sql_root / relative_path
    if not sql_path.exists():
        raise SQLExecutionError(f"SQL asset not found: {sql_path}")

    return sql_path.read_text(encoding="utf-8")


def _get_connection():
    db_session = g.get("db_session")
    if db_session is None:
        return None
    return db_session.connection


def fetch_all(
    relative_path: str,
    params: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    connection = _get_connection()
    if connection is None:
        return []

    query = _load_sql(relative_path)
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query, params or {})
        return cursor.fetchall()


def fetch_one(
    relative_path: str,
    params: Mapping[str, Any] | None = None,
) -> dict[str, Any] | None:
    connection = _get_connection()
    if connection is None:
        return None

    query = _load_sql(relative_path)
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query, params or {})
        return cursor.fetchone()


def execute_statement(
    relative_path: str,
    params: Mapping[str, Any] | None = None,
) -> None:
    connection = _get_connection()
    if connection is None:
        return

    query = _load_sql(relative_path)
    with connection.cursor() as cursor:
        cursor.execute(query, params or {})
    connection.commit()
