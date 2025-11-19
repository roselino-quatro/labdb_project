from flask import Flask

from app.routes.admin import admin_blueprint, init_app as init_admin_routes
from app.routes.auth import auth_blueprint
from app.routes.debug import debug_blueprint, init_app as init_debug_routes
from app.routes.external import external_blueprint, init_app as init_external_routes
from app.routes.home import home_blueprint
from app.routes.internal import internal_blueprint, init_app as init_internal_routes
from app.routes.staff import staff_blueprint, init_app as init_staff_routes
from app.routes.reports import reports_blueprint, init_app as init_reports_routes


def register_routes(app: Flask) -> None:
    init_admin_routes()
    init_reports_routes()
    init_staff_routes()
    init_internal_routes()
    init_external_routes()
    init_debug_routes()
    app.register_blueprint(external_blueprint)
    app.register_blueprint(internal_blueprint)
    app.register_blueprint(staff_blueprint)
    app.register_blueprint(reports_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(debug_blueprint)
