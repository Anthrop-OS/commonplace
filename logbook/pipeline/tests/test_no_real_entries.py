"""Guard: the pipeline must never create a real entry inside this repo.

AGENTS.md rule 2 / ADR-0005 — the record lives in a separate, gitignored repo.
The default store roots outside the working tree; this test asserts that and
that the test run left no ``*.entry.md`` anywhere under the repo.
"""

from __future__ import annotations

from pathlib import Path

from commonplace_logbook import StoreConfig, write_entry

from conftest import make_entry

REPO_ROOT = Path(__file__).resolve().parents[3]


def test_default_store_root_is_outside_repo():
    home = StoreConfig.from_env(environ={}).home
    assert REPO_ROOT not in home.parents
    assert home != REPO_ROOT


def test_writing_uses_only_the_given_out_of_repo_config(tmp_path):
    cfg = StoreConfig(home=tmp_path / "store")
    result = write_entry(make_entry(), config=cfg)
    assert tmp_path in result.path.parents


def test_repo_tree_contains_no_real_entries():
    offenders = [
        p
        for p in REPO_ROOT.rglob("*.entry.md")
        if ".git" not in p.parts
    ]
    assert offenders == [], f"real entries leaked into the repo: {offenders}"
