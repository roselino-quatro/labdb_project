from __future__ import annotations

from datetime import date
from types import SimpleNamespace
from typing import Iterable, Sequence

from flask import url_for


class Pagination(SimpleNamespace):
    pass


def build_option_list(
    values: Iterable[tuple[str, str]], selected_value: str | None = None
) -> list[dict[str, str | bool]]:
    option_list: list[dict[str, str | bool]] = []
    for value, label in values:
        option_list.append(
            {
                "value": value,
                "label": label,
                "selected": selected_value == value,
            }
        )
    if selected_value is None and option_list:
        option_list[0]["selected"] = True
    return option_list


def empty_model(fields: Sequence[str]) -> SimpleNamespace:
    return SimpleNamespace(**{field: "" for field in fields})


def stub_pagination(endpoint: str) -> Pagination:
    return Pagination(
        start=0,
        end=0,
        total=0,
        prev_url=None,
        next_url=None,
        self_url=url_for(endpoint),
    )


def today_iso() -> str:
    return date.today().isoformat()
