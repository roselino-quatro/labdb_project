from flask import Flask, g
from flask_cors import CORS

from app.database import DBSession
from app.services.database.bootstrap import ensure_schema_populated


def register_extensions(app: Flask) -> None:
    # Permitir todas as origens em desenvolvimento para facilitar o desenvolvimento
    # Em produção, especificar origens específicas
    import os
    debug_mode = app.config.get("DEBUG", False) or os.environ.get("FLASK_DEBUG", "false").lower() == "true"

    if debug_mode:
        # Em desenvolvimento, permitir todas as origens locais
        CORS(app, supports_credentials=True, origins=[
            'http://localhost:3000',
            'http://localhost:3001',
            'http://127.0.0.1:3000',
            'http://127.0.0.1:3001',
            'http://nextjs_app:3000',
        ])
    else:
        # Em produção, apenas origens específicas
        CORS(app, supports_credentials=True, origins=['http://localhost:3000', 'http://nextjs_app:3000'])
    _register_db_session(app)


def _register_db_session(app: Flask) -> None:
    @app.before_request
    def _create_db_session() -> None:
        from flask import request
        # Pular bootstrap para rotas de debug para evitar loop infinito
        if request.endpoint and request.endpoint.startswith('debug.'):
            try:
                g.db_session = DBSession(
                    schema=app.config.get("DB_SCHEMA"),
                    host=app.config.get("DB_HOST"),
                    port=app.config.get("DB_PORT"),
                    database=app.config.get("DB_NAME"),
                    user=app.config.get("DB_USER"),
                    password=app.config.get("DB_PASSWORD"),
                )
            except Exception as exc:
                app.logger.error(f"Failed to create database session: {exc}")
                if 'db_session' not in g:
                    g.db_session = None
            return

        try:
            g.db_session = DBSession(
                schema=app.config.get("DB_SCHEMA"),
                host=app.config.get("DB_HOST"),
                port=app.config.get("DB_PORT"),
                database=app.config.get("DB_NAME"),
                user=app.config.get("DB_USER"),
                password=app.config.get("DB_PASSWORD"),
            )
            # Sempre garantir que o schema existe antes de processar a requisição
            app.logger.info("Chamando ensure_schema_populated...")
            ensure_schema_populated(g.db_session)
            app.logger.info("ensure_schema_populated concluído")
        except Exception as exc:  # pragma: no cover - database might be unavailable locally
            app.logger.error(
                "Failed to create database session or populate schema: %s", exc, exc_info=exc
            )
            # Não remover db_session se já foi criado - apenas logar o erro
            # Isso permite que a aplicação continue tentando criar o schema
            if 'db_session' not in g:
                g.db_session = None

    @app.teardown_appcontext
    def _teardown_db_session(_: Exception | None) -> None:
        db_session: DBSession | None = g.pop("db_session", None)
        if db_session is not None:
            db_session.close()
