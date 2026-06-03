# TASKS.md — repository population plan

Ordered. **One task per branch/PR. Stop after each for operator review.** Obey `AGENTS.md`.

**Routing:** `cloud` = OK on a cloud coding agent · `local` = must run on a local model
(touches private/personal data).

## Milestone 0 — clean-room, end-to-end

**Definition of done:** an agent autonomously inhabits a **Melvor** instance, selects actions
by autotelic drives (not reward), writes `private` logbook entries, and pushes to the operator
only when it judges an entry salient — with the operator able to act on the same instance.
Everything below builds toward this. Substrates other than Melvor are deferred.

---

### T1 · bridge interface — `cloud`
- **Scope:** `harness/bridge/` — substrate-agnostic `Perception` / `Action` / `Bridge(observe, act)`.
  Language + shape fixed by `decisions/adr-0006-*` (polyglot): TS types bound to a canonical
  JSON Schema in `harness/bridge/schema/`. See `harness/bridge/README.md`.
- **Out of scope:** any game specifics; the IPC transport (T5).
- **Acceptance:** types compile (`tsc --noEmit`); no game logic; a `NullBridge` stub passes a smoke
  test that validates `observe()` against the canonical schema.
- **Depends on:** —

### T2 · Melvor adapter — `cloud`
- **Scope:** `harness/adapters/melvor/` implementing `Bridge`. Read the global `game` object;
  act via the mod API or a CDP/headless-Chromium connection (choose and justify in a comment).
- **Acceptance:** `observe()` returns a populated `Perception` from a running Melvor; `act()`
  performs at least one skill action; mod/bridge code only (game not vendored). Shared-avatar
  concurrency (human + agent on one save) surfaced in comments, not yet solved.
- **Depends on:** T1

### T3 · logbook pipeline — `cloud` (code) / `local` (at runtime)
- **Scope:** writer/reader validating against `entry.schema.yaml`; tier routing (private →
  gitignored store / Obsidian); optional ntfy/Discord push hook the agent calls when salient.
- **Acceptance:** round-trips the synthetic sample; refuses to emit `shareable`/`narrative`
  without `redaction_checked: true`; creates **no** real entries in the repo.
- **Depends on:** — (parallel with T1/T2)

### T4 · drive layer (templates) — `cloud` (templates) / `local` (fills)
- **Scope:** `drives/` templates — `identity`, `needs/drives` (rise/fall over time/events),
  an **autotelic selector** (novelty / open-question weighted, NOT reward), memory/reflection hooks.
- **Hard constraint:** templates only; fills are gitignored. The selector must not rank actions
  by expected reward or skill gain.
- **Acceptance:** given a `Perception`, the selector proposes an `Action` whose stated reason is
  a question/novelty, not a payoff; detours are reachable. No personalized fills committed.
- **Depends on:** T1

### T5 · orchestration + run — `cloud` (framework) / routing configured
- **Scope:** long-running loop `observe → autotelic select → act → log(tier) → periodic reflect
  → salient push`. Model-routing config (local for private/personal, cloud otherwise).
  docker-compose / run script. Fill README's "Reproducing the system". Default substrate = Melvor.
- **Acceptance:** Milestone 0 reached. Loop timing permits idle dwelling and detours — **not**
  optimized for throughput.
- **Depends on:** T1, T2, T3, T4

---

## Explicitly deferred (not now)
- Stendhal / 2004scape / AI Town substrates — clean-room (Melvor) first.
- Publishing any `shareable` dataset — the record stays private by default.
- Multi-agent — a single dyad first.
- Solving shared-avatar concurrency — surface it in T2, design it after Milestone 0.
