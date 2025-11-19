from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from flask import Flask, session


PROFILE_DEFINITIONS: list[dict[str, str]] = [
    {
        "key": "admin",
        "endpoint": "admin.dashboard",
        "label": "Administrador",
    },
    {
        "key": "staff",
        "endpoint": "staff.dashboard",
        "label": "Funcionário CEFER",
    },
    {
        "key": "internal",
        "endpoint": "internal.dashboard",
        "label": "Interno USP",
    },
    {
        "key": "external",
        "endpoint": "external.dashboard",
        "label": "Externo USP",
    },
]

PROFILE_KEY_INDEX: set[str] = {
    profile_definition["key"] for profile_definition in PROFILE_DEFINITIONS
}


def register_context_processors(app: Flask) -> None:
    @app.context_processor
    def inject_profile_navigation() -> dict[str, Any]:
        allowed_profile_keys = _resolve_allowed_profiles(session.get("profile_access"))
        allowed_profile_keys_set = set(allowed_profile_keys)

        profile_navigation = [
            _build_profile_payload(profile_definition)
            for profile_definition in PROFILE_DEFINITIONS
            if profile_definition["key"] in allowed_profile_keys_set
        ]

        # Add current user information
        current_user = None
        if session.get("user_id"):
            current_user = {
                "user_id": session.get("user_id"),
                "email": session.get("user_email"),
                "nome": session.get("user_nome"),
            }

        return {
            "profile_navigation": profile_navigation,
            "current_user": current_user,
        }


def _build_profile_payload(profile_definition: dict[str, str]) -> dict[str, str]:
    return {
        "key": profile_definition["key"],
        "endpoint": profile_definition["endpoint"],
        "label": profile_definition["label"],
    }


def _resolve_allowed_profiles(raw_value: Any) -> Iterable[str]:
    if raw_value is None:
        return [profile_definition["key"] for profile_definition in PROFILE_DEFINITIONS]

    if isinstance(raw_value, dict):
        return [
            str(key)
            for key, value in raw_value.items()
            if value and key in PROFILE_KEY_INDEX
        ]

    if isinstance(raw_value, (list, tuple, set)):
        return [
            str(value)
            for value in raw_value
            if str(value) in PROFILE_KEY_INDEX
        ]

    if isinstance(raw_value, str):
        if raw_value in PROFILE_KEY_INDEX:
            return [raw_value]
        return []

    return []
