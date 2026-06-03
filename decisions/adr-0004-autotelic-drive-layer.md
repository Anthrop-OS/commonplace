---
id: 0004
uuid: 9ce72919
title: The drive layer is autotelic, not a reward optimizer
date: 2026-06-03
status: accepted
---

# ADR-0004 — The drive layer is autotelic, not a reward optimizer

> uuid `9ce72919` (stable alias; authored as
> `adr-0004-autotelic-drive-layer`, numbered on merge). Output of a
> decision acked by the operator (cyber-ayi), 2026-06-03.

## Decision

The agent's cognition (L3) is built from **drive seeds, not a reward function**:
identity (direction) + needs/drives (engine) + memory/reflection (coherence).
Exploration is **autotelic** — an end in itself. The agent may detour, dawdle,
and chase questions that yield nothing useful; "purposeless" exploration is
intended behavior, not a bug to optimize away.

The drive layer must **not** introduce reward maximization, efficiency
objectives, skill-grinding loops, or expected-payoff action ranking. The
selector ranks by novelty / open-question, never by expected reward or skill
gain. Evaluation is relational/qualitative (the logbook `curiosity` block —
question / detour / surprise), not efficiency-based.

## Context

| Constraint | Source |
|---|---|
| Persistent personality sustaining non-optimal, believable long-horizon behavior is essentially unstudied | `design/autotelic-drives.md`; consensus review |
| "Purposeless exploration" is a failure mode in mainstream RL (noisy-TV, reward hacking) — here it is the *intended* behavior | `design/autotelic-drives.md` |
| The field lacks metrics for non-task engagement; we must build our own | `design/autotelic-drives.md` |

## Consequences

**Positive**
- The behavior of interest (non-instrumental dwelling) is producible, not
  optimized away — the project's core IP and research contribution.
- A homegrown, relational evaluation seed exists from day one (`curiosity` block).

**Negative**
- Runs against the grain of RL tooling and intuition; design + evaluation must
  state the inversion explicitly each time.
- No borrowed benchmark — evaluation must be defined, not imported.

**Rejected alternatives**
- **Intrinsically-motivated goal-conditioned RL** — nearest prior art, but still
  serves skill acquisition; collapses dwelling into a means.
- **Any single optimized objective / reward** — produces a grinder, destroying
  the phenomenon under study.

## References

- `design/autotelic-drives.md`, `drives/README.md`
- `logbook/schema/entry.schema.yaml` (`curiosity` block), `AGENTS.md` rule 5
