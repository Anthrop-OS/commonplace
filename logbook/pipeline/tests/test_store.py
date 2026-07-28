from __future__ import annotations

from pathlib import Path

import pytest

from commonplace_logbook import NARRATIVE, PRIVATE, SHAREABLE, StoreConfig, entry_filename
from commonplace_logbook.store import DEFAULT_HOME

from conftest import make_entry


def test_default_store_is_outside_the_repo():
    cfg = StoreConfig.from_env(environ={})
    home = cfg.home
    assert home == DEFAULT_HOME.expanduser()
    repo_root = Path(__file__).resolve().parents[3]
    assert repo_root not in home.parents and home != repo_root


def test_env_overrides(tmp_path):
    cfg = StoreConfig.from_env(
        environ={
            "COMMONPLACE_LOGBOOK_HOME": str(tmp_path / "store"),
            "COMMONPLACE_OBSIDIAN_VAULT": str(tmp_path / "vault"),
        }
    )
    assert cfg.home == tmp_path / "store"
    assert cfg.obsidian_vault == tmp_path / "vault"


def test_private_routes_to_entries(tmp_path):
    cfg = StoreConfig(home=tmp_path)
    assert cfg.dir_for(PRIVATE) == tmp_path / "entries"


def test_private_routes_to_obsidian_when_set(tmp_path):
    cfg = StoreConfig(home=tmp_path, obsidian_vault=tmp_path / "vault")
    assert cfg.dir_for(PRIVATE) == tmp_path / "vault"


def test_shareable_and_narrative_dirs(tmp_path):
    cfg = StoreConfig(home=tmp_path)
    assert cfg.dir_for(SHAREABLE) == tmp_path / "shareable"
    assert cfg.dir_for(NARRATIVE) == tmp_path / "narrative"


def test_unknown_tier_raises(tmp_path):
    with pytest.raises(ValueError, match="unknown visibility tier"):
        StoreConfig(home=tmp_path).dir_for("public")


def test_filename_is_deterministic_and_sortable():
    e = make_entry()
    name = entry_filename(e)
    assert name == entry_filename(e)  # content-addressed -> stable
    assert name.startswith("20260603T142200Z-reflection-")
    assert name.endswith(".entry.md")


def test_filename_changes_with_content():
    a = entry_filename(make_entry(curiosity={"question": "a?"}))
    b = entry_filename(make_entry(curiosity={"question": "b?"}))
    assert a != b


def test_filename_undated_when_ts_not_datetime():
    e = make_entry()
    e.data["ts"] = "raw-string"  # not yet validated to a datetime
    assert entry_filename(e).startswith("undated-reflection-")
