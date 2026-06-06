---
topic: substrate-evennia-multi-agent
status: open
date: 2026-06-06
related-adrs: [adr-0003, adr-0007, adr-0004]
resolves-to:
---

# Substrate option — multi-agent text MUD (Evennia + N×LLM NPCs) — exploration

> Status: **open**. Not binding. Resolves into an ADR if all three gating
> spikes (S1/S2/S3) clear *and* the operator acks the co-presence UX.

## Question

Should the substrate ladder ([[adr-0007-substrate-ladder]]) **replace its
deferred AI Town slot** with a self-hosted text MUD (Evennia, possibly DikuMUD-
area-fed) populated by N≥3 autonomous LLM-driven NPCs + one operator + one
designated "main agent"? Are there forms of this option that fit elsewhere on
the ladder?

## Background — why this comes up now

Two conversational explorations triggered the note:

1. **"Text MUDs as L1?"** Public MMO MUDs (real humans) are ruled out by
   ethics / ToS / PII and are dominated by 2004scape in the IP-gray slot.
   Self-hosted Evennia surfaced as a credible **AI Town replacement** —
   strictly dominates AI Town on integration cost, content depth, text-
   nativeness, and project-stack fit (Python+Ollama already in tree).
2. **"Are there equivalents in the Chinese community?"** Research surfaced
   GenerativeAgentsCN (verified N=25 LLM agents on local Ollama+Qwen3-4B),
   AgentScope, AgentVerse, EconAgent, CharacterGLM, wuxia-MUD assets,
   and multi-AI-co-presence consumer-product validation. Documented in
   [[prior-art-l2-l3]] (Chinese-community supplement, 2026-06-06).

The combination — **self-hosted Evennia × N≥3 autotelic LLM-NPCs × one
operator channel × one designated main-agent protagonist × deterministic
seeded tick** — is confirmed unfilled (see prior-art "white space").

## Options

| Option | Description |
|---|---|
| **A. No-op** | Keep AI Town deferred as-is in [[adr-0007-substrate-ladder]]. Lowest risk; ignores the zh-ecosystem evidence. |
| **B. Replace AI Town slot** *(focus of this note)* | Multi-agent self-hosted Evennia replaces the AI Town deferred slot. Setting TBD (generic / wuxia / hand-built / DikuMUD-area import). |
| **C. New P0.5 between Melvor and Stardew** | Insert verbal multi-agent clean-room before Stardew. Adds ladder complexity; pushes back P1 dual-control. |
| **D. Defer + research-only** | Acknowledge the gap in the prior-art note; no ladder change yet; revisit after T4 makes drive-layer needs concrete. |

## Criteria

Reuse the seven criteria from [[exploration-substrate-selection]] + three
multi-agent-specific:

| New criterion | Why |
|---|---|
| **NPC cost ceiling** | N×LLM tokens; operator's local hardware is finite. GenerativeAgentsCN's N=25 + Qwen3-4B benchmark is the anchor. |
| **Dyad-vs-multi-agent attention split** | Project's IP is the *operator-agent* dyad ([[informed-symbiosis]] design); N background NPCs could dilute the agent's attention to the operator. Must architect a hard foreground/background asymmetry. |
| **Determinism survivability** | Multi-LLM = default non-deterministic. Seeded local-LLM + logical tick + content-cache may approach replayability — Paracosm/Miniverse closest, neither MUD-shaped. |

## Evaluation — Option B vs ladder anchors

| Dimension | Option B (multi-agent Evennia) | AI Town (current deferred) | Melvor P0 | Stardew P1+ |
|---|---|---|---|---|
| Depth kind | social + verbal + light spatial + economy (via DikuMUD area) | social, sparse content | progression only | social + spatial + season |
| Integration cost | **lowest** (telnet/Evennia Python in-process; project already Python+Ollama) | medium (Convex+TS, not project stack) | low (mod API) | med (SMAPI+MCP) |
| Local-LLM cost evidence | **GenerativeAgentsCN N=25 verified on Qwen3-4B** | N=25 hand-shown by AI Town authors, but with paid models | n/a (no LLM NPCs) | n/a |
| Content supply | DikuMUD area packs (free, ample) **+ wuxia-MUD lib** (zh) **+ hand-craft** | hand-craft only, sparse | game-fixed | game-fixed |
| Dual-control | **native** (each character = own connection) | possible | **no co-presence** | native via co-op |
| Determinism | **gateable** via seeded local + logical tick + LLM-response cache (unprecedented at this combo) | not done | high | medium |
| IP / ethics | **clean** (Evennia MIT, FOSS) | clean (MIT) | mod-only | proprietary mod |
| **Operator co-presence appeal** | **uncertain** — text-MUD aesthetic not warm like Stardew | uncertain | n/a (single-avatar) | high (graphical, named NPCs, calendar) |
| Dyad-attention dilution risk | **high** — explicit architectural mitigation required | medium | low (only-actor) | low (NPCs are scripted, not LLM) |

**Net:** Option B strictly dominates AI Town on integration / content / cost-
evidence / determinism feasibility. It does **not** dominate Stardew P1 on the
dimension Stardew P1 was chosen for — operator co-presence warmth.

## Three core tensions

1. **Dyad-vs-multi-agent attention (most important).** The project's research
   core is the *operator-agent* dyad ([[informed-symbiosis]] / [[adr-0004]]),
   not a multi-agent social sim. Without a hard architectural foreground/
   background asymmetry, Option B drifts toward "Generative Agents +
   Concordia, again." **Mitigation (load-bearing):** operator + main agent run
   full memory/drives/reflection (cloud-or-local routing per
   [[adr-0006]]); NPCs run small local model + short context + do **not**
   enter the main agent's reflection loop except as raw perception. The main
   agent's relationship graph weights operator >> NPC.

2. **Setting choice cuts across criteria.** Generic fantasy / wuxia / custom-
   built / DikuMUD-area-import all trade off differently. Wuxia gives RAG +
   zh-cultural alignment + a 30-year asset trove (pkuxkx wiki, mudcore — see
   [[prior-art-l2-l3]] supplement), but wuxia's 升级打怪 culture is the same
   skill-grinding tax that makes Melvor's autotelic detour thin — directly
   risks `adr-0004`. Cannot resolve until S2 spike + operator setting ack.

3. **Determinism is unprecedented at this combination.** No prior project
   combines (multi-LLM agents × persistent navigable world × seeded byte-
   equal replay). Paracosm/Miniverse close on the multi-LLM subset; Concordia/
   AI Town don't seed at all. Either pay this engineering cost (S3 spike) or
   accept non-replayable runs — acceptable for research output, blocked for CI.

## Out of scope (explicitly)

- **Public MMO MUDs** (real humans on public servers) — ruled out in
  conversation (ethics / PII / ToS, dominated by 2004scape).
- **Stendhal MMO** — separate name-clash caveat per [[project-commonplace]];
  separate evaluation if revisited.
- **Multi-LLM NPCs replacing Stardew villagers** — different decision, would
  require Stardew P1 modding work that's not started; out of this note.
- **The main agent's cognition design** — lives in T4 / [[adr-0004]].

## Gating spikes (must all pass before resolving)

| ID | Spike | Output | Effort |
|---|---|---|---|
| **S1** | Fork `GenerativeAgentsCN`; run N=25 with Qwen3-4B via Ollama on operator hardware. Measure tokens/tick, peak/sustained VRAM, wall-clock per logical tick. | concrete cost-ceiling number → answers "can we afford N=25 NPCs?" | low — repo is fork-and-run |
| **S2** | Import one DikuMUD `tbamud` area into Evennia; *separately* skim wuxia-MUD lib (pkuxkx wiki, mudcore) for asset-quality + tone-fit. | content-track decision input (generic vs wuxia vs hand-craft) | medium |
| **S3** | Single-node Ollama + fixed seed + greedy + logical tick + content-addressed LLM-response cache. Run twice, byte-compare outputs of a 50-tick scripted scenario. | determinism feasibility → CI-replayability story | medium-high (novel) |
| S0 (optional, after S1–S3) | AgentScope vs ElizaOS-core multi-agent-comms primitive bench-off — see [[prior-art-l2-l3]] Open items. | runtime choice within Option B | low |

## Decision gates

- **All of S1/S2/S3 pass + operator acks co-presence UX** → status moves to
  `converging`, propose ADR replacing AI Town's deferred slot with multi-
  agent Evennia.
- **Any spike fails** → status to `resolved` (deferred); document why and
  leave AI Town in its current ladder slot.
- **Operator declines co-presence ask** → status to `resolved` (deferred);
  Option B reduces to single-agent Evennia, which doesn't justify
  displacing AI Town.

## Open items

- **Operator UX ack (blocking S2):** would you actually telnet (or use a
  Mudlet client) into a populated text MUD as your "play with the agent"
  time, or is the aesthetic gap from Stardew's graphical warmth too far?
  The zh consumer-product evidence (筑梦岛/猫箱/星野/Tavo all ship multi-
  AI-in-shared-scene features) is a weak positive signal but UI form is
  app-chat, not telnet.
- **Operator setting preference (blocking S2):** generic fantasy / wuxia
  (with culture-tax caveat) / agnostic / hand-built?
- **N choice:** 3 / 8 / 25. GenerativeAgentsCN benchmarks at 25; budget may
  prefer fewer. S1 informs.
- **Contact `mud.ren/threads/436` "Yanhuang MUD" (炎黄 MUD) author** — single
  public zh MUD+LLM signal found; cheap, possibly high-value insight.
- **Per-task impact:** Option B has no impact on T2 (Melvor adapter, in
  flight) or T4 (drive layer, ongoing). It would land **after** P0/P1
  substrates are exercised, replacing the AI Town slot.

## Sources

**In-repo:**
- [[exploration-substrate-selection]] (resolved → [[adr-0007-substrate-ladder]])
- [[adr-0003-melvor-clean-room-first]] · [[adr-0004-autotelic-drive-layer]] · [[adr-0006-polyglot-ts-harness-python-cognition]]
- [[prior-art-l2-l3]] (incl. 2026-06-06 zh supplement)
- `design/informed-symbiosis.md` · `harness/bridge/README.md` · `harness/bridge/synthetic-bridge.ts`

**External — substrate + tooling:**
- Evennia — https://www.evennia.com/ · `contrib.rpg.llm` https://www.evennia.com/docs/latest/Contribs/Contrib-Llm.html
- LIGHT (Meta, 2019, closest MUD-AI historical precedent) — https://arxiv.org/pdf/2002.02878 · https://github.com/facebookresearch/LIGHT
- DikuMUD `tbamud` open areas — https://github.com/tbamud/tbamud
- AI People (GoodAI, closest commercial parallel — closed) — https://blog.marekrosa.org/2024/04/ai-people-announcement/

**External — multi-agent prior art (added beyond prior-art note):**
- GenerativeAgentsCN — https://github.com/x-glacier/GenerativeAgentsCN
- AgentScope — https://github.com/modelscope/agentscope
- AgentVerse — https://github.com/OpenBMB/AgentVerse · arxiv [2308.10848](https://arxiv.org/abs/2308.10848)
- Concordia (DeepMind, Apache-2.0) — https://github.com/google-deepmind/concordia · paper [arxiv 2411.07038](https://arxiv.org/pdf/2411.07038)

**External — determinism prior art:**
- Paracosm / AgentOS — https://paracosm.agentos.sh/
- Miniverse — https://github.com/miniverse-ai/miniverse
- vLLM reproducibility — https://docs.vllm.ai/en/latest/usage/reproducibility/
- TextWorldExpress (single-agent determinism reference, 1M SPS) — https://github.com/cognitiveailab/TextWorldExpress

**External — zh ecosystem (full list in [[prior-art-l2-l3]] supplement):**
- pkuxkx wiki — https://www.pkuxkx.net/wiki
- mudcore (gitee) — https://gitee.com/mudcore/mudcore
- mudchina站点列表 — https://mudchina.github.io/
- mud.ren/threads/436 — 炎黄 MUD — https://mud.ren/threads/436
