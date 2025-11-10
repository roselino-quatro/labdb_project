from flask import Flask, g

from dbsession import DBSession


def register_extensions(app: Flask) -> None:
    _register_db_session(app)


def _register_db_session(app: Flask) -> None:
    @app.before_request
    def _create_db_session() -> None:
        try:
            g.db_session = DBSession(
                schema=app.config.get("DB_SCHEMA"),
                host=app.config.get("DB_HOST"),
                port=app.config.get("DB_PORT"),
                database=app.config.get("DB_NAME"),
                user=app.config.get("DB_USER"),
                password=app.config.get("DB_PASSWORD"),
            )
        except Exception as exc:  # pragma: no cover - database might be unavailable locally
            app.logger.error(
                "Failed to create database session: %s", exc, exc_info=exc
            )
            g.db_session = None

    @app.teardown_appcontext
    def _teardown_db_session(_: Exception | None) -> None:
        db_session: DBSession | None = g.pop("db_session", None)
        if db_session is not None:
            db_session.close()
