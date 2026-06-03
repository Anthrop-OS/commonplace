---
id: pending
uuid: cebf54db
title: Split system (public) from record (private) into two repos, day one
date: 2026-06-03
status: accepted
---

# ADR-XXXX — Split system (public) from record (private) into two repos, day one

> uuid `cebf54db` (stable alias; authored as
> `adr-pending-cebf54db-public-private-split`, numbered on merge). Output of a
> decision acked by the operator (cyber-ayi), 2026-06-03.

## Decision

The reproducible **system** and the lived **record** live in two separate repos:

| Layer | Repo | Contents |
|---|---|---|
| System (public) | `Anthrop-OS/commonplace` | runtime/bridge, drive templates, design, logbook *schema*, redacted samples |
| Record (private) | `homelab-s5oyt03iv9/commonplace-book` | real logbook entries, personalized fills, IP-sensitive adapters |

The split is enforced day one, not as a later cleanup: the public repo's
`.gitignore` excludes the record by construction, and the record is a separate
repo so a gitignore slip cannot surface a private entry. Every logbook entry
carries a `visibility` tier (`private` default); a future shareable dataset is a
filter on that tier, not a retroactive scrub.

## Context

| Constraint | Source |
|---|---|
| Git history is forever — commit-then-delete does not remove a leaked entry | `AGENTS.md` rule 2 |
| The record is potential research data; "publish a dataset later" must stay clean | `README.md`; project intent |
| Personal/relational content and IP-gray adapters must never enter the public tree | `logbook/schema/entry.schema.yaml`; harness IP boundary |

## Consequences

**Positive**
- A gitignore mistake in the public repo cannot expose the record — the files
  are simply not there.
- Deliberate dataset publication later is a `visibility == shareable` filter.
- Personal fills and private adapters get the same hard isolation as the logbook.

**Negative**
- Two repos to keep coordinated (schema lives public, entries live private).
- The private repo on GitHub is still third-party-hosted; strongest isolation
  needs an operator-controlled mirror (noted as a threat-model caveat).

**Rejected alternatives**
- **Single repo with `.gitignore`** — one slip leaks history permanently.
- **Tailscale-mesh-only record (no GitHub)** — stronger isolation but loses
  convenient hosting; can still be added as a mirror later.

## References

- `README.md`, `AGENTS.md` rule 2, `logbook/schema/entry.schema.yaml`
- `homelab-s5oyt03iv9/commonplace-book` (private record repo)
- Related: [[adr-0001-adopt-homelab-ops-governance]], [[adr-pending-49c91ca1-licensing]]
