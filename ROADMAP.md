# ROADMAP — where commonplace is going, and where it stands

A navigation map, not a task list. The ordered work lives in `TASKS.md`; the
locked decisions live in `decisions/`; the design rationale lives in `design/`.
This file is the layer above them: the dependency shape, the critical path, the
decisions still ahead, and a dated snapshot of where we are.

> **Why this project exists.** commonplace is an **operator-agent relationship
> research instrument** — the game is the method, not the goal. Milestone 0's real
> output is the start of a private **record** (potential research data); the
> logbook's `curiosity` block is the seed of a homegrown autotelic metric
> ("evaluation must be built, not borrowed" — `design/autotelic-drives.md`).
> See `README.md` / `ETHICS.md`.

## Architecture — the fixed skeleton (L1 / L2 / L3)

| Layer | Is | Milestone 0 choice | Reference |
|---|---|---|---|
| **L1** substrate | the world itself | **Melvor = P0** (clean-room); **Stardew Valley = P1+** (dual-control); others deferred | `adr-0003-*`, `adr-0007` substrate ladder |
| **L2** harness + bridge | executor + perception↔action seam | **TypeScript**; runtime (OpenClaw / ElizaOS / Hermes) **unchosen** | `harness/README.md`, `harness/bridge/README.md`, `decisions/adr-0006-*` |
| **L3** cognition | autotelic drives (core IP) | **Python** | `drives/README.md`, `decisions/adr-0004-*`, `adr-0006-*` |

## Milestone 0 — clean-room, end-to-end

> **Definition of done** (`TASKS.md`): an agent autonomously inhabits a Melvor
> instance, selects actions by autotelic drives (not reward), writes `private`
> logbook entries, and pushes to the operator only when it judges an entry
> salient — with the operator able to act on the same instance.

### Dependency graph

```
        ┌───────────────────────────────┐
        │  T1  bridge interface  (root)  │   substrate-agnostic
        │      Perception/Action/Bridge  │   DONE ✓ (PR #14)
        └───────┬───────────────┬────────┘
                │               │
        ┌───────▼──────┐ ┌──────▼────────┐    ┌───────────────────┐
        │ T2 Melvor    │ │ T4 drive layer│    │ T3 logbook pipeline│
        │    adapter   │ │    templates  │    │    (independent)    │
        └───────┬──────┘ └──────┬────────┘    └─────────┬─────────┘
                └───────┬───────┴───────────────────────┘
                ┌───────▼───────────────────────┐
                │ T5 orchestration + run loop    │   integration, last
                │ observe→select→act→log→reflect │
                │       →salient push            │
                └────────────────────────────────┘
```

**Critical path:** T1 → (T2 ∥ T4) → T5. **T3 is independent** and can land any
time (parallel with T1/T2). **T1 was the single gate — now landed**, so T2 and T4
are unblocked and parallelize, and T3 proceeds on its own.

### Task status (authoritative status: the issue tracker, not this file)

| Task | Routing | Depends | State (2026-06-03) |
|---|---|---|---|
| **T1** bridge interface | `cloud` | — | **done** — `harness/bridge/` shipped (PR #14, closed #9): canonical `schema/*.json` + TS types + `NullBridge` + schema-validating smoke test |
| **T2** Melvor adapter | `cloud` | T1 | **ready** (T1 landed) — not started |
| **T3** logbook pipeline | `cloud` / `local` at runtime | — | **ready** (independent) — not started |
| **T4** drive layer templates | `cloud` / `local` fills | T1 | **ready** (T1 landed) — not started |
| **T5** orchestration + run | `cloud` / routing configured | T1–T4 | blocked on T2–T4 |

### Automated acceptance (CI)

CI checks are **signals, not hard ruleset gates** — matching homelab-ops governance
(`adr-0001`): `protect-main` only enforces `deletion` / `non_fast_forward` /
`pull_request`. cc waits for green before self-merging; nothing mechanically blocks
a merge on a red check (a deliberate hard gate is deferred to Phase D, where a
GitHub App lets bot PRs trigger checks without the numbering-PR deadlock).

| Check | Scope | Enforcement |
|---|---|---|
| **`harness-ci`** (`.github/workflows/harness-ci.yml`) | every PR: `npm ci` → typecheck → tests + **100% coverage** of the L2 runtime surface | signal; cc gates self-merge on green |
| **`adr-pr-check`** | ADR invariants on `decisions/**` PRs | signal (on ADR PRs) |

L2 toolchain: `harness/` is the TypeScript project root (`package.json`, strict
`tsconfig`, tsx + `node:test` + ajv). `drives/` will be the Python root (T4).

## Decisions still ahead (future decision-gates → ADRs)

Each downstream task carries its own small decision-gate. None block T1.

| Open decision | Surfaces in | Status |
|---|---|---|
| harness **runtime**: OpenClaw vs ElizaOS vs Hermes | T2 / T5 | unchosen; **lean = ElizaOS-core + OpenClaw-gateway + Hermes-fallback** per `exploration/prior-art-l2-l3.md` |
| **IPC transport** TS↔Python (how JSON crosses the seam) | T5 | explicitly deferred by ADR-0006 |
| Melvor **act path**: mod API vs CDP / headless-Chromium | T2 | `TASKS.md` requires choose-and-justify |
| **gateway / salient push** channel | T3 | **resolved → adr-pending-37140cf6**: Matrix (continuwuity, fed-off, plaintext) + mautrix-go thin Go gateway. Supersedes the AstrBot/Discord lean (Telegram/Discord fail adr-0005; AstrBot fails transport-not-brain). XMPP+slixmpp = kept fallback. |

## Open explorations (pre-decision)

Evaluations still in motion live in `exploration/` and resolve into ADRs.

| Note | Status | About |
|---|---|---|
| `exploration/substrate-selection.md` | **resolved → adr-0007** | substrate ladder: Melvor P0, Stardew P1+ (dual-control staged to P1) |
| `exploration/gateway-selection.md` | **resolved → adr-pending-37140cf6** | operator↔agent channel = Matrix (continuwuity) + mautrix-go thin Go gateway; Discord soft-constraint, Telegram/Discord out on adr-0005, XMPP kept fallback |
| `exploration/prior-art-l2-l3.md` | converging | L2 runtimes + L3 cognition survey; feeds T2 (runtime) and T4 (drive design): reuse-vs-refuse, drop the optimization objective |

## Governance / ops track (parallel to the product)

Adopted from `homelab-s5oyt03iv9/homelab-ops`. This track makes agent collaboration
safe; it does not block the product critical path.

| Phase | Scope | State |
|---|---|---|
| **A** | commit trailers (`Session-Id` + `Agent`), 3-tier funnel, `protect-main` ruleset | **done** |
| **B** | tooling scripts (`scripts/`, `.githooks/`), ADR system, issue templates | **done** |
| **C** | claim protocol (branch-ref-as-lock), `claim:*` PR-decision gates, full label taxonomy | when concurrent sessions appear |
| **D** | per-persona GitHub Apps under `Anthrop-OS` | eventually |

## Beyond Milestone 0 — explicitly deferred (not now)

- **Other substrates** — Stendhal (social layer), AI Town, 2004scape (private
  adapter). The *rich vs clean world* tension is unresolved.
- **Publishing a `shareable` dataset** — the record stays `private` by default; a
  dataset is a later `visibility` filter, not a retroactive scrub (`adr-0005`).
- **Multi-agent** — a single dyad first.
- **Shared-avatar concurrency** (human + agent on one save) — surfaced in T2,
  designed after Milestone 0.

## Maintaining this file

- This is a **map**, not a source of truth. When it disagrees with `TASKS.md`,
  `decisions/`, or the issue tracker, *they* win — fix the map.
- The task-status table is a dated snapshot; treat the GitHub issues/PRs as live.
- A new locked decision = a new `decisions/adr-NNNN-*`; then update the tables here.
