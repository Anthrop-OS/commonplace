"""Salient-push hook — **transport, not brain**.

The agent's cognition (L3 / the drive layer) decides *whether* an entry is
salient; this module only *carries* an already-chosen entry to the operator's
async channel. There is deliberately no salience scoring, LLM call, or filtering
here — adding any would duplicate the brain in the transport, the exact failure
``exploration/gateway-selection.md`` warns against.

Channel (converged in that note): **AstrBot over Discord, two-way**. A direct
Discord webhook is the documented thin fallback. The sink is pluggable; the
default :class:`NullSink` is a no-op so importing the pipeline never reaches the
network.

Note on visibility: the push targets the operator's *own* dyad channel, not a
public dataset, so the redaction gate (a publication control) does not apply
here. A private entry may be surfaced to the operator; it is never published.
"""

from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .entry import Entry

# transport(url, payload_bytes, headers) -> status_code
Transport = Callable[[str, bytes, Dict[str, str]], int]

_BODY_EXCERPT = 280


def format_message(entry: Entry, note: Optional[str] = None) -> str:
    """Render a compact operator-facing notification. Formatting only."""
    head = f"[{entry.visibility}] {entry.type} · {entry.ts}"
    body = (entry.body or "").strip()
    if len(body) > _BODY_EXCERPT:
        body = body[: _BODY_EXCERPT - 1].rstrip() + "…"
    parts: List[str] = [head]
    if note:
        parts.append(note)
    curiosity = entry.data.get("curiosity") or {}
    question = curiosity.get("question") if isinstance(curiosity, dict) else None
    if question:
        parts.append(f"Q: {question}")
    if body:
        parts.append(body)
    return "\n\n".join(parts)


def _urllib_post(url: str, payload: bytes, headers: Dict[str, str]) -> int:  # pragma: no cover - network
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.getcode()


class SalientSink:
    """Interface: carry an entry to the operator. Implementations transport only."""

    def push(self, entry: Entry, note: Optional[str] = None) -> None:
        raise NotImplementedError


@dataclass
class NullSink(SalientSink):
    """Default no-op sink. Records pushes in-memory for observability/tests."""

    pushed: List[Dict[str, Any]] = field(default_factory=list)

    def push(self, entry: Entry, note: Optional[str] = None) -> None:
        self.pushed.append({"entry": entry, "note": note, "message": format_message(entry, note)})


@dataclass
class AstrBotSink(SalientSink):
    """POST a message to an AstrBot inbound endpoint (plugin bridge / webhook).

    AstrBot is pure I/O here: its own LLM/persona pipeline is bypassed. The
    payload is just the rendered message plus a routing target.
    """

    endpoint: str
    target: Optional[str] = None
    token: Optional[str] = None
    transport: Transport = _urllib_post

    def push(self, entry: Entry, note: Optional[str] = None) -> None:
        payload = {"message": format_message(entry, note), "visibility": entry.visibility}
        if self.target:
            payload["target"] = self.target
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        self.transport(self.endpoint, json.dumps(payload).encode("utf-8"), headers)


@dataclass
class DiscordWebhookSink(SalientSink):
    """Documented thin fallback: a plain Discord webhook (no discord.py needed)."""

    webhook_url: str
    transport: Transport = _urllib_post

    def push(self, entry: Entry, note: Optional[str] = None) -> None:
        payload = {"content": format_message(entry, note)}
        headers = {"Content-Type": "application/json"}
        self.transport(self.webhook_url, json.dumps(payload).encode("utf-8"), headers)


def sink_from_env(environ: Optional[dict] = None) -> SalientSink:
    """Pick a sink from env config; :class:`NullSink` if no channel is configured."""
    environ = environ if environ is not None else os.environ
    endpoint = environ.get("COMMONPLACE_ASTRBOT_ENDPOINT")
    if endpoint:
        return AstrBotSink(
            endpoint=endpoint,
            target=environ.get("COMMONPLACE_ASTRBOT_TARGET"),
            token=environ.get("COMMONPLACE_ASTRBOT_TOKEN"),
        )
    webhook = environ.get("COMMONPLACE_DISCORD_WEBHOOK")
    if webhook:
        return DiscordWebhookSink(webhook_url=webhook)
    return NullSink()


def salient_push(
    entry: Entry,
    *,
    sink: Optional[SalientSink] = None,
    note: Optional[str] = None,
) -> None:
    """The hook the agent calls when **it** has judged an entry salient.

    Pure transport: no salience decision is made here. ``sink`` defaults to the
    env-configured channel (NullSink if none), so this is safe to call
    unconditionally in environments without a channel.
    """
    (sink if sink is not None else sink_from_env()).push(entry, note)
