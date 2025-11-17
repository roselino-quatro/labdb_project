from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence

from flask import session


AUTH_SESSION_KEY = "auth_context"
PROFILE_ACCESS_KEY = "profile_access"
PRIMARY_ENDPOINT_KEY = "primary_endpoint"
MappingPayload = Mapping[str, Any]


def begin_session(payload: MappingPayload, *, remember: bool = False) -> None:
    roles = _normalize_roles(payload.get("roles"))

    session[AUTH_SESSION_KEY] = {
        "user_id": payload.get("user_id"),
        "cpf": payload.get("cpf"),
        "email": payload.get("email"),
        "primary_role": payload.get("primary_role"),
    }
    session[PROFILE_ACCESS_KEY] = roles
    session[PRIMARY_ENDPOINT_KEY] = payload.get("redirect_endpoint") or "/"
    session.permanent = bool(remember)


def end_session() -> None:
    session.clear()


def is_authenticated() -> bool:
    return AUTH_SESSION_KEY in session


def get_session_roles() -> list[str]:
    return _normalize_roles(session.get(PROFILE_ACCESS_KEY))


def get_primary_endpoint() -> str:
    return session.get(PRIMARY_ENDPOINT_KEY, "/")


def get_current_user() -> dict[str, Any] | None:
    return session.get(AUTH_SESSION_KEY)


def has_any_role(required_roles: Sequence[str] | None) -> bool:
    if not required_roles:
        return True
    required = {role.lower() for role in required_roles}
    current = {role.lower() for role in get_session_roles()}
    return bool(current & required)


def _normalize_roles(raw_value: Any) -> list[str]:
    if raw_value is None:
        return []
    if isinstance(raw_value, str):
        return [raw_value]
    if isinstance(raw_value, Iterable):
        normalized: list[str] = []
        for value in raw_value:
            if value:
                normalized.append(str(value))
        return normalized
    return []
