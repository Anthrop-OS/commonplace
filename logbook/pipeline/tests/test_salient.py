"""The salient-push hook is transport-only: it carries, it does not decide."""

from __future__ import annotations

import json

import pytest

from commonplace_logbook import (
    AstrBotSink,
    DiscordWebhookSink,
    NullSink,
    format_message,
    salient_push,
    sink_from_env,
)
from commonplace_logbook.salient import SalientSink

from conftest import make_entry


class FakeTransport:
    def __init__(self):
        self.calls = []

    def __call__(self, url, payload, headers):
        self.calls.append((url, json.loads(payload.decode("utf-8")), headers))
        return 204


def test_format_message_includes_tier_type_and_curiosity():
    e = make_entry(curiosity={"question": "what is past the ridge?"})
    msg = format_message(e, note="felt worth saying")
    assert "[private]" in msg
    assert "reflection" in msg
    assert "felt worth saying" in msg
    assert "Q: what is past the ridge?" in msg


def test_format_message_truncates_long_body():
    e = make_entry()
    e.body = "x" * 1000
    msg = format_message(e)
    assert msg.endswith("…")
    assert len(msg) < 1000


def test_format_message_omits_empty_body():
    e = make_entry()
    e.body = ""
    msg = format_message(e)
    assert "[private]" in msg
    assert msg.endswith("reflection · " + str(e.ts))  # no trailing body block


def test_null_sink_records_without_network():
    sink = NullSink()
    salient_push(make_entry(), sink=sink, note="hi")
    assert len(sink.pushed) == 1
    assert sink.pushed[0]["note"] == "hi"


def test_astrbot_sink_posts_payload():
    fake = FakeTransport()
    sink = AstrBotSink(endpoint="http://astr/inbound", target="dyad", token="t", transport=fake)
    salient_push(make_entry(visibility="private"), sink=sink)
    url, body, headers = fake.calls[0]
    assert url == "http://astr/inbound"
    assert body["target"] == "dyad"
    assert body["visibility"] == "private"
    assert headers["Authorization"] == "Bearer t"


def test_astrbot_sink_without_target_or_token():
    fake = FakeTransport()
    AstrBotSink(endpoint="http://astr", transport=fake).push(make_entry())
    _, body, headers = fake.calls[0]
    assert "target" not in body
    assert "Authorization" not in headers


def test_discord_webhook_sink_posts_content():
    fake = FakeTransport()
    DiscordWebhookSink(webhook_url="http://discord/hook", transport=fake).push(make_entry())
    url, body, _ = fake.calls[0]
    assert url == "http://discord/hook"
    assert "content" in body


def test_sink_from_env_prefers_astrbot():
    sink = sink_from_env({"COMMONPLACE_ASTRBOT_ENDPOINT": "http://a", "COMMONPLACE_DISCORD_WEBHOOK": "http://d"})
    assert isinstance(sink, AstrBotSink)


def test_sink_from_env_falls_back_to_discord():
    sink = sink_from_env({"COMMONPLACE_DISCORD_WEBHOOK": "http://d"})
    assert isinstance(sink, DiscordWebhookSink)


def test_sink_from_env_defaults_to_null():
    assert isinstance(sink_from_env({}), NullSink)


def test_salient_push_resolves_sink_from_env(monkeypatch):
    monkeypatch.delenv("COMMONPLACE_ASTRBOT_ENDPOINT", raising=False)
    monkeypatch.delenv("COMMONPLACE_DISCORD_WEBHOOK", raising=False)
    # No sink + no env channel -> NullSink, no network, no error.
    salient_push(make_entry())


def test_base_sink_is_abstract():
    with pytest.raises(NotImplementedError):
        SalientSink().push(make_entry())
