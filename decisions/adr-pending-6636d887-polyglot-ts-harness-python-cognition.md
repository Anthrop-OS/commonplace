---
id: pending
uuid: 6636d887
title: Milestone 0 is polyglot — TypeScript harness, Python cognition, JSON bridge seam
date: 2026-06-03
status: accepted
---

# ADR-XXXX — Milestone 0 is polyglot — TypeScript harness, Python cognition, JSON bridge seam

> uuid `6636d887` (stable alias; authored as
> `adr-pending-6636d887-polyglot-ts-harness-python-cognition`, numbered on
> merge). Output of a decision acked by the operator (cyber-ayi), 2026-06-03,
> in the T1 planning session.

## Decision

| Aspect | Choice |
|---|---|
| Harness / runtime + bridge + adapters (L2) | **TypeScript** |
| Cognition — drives, autotelic selector, memory/reflection (L3) | **Python** |
| Bridge boundary (`Perception` / `Action` / `ActionResult`) | language-neutral **JSON**, canonical **JSON Schema** under `harness/bridge/schema/` as the single source of truth |
| Cross-language transport (IPC) | **deferred to T5** orchestration; T1 fixes only the *contract*, not the wire |

The language seam is the bridge seam: TypeScript produces a `Perception` and
executes an `Action` against the world; Python consumes the `Perception` and
emits an `Action`. Both bind to the same JSON Schema, so neither owns the type.

## Context

| Constraint | Source |
|---|---|
| Melvor is a browser game; the richest, lowest-latency perception is an in-process mod reading the `game` global — not CDP `eval` round-trips | `harness/README.md:24-32`, `TASKS.md:23-29` |
| The drive layer + local model (Ollama/Qwen) live in the Python LLM / memory ecosystem | `TASKS.md:38-45`, `AGENTS.md` rule 6 |
| `Perception` / `Action` are the bridge's substrate-agnostic core — already a natural data boundary, not a function-call boundary | `TASKS.md:17-21` |
| One-task-per-PR, stop-for-review cadence scopes work per layer | `AGENTS.md` "How to work" |

## Consequences

**Positive**
- Each layer sits in its strongest ecosystem: TS drives Melvor in-process (no
  CDP `eval` serialization); Python gets first-class LLM / memory tooling for
  the project's core IP (the drive layer).
- The bridge becomes a real wire contract (canonical JSON Schema) — a stronger
  reading of "substrate-agnostic" than a single-language interface would give.
- No new architectural split is introduced: the language boundary *is* the
  bridge boundary that already existed in the design.

**Negative**
- Two toolchains (Node + Python) and a standing serialization discipline:
  `Perception` / `Action` MUST stay JSON-serializable (no methods, no classes
  on the wire).
- An IPC transport must exist before the loop runs end-to-end (T5); until then
  each layer is exercised in isolation against the schema.
- The JSON Schema is the single source of truth — the TS and Python types must
  both bind to it or they silently drift. Conformance is enforced by validating
  against the schema in tests, not by trusting either language's types.

**Rejected alternatives**
- **Single-language TypeScript** — simplest M0 and keeps in-process Melvor, but
  pushes the drive layer (core IP, `TASKS.md` T4) out of the Python LLM / memory
  ecosystem. The project's most original layer should sit where its tooling is
  richest, not where the substrate happens to be.
- **Single-language Python** — best for cognition, but forces the Melvor adapter
  through Playwright / CDP `eval`, making `Perception` extraction from the
  `game` global slower and more brittle than an in-process mod.

## References

- PR: #<NN>
- `TASKS.md` (T1–T5 scope + routing), `harness/README.md` (runtime candidates,
  IP boundary), `AGENTS.md` rule 6 (cloud/local model routing)
- Related: [[adr-0003-melvor-clean-room-first]], [[adr-0004-autotelic-drive-layer]]
