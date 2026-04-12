#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Sequence


def format_value(value: Any, *, digits: int = 3, none_label: str = "n/a") -> str:
    if value is None:
        return none_label
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def code(value: Any, *, digits: int = 3, none_label: str = "n/a") -> str:
    return f"`{format_value(value, digits=digits, none_label=none_label)}`"


def render_markdown_table(headers: Sequence[str], rows: Iterable[Sequence[str]]) -> list[str]:
    normalized_rows = [list(row) for row in rows]
    return [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
        *("| " + " | ".join(row) + " |" for row in normalized_rows),
    ]


def write_markdown(path: Path, lines: Sequence[str], *, bom: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if bom else "utf-8"
    text = "\n".join(lines).rstrip() + "\n"
    path.write_text(text, encoding=encoding)


def write_json(path: Path, payload: Any, *, bom: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if bom else "utf-8"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding=encoding)
