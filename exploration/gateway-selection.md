---
topic: gateway-selection
status: converging
date: 2026-06-03
related-adrs: [adr-0006]
resolves-to:
---

# Gateway selection — the operator↔agent async channel

> Status: **converging**. The MVP channel is decided (direct Discord, two-way);
> the multi-platform *framework* choice is deferred. Resolves into an ADR.

## Question

What carries the **dyad's async channel** — operator ↔ agent, including the
agent's **self-initiated salient push** — for Milestone 0, and later?

## First: two different things are both called "gateway"

| Sense | Examples | Relevance |
|---|---|---|
| **IM / message gateway** — operator↔agent chat | OpenClaw, AstrBot, LangBot, NoneBot2, direct discord.py | **this note** |
| **LLM API gateway** — provider proxy / routing | LiteLLM, Bifrost, Kong | a *different* layer — future cloud/local **model routing** (ADR-0006 rule 6), not the dyad channel |

Don't conflate them. This note is the IM channel.

## Criteria

| Criterion | Why |
|---|---|
| Async + **Discord** | the dyad's stated channel (operator acts async via Discord) |
| **Agent-initiated push** | agent self-judges salience and *pushes* — most bots are reply-only; this is the decisive, unusual requirement (T3/T5) |
| Self-host + local model | the record is private (ADR-0005) — keep the channel self-hosted |
| **Transport, not brain** | L3 cognition is the custom IP; the channel must not impose its own agent/LLM loop |
| 1:1 dyad | single operator, single agent, single platform — multi-platform/multi-user is *not* an MVP need |
| Python co-location | L3 is Python (ADR-0006); a Python channel shares its process domain |

## Options & evaluation

| Option | Type / lang | Discord | Transport-not-brain | Agent push | Self-host | Ops cost | Fit |
|---|---|---|---|---|---|---|---|
| **direct discord.py** | thin lib / Python | ✓ | **✓ purest** (you own it) | **✓ native** (`channel.send` anytime) | ✓ | **low for 1 platform** | **MVP** |
| **LangBot** | IM↔backend **bridge** / Python, Apache-2.0 | ✓ (10+) | ✓ (designed to front your backend) | event-driven, supports outbound | ✓ Ollama | medium | best *framework* when multi-platform is needed |
| **AstrBot** | agentic IM infra / Python, 33k★ | ✓ | △ wants to be the agent (own LLM/persona/RAG) | needs a plugin to emit | ✓ | lowest (WebUI+Docker) | ops-heavy turnkey; overkill at 1:1 |
| **NoneBot2** | low-level bot **framework** / Python | ✓ | ✓ you control all | ✓ framework-level | ✓ | high (write it all) | if direct discord.py outgrows itself |
| **OpenClaw** | full agent app / TS+Electron | ✓ (+ many) | △ bundles its own runtime | runtime-coupled | ✓ | high (Electron/sandboxes) | its real strength is the browser/CDP harness, not a pure channel |
| **ntfy** | one-way push service | ✗ (no chat) | ✓ | ✓ push-only | ✓ | minimal | only if the channel were one-way |

## Sub-decision: one-way vs two-way → **two-way**

The `salient push: ntfy vs Discord` gate (ROADMAP) reduces to this. The dyad form
— *operator can also act / converse async* — needs **two-way**, so the minimal
one-way pusher (ntfy) is out for MVP. The channel is **Discord, two-way**.

## Current lean / MVP decision

**MVP = a direct, thin Discord bot (discord.py), two-way.** Operator DMs/channels
the agent; the agent replies *and* pushes when it self-judges an entry salient.

Why direct over a framework, for MVP:

- The dyad is **1 operator / 1 agent / 1 platform** — the multi-platform gateways'
  main value (many platforms, many users, a WebUI control plane) solves a problem
  the MVP doesn't have.
- **Agent-initiated push** — the decisive requirement — is trivial and fully under
  our control with `discord.py` (`channel.send()` / DM anytime); a framework only
  adds indirection between the drive layer and the wire.
- **Transport-not-brain** is purest with a direct lib: zero framework cognition to
  fight the custom L3.
- Python `discord.py` **co-locates with the Python L3** (ADR-0006).
- Cost is small for a single platform.

**Deferred (not MVP):** adopt a framework when multi-platform reach or an ops/WebUI
control plane is actually needed. **LangBot** is the front-runner then — it is
explicitly an *IM↔your-backend bridge* (transport-not-brain), Apache-2.0, event-
driven, 10+ platforms, and even lists openclaw/hermes as pluggable backends.

## Open items

- Agent-push via `discord.py` is a known capability (low risk) — no spike needed;
  a smoke test in T3/T5 suffices.
- Formalize the MVP channel decision as an ADR (channel = direct Discord, two-way;
  frameworks deferred) and set this note `resolved`.
- Revisit the framework choice (LangBot) only when multi-platform/ops is real.
- Keep the IM gateway distinct from the future **LLM API gateway** (model routing).

## Sources

- [AstrBot](https://github.com/AstrBotDevs/AstrBot); [LangBot](https://github.com/langbot-app/LangBot); [LangBot site](https://langbot.app/en)
- [OpenClaw vs Hermes comparison](https://innfactory.ai/en/blog/openclaw-vs-hermes-agent-comparison/); [OpenClaw browser harness](https://openclawlaunch.com/guides/openclaw-browser-harness)
- [7 open-source frameworks for AI bots on messaging platforms (2026)](https://aibotbuilder.hashnode.dev/7-open-source-frameworks-for-deploying-ai-bots-to-messaging-platforms-in-2026)
- LLM API gateways (different layer): [open-source LLM gateways self-hosted 2026](https://www.getmaxim.ai/articles/5-best-open-source-llm-gateways-for-self-hosted-deployments-in-2026/)
