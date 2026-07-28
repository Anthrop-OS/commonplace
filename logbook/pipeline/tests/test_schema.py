from __future__ import annotations

import pytest

from commonplace_logbook import SchemaError, load_schema
from commonplace_logbook.schema import BODY_FIELD, SUPPORTED_VERSION, default_schema_path


def test_loads_canonical_schema(schema):
    assert schema.version == SUPPORTED_VERSION
    assert schema.fields["visibility"].required is True
    assert schema.fields["visibility"].default == "private"
    assert schema.fields["visibility"].values == ["private", "shareable", "narrative"]
    assert schema.fields["redaction_checked"].required is False
    assert schema.fields["redaction_checked"].default is False
    # object subfields parsed
    assert set(schema.fields["curiosity"].fields) == {"question", "detour", "surprise"}
    assert schema.fields["relation"].fields["kind"].type == "enum"


def test_body_is_not_a_frontmatter_field(schema):
    assert BODY_FIELD in schema.fields
    assert BODY_FIELD not in schema.frontmatter_fields


def test_default_path_env_override(monkeypatch, tmp_path):
    target = tmp_path / "x.yaml"
    monkeypatch.setenv("COMMONPLACE_LOGBOOK_SCHEMA", str(target))
    assert default_schema_path() == target


def test_missing_file_raises(tmp_path):
    with pytest.raises(SchemaError, match="not found"):
        load_schema(tmp_path / "nope.yaml")


def test_rejects_wrong_version(tmp_path):
    p = tmp_path / "s.yaml"
    p.write_text('$schema: "wrong/v9"\nrequired: {}\n', encoding="utf-8")
    with pytest.raises(SchemaError, match="unsupported schema version"):
        load_schema(p)


def test_rejects_non_mapping_root(tmp_path):
    p = tmp_path / "s.yaml"
    p.write_text("- a\n- b\n", encoding="utf-8")
    with pytest.raises(SchemaError, match="root must be a mapping"):
        load_schema(p)


def test_rejects_unknown_field_type(tmp_path):
    p = tmp_path / "s.yaml"
    p.write_text(
        f'$schema: "{SUPPORTED_VERSION}"\nrequired:\n  x: {{type: blob}}\n', encoding="utf-8"
    )
    with pytest.raises(SchemaError, match="unsupported type"):
        load_schema(p)


def test_rejects_enum_without_values(tmp_path):
    p = tmp_path / "s.yaml"
    p.write_text(
        f'$schema: "{SUPPORTED_VERSION}"\nrequired:\n  x: {{type: enum}}\n', encoding="utf-8"
    )
    with pytest.raises(SchemaError, match="non-empty 'values'"):
        load_schema(p)


def test_rejects_empty_schema(tmp_path):
    p = tmp_path / "s.yaml"
    p.write_text(f'$schema: "{SUPPORTED_VERSION}"\n', encoding="utf-8")
    with pytest.raises(SchemaError, match="no fields"):
        load_schema(p)


def test_rejects_non_mapping_field_spec(tmp_path):
    p = tmp_path / "s.yaml"
    p.write_text(f'$schema: "{SUPPORTED_VERSION}"\nrequired:\n  x: "scalar"\n', encoding="utf-8")
    with pytest.raises(SchemaError, match="expected a mapping"):
        load_schema(p)


def test_rejects_object_fields_non_mapping(tmp_path):
    p = tmp_path / "s.yaml"
    p.write_text(
        f'$schema: "{SUPPORTED_VERSION}"\n'
        "required:\n  x: {type: object, fields: [a, b]}\n",
        encoding="utf-8",
    )
    with pytest.raises(SchemaError, match="'fields' must be a mapping"):
        load_schema(p)


def test_rejects_non_mapping_block(tmp_path):
    p = tmp_path / "s.yaml"
    p.write_text(f'$schema: "{SUPPORTED_VERSION}"\nrequired: 3\n', encoding="utf-8")
    with pytest.raises(SchemaError, match="block must be a mapping"):
        load_schema(p)


def test_rejects_duplicate_field(tmp_path):
    p = tmp_path / "s.yaml"
    p.write_text(
        f'$schema: "{SUPPORTED_VERSION}"\n'
        "required:\n  x: {type: string}\n"
        "optional:\n  x: {type: bool}\n",
        encoding="utf-8",
    )
    with pytest.raises(SchemaError, match="declared twice"):
        load_schema(p)
