"""Exceptions raised by the logbook pipeline."""

from __future__ import annotations


class LogbookError(Exception):
    """Base class for all pipeline errors."""


class SchemaError(LogbookError):
    """The schema file itself is malformed or unsupported."""


class ValidationError(LogbookError):
    """An entry does not conform to ``entry.schema.yaml``.

    ``problems`` is the list of human-readable field-level failures.
    """

    def __init__(self, problems: list[str]):
        self.problems = list(problems)
        super().__init__("; ".join(self.problems) if self.problems else "invalid entry")


class RedactionRequiredError(LogbookError):
    """Refused to emit a ``shareable``/``narrative`` entry without ``redaction_checked: true``.

    AGENTS.md rule 3: tooling defaults to ``private`` and must refuse to emit a
    non-private tier until a redaction pass is explicitly recorded on the entry.
    This is a publication gate, not a validation failure — the entry is well
    formed; it simply may not leave the private tier yet.
    """


class EntryFormatError(LogbookError):
    """A serialized entry could not be parsed (missing/garbled frontmatter)."""
