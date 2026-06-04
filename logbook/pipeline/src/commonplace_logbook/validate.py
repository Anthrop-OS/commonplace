"""Validate an :class:`Entry` against the parsed schema.

Validation is *structural*: required fields present, enum membership, datetime
parses with a timezone offset, object subfields well typed, no unknown keys.
Defaults declared in the schema (``visibility: private``, ``redaction_checked:
false``) are applied here. The redaction *gate* is deliberately NOT enforced
here — a ``shareable`` entry with ``redaction_checked: false`` is still well
formed; refusing to *emit* it is the writer's job (see :mod:`writer`).
"""

from __future__ import annotations

import datetime as _dt
from typing import Any, Dict, List, Tuple

from .entry import Entry
from .errors import ValidationError
from .schema import FieldSpec, SchemaSpec, load_schema


def _parse_datetime(value: Any) -> Tuple[Any, List[str]]:
    if isinstance(value, _dt.datetime):
        dt = value
    elif isinstance(value, str):
        raw = value.strip()
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        try:
            dt = _dt.datetime.fromisoformat(raw)
        except ValueError:
            return None, [f"not a valid ISO-8601 datetime: {value!r}"]
    else:
        return None, [f"expected an ISO-8601 datetime string, got {type(value).__name__}"]

    if dt.tzinfo is None or dt.utcoffset() is None:
        return None, ["datetime must carry a timezone offset (ISO-8601 with offset)"]
    return dt, []


def _check_field(spec: FieldSpec, value: Any) -> Tuple[Any, List[str]]:
    prefix = spec.name

    if spec.type == "enum":
        sval = value if isinstance(value, str) else str(value)
        if sval not in (spec.values or []):
            return None, [f"{prefix}: {value!r} is not one of {spec.values}"]
        return sval, []

    if spec.type == "datetime":
        dt, errs = _parse_datetime(value)
        return (dt, [f"{prefix}: {e}" for e in errs]) if errs else (dt, [])

    if spec.type in ("markdown", "string"):
        if not isinstance(value, str):
            return None, [f"{prefix}: expected a string, got {type(value).__name__}"]
        return value, []

    if spec.type == "bool":
        if not isinstance(value, bool):
            return None, [f"{prefix}: expected a bool, got {type(value).__name__}"]
        return value, []

    if spec.type == "object":
        if not isinstance(value, dict):
            return None, [f"{prefix}: expected a mapping, got {type(value).__name__}"]
        normalized: Dict[str, Any] = {}
        problems: List[str] = []
        for key in value:
            if key not in spec.fields:
                problems.append(f"{prefix}: unknown field {key!r}")
        for sub_name, sub_spec in spec.fields.items():
            if sub_name not in value:
                continue
            norm, errs = _check_field(sub_spec, value[sub_name])
            problems.extend(errs)
            if not errs:
                normalized[sub_name] = norm
        return (normalized, problems) if problems else (normalized, [])

    # Unreachable: schema loader rejects unknown types.
    return None, [f"{prefix}: unsupported field type {spec.type!r}"]  # pragma: no cover


def validate_payload(payload: Dict[str, Any], schema: SchemaSpec) -> Dict[str, Any]:
    problems: List[str] = []
    normalized: Dict[str, Any] = {}

    for key in payload:
        if key not in schema.fields:
            problems.append(f"unknown field {key!r}")

    for name, spec in schema.fields.items():
        if name in payload:
            norm, errs = _check_field(spec, payload[name])
            problems.extend(errs)
            if not errs:
                normalized[name] = norm
        elif spec.has_default:
            normalized[name] = spec.default
        elif spec.required:
            problems.append(f"missing required field {name!r}")
        # else: optional, no default, absent -> simply omitted

    if problems:
        raise ValidationError(sorted(problems))
    return normalized


def validate_entry(entry: Entry, schema: SchemaSpec = None) -> Entry:
    """Return a normalized copy of ``entry`` (defaults applied, ts as datetime).

    Raises :class:`ValidationError` listing every structural problem found.
    """
    schema = schema if schema is not None else load_schema()
    normalized = validate_payload(entry.as_validation_payload(), schema)
    body = normalized.pop("body", entry.body)
    return Entry(data=normalized, body=body)
