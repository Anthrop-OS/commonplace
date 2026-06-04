"""Acceptance: the synthetic sample round-trips with full fidelity."""

from __future__ import annotations

import datetime as _dt

from commonplace_logbook import loads, read_entry, to_markdown


def test_sample_reads_and_validates(sample_path):
    entry = read_entry(sample_path)
    assert entry.visibility == "shareable"
    assert entry.type == "reflection"
    assert entry.actor == "agent"
    assert entry.redaction_checked is True
    assert isinstance(entry.ts, _dt.datetime)
    assert entry.ts.utcoffset() == _dt.timedelta(hours=-2, minutes=-30)
    assert entry.data["curiosity"]["detour"] is True
    assert "second clearing" in entry.body


def test_roundtrip_is_semantically_stable(sample_path):
    original = read_entry(sample_path)
    reparsed = loads(to_markdown(original))
    assert reparsed.data == original.data
    assert reparsed.body == original.body


def test_roundtrip_serialization_is_idempotent(sample_path):
    once = to_markdown(read_entry(sample_path))
    twice = to_markdown(loads(once))
    assert once == twice


def test_read_without_validation_skips_normalization(sample_path):
    # validate=False -> raw parse, ts stays whatever YAML produced, no defaults.
    raw = loads(sample_path.read_text(encoding="utf-8"), validate=False)
    assert raw.visibility == "shareable"
    assert "redaction_checked" in raw.data  # present in this sample


def test_body_is_preserved_verbatim(sample_path):
    raw = sample_path.read_text(encoding="utf-8")
    # The body is everything after the closing frontmatter delimiter.
    body_in_file = raw.split("---", 2)[2].strip("\n")
    assert read_entry(sample_path).body == body_in_file
