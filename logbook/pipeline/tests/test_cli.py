from __future__ import annotations

import pytest

from commonplace_logbook.cli import main


def _write_entry_file(tmp_path, visibility="private", redaction=False):
    text = (
        "---\n"
        f"visibility: {visibility}\n"
        "ts: 2026-06-03T14:22:00Z\n"
        "type: reflection\n"
        "actor: agent\n"
        f"redaction_checked: {str(redaction).lower()}\n"
        "---\n\nbody\n"
    )
    p = tmp_path / "e.md"
    p.write_text(text, encoding="utf-8")
    return p


def test_validate_ok(tmp_path, capsys):
    p = _write_entry_file(tmp_path)
    assert main(["validate", str(p)]) == 0
    assert "ok: valid private" in capsys.readouterr().out


def test_validate_reports_error(tmp_path, capsys):
    p = tmp_path / "bad.md"
    p.write_text("---\nvisibility: public\n---\nbody\n", encoding="utf-8")
    assert main(["validate", str(p)]) == 1
    assert "error:" in capsys.readouterr().err


def test_route_shows_tier_and_path(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("COMMONPLACE_LOGBOOK_HOME", str(tmp_path / "store"))
    p = _write_entry_file(tmp_path)
    assert main(["route", str(p)]) == 0
    out = capsys.readouterr().out
    assert out.startswith("private\t")
    assert "entries" in out


def test_emit_dry_run_writes_nothing(tmp_path, monkeypatch, capsys):
    store = tmp_path / "store"
    monkeypatch.setenv("COMMONPLACE_LOGBOOK_HOME", str(store))
    p = _write_entry_file(tmp_path)
    assert main(["emit", str(p), "--dry-run"]) == 0
    assert "would write" in capsys.readouterr().out
    assert not store.exists()


def test_emit_writes_to_store(tmp_path, monkeypatch, capsys):
    store = tmp_path / "store"
    monkeypatch.setenv("COMMONPLACE_LOGBOOK_HOME", str(store))
    p = _write_entry_file(tmp_path)
    assert main(["emit", str(p)]) == 0
    assert "wrote [private]" in capsys.readouterr().out
    assert list((store / "entries").glob("*.entry.md"))


def test_emit_gate_blocks_shareable(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("COMMONPLACE_LOGBOOK_HOME", str(tmp_path / "store"))
    p = _write_entry_file(tmp_path, visibility="shareable", redaction=False)
    assert main(["emit", str(p)]) == 1
    assert "redaction_checked" in capsys.readouterr().err


def test_stdin_source(monkeypatch, capsys):
    text = "---\nvisibility: private\nts: 2026-06-03T14:22:00Z\ntype: action\nactor: dyad\n---\n\nb\n"
    monkeypatch.setattr("sys.stdin", _FakeStdin(text))
    assert main(["validate", "-"]) == 0
    assert "ok: valid private action" in capsys.readouterr().out


class _FakeStdin:
    def __init__(self, text):
        self._text = text

    def read(self):
        return self._text
