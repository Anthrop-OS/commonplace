# AGENTS.md — binding rules for anyone (human or agent) working this repo

This repo is the reproducible **system** of a human + AI-agent *dyad* that inhabits an
open-ended game world together — to explore and co-dwell, not to win. The lived **record**
of any real dyad is private and lives elsewhere. Read `README.md`, `ETHICS.md`, and
`design/*.md` before writing code.

## Hard rules — do not violate

1. **Licensing.** Code is `AGPL-3.0-only`; docs are `CC-BY-SA-4.0`. See `LICENSE` /
   `LICENSE-docs`. No per-file SPDX header required — the LICENSE files cover the tree.

2. **The public/private split is absolute, and git history is forever.** NEVER commit
   anything matched by `.gitignore`: the real logbook (`logbook/entries/`), personalized
   drive fills (`*.local.*`, `drives/identity/*.filled.*`), private adapters
   (`harness/adapters/private/`), secrets. Commit-then-delete does **not** remove it from
   history. If unsure whether something is private, treat it as private and ask the operator.

3. **Visibility tiers.** Every logbook entry carries a `visibility` tier (`private` by
   default) per `logbook/schema/entry.schema.yaml`. Tooling defaults to `private` and must
   refuse to emit `shareable`/`narrative` without `redaction_checked: true`.

4. **Adapter IP boundary** (see `harness/README.md`): NO public adapter for RuneScape-derived
   servers (2004scape) — those stay in the gitignored private path. Melvor: ship mod/bridge
   code only, never the game body. AI Town derivatives (MIT): fine. Stendhal (copyleft):
   verify terms before vendoring.

5. **The drive layer is NOT a reward optimizer.** Exploration is *autotelic* — an end in
   itself. The agent may detour, dawdle, and chase questions that yield nothing useful;
   "purposeless" exploration is intended behavior here, not a bug to optimize away. Do not
   introduce reward maximization, efficiency objectives, or skill-grinding loops. See
   `design/autotelic-drives.md`.

6. **Cloud/local model routing.** Anything that touches personalized fills or the real
   logbook runs on a **local** model (Ollama/Qwen) — never a cloud API. Cloud agents may
   work only on public, non-personal code (templates, bridge, adapters, orchestration
   framework).

7. **Commit trailers.** Every agent-authored commit MUST carry two trailers below the
   final blank line of the message:

   ```
   Session-Id: <uuidv7>
   Agent: <persona>-bot
   ```

   One `Session-Id` per cc invocation (UUIDv7 / RFC 9562); all commits in that session
   share it. Persona names follow the homelab-ops convention (per ADR-0013 in
   `homelab-s5oyt03iv9/homelab-ops`); the cc-rc daemon authoring scaffold commits writes
   `Agent: cc-rc-bot`. Transitional note: GitHub App identities are not yet registered for
   this repo, so the commit *author* may still be `cyber-ayi`; the trailer is the
   authoritative persona record until the App lands.

## Exploration ceiling — the 3-tier funnel

A hard ceiling on exploration before STOP-and-ask. Adopted from homelab-ops AGENTS.md
(`#118 tier ③`). STOP on hit; on the final miss, record the fallback and STOP — never
unbounded explore.

| Layer | Cost | Action | Outcome |
|---|---|---|---|
| T1 foundational | ~3K tok | `gh pr/issue list --search`; `ls design/`; `grep -l <topic>` | hit → STOP, act |
| T2 bridging | medium | read one peer file in full; fetch the latest spec / comment | hit → STOP, act |
| T3 moonshot | expensive | one broadened-keyword search | miss → record fallback, STOP |

Budget exhausted without an answer = STOP-and-ask, not a license to keep digging.

## Ethics

`ETHICS.md` is a non-binding notice, **not** a license condition — do not turn it into one
(that would break AGPL/OSI). Honor its spirit in the design: boundary scaffolding,
transparency, scaffold-not-replace.

## How to work

Follow `TASKS.md` in order. **One task per branch/PR. Stop after each task for operator
review — do not chain tasks autonomously.** The clean-room milestone in `TASKS.md` is the
first definition of done.
