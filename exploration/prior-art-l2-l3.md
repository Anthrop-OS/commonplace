---
topic: prior-art-l2-l3
status: converging
date: 2026-06-03
related-adrs: [adr-0004, adr-0006]
resolves-to: adr-pending-a36d1d8e-l2-harness-runtime
---

# Prior art — L2 runtimes & L3 cognition (what to build on, what to refuse)

> Status: **L2 runtime portion resolved** → [[adr-pending-a36d1d8e-l2-harness-runtime]]
> (operator, 2026-06-25): **self-built thin run-loop, all frameworks rejected** (the ADR
> carries the full rejected-alternatives audit, broadened beyond this note via third-party
> sourcing). The **L3 cognition** survey below remains **input to T4** (drive-layer design)
> — still open. Original survey of 2026 community/research work for the harness runtime
> (L2) and the cognition layer (L3), mapped to our needs.

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
| **AgentScope** (Alibaba DAMO, Apache-2.0) | Python multi-agent framework; **`msghub` broadcast** + pipeline orchestration; official 7-agent Werewolf game template; Ollama / local-LLM friendly | **multi-agent comms primitive** — closest thing to a "drop N agents into a room" runtime; useful for the multi-agent substrate option in [[substrate-evennia-multi-agent]] | workflow/task-oriented; less *persistent-world* precedent than Eliza — needs a world layer above |

## L3 — cognition / memory / autotelic motivation

| Impl | What | Fits | Gap / risk |
|---|---|---|---|
| **Generative Agents** (Park 2023) | memory stream + **reflection** + planning | memory/reflection **paradigm reusable directly** | behavior still serves schedules/goals |
| **Letta/MemGPT · Mem0** | tiered memory (core/recall/archival), auto promote/compress | **memory infrastructure off the shelf** | memory layer only; no drive/identity |
| **autotelic line** (Colas; **MAGELLAN** ICML'25; "Beyond Utility" NeurIPS'25) | agents self-generate NL goals; MAGELLAN uses **learning-progress (LP)** to guide goal choice | goal-generation machinery = the selector's theoretical core | **LP is an intrinsic reward → still optimizing**; borrow the mechanism, **drop the optimization objective** |
| **needs / personality / artificial life** (**Sophia** 2512.18202; "personality from **needs alone**"; evolving_personality; SPeCtrum) | personality/behavior **emerging from basic needs**; persistent identity | closest to the identity+needs engine | social-emergence framing; known **persona drift** + convergence to "average persona" |
| **GenerativeAgentsCN** (x-glacier, MIT, 463⭐) | Smallville Chinese reimplementation; **verified Ollama + Qwen3-4B / DeepSeek-R1 running 25 agents** locally | **concrete local-LLM cost evidence** for an N≥25 multi-agent run + a ready zh scaffold; fork-and-run start for multi-agent emergence work | still Smallville-shaped (schedules/goals) — same optimization framing as Park 2023 |
| **AgentVerse — `simulation` track** (OpenBMB/Tsinghua, arxiv 2308.10848) | LLM multi-agent framework split into `task-solving` + `simulation`; Minecraft branch studies emergent multi-agent behavior | third multi-agent-emergence reference besides Smallville/PIANO; cleaner sim/task separation than ElizaOS | not autotelic — sim runs still framed by task success |
| **EconAgent** (Tsinghua, ACL'24 Outstanding) | 100 LLM agents × 20 simulated years; macro-economic sim that **reproduces stylized economic facts** | strongest existing evidence that a **long-horizon multi-LLM sim can stay coherent** — supports the "non-optimal believable long-horizon" feasibility | optimization-shaped objective (macro outcomes) → borrow the coherence-evidence, not the objective |

## Chinese-community supplement (added 2026-06-06)

Section added after the original note converged. Covers Chinese-ecosystem
items that sit alongside the L2/L3 tables — role-LLM model layer, RP corpora,
and MUD assets — plus a relevant consumer-product observation. The new L2/L3
rows above (AgentScope, GenerativeAgentsCN, AgentVerse-sim, EconAgent) belong
in their tables; this subsection is for the items that don't.

- **CharacterGLM-6B** (THU CoAI + Lingxin AI, EMNLP'24, open 6B) — Chinese
  role-customised dialogue **pre-trained** model with a six-dimension subjective
  evaluator. Candidate **NPC local model** when role-fidelity matters more than
  general capability; slots beneath the L3 table as a model-layer choice.
- **Chinese RP / role-eval corpora**: ChatHaruhi (54k dialogues, 32 zh+en
  characters, MIT) · CharacterEval (1785 multi-turn dialogues, 77 zh
  novel/drama characters) · RoleBench · SuperCLUE-Role. Collectively the
  largest open Chinese role-fidelity dataset stack. Reusable as (a) NPC
  persona-fidelity evaluator, (b) drive-layer believability evaluator,
  (c) RAG corpus for character knowledge.
- **Wuxia-MUD lib assets** (pkuxkx.net wiki + `mudcore` / `xwjy_mud/mudcore`):
  30 years of LPMud-based Chinese MUD content — characters / sects / techniques
  / geography / NPC dialogue — usable as RAG corpus *if* a Chinese-setting
  substrate is chosen. Setting choice is left to [[substrate-evennia-multi-agent]];
  the asset's existence is the relevant prior-art fact.
- **AI-companion product observation** (informative, not adoptable): closed-
  source Chinese RP apps — 筑梦岛 (Yuewen/Tencent), 猫箱 (ByteDance), 星野
  (MiniMax), Tavo — all ship "multi-AI characters in one shared scene" features.
  **Multi-agent co-presence has consumer-product validation in the zh market**
  that the en market lacks — a weak signal that the operator-in-multi-agent-world
  UX is not unprecedented (relevant to [[substrate-evennia-multi-agent]]).
- **One MUD × LLM lead** — `mud.ren/threads/436` describes a project called
  "Yanhuang MUD" (炎黄 MUD) running `npc_manager.py` for LLM NPCs with memory +
  knowledge-base retrieval. No GitHub repo surfaced; appears to be single-NPC,
  not multi-agent. The **only public Chinese MUD + LLM signal found**; worth
  contacting the thread author if multi-agent MUD work proceeds.

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
  **AgentScope** is a newly surfaced multi-agent-comms candidate (`msghub` + Werewolf
  template); merits a spike comparison vs ElizaOS-core *only if* the multi-agent
  substrate option in [[substrate-evennia-multi-agent]] is pursued.
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
- **Multi-agent substrate spike** (gated by [[substrate-evennia-multi-agent]]): fork
  `GenerativeAgentsCN`, measure token/tick at N=25 with Qwen3-4B on operator's local
  hardware; only then is AgentScope-vs-ElizaOS-core comparison decisive.
- Contact `mud.ren/threads/436` author re: "Yanhuang MUD" — the single public
  zh MUD × LLM lead; cheap, may yield code or design insight.

## Sources

- L2: [ElizaOS](https://www.elizaos.ai/) · [ElizaOS/OpenClaw/Hermes compared](https://innfactory.ai/en/blog/openclaw-vs-hermes-agent-comparison/) · [OpenClaw browser harness](https://openclawlaunch.com/guides/openclaw-browser-harness) · [Hermes Agent](https://github.com/nousresearch/hermes-agent) · [Voyager](https://voyager.minedojo.org/) · [ODYSSEY](https://openreview.net/pdf?id=vtGLtSxtqv) · [MindForge](https://arxiv.org/pdf/2411.12977) · [Project Sid / PIANO](https://arxiv.org/abs/2411.00114) · [AgentScope](https://github.com/modelscope/agentscope)
- L3: [Generative Agents](https://arxiv.org/pdf/2304.03442) · [Letta/MemGPT vs Mem0](https://vectorize.io/articles/mem0-vs-letta) · [Augmenting Autotelic Agents w/ LLMs (Colas)](https://proceedings.mlr.press/v232/colas23a/colas23a.pdf) · [Colas publications (MAGELLAN)](https://cedriccolas.com/publications/) · [LLM Agents Beyond Utility](https://arxiv.org/abs/2510.14548) · [Sophia: Persistent Agent Framework for Artificial Life](https://arxiv.org/pdf/2512.18202) · [Personality from needs alone](https://www.eurekalert.org/news-releases/1099709) · [SPeCtrum identity](https://arxiv.org/pdf/2502.08599) · [GenerativeAgentsCN](https://github.com/x-glacier/GenerativeAgentsCN) · [AgentVerse](https://github.com/OpenBMB/AgentVerse) (paper: [arxiv 2308.10848](https://arxiv.org/abs/2308.10848)) · [EconAgent (ACL'24)](https://aclanthology.org/2024.acl-long.829/)
- Chinese-community supplement: [CharacterGLM-6B](https://github.com/thu-coai/CharacterGLM-6B) · [Chat-Haruhi-Suzumiya](https://github.com/LC1332/Chat-Haruhi-Suzumiya) · [CharacterEval](https://arxiv.org/abs/2401.01275) · [RoleBench / RoleLLM](https://github.com/InteractiveNLP-Team/RoleLLM-public) · [SuperCLUE-Role](https://github.com/CLUEbenchmark/SuperCLUE-Role) · [pkuxkx wiki](https://www.pkuxkx.net/wiki) · [mudcore](https://gitee.com/mudcore/mudcore) · [mudchina站点列表](https://mudchina.github.io/) · [mud.ren/threads/436 — 炎黄 MUD](https://mud.ren/threads/436) · [筑梦岛](https://zhumengdao.com/) · [猫箱 (ByteDance)](https://www.maoxiang.com/)
