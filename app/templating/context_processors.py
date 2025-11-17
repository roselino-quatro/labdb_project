from __future__ import annotations

from typing import Any

from flask import Flask, get_flashed_messages

from app.services import auth_session


PROFILE_DEFINITIONS: list[dict[str, str]] = [
    {
        "key": "staff",
        "endpoint": "staff.dashboard",
        "label": "Staff Workspace",
    },
    {
        "key": "internal",
        "endpoint": "internal.dashboard",
        "label": "Internal USP Portal",
    },
    {
        "key": "external",
        "endpoint": "external.dashboard",
        "label": "External Guests",
    },
]

PROFILE_KEY_INDEX: set[str] = {
    profile_definition["key"] for profile_definition in PROFILE_DEFINITIONS
}


def register_context_processors(app: Flask) -> None:
    @app.context_processor
    def inject_template_defaults() -> dict[str, Any]:
        allowed_profile_keys = set(
            key for key in auth_session.get_session_roles() if key in PROFILE_KEY_INDEX
        )

        profile_navigation = [
            _build_profile_payload(profile_definition)
            for profile_definition in PROFILE_DEFINITIONS
            if profile_definition["key"] in allowed_profile_keys
        ]

        messages = get_flashed_messages(with_categories=True)

        return {
            "profile_navigation": profile_navigation,
            "messages": messages,
        }


def _build_profile_payload(profile_definition: dict[str, str]) -> dict[str, str]:
    return {
        "key": profile_definition["key"],
        "endpoint": profile_definition["endpoint"],
        "label": profile_definition["label"],
    }
