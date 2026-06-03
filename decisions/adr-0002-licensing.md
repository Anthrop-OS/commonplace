---
id: 0002
uuid: 49c91ca1
title: License code AGPL-3.0, docs CC-BY-SA-4.0, ethics as a non-binding notice
date: 2026-06-03
status: accepted
---

# ADR-0002 — License code AGPL-3.0, docs CC-BY-SA-4.0, ethics as a non-binding notice

> uuid `49c91ca1` (stable alias; authored as `adr-0002-licensing`,
> numbered on merge). Output of a decision acked by the operator (cyber-ayi),
> 2026-06-03.

## Decision

| Artifact | License |
|---|---|
| Code | `AGPL-3.0-only` (`LICENSE`) |
| Docs & design | `CC-BY-SA-4.0` (`LICENSE-docs`) |
| Ethics | a **non-binding notice** (`ETHICS.md`), explicitly NOT a license condition |
| Future shareable dataset (if ever published) | intended `CC0` / `ODC-By`, not now |

`ETHICS.md` states intent (no engagement-maximization, fostered dependency, or
deceptive companionship) but does **not** modify or restrict the AGPL grant.

## Context

| Constraint | Source |
|---|---|
| Network copyleft wanted: a modified hosted version must release its changes | the system may run as a service; AGPL closes the SaaS loophole |
| Real safeguards must live in design + open record, not unenforceable license text | `ETHICS.md`; companion-systems harm literature |
| Must stay genuinely open-source (OSI) | adding use-restrictions would break AGPL/OSI status |

## Consequences

**Positive**
- Strong copyleft on a network service; docs share-alike.
- Stays OSI-open — no ethical-source carve-outs that fragment the license.
- The ethical stance is public and legible without being legally brittle.

**Negative**
- AGPL deters some commercial adopters (intended, not incidental).
- A non-binding notice cannot stop bad-faith reuse — only make it legible.

**Rejected alternatives**
- **Permissive (MIT/Apache)** — no network copyleft; a hosted fork could close
  its changes.
- **Ethical-source license** (use-restrictions in the grant) — breaks OSI-open
  status and is, in practice, near-unenforceable.

## References

- `LICENSE`, `LICENSE-docs`, `ETHICS.md`, `README.md`
- Related: [[adr-0005-public-private-split]]
