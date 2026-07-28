"""commonplace logbook pipeline — writer/reader, tier routing, salient push.

Validates against ``logbook/schema/entry.schema.yaml``; defaults every entry to
the ``private`` tier and refuses to emit ``shareable``/``narrative`` without
``redaction_checked: true`` (AGENTS.md rule 3). It provides the *mechanism* for
writing and pushing entries — never the judgment of what to write or what is
salient (that is the drive layer, T4/T5).
"""

from __future__ import annotations

from .entry import Entry, parse_markdown, to_markdown
from .errors import (
    EntryFormatError,
    LogbookError,
    RedactionRequiredError,
    SchemaError,
    ValidationError,
)
from .reader import loads, read_entry
from .salient import (
    AstrBotSink,
    DiscordWebhookSink,
    NullSink,
    SalientSink,
    format_message,
    salient_push,
    sink_from_env,
)
from .schema import SchemaSpec, load_schema
from .store import NARRATIVE, PRIVATE, SHAREABLE, StoreConfig, entry_filename
from .validate import validate_entry, validate_payload
from .writer import WriteResult, write_entry

__all__ = [
    "Entry",
    "parse_markdown",
    "to_markdown",
    "LogbookError",
    "SchemaError",
    "ValidationError",
    "RedactionRequiredError",
    "EntryFormatError",
    "loads",
    "read_entry",
    "load_schema",
    "SchemaSpec",
    "validate_entry",
    "validate_payload",
    "write_entry",
    "WriteResult",
    "StoreConfig",
    "entry_filename",
    "PRIVATE",
    "SHAREABLE",
    "NARRATIVE",
    "salient_push",
    "sink_from_env",
    "format_message",
    "SalientSink",
    "NullSink",
    "AstrBotSink",
    "DiscordWebhookSink",
]

__version__ = "0.1.0"
