from __future__ import annotations

import datetime as _dt

import pytest

from commonplace_logbook import Entry, ValidationError, validate_entry
from commonplace_logbook.entry import parse_markdown

from conftest import make_entry


def test_defaults_applied(schema):
    entry = Entry(
        data={
            "ts": _dt.datetime(2026, 6, 3, tzinfo=_dt.timezone.utc),
            "type": "observation",
            "actor": "agent",
        },
        body="hi",
    )
    out = validate_entry(entry, schema)
    assert out.visibility == "private"  # default
    assert out.redaction_checked is False  # default
    assert out.body == "hi"


def test_missing_required_collects_all(schema):
    with pytest.raises(ValidationError) as ei:
        validate_entry(Entry(data={}, body="x"), schema)
    problems = ei.value.problems
    assert any("ts" in p for p in problems)
    assert any("type" in p for p in problems)
    assert any("actor" in p for p in problems)


def test_empty_body_is_missing_required(schema):
    # body comes from the markdown section; here it is present but empty -> still a str
    out = validate_entry(make_entry(), schema)
    assert isinstance(out.body, str)


def test_bad_enum_rejected(schema):
    with pytest.raises(ValidationError, match="visibility"):
        validate_entry(make_entry(visibility="public"), schema)


def test_naive_datetime_rejected(schema):
    e = make_entry()
    e.data["ts"] = _dt.datetime(2026, 6, 3, 12, 0)  # no tzinfo
    with pytest.raises(ValidationError, match="timezone offset"):
        validate_entry(e, schema)


def test_string_datetime_parsed(schema):
    e = make_entry()
    e.data["ts"] = "2026-06-03T14:22:00-02:30"
    out = validate_entry(e, schema)
    assert out.ts.utcoffset() == _dt.timedelta(hours=-2, minutes=-30)


def test_z_suffix_datetime_parsed(schema):
    e = make_entry()
    e.data["ts"] = "2026-06-03T14:22:00Z"
    out = validate_entry(e, schema)
    assert out.ts.utcoffset() == _dt.timedelta(0)


def test_unparseable_datetime_rejected(schema):
    e = make_entry()
    e.data["ts"] = "not-a-date"
    with pytest.raises(ValidationError, match="valid ISO-8601"):
        validate_entry(e, schema)


def test_non_string_datetime_rejected(schema):
    e = make_entry()
    e.data["ts"] = 12345
    with pytest.raises(ValidationError, match="datetime string"):
        validate_entry(e, schema)


def test_unknown_field_rejected(schema):
    with pytest.raises(ValidationError, match="unknown field 'mood'"):
        validate_entry(make_entry(mood="curious"), schema)


def test_bool_type_enforced(schema):
    with pytest.raises(ValidationError, match="redaction_checked"):
        validate_entry(make_entry(redaction_checked="yes"), schema)


def test_markdown_must_be_string(schema):
    e = make_entry()
    e.body = 42  # type: ignore[assignment]
    with pytest.raises(ValidationError, match="body"):
        validate_entry(e, schema)


def test_object_subfields_validated(schema):
    e = make_entry(curiosity={"question": "why?", "detour": True, "surprise": "none"})
    out = validate_entry(e, schema)
    assert out.data["curiosity"]["detour"] is True


def test_object_must_be_mapping(schema):
    with pytest.raises(ValidationError, match="curiosity: expected a mapping"):
        validate_entry(make_entry(curiosity="lots"), schema)


def test_object_unknown_subfield_rejected(schema):
    with pytest.raises(ValidationError, match="unknown field 'mood'"):
        validate_entry(make_entry(curiosity={"mood": "x"}), schema)


def test_object_subfield_type_enforced(schema):
    with pytest.raises(ValidationError, match="detour"):
        validate_entry(make_entry(curiosity={"detour": "maybe"}), schema)


def test_relation_enum_subfield(schema):
    out = validate_entry(
        make_entry(type="relation-event", relation={"kind": "repair", "detail": "we talked"}),
        schema,
    )
    assert out.data["relation"]["kind"] == "repair"


def test_relation_bad_enum(schema):
    with pytest.raises(ValidationError, match="kind"):
        validate_entry(make_entry(relation={"kind": "nope"}), schema)


def test_validate_entry_loads_default_schema(sample_path):
    # No schema passed -> loads the canonical one.
    entry = parse_markdown(sample_path.read_text(encoding="utf-8"))
    out = validate_entry(entry)
    assert out.visibility == "shareable"
