"""Load and model ``logbook/schema/entry.schema.yaml``.

The schema file is a small hand-rolled DSL (not JSON Schema): a ``required`` and
an ``optional`` block, each mapping a field name to a spec with a ``type`` and,
depending on the type, ``values`` (enum), ``default``, or nested ``fields``
(object). This module parses that DSL into :class:`SchemaSpec` so the validator
binds to the *file*, never to hand-copied field lists that could drift from it.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .errors import SchemaError

SCALAR_TYPES = frozenset({"enum", "datetime", "markdown", "bool", "string"})
SUPPORTED_VERSION = "commonplace/logbook-entry/v0.1"

# The field that lives in the markdown body, not the frontmatter.
BODY_FIELD = "body"

_UNSET = object()


@dataclass(frozen=True)
class FieldSpec:
    name: str
    type: str
    required: bool
    values: Optional[List[str]] = None
    default: Any = _UNSET
    fields: Dict[str, "FieldSpec"] = field(default_factory=dict)

    @property
    def has_default(self) -> bool:
        return self.default is not _UNSET


@dataclass(frozen=True)
class SchemaSpec:
    version: str
    fields: Dict[str, FieldSpec]

    @property
    def frontmatter_fields(self) -> Dict[str, FieldSpec]:
        return {n: f for n, f in self.fields.items() if n != BODY_FIELD}


def default_schema_path() -> Path:
    """Resolve the canonical schema path.

    Honors ``COMMONPLACE_LOGBOOK_SCHEMA`` if set, else the in-tree
    ``logbook/schema/entry.schema.yaml`` relative to this package.
    """
    override = os.environ.get("COMMONPLACE_LOGBOOK_SCHEMA")
    if override:
        return Path(override).expanduser()
    # src/commonplace_logbook/schema.py -> logbook/schema/entry.schema.yaml
    return Path(__file__).resolve().parents[3] / "schema" / "entry.schema.yaml"


def _parse_field(name: str, raw: Any, *, required: bool) -> FieldSpec:
    if not isinstance(raw, dict):
        raise SchemaError(f"field {name!r}: expected a mapping, got {type(raw).__name__}")
    ftype = raw.get("type")
    if ftype not in SCALAR_TYPES and ftype != "object":
        raise SchemaError(f"field {name!r}: unsupported type {ftype!r}")

    values = None
    if ftype == "enum":
        values = raw.get("values")
        if not isinstance(values, list) or not values:
            raise SchemaError(f"enum field {name!r}: requires a non-empty 'values' list")
        values = [str(v) for v in values]

    subfields: Dict[str, FieldSpec] = {}
    if ftype == "object":
        raw_fields = raw.get("fields", {})
        if not isinstance(raw_fields, dict):
            raise SchemaError(f"object field {name!r}: 'fields' must be a mapping")
        # Object subfields are themselves optional unless re-declared required.
        subfields = {
            sub: _parse_field(f"{name}.{sub}", spec, required=False)
            for sub, spec in raw_fields.items()
        }

    default = raw["default"] if "default" in raw else _UNSET
    return FieldSpec(
        name=name,
        type=ftype,
        required=required,
        values=values,
        default=default,
        fields=subfields,
    )


def load_schema(path: Optional[Path] = None) -> SchemaSpec:
    schema_path = Path(path) if path is not None else default_schema_path()
    if not schema_path.is_file():
        raise SchemaError(f"schema not found: {schema_path}")
    raw = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise SchemaError("schema root must be a mapping")

    version = raw.get("$schema")
    if version != SUPPORTED_VERSION:
        raise SchemaError(
            f"unsupported schema version {version!r} (expected {SUPPORTED_VERSION!r})"
        )

    fields: Dict[str, FieldSpec] = {}
    for block, is_required in (("required", True), ("optional", False)):
        section = raw.get(block, {}) or {}
        if not isinstance(section, dict):
            raise SchemaError(f"'{block}' block must be a mapping")
        for name, spec in section.items():
            if name in fields:
                raise SchemaError(f"field {name!r} declared twice")
            fields[name] = _parse_field(name, spec, required=is_required)

    if not fields:
        raise SchemaError("schema declares no fields")
    return SchemaSpec(version=version, fields=fields)
