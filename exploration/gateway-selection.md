---
topic: gateway-selection
status: converging
date: 2026-06-03
related-adrs: [adr-0006]
resolves-to:
---

# Gateway selection — the operator↔agent async channel

> Status: **converging**. MVP comms tool = **AstrBot** over Discord, two-way
> (operator direction), used transport-not-brain. One open spike: the L3
> integration path. Resolves into an ADR.

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
| **direct discord.py** | thin lib / Python | ✓ | **✓ purest** (you own it) | **✓ native** (`channel.send` anytime) | ✓ | **low for 1 platform** | fallback — thinnest if AstrBot is too heavy |
| **LangBot** | IM↔backend **bridge** / Python, Apache-2.0 | ✓ (10+) | ✓ (designed to front your backend) | event-driven, supports outbound | ✓ Ollama | medium | best *framework* when multi-platform is needed |
| **AstrBot** | agentic IM infra / Python, 33k★ | ✓ | △ has own LLM/persona/RAG — must bypass via plugin so L3 stays the brain | **✓ via plugin** (event+scheduler send pipeline; `astrbot_plugin_proactive_chat` precedent) | ✓ Ollama/LM Studio | lowest (WebUI+Docker) | **MVP (operator choice)** — WebUI console + multi-platform-ready |
| **NoneBot2** | low-level bot **framework** / Python | ✓ | ✓ you control all | ✓ framework-level | ✓ | high (write it all) | if direct discord.py outgrows itself |
| **OpenClaw** | full agent app / TS+Electron | ✓ (+ many) | △ bundles its own runtime | runtime-coupled | ✓ | high (Electron/sandboxes) | its real strength is the browser/CDP harness, not a pure channel |
| **ntfy** | one-way push service | ✗ (no chat) | ✓ | ✓ push-only | ✓ | minimal | only if the channel were one-way |

## Sub-decision: one-way vs two-way → **two-way**

The `salient push: ntfy vs Discord` gate (ROADMAP) reduces to this. The dyad form
— *operator can also act / converse async* — needs **two-way**, so the minimal
one-way pusher (ntfy) is out for MVP. The channel is **Discord, two-way**.

## Current lean / MVP decision

**MVP = AstrBot as the communication tool** (operator direction), two-way over
Discord. AstrBot provides the message I/O, a WebUI ops console, Docker deploy, and
a ready proactive-send pipeline; the operator gets a real control plane and
multi-platform headroom from day one.

Both decisive capabilities are confirmed:
- **Agent-initiated salient push** — AstrBot's event+scheduler send pipeline
  supports bot-initiated messages (the `astrbot_plugin_proactive_chat` plugin is a
  working precedent). The L3 calls this to push when it judges an entry salient.
- **Custom backend** — AstrBot takes a custom LLM provider via an OpenAI-compatible
  interface, and a plugin framework for bespoke logic. Python — co-locates with the
  Python L3 (ADR-0006).

**The discipline that makes this work — transport-not-brain.** AstrBot ships its own
LLM loop, persona, RAG, and context-compression; the project's **L3 must stay the
brain**. Integrate so AstrBot's cognition is bypassed, not stacked on top of L3:

- **Preferred — plugin bridge:** a thin AstrBot plugin forwards inbound operator
  messages to L3 and uses the send API for L3's outbound/proactive pushes. AstrBot's
  LLM pipeline is bypassed entirely; it is pure I/O + ops console.
- **Alternative — provider:** wrap L3 behind an OpenAI-compatible endpoint and
  register it as AstrBot's provider, with AstrBot's own session/persona/context
  features **disabled** so L3's memory/identity stays authoritative (else you get
  two competing memory layers).

**Fallback:** if AstrBot proves too heavy or its cognition can't be cleanly bypassed,
drop to a **direct `discord.py`** bot (thinnest, purest transport-not-brain). The
evaluation above stands; only the chosen tool changes.

## Open items

- **Spike: pick the integration path** (plugin bridge vs provider) and confirm
  AstrBot's own context/persona layer can be fully bypassed so L3 is the sole brain.
  This is the one real risk — verify before committing T3/T5 to AstrBot.
- Confirm proactive push works end-to-end (L3 → AstrBot send → operator) with a
  smoke test in T3/T5.
- Formalize as an ADR once the integration path is validated (channel = AstrBot
  over Discord, two-way, transport-not-brain), then set this note `resolved`.
- Keep the IM gateway distinct from the future **LLM API gateway** (model routing).

## Sources

- [AstrBot](https://github.com/AstrBotDevs/AstrBot); [LangBot](https://github.com/langbot-app/LangBot); [LangBot site](https://langbot.app/en)
- [OpenClaw vs Hermes comparison](https://innfactory.ai/en/blog/openclaw-vs-hermes-agent-comparison/); [OpenClaw browser harness](https://openclawlaunch.com/guides/openclaw-browser-harness)
- [7 open-source frameworks for AI bots on messaging platforms (2026)](https://aibotbuilder.hashnode.dev/7-open-source-frameworks-for-deploying-ai-bots-to-messaging-platforms-in-2026)
- LLM API gateways (different layer): [open-source LLM gateways self-hosted 2026](https://www.getmaxim.ai/articles/5-best-open-source-llm-gateways-for-self-hosted-deployments-in-2026/)
