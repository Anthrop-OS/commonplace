from __future__ import annotations

import pytest

from commonplace_logbook import EntryFormatError, parse_markdown, to_markdown
from commonplace_logbook.entry import Entry


def test_no_leading_delimiter():
    with pytest.raises(EntryFormatError, match="must start with"):
        parse_markdown("visibility: private\nbody")


def test_unterminated_frontmatter():
    with pytest.raises(EntryFormatError, match="unterminated"):
        parse_markdown("---\nvisibility: private\nbody text")


def test_frontmatter_not_yaml():
    with pytest.raises(EntryFormatError, match="not valid YAML"):
        parse_markdown("---\nfoo: [unclosed\n---\nbody")


def test_frontmatter_not_a_mapping():
    with pytest.raises(EntryFormatError, match="must be a YAML mapping"):
        parse_markdown("---\n- a\n- b\n---\nbody")


def test_empty_frontmatter_yields_empty_data():
    entry = parse_markdown("---\n---\n\nbody here")
    assert entry.data == {}
    assert entry.body == "body here"


def test_blank_frontmatter_yields_empty_data():
    entry = parse_markdown("---\n\n---\n\nbody")
    assert entry.data == {}


def test_to_markdown_method_matches_function():
    e = Entry(data={"visibility": "private"}, body="x")
    assert e.to_markdown() == to_markdown(e)


def test_body_internal_blank_lines_preserved():
    e = Entry(data={"visibility": "private"}, body="para one\n\npara two")
    assert parse_markdown(to_markdown(e)).body == "para one\n\npara two"


def test_yamlify_handles_lists():
    e = Entry(data={"tags": ["a", "b"], "visibility": "private"}, body="x")
    md = to_markdown(e)
    assert "- a" in md and "- b" in md


def test_null_frontmatter_yields_empty_data():
    # Non-blank frontmatter that parses to None (`null`) -> empty data.
    entry = parse_markdown("---\nnull\n---\n\nbody")
    assert entry.data == {}
    assert entry.body == "body"
