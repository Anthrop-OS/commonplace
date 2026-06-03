---
id: pending
uuid: 533e2960
title: Start on Melvor as a clean-room substrate; defer richer worlds
date: 2026-06-03
status: accepted
---

# ADR-XXXX — Start on Melvor as a clean-room substrate; defer richer worlds

> uuid `533e2960` (stable alias; authored as
> `adr-pending-533e2960-melvor-clean-room-first`, numbered on merge). Output of a
> decision acked by the operator (cyber-ayi), 2026-06-03.

## Decision

Milestone 0 runs against **Melvor Idle** as a "relationship clean room" — strip
MMO/social noise to validate the dyad itself (autotelic agent + operator on one
instance, salience-gated push, private logbook). Richer substrates are deferred:

| Substrate | Role | When |
|---|---|---|
| **Melvor** | clean-room; validate the dyad | now (Milestone 0) |
| **Stendhal** | add the social layer | after Milestone 0 |
| **AI Town** | L3 generative-agents reference; possible L1 substitute | reference now; substrate TBD |

The "rich vs clean world" tension (AI Town/Stendhal richness vs Melvor quiet) is
**explicitly left open** — clean room first answers the dyad question before
adding world complexity.

## Context

| Constraint | Source |
|---|---|
| Validate the dyad without MMO confounds first | `TASKS.md` Milestone 0; project intent |
| Browser-harness path removes game-bridge + gateway glue for a single-machine prototype | `harness/README.md` (OpenClaw) |
| Melvor is closed buy-to-play: ship mod/bridge code only, never the game body | `AGENTS.md` rule 4 |
| Shared-avatar concurrency (human + agent on one save) is unsolved | `TASKS.md` T2 — surface, don't yet solve |

## Consequences

**Positive**
- The dyad is tested in isolation before world complexity is layered on.
- Fastest path to an end-to-end loop (browser harness, no bridge glue).

**Negative**
- Melvor's quiet may under-exercise the social/relational behaviors of interest;
  Stendhal is the planned next step, not a maybe.
- Defers resolving the rich-vs-clean question rather than settling it.

**Rejected alternatives**
- **Start with a rich world (Stendhal / AI Town)** — couples dyad validation to
  social-layer complexity; harder to attribute what's working.
- **AI Town as L1 immediately** — viable later, but adopting it now front-loads
  the unresolved richness tradeoff.

## References

- `TASKS.md` (Milestone 0, T2), `harness/README.md`, `AGENTS.md` rule 4
- Related: [[adr-0001-adopt-homelab-ops-governance]],
  [[adr-pending-9ce72919-autotelic-drive-layer]]
