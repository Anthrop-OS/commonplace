---
id: pending
uuid: a36d1d8e
title: L2 harness runtime — self-built thin run-loop, no agent framework
date: 2026-06-25
status: accepted
---

# ADR-XXXX — L2 harness runtime — self-built thin run-loop, no agent framework

> uuid `a36d1d8e` (stable alias; authored as
> `adr-pending-a36d1d8e-l2-harness-runtime`, numbered on merge). Output of a
> decision acked by the operator (cyber-ayi), 2026-06-25, across a multi-agent
> third-party harness-selection review (vendor sources discounted; synthetic
> -pollution intercepted and cross-verified). Resolves the ROADMAP
> `harness runtime` decision-gate and [[prior-art-l2-l3]].

## Decision

| Aspect | Choice |
|---|---|
| L2 harness runtime (T5 run-loop) | **Self-built thin TypeScript run-loop** over the shipped `harness/bridge/` contract (T1). **No agent framework adopted.** |
| L3 memory / reflection | Reuse **libraries** (Letta/Mem0; Generative-Agents reflection pattern) — not a framework |
| L3 autotelic selector + per-substrate adapters (T2/T4) | **Self-built** — no reusable prior art (autotelic-not-reward, `adr-0004`) |
| `Python co-location` of the run-loop | not a constraint here — L2 stays TS (`adr-0006`); the loop is glue over the Bridge |

The run-loop (`observe → select → act → log → reflect → salient push`) is authored
in-repo as a small state machine binding the existing `Perception`/`Action`/
`ActionResult` schema. Reuse happens at the **library** level where it pays
(memory, gateway), never by adopting a runtime that owns the cognition loop.

## Context

| Constraint | Source |
|---|---|
| L3 cognition is **external Python over the JSON-Schema seam** → a TS framework's LLM-orchestration core is bypassed; only its executor shell would be used | `adr-0006`; `harness/bridge/` |
| T1 Bridge already shipped — zero runtime deps, 100% coverage → the L2 run-loop workload is **small** | `harness/bridge/`, `ROADMAP.md` |
| autotelic **not reward** → every surveyed framework/selector carries reward/curriculum/skill bias; none reusable for the selector | `adr-0004`; `exploration/prior-art-l2-l3.md` |
| Substrate = Melvor (in-process mod) + Stardew (SMAPI/MCP) — **no browser** → CDP/browser harnesses moot | `adr-0007` |
| operator↔agent channel decided separately → the harness need not provide a gateway | `exploration/gateway-selection.md` |
| Workload concentrates where **no reusable component exists** (autotelic selector + game adapters); the reusable parts (memory, gateway) are already reused as libraries | this review |

## Consequences

**Positive**
- Zero runtime dependencies preserved; L2 stays same-source as the Bridge; the
  transport↔cognition seam stays explicit (JSON Schema), not buried in a framework.
- No framework cognition competes with the self-built L3 — the autotelic selector
  stays authoritative (no second memory/persona/evaluator loop to disable).
- Nothing to "strip" (crypto / persona / evaluators) and no abstraction to conform
  to (Worlds/Rooms, providers, graph nodes) → no adaptation tax.

**Negative**
- The run-loop orchestration + the TS↔Python IPC transport are ours to build and
  maintain (small, but not free; transport deferred to T5 per `adr-0006`).
- Forgo framework-level battle-tested memory/state infra — mitigated by reusing
  **Letta/Mem0 as libraries** at L3, not as a runtime.

**Rejected alternatives** — the full audit (each third-party-sourced; the common
death-knell: external Python brain ⇒ a framework's LLM-orchestration value is
bypassed, leaving dead weight; general harnesses additionally carry cognition that
invades L3):

| Candidate | Layer / lang | Why not |
|---|---|---|
| **ElizaOS** | TS | Loop+memory bypassed; memory not cleanly extractable; bus-factor≈1, `develop` history-rewrite, memory-poisoning fund-theft demo (arXiv 2503.16248), SDNY class action 1:26-cv-3238. Net-negative. |
| **Mastra** | TS | 226 transitive deps + PostHog telemetry + open-core `ee/` + 2026-06 supply-chain poisoning; only real survivor (durable workflow) mismatches a single-chain loop. |
| **Inngest AgentKit** | TS | Half-dormant (last stable 2025-11); strips to an empty shell without LLM; real durable-exec lives in `inngest` core below it + platform commitment. |
| **Vercel AI SDK** | TS | LLM-orchestration is its whole value; TS side calls no LLM → dead weight (only zod/SSE residual, already covered by JSON Schema). |
| **VoltAgent** | TS | Heaviest (317 transitive deps), youngest, thinnest community, OTel-on-by-default. |
| **OpenAI Agents JS** | TS | Built around `run()` LLM-loop; hard-pulls ~10 MB openai client + default telemetry; zod version-lock. |
| **LangGraph.js** | TS | Graph orchestration = over-abstraction for a single-chain loop; still pulls heavy `@langchain/core`. |
| **OpenClaw** | TS | Over-heavy multi-channel assistant; star-inflation + plugin-security doubts. (NOT "CDP double-fail" — that dismissal was corrected; browser is one tool among many.) |
| **hermes-agent** | Python | Brain-internal monolith; cannot degrade to a pure executor (ACP/MCP expose its own brain); adopting collapses the `adr-0006` TS-L2 seam; ~80% of its workload (dev tools / messaging / cron) unusable for a game agent; bus-factor≈1, ~23k issue backlog, state.db corruption reports. |
| **AgentScope / LangGraph-py** | Python | Collapses `adr-0006` — the executor would fall to Python, dissolving the polyglot seam. |

**Design inputs adopted (read-only — no code, no dependency):**
`gigio1023/minecraft-llm-agent-community` (TS three-layer cognition→execution→
**verification**, "LLM selects but does not own world truth" gate); ElizaOS
`runActionsByMode` phasing + World/Room/Entity memory-scoping shape; Mastra
durable-workflow/storage pattern (only if a cross-restart durable need emerges);
LangGraph StateGraph reducer model (only if the loop ever branches).

## References

- PR: #<NN>
- Resolves: `exploration/prior-art-l2-l3.md`; ROADMAP `harness runtime` gate.
- Related: [[adr-0004-autotelic-drive-layer]], [[adr-0006-polyglot-ts-harness-python-cognition]], [[adr-0007-substrate-ladder]]
