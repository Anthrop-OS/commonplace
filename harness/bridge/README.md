# harness/bridge/ — the substrate-agnostic perception↔action contract

The seam between the agent and *any* world. `bridge/` defines **what an
observation and an action are** — independent of which game produces them.
Per-substrate adapters (Melvor, …) live in `../adapters/` and *implement* this
contract; game specifics never leak back into here.

This directory is the root of the dependency graph — `TASKS.md` T1. Everything
downstream (the Melvor adapter, the autotelic selector, the orchestration loop)
is shaped to this contract, so it is designed once.

## The contract is language-neutral (ADR-0006)

Milestone 0 is polyglot. The **TypeScript** harness produces a `Perception` and
executes an `Action`; the **Python** cognition layer (`drives/`) consumes the
`Perception` and emits an `Action`. Neither language owns the types — the
**canonical JSON Schema in `schema/` is the single source of truth**, and both
sides bind to it.

```
bridge/
├── schema/                    canonical, language-neutral (the source of truth)
│   ├── perception.schema.json
│   ├── action.schema.json
│   └── action-result.schema.json
├── *.ts                       TS binding: Perception<TState>, Action, Bridge, NullBridge
└── (Python binding lands in T4, bound to the same schema)
```

**Consequence:** `Perception` / `Action` / `ActionResult` are **plain JSON** — no
methods, no classes on the wire. Conformance is proven by validating against the
schema, not by trusting either language's types. The IPC transport that actually
carries JSON between the two languages is **not here** — it is orchestration (T5).

## The three types

| Type | Is | Key fields |
|---|---|---|
| `Perception` | one world snapshot | `substrate`, `observedAt`, `state`, `affordances[]` |
| `Action` | one intent to act | `affordance` (an `ActionSpec` id), `params?`, `reason?` |
| `ActionResult` | the outcome of `act()` | `status` (`ok` / `rejected` / `error`), `detail?` |

- **`affordances` ride inside `Perception`.** `observe()` returns both the current
  state *and* what the agent could do now. That `ActionSpec[]` is the menu the
  autotelic selector chooses from — perception and possibility arrive together.
- **`Action.reason` is first-class.** It carries the *why*: a question, a novelty,
  a surprise — the logbook's `curiosity` block (`design/autotelic-drives.md`). It
  is **not** a payoff or expected reward (ADR-0004). The bridge ignores it; the
  logbook records it. This field is how the project's thesis flows through the system.
- **`Bridge<TState = unknown>`** stays substrate-agnostic *here*. An adapter
  specializes `TState` for its world (e.g. the Melvor `game` object in T2); `bridge/`
  itself never names a game field.

## The Bridge interface

| Method | Purpose |
|---|---|
| `observe(): Promise<Perception>` | read the world (state + affordances) |
| `act(a: Action): Promise<ActionResult>` | attempt one action; the next `observe()` reflects its effect |
| `close?(): Promise<void>` | release the connection (optional) |

`NullBridge` is the contract's reference no-op: `observe()` returns a valid empty
`Perception`, `act()` is a no-op returning `status: 'ok'`. Its smoke test validates
`observe()` against the canonical schema — proving the contract holds with **no
game attached**. That is the T1 acceptance bar.

## Out of scope — by design

| Not here | Where |
|---|---|
| Any game / Melvor state fields | `../adapters/` (T2) |
| IPC transport between TS and Python | orchestration (T5) |
| The Python type binding | `drives/` (T4) — binds to the same `schema/` |
| The selector that *picks* an `Action` | `drives/` (L3, T4) |
| Shared-avatar concurrency (human + agent on one save) | surfaced in T2, designed after Milestone 0 |

## See also

- `TASKS.md` — T1 scope + acceptance; T2–T5 for what this contract must serve.
- `decisions/adr-0006-polyglot-ts-harness-python-cognition.md` — the language decision.
- `decisions/adr-0004-autotelic-drive-layer.md` — why `Action.reason` is novelty, not reward.
- `../README.md` — the L2 runtime ↔ bridge ↔ adapter boundary and the adapter IP rules.
