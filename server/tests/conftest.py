import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
from app.database import DBSession

@pytest.fixture
def dbsession():
    with DBSession() as db:
        with db.connection.cursor() as cur:
            cur.execute("DROP SCHEMA IF EXISTS tests CASCADE;")
            cur.execute("CREATE SCHEMA tests;")
            db.connection.commit()

    session = DBSession(schema="tests")
    try:
        yield session
    finally:
        try:
            session.connection.commit()
        except Exception:
            session.connection.rollback()
        session.close()

        with DBSession() as cleanup_db:
            with cleanup_db.connection.cursor() as cur:
                cur.execute("DROP SCHEMA IF EXISTS tests CASCADE;")
                cleanup_db.connection.commit()
