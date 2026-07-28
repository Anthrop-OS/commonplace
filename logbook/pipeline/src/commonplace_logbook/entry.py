"""The :class:`Entry` model and the on-disk markdown serialization.

An entry is YAML frontmatter (the typed fields) plus a markdown ``body``,
matching ``logbook/schema/sample.redacted.md``::

    ---
    visibility: private
    ts: 2026-06-03T14:22:00-02:30
    type: reflection
    actor: agent
    ---

    body markdown here
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field
from typing import Any, Dict

import yaml

from .errors import EntryFormatError

_DELIM = "---"


@dataclass
class Entry:
    """A logbook entry: typed frontmatter ``data`` + markdown ``body``."""

    data: Dict[str, Any] = field(default_factory=dict)
    body: str = ""

    @property
    def visibility(self) -> Any:
        return self.data.get("visibility")

    @property
    def ts(self) -> Any:
        return self.data.get("ts")

    @property
    def type(self) -> Any:
        return self.data.get("type")

    @property
    def actor(self) -> Any:
        return self.data.get("actor")

    @property
    def redaction_checked(self) -> bool:
        return bool(self.data.get("redaction_checked", False))

    def as_validation_payload(self) -> Dict[str, Any]:
        """Flatten to ``{**frontmatter, body}`` for schema validation.

        ``body`` is a schema field that lives in the markdown section rather
        than the frontmatter, so validation needs it folded back in.
        """
        payload = dict(self.data)
        payload["body"] = self.body
        return payload

    def to_markdown(self) -> str:
        return to_markdown(self)


def _yamlify(value: Any) -> Any:
    """Coerce values into stable YAML scalars.

    Datetimes are emitted as ISO-8601 strings (with the ``T`` separator and the
    original UTC offset) so the serialized form is deterministic and re-reads to
    an equal datetime, rather than PyYAML's space-separated default.
    """
    if isinstance(value, _dt.datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _yamlify(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_yamlify(v) for v in value]
    return value


def to_markdown(entry: Entry) -> str:
    front = {k: _yamlify(v) for k, v in entry.data.items()}
    fm = yaml.safe_dump(
        front,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )
    if not fm.endswith("\n"):  # pragma: no cover - safe_dump always ends with a newline
        fm += "\n"
    body = entry.body.strip("\n")
    return f"{_DELIM}\n{fm}{_DELIM}\n\n{body}\n"


def parse_markdown(text: str) -> Entry:
    lines = text.split("\n")
    if not lines or lines[0].strip() != _DELIM:
        raise EntryFormatError("entry must start with a '---' frontmatter delimiter")

    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == _DELIM:
            end = i
            break
    if end is None:
        raise EntryFormatError("unterminated frontmatter: missing closing '---'")

    fm_text = "\n".join(lines[1:end])
    body = "\n".join(lines[end + 1 :]).strip("\n")

    try:
        data = yaml.safe_load(fm_text) if fm_text.strip() else {}
    except yaml.YAMLError as exc:
        raise EntryFormatError(f"frontmatter is not valid YAML: {exc}") from exc
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise EntryFormatError("frontmatter must be a YAML mapping")

    return Entry(data=data, body=body)
