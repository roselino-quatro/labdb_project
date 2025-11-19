from functools import wraps

from flask import flash, redirect, session, url_for


def require_auth(f):
    """Decorator to require user authentication."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("Autenticação necessária", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def require_role(*allowed_roles):
    """Decorator to require specific user roles.

    Args:
        *allowed_roles: One or more role names (e.g., 'admin', 'staff')
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get("user_id"):
                flash("Autenticação necessária", "error")
                return redirect(url_for("auth.login"))

            profile_access = session.get("profile_access", {})
            has_role = any(profile_access.get(role) for role in allowed_roles)

            if not has_role:
                flash("Permissões insuficientes", "error")
                return redirect(url_for("home.index"))

            return f(*args, **kwargs)

        return decorated_function

    return decorator
