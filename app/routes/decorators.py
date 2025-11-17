from __future__ import annotations

from functools import wraps
from typing import Any, Callable, Sequence

from flask import flash, redirect, request, url_for

from app.services import auth_session


ViewFunc = Callable[..., Any]


def require_roles(*role_keys: str) -> Callable[[ViewFunc], ViewFunc]:
    normalized = tuple(role.lower() for role in role_keys if role)

    def decorator(view_func: ViewFunc) -> ViewFunc:
        @wraps(view_func)
        def wrapper(*args: Any, **kwargs: Any):
            if not auth_session.is_authenticated():
                flash("Please login to continue.", "error")
                return redirect(_login_redirect_target())

            if normalized and not auth_session.has_any_role(normalized):
                flash("You do not have permission to access this area.", "error")
                return redirect(auth_session.get_primary_endpoint() or "/")

            return view_func(*args, **kwargs)

        return wrapper

    return decorator


def _login_redirect_target() -> str:
    next_url = request.path
    return url_for("auth.login", next=next_url)
