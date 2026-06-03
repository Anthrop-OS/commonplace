---
id: 0001
uuid: 48da3cf2
title: Adopt homelab-ops governance patterns
date: 2026-06-03
status: accepted
---

# ADR-0001 — Adopt homelab-ops governance patterns

> uuid `48da3cf2` (stable alias; authored as
> `adr-0001-adopt-homelab-ops-governance`, numbered on merge).
> Output of a decision acked by the operator (cyber-ayi), 2026-06-03.

## Decision

commonplace adopts the operational governance of
`homelab-s5oyt03iv9/homelab-ops`, phased by present need rather than wholesale:

| Pattern | Status | Where |
|---|---|---|
| Protected `main`, PR-only (server-side ruleset + client `pre-push`) | **adopted** | ruleset `protect-main`; `.githooks/pre-push` |
| Worktree-per-task | **adopted** | `scripts/{bootstrap,new-task,preflight}.sh` |
| `Session-Id` + `Agent` commit trailers | **adopted** | `AGENTS.md` rule 7 |
| 3-tier funnel exploration ceiling | **adopted** | `AGENTS.md` |
| ADR system (`adr-pending-<uuid>` + auto-number on merge) | **adopted** | `tools/adr-verify.sh`, `.github/workflows/adr-*.yml` |
| Claim protocol (branch-ref-as-lock), `claim:*` PR gates | **deferred → Phase C** | when concurrent sessions appear |
| commonplace-flavored label taxonomy | **deferred → Phase C** | — |
| Per-persona GitHub Apps | **deferred → Phase D** | reuse `cc-rc-bot` trailer until then |

Shared scripts are **copied and maintained locally** for now; a single-SSoT
toolkit extraction is tracked upstream.

## Context

| Constraint | Source |
|---|---|
| commonplace is agent-operated; needs reviewable history + a record of decisions | project intent — this repo is itself a research instrument on agent operation |
| Collision safety across sessions is a real future need, not a present one | single operator + a few cc sessions today; concurrency is Phase C |
| The machinery is already battle-tested upstream (numbering, verify, hooks) | `homelab-s5oyt03iv9/homelab-ops` AGENTS.md, ADR-0013/0012/0007 |
| Re-deriving a bespoke process would diverge and force a later migration | toolkit-extraction follow-up: homelab-ops#594 |

## Consequences

**Positive**
- Reviewable PR-only history and a protected `main` from the first real commit.
- An ADR trail captures decisions already made (this batch) and future ones.
- Low migration cost when Phase C/D land — the conventions already match upstream.

**Negative**
- Process overhead is heavy relative to the repo's current size.
- Scripts are copied, so they can drift from upstream until homelab-ops#594
  extracts a shared toolkit.
- Adopting the full ADR auto-numbering required enabling, org-wide on Anthrop-OS,
  "Allow GitHub Actions to create and approve pull requests" — a broader grant
  than a single repo.

**Rejected alternatives**
- **Bespoke lightweight process** — would diverge from homelab-ops and force a
  migration once concurrency arrives; loses the already-debugged machinery.
- **No process (direct pushes, no ADRs)** — loses reviewability, collision
  safety, and the decision record that is itself part of this project's purpose.
- **Full mirror immediately (claim protocol + labels + Apps now)** — pays Phase
  C/D costs before the concurrency that justifies them.

## References

- Upstream governance: `homelab-s5oyt03iv9/homelab-ops` `AGENTS.md`
- Shared-toolkit extraction: homelab-s5oyt03iv9/homelab-ops#594
- Implementing PRs: #1 (worktree + pre-push), #2 (tr fix), #3 (ADR system)
- Design context: `AGENTS.md`, `README.md`
