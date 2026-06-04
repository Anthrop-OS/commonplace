"""The redaction gate and tier-routed writing — the heart of the acceptance."""

from __future__ import annotations

import pytest

from commonplace_logbook import RedactionRequiredError, read_entry, write_entry

from conftest import make_entry


def test_private_writes_to_entries(store):
    result = write_entry(make_entry(visibility="private"), config=store)
    assert result.tier == "private"
    assert result.path.parent == store.home / "entries"
    assert result.path.exists()
    # round-trips off disk
    assert read_entry(result.path).body == "a small note about going north."


@pytest.mark.parametrize("tier", ["shareable", "narrative"])
def test_gated_tiers_refused_without_redaction(tier, store):
    with pytest.raises(RedactionRequiredError, match=tier):
        write_entry(make_entry(visibility=tier, redaction_checked=False), config=store)


@pytest.mark.parametrize("tier", ["shareable", "narrative"])
def test_gated_tiers_refused_when_flag_absent(tier, store):
    # redaction_checked defaults to False -> still refused
    with pytest.raises(RedactionRequiredError):
        write_entry(make_entry(visibility=tier), config=store)


@pytest.mark.parametrize("tier", ["shareable", "narrative"])
def test_gated_tiers_allowed_with_redaction(tier, store):
    result = write_entry(
        make_entry(visibility=tier, redaction_checked=True), config=store
    )
    assert result.tier == tier
    assert result.path.parent == store.home / tier
    assert result.path.exists()


def test_gate_fires_even_on_dry_run(store):
    with pytest.raises(RedactionRequiredError):
        write_entry(make_entry(visibility="shareable"), config=store, dry_run=True)


def test_dry_run_does_not_touch_disk(store):
    result = write_entry(make_entry(visibility="private"), config=store, dry_run=True)
    assert result.written is False
    assert not result.path.exists()
    assert not store.home.exists()


def test_write_is_idempotent(store):
    e = make_entry(visibility="private")
    first = write_entry(e, config=store)
    second = write_entry(e, config=store)
    assert first.path == second.path  # content-addressed
    assert list((store.home / "entries").glob("*.entry.md")) == [first.path]


def test_invalid_entry_rejected_before_write(store):
    with pytest.raises(Exception):
        write_entry(make_entry(visibility="public"), config=store)
    assert not store.home.exists()
