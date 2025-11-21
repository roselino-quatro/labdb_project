from functools import wraps

from flask import jsonify, session


def require_auth(f):
    """Decorator to require user authentication."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id") and not session.get("external_token"):
            return jsonify({"success": False, "message": "Autenticação necessária"}), 401
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
            # Check for regular user authentication
            if session.get("user_id"):
                profile_access = session.get("profile_access", {})
                has_role = any(profile_access.get(role) for role in allowed_roles)

                if not has_role:
                    return jsonify({"success": False, "message": "Permissões insuficientes"}), 403

                return f(*args, **kwargs)

            # Check for external token authentication
            if session.get("external_token") and "external" in allowed_roles:
                return f(*args, **kwargs)

            return jsonify({"success": False, "message": "Autenticação necessária"}), 401

        return decorated_function

    return decorator


def require_external_auth():
    """Decorator to require external user authentication via token."""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get("external_token"):
                return jsonify({"success": False, "message": "Autenticação externa necessária"}), 401

            if not session.get("invite_id"):
                return jsonify({"success": False, "message": "Sessão de convite inválida"}), 401

            return f(*args, **kwargs)

        return decorated_function

    return decorator
