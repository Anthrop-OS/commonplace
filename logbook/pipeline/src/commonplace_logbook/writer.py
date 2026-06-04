"""Write an entry: validate, enforce the redaction gate, route by tier.

The redaction gate (AGENTS.md rule 3) lives here: a ``shareable``/``narrative``
entry is refused unless it carries ``redaction_checked: true``. ``private`` is
the default tier and is always emittable to the private store.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .entry import Entry, to_markdown
from .errors import RedactionRequiredError
from .schema import SchemaSpec, load_schema
from .store import PRIVATE, StoreConfig, entry_filename
from .validate import validate_entry

GATED_TIERS = ("shareable", "narrative")


@dataclass(frozen=True)
class WriteResult:
    path: Path
    tier: str
    markdown: str
    written: bool


def _assert_emittable(entry: Entry) -> None:
    tier = entry.visibility or PRIVATE
    if tier in GATED_TIERS and not entry.redaction_checked:
        raise RedactionRequiredError(
            f"refusing to emit a {tier!r} entry without redaction_checked: true "
            "(AGENTS.md rule 3 — run the redaction pass and set the flag first)"
        )


def write_entry(
    entry: Entry,
    *,
    schema: Optional[SchemaSpec] = None,
    config: Optional[StoreConfig] = None,
    dry_run: bool = False,
) -> WriteResult:
    schema = schema if schema is not None else load_schema()
    entry = validate_entry(entry, schema)
    _assert_emittable(entry)

    config = config if config is not None else StoreConfig.from_env()
    tier = entry.visibility or PRIVATE
    target_dir = config.dir_for(tier)
    path = target_dir / entry_filename(entry)
    markdown = to_markdown(entry)

    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown, encoding="utf-8")

    return WriteResult(path=path, tier=tier, markdown=markdown, written=not dry_run)
