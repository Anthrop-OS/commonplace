---
topic: prior-art-l2-l3
status: converging
date: 2026-06-03
related-adrs: [adr-0004, adr-0006]
resolves-to:
---

# Prior art — L2 runtimes & L3 cognition (what to build on, what to refuse)

> Status: **converging**. A survey of current (2026) community/research work for
> the harness runtime (L2) and the cognition layer (L3), mapped to our needs.
> Feeds T2 (runtime choice) and T4 (drive-layer design). Resolves into ADRs when
> those are committed.

## Question

What existing L2 runtimes and L3 cognition systems do we stand on, and which
carry biases (reward/optimization) we must **not** adopt given autotelic-not-reward
(`adr-0004`)?

## Criteria

- **L2 harness:** runtime + perception↔action loop, local-model friendly, async
  operator channel, tolerant of dual-control; **no built-in reward/curriculum bias**.
- **L3 cognition:** autotelic-not-reward, identity + needs/drives + memory/reflection,
  long-horizon *non-optimal believable* behavior.

## L2 — harness / runtime / game-playing agents

| Impl | What | Fits | Don't / risk |
|---|---|---|---|
| **ElizaOS** | TS agent runtime; plugin = actions/providers/**evaluators** loop; PostgreSQL memory; Worlds/Rooms; targets game NPCs/companions | best cognition-friendly harness; TS (adr-0006); "agent-in-world" precedent | heavily **Web3/crypto**-oriented now — use only the core loop |
| **OpenClaw** | TS/Node/Electron; messaging-platform UI; **browser relay over CDP**; Ollama | browser/CDP + **operator async gateway** | heavy (Electron/sandboxes); CDP moot for SMAPI/MCP substrates |
| **Hermes** (NousResearch) | provider-agnostic, **local-first** (Ollama/LM Studio) | local "fallback brain" (privacy routing, adr-0006 rule 6) | needs ≥64k ctx; no world precedent |
| **Voyager / ODYSSEY / MindForge / Co-Voyager** | Minecraft open-world agents: **auto-curriculum + skill library** | reference architecture for open-world exploration | **skill-acquisition + curriculum = reward-shaped → conflicts with adr-0004**; reference only |
| **PIANO** (Project Sid / Altera) | parallel multi-stream cognition; agents **generate own goals** from social motivation; 1000+ agents | good **L3** reference (multi-stream + self-generated goals) | civilization/multi-agent framing; not a single-dyad harness |

## L3 — cognition / memory / autotelic motivation

| Impl | What | Fits | Gap / risk |
|---|---|---|---|
| **Generative Agents** (Park 2023) | memory stream + **reflection** + planning | memory/reflection **paradigm reusable directly** | behavior still serves schedules/goals |
| **Letta/MemGPT · Mem0** | tiered memory (core/recall/archival), auto promote/compress | **memory infrastructure off the shelf** | memory layer only; no drive/identity |
| **autotelic line** (Colas; **MAGELLAN** ICML'25; "Beyond Utility" NeurIPS'25) | agents self-generate NL goals; MAGELLAN uses **learning-progress (LP)** to guide goal choice | goal-generation machinery = the selector's theoretical core | **LP is an intrinsic reward → still optimizing**; borrow the mechanism, **drop the optimization objective** |
| **needs / personality / artificial life** (**Sophia** 2512.18202; "personality from **needs alone**"; evolving_personality; SPeCtrum) | personality/behavior **emerging from basic needs**; persistent identity | closest to the identity+needs engine | social-emergence framing; known **persona drift** + convergence to "average persona" |

## Two tensions

1. **Optimization bias is everywhere.** Open-world agents (Voyager/PIANO) and
   "autotelic RL" (Colas/MAGELLAN learning-progress) ultimately **optimize**
   (skills / curriculum / LP). Our stance ("purposeless, non-optimal, an end in
   itself") is *more radical*. → borrow goal-generation machinery, **deliberately
   discard the optimization objective**, or the drive layer collapses back into a
   reward maximizer (`adr-0004`).
2. **The gap is confirmed.** "Persistent personality/needs sustaining long-horizon
   *non-optimal believable* behavior" is essentially unstudied — exactly the niche
   `design/autotelic-drives.md` claims. The 2026 needs/artificial-life line is the
   closest but still social-emergence-framed and drift-prone. **This unfilled niche
   is the project's contribution.**

## Recommendations

- **L2 (don't build a runtime — adopt one):** **ElizaOS** core (cognition-friendly
  loop + memory + world precedent, TS) — *strip the crypto*; **OpenClaw** for
  browser/CDP + the operator async gateway when needed; **Hermes** as the local-first
  fallback brain. Voyager/PIANO are **reference architectures only** (reward bias).
- **L3 (self-build — it's the IP — but stand on giants):** reuse **Generative Agents**
  memory+reflection + **Letta/Mem0** for storage; take goal-generation from
  **Colas/MAGELLAN** but **cut the learning-progress reward**; take identity+needs
  from the **needs-emergence/Sophia** line. Spend the budget on the unfilled niche:
  long-horizon, non-optimal, believable inhabitation.

## Per-task relevance

- **T2 (Melvor adapter / runtime):** the L2 table + lean (ElizaOS-core / OpenClaw-
  gateway / Hermes-fallback) is the input to the `harness runtime` decision-gate
  (ROADMAP). Note: for Melvor/Stardew (mod/SMAPI/MCP adapters) OpenClaw's CDP edge
  is less decisive.
- **T4 (drive layer):** the L3 table + the two tensions are the design backdrop —
  *what to reuse, what to refuse*. The "drop the optimization objective" rule is the
  load-bearing constraint, alongside `adr-0004`.

## Open items

- Commit the L2 runtime choice → a `harness runtime` ADR (resolves the ROADMAP gate).
- T4 will likely spawn its own exploration (selector design without an optimization
  objective; memory/identity stack choice).

## Sources

- L2: [ElizaOS](https://www.elizaos.ai/) · [ElizaOS/OpenClaw/Hermes compared](https://innfactory.ai/en/blog/openclaw-vs-hermes-agent-comparison/) · [OpenClaw browser harness](https://openclawlaunch.com/guides/openclaw-browser-harness) · [Hermes Agent](https://github.com/nousresearch/hermes-agent) · [Voyager](https://voyager.minedojo.org/) · [ODYSSEY](https://openreview.net/pdf?id=vtGLtSxtqv) · [MindForge](https://arxiv.org/pdf/2411.12977) · [Project Sid / PIANO](https://arxiv.org/abs/2411.00114)
- L3: [Generative Agents](https://arxiv.org/pdf/2304.03442) · [Letta/MemGPT vs Mem0](https://vectorize.io/articles/mem0-vs-letta) · [Augmenting Autotelic Agents w/ LLMs (Colas)](https://proceedings.mlr.press/v232/colas23a/colas23a.pdf) · [Colas publications (MAGELLAN)](https://cedriccolas.com/publications/) · [LLM Agents Beyond Utility](https://arxiv.org/abs/2510.14548) · [Sophia: Persistent Agent Framework for Artificial Life](https://arxiv.org/pdf/2512.18202) · [Personality from needs alone](https://www.eurekalert.org/news-releases/1099709) · [SPeCtrum identity](https://arxiv.org/pdf/2502.08599)
