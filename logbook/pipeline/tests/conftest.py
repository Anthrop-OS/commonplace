from __future__ import annotations

import datetime as _dt
from pathlib import Path

import pytest

from commonplace_logbook import Entry, StoreConfig, load_schema

REPO_LOGBOOK = Path(__file__).resolve().parents[2]
SAMPLE = REPO_LOGBOOK / "schema" / "sample.redacted.md"


@pytest.fixture(scope="session")
def schema():
    return load_schema()


@pytest.fixture
def sample_path() -> Path:
    return SAMPLE


@pytest.fixture
def store(tmp_path) -> StoreConfig:
    """A store rooted entirely in a tmp dir — never the repo."""
    return StoreConfig(home=tmp_path / "logbook")


def make_entry(visibility="private", redaction_checked=None, **extra) -> Entry:
    data = {
        "visibility": visibility,
        "ts": _dt.datetime(2026, 6, 3, 14, 22, tzinfo=_dt.timezone.utc),
        "type": "reflection",
        "actor": "agent",
    }
    if redaction_checked is not None:
        data["redaction_checked"] = redaction_checked
    data.update(extra)
    return Entry(data=data, body="a small note about going north.")
