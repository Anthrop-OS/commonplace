"""Visibility-tier routing to on-disk locations.

The private record never lives in this repo (AGENTS.md rule 2 / ADR-0005). So
the default store roots **outside** the repo — ``~/.commonplace/logbook`` — and
every path is env-overridable for the operator's own setup (e.g. an Obsidian
vault). Nothing here writes into the working tree by default; a stray entry can
therefore never be committed.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .entry import Entry, to_markdown

PRIVATE = "private"
SHAREABLE = "shareable"
NARRATIVE = "narrative"

DEFAULT_HOME = Path("~/.commonplace/logbook")


@dataclass(frozen=True)
class StoreConfig:
    home: Path
    obsidian_vault: Optional[Path] = None

    @classmethod
    def from_env(cls, environ: Optional[dict] = None) -> "StoreConfig":
        environ = environ if environ is not None else os.environ
        home = Path(environ.get("COMMONPLACE_LOGBOOK_HOME", str(DEFAULT_HOME))).expanduser()
        vault_raw = environ.get("COMMONPLACE_OBSIDIAN_VAULT")
        vault = Path(vault_raw).expanduser() if vault_raw else None
        return cls(home=home, obsidian_vault=vault)

    def dir_for(self, tier: str) -> Path:
        if tier == PRIVATE:
            return self.obsidian_vault if self.obsidian_vault is not None else self.home / "entries"
        if tier == SHAREABLE:
            return self.home / "shareable"
        if tier == NARRATIVE:
            return self.home / "narrative"
        raise ValueError(f"unknown visibility tier: {tier!r}")


def _ts_prefix(ts: object) -> str:
    if isinstance(ts, _dt.datetime):
        return ts.astimezone(_dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return "undated"


def entry_filename(entry: Entry) -> str:
    """Deterministic, sortable, collision-resistant filename for an entry.

    ``<utc-timestamp>-<type>-<content-hash8>.entry.md`` — content-addressed so
    re-emitting the same entry overwrites in place (idempotent) rather than
    accumulating duplicates.
    """
    digest = hashlib.sha1(to_markdown(entry).encode("utf-8")).hexdigest()[:8]
    etype = entry.type or "entry"
    return f"{_ts_prefix(entry.ts)}-{etype}-{digest}.entry.md"
