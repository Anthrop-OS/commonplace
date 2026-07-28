"""Read entries back from disk (or a string), validating against the schema."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

from .entry import Entry, parse_markdown
from .schema import SchemaSpec, load_schema
from .validate import validate_entry


def loads(text: str, *, schema: Optional[SchemaSpec] = None, validate: bool = True) -> Entry:
    entry = parse_markdown(text)
    if validate:
        entry = validate_entry(entry, schema if schema is not None else load_schema())
    return entry


def read_entry(
    path: Union[str, Path],
    *,
    schema: Optional[SchemaSpec] = None,
    validate: bool = True,
) -> Entry:
    text = Path(path).read_text(encoding="utf-8")
    return loads(text, schema=schema, validate=validate)
