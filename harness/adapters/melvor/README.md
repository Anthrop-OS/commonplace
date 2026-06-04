# harness/adapters/melvor/ — the Melvor Idle adapter

A `Bridge<MelvorState>` over a running **Melvor Idle** instance (`TASKS.md` T2).
It implements the substrate-agnostic contract from `../../bridge/` for Melvor:
`observe()` snapshots the game; `act()` performs a skill action. Game specifics
live here and never leak back into `bridge/`.

```
melvor/
├── melvor-bridge.ts   MelvorBridge — observe()/act(); MelvorState + MelvorGameApi (the port)
├── melvor-mod.ts      mod glue — binds the in-process `game` global to the port; createMelvorBridge()
├── index.ts           public surface
└── melvor-bridge.test.ts
```

The shape mirrors `../../bridge/synthetic-bridge.ts`: a per-affordance switch in
`act()` and a snapshot in `observe()`. The difference is the world is **external**
(a live game), so the bridge holds a reference to the game rather than owning
in-memory state.

## Perception & affordances

`observe()` returns a `Perception<MelvorState>`:

- `state.skills` — every skill with `id` / `name` / `level` / `xp`.
- `state.activeActionId` — the one running action, or `null` when idle.
- `affordances` — one `train:<skillId>` per skill (the target is in the id, so an
  `Action` needs no params), plus `stop`. This is the menu the autotelic selector
  chooses from.

`act()` accepts `train:<skillId>` (→ start that skill) or `stop`; anything else is
`rejected`. `observedAt` is the wall clock (Melvor is real-time, unlike the
synthetic fixture's logical tick).

## Act path: mod API (in-process), not CDP — decided by ADR-0006

The act path was **already chosen at the architectural level by `adr-0006`**
(polyglot: TS harness, Python cognition). That ADR picked the TypeScript harness
*precisely so the adapter reads the `game` global in-process*, and explicitly
rejected single-language Python because it "forces the Melvor adapter through
Playwright / CDP `eval`, making `Perception` extraction … slower and more
brittle than an in-process mod." So **no new ADR is filed** for T2 — this is the
ADR's decision, applied:

| | In-process mod (chosen) | CDP / headless-Chromium (rejected for perception) |
|---|---|---|
| Read | direct property access on `game` — no serialization | `Runtime.evaluate` round-trip returning a serialized snapshot |
| Latency | none (same process) | one round-trip per read |
| Fidelity | full object graph in scope | deep/cyclic game objects serialize poorly |

CDP / OpenClaw stays relevant for the **operator gateway** (an orthogonal
concern; `exploration/prior-art-l2-l3.md`), not for perception.

The L2 **runtime** choice (ElizaOS-core / OpenClaw-gateway / Hermes-fallback lean)
is *not* made here — T2 only needs the Bridge contract. It is committed via its
own ADR when the loop needs it, **deferred to T5** (issue #25).

## Shared-avatar concurrency — surfaced, not solved

Melvor is **single-avatar**: one active action on one save. If the operator and
the agent both drive the same instance, their `act()` calls race on that single
slot (start-skill is last-writer-wins), and the agent's next `observe()` reports
an `activeActionId` it did not set. This adapter does **not** arbitrate that —
no lock, no turn-taking, no operator/agent identity on `Action`.

Per `adr-0007`, the dyad's *operator-acts-in-world* half is staged to **Stardew
(P1)**, whose native co-op gives separate avatars in one world and sidesteps the
shared-avatar race entirely. Melvor (P0) proves only the agent-side loop.
`SyntheticBridge.operatorAct()` is where dual-control is exercised
deterministically in the meantime.

## IP boundary — mod/bridge code only (AGENTS.md rule 4 · adr-0003)

The Melvor game body is **never vendored**. The interfaces in `melvor-mod.ts`
declare only the *shape* of the small in-process surface we bind to (clean-room);
they are not copied from Melvor's source. Concrete field/method names are
confirmed against the live `game` object at integration (the implementer runs a
real Melvor + its mod toolchain — issue #25 preconditions). All game-coupling is
isolated in `melvor-mod.ts`, so a name change touches one file.

## Loading & testing

- **In Melvor:** load the mod in-page and call `createMelvorBridge()`, which reads
  `globalThis.game`. It throws off-page (e.g. plain Node) — the adapter only
  works in-process.
- **Tests:** a fake stands in for `game` (no Melvor needed). Run from `harness/`:
  `npm run ci` (typecheck + tests + 100% coverage of the runtime surface).
