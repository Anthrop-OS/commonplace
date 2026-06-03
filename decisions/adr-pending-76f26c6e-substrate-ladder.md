---
id: pending
uuid: 76f26c6e
title: Substrate ladder — Melvor is P0, Stardew Valley is P1+
date: 2026-06-03
status: accepted
---

# ADR-XXXX — Substrate ladder — Melvor is P0, Stardew Valley is P1+

> uuid `76f26c6e` (stable alias; authored as `adr-pending-76f26c6e-substrate-ladder`,
> numbered on merge). Output of a decision acked by the operator (cyber-ayi),
> 2026-06-03. Resolves [[exploration-substrate-selection]]; extends
> [[adr-0003-melvor-clean-room-first]].

## Decision

| Priority | Substrate | Role |
|---|---|---|
| **P0** | **Melvor** | Clean-room first. Stand up the research apparatus (T3 logbook · T4 drives · T5 loop) and the **agent-side dyad** (autonomous autotelic play + `private` logbook + agent→operator salient push). Single avatar; **no dual-control** — Melvor has no co-presence. |
| **P1+** | **Stardew Valley** | The next substrate, where **dual-control** lands: native co-op (operator = Player 1, agent = Player 2, **shared farm, separate avatars**) gives the operator-acts-in-world half of the dyad without the shared-avatar concurrency problem. Adds social/relational depth. Integrate via SMAPI + existing MCP. |
| deferred | AI Town · 2004scape (private) · Dwarf Fortress (stretch) | per [[exploration-substrate-selection]] |

**Consequence for the MVP scope.** The MVP target is full Milestone 0 *including*
dual-control. Because Melvor structurally cannot do dual-control, that half is
**staged to P1 (Stardew)**: P0 proves the apparatus + the agent→operator half on
Melvor; P1 completes the dyad with operator→world dual-control on Stardew.

## Context

| Constraint | Source |
|---|---|
| Substrate complexity is a tax that does not buy research value — value is in L3 | `exploration/substrate-selection.md` |
| Melvor is lowest-complexity + deterministic — best to stand up the apparatus | `adr-0003`; `harness/README.md` |
| MVP = full Milestone 0 *with* dual-control (operator + agent act in one world) | operator decision (2026-06-03) |
| Melvor has no co-presence → cannot exercise dual-control | `exploration/substrate-selection.md` |
| Stardew co-op = separate avatars in one world → native dual-control, no shared-avatar race | `exploration/substrate-selection.md` (sources: StardewValley-MCP, SMAPI) |
| The `Bridge` contract is substrate-agnostic → P0→P1 swap is an adapter change | `harness/bridge/`, `adr-0006` |

## Consequences

**Positive**
- P0 minimizes complexity to prove the loop/drives/logbook deterministically.
- The substrate-agnostic `Bridge` (T1) makes the Melvor→Stardew swap an adapter
  change, not a rewrite; a `SyntheticBridge` fixture can develop dual-control
  logic before either real adapter exists.
- Stardew's co-op delivers dual-control without solving shared-avatar concurrency.

**Negative**
- Full dual-control Milestone 0 is **not** reached on Melvor alone — it is staged
  to P1; the "agent-side" and "operator-side" halves land on different substrates.
- Two adapters to build (Melvor mod; Stardew SMAPI/MCP).

**Rejected alternatives**
- **Stardew as P0** — front-loads more complexity (real-time-ish, co-op, SMAPI)
  before the apparatus is proven; against the clean-room principle.
- **Skip Melvor, go straight to dual-control** — loses the deterministic clean-room
  that de-risks T3/T4/T5.

## References

- Resolves: `exploration/substrate-selection.md`
- Extends: [[adr-0003-melvor-clean-room-first]]; relates to [[adr-0004-autotelic-drive-layer]], [[adr-0006-polyglot-ts-harness-python-cognition]]
- `TASKS.md` (T2 adapter), `harness/bridge/` (substrate-agnostic contract)
