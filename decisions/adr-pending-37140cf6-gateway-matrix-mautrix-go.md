---
id: pending
uuid: 37140cf6
title: operator↔agent gateway — Matrix (continuwuity) + mautrix-go, separate Go gateway process
date: 2026-06-25
status: accepted
---

# ADR-XXXX — operator↔agent gateway — Matrix (continuwuity) + mautrix-go, separate Go gateway process

> uuid `37140cf6` (stable alias; authored as
> `adr-pending-37140cf6-gateway-matrix-mautrix-go`, numbered on merge). Output of
> a decision acked by the operator (cyber-ayi), 2026-06-25, across a multi-agent
> third-party gateway + SDK review (vendor sources discounted; a WebFetch
> summarizer hallucinated the mautrix-go license as AGPL — corrected to MPL-2.0
> via the GitHub API). Resolves [[gateway-selection]] and the ROADMAP
> `salient push channel` gate. Supersedes the prior MVP lean (AstrBot over Discord).

## Decision

| Aspect | Choice |
|---|---|
| operator↔agent channel | **Matrix**, self-hosted, **federation off**, **plaintext rooms**, **E2EE off** |
| homeserver | **continuwuity** (Rust single-binary; recheck `tuwunel` fork periodically) |
| SDK + gateway process | **mautrix-go** — pure `mautrix` client layer (**not** `bridgev2`), run as a **separate thin Go gateway process** that talks to the Python L3 over the IPC seam |
| `Python co-location` | **downgraded** from a selection criterion to a **soft preference** |
| E2EE | **off** for MVP — privacy comes from self-hosting + federation-off, not encryption; pin off so a client cannot auto-encrypt and lock the bot out |

Privacy model: a single-user, federation-off homeserver keeps content and metadata
on our own box — so the matrix-nio/E2EE-on-bots friction is structurally avoided by
**not** running E2EE. Server/backup at-rest is covered by disk/backup encryption,
not the channel.

## Context

| Constraint | Source |
|---|---|
| **transport-not-brain** — L3 (Python) is the brain; the channel must not impose its own agent/LLM loop | `exploration/gateway-selection.md`; `adr-0004` |
| **self-host + private** — the record is `private`; content must not transit a third party | `adr-0005` |
| **agent-initiated salient push** (decisive, unusual) — the agent self-judges salience and pushes | `gateway-selection.md` (T3/T5) |
| **7×24 long-lived robustness** — reconnect + since-token resume on a standing bot | this review |
| substrate = Melvor mod + Stardew SMAPI/MCP — **no browser** → no CDP/browser channel value | `adr-0007` |
| architecture is already **polyglot** (TS L2 + Python L3 over a JSON seam) → adding a Go gateway is one more same-shape seam, not a new paradigm | `adr-0006` |

## Consequences

**Positive**
- Self-hosted + federation-off → content stays on our box; the E2EE×bot fiddliness
  is sidestepped (E2EE off).
- **mautrix-go is the healthiest, production-proven Matrix library** — monthly
  release train (v0.28.1, 2026-06-16); it is the client layer the 7×24 mautrix
  bridges (whatsapp/signal/telegram) `require`. Go static binary = most reliable
  long-lived runtime (no venv/GIL).
- The Go↔Python **language boundary physically enforces transport-not-brain** —
  cognition cannot be smuggled into the transport.
- Pure client (no `bridgev2`) → thin; **MPL-2.0** is file-level copyleft and does
  **not** infect the Python L3 IP. E2EE-off ⇒ no `crypto`/libolm/cgo burden.
- Operator gets a real daily client (Element) — UX the runner-up (XMPP) lacks.
- Eliminates `gateway-selection.md`'s "one real risk" (bypassing AstrBot's own
  cognition): a pure-protocol channel has no cognition to bypass.

**Negative**
- Polyglot **2 → 3 languages** (TS L2 + Python L3 + **Go** gateway) + one IPC seam
  (Go↔Python) to build and test. Accepted on condition the gateway stays **thin**
  (a few hundred lines of pure send/recv/reconnect — never grows cognition).
- **bus-factor = 1** (tulir) — Go does **not** fix this (same maintainer as
  mautrix-python); mitigate by pinning + retaining fork ability. (Matrix's whole
  SDK ecosystem fails a strict bus-factor bar — mitigation, not avoidance.)
- Default reconnect is **fixed 10 s**, not exponential backoff; customize
  `Syncer.OnFailedSync` if 5→320 s is wanted. since-token resume IS built in.
- continuwuity↔tuwunel **fork-churn** (conduwuit archived 2026-05-29) — recheck the
  active branch periodically; pin the binary.

**Rejected alternatives**

| Candidate | Why not |
|---|---|
| **AstrBot** (prior MVP pick) | Full agent framework with its own LLM / persona / RAG / sandbox → violates transport-not-brain (would have to gut its brain); AGPL-3.0. |
| **Telegram** (python-telegram-bot) | Bot chats are **not E2EE**, plaintext on Telegram cloud → conflicts with `adr-0005`; must never carry secrets/keys/IP (homelab `#133` discipline). Push is most mature, but privacy is a hard veto. |
| **Discord** (discord.py) | discord.py is a clean transport, but Discord cloud stores plaintext with no text E2EE → same `adr-0005` veto. |
| **Signal** (signal-cli) | Only content-E2EE + only cold-push, but **pseudo-self-host** (dedicated phone number, rides Signal servers) and heaviest ops (~3-month relink / client-expiry / daemon CPU-degrade, signal-cli #1585). Conditional-only. |
| **XMPP** (Prosody + slixmpp) | Clean **runner-up** — lightest ops (~25 MB), single healthy SDK (slixmpp more active than the Matrix Python libs). Loses on operator client UX (Gajim/Conversations < Element). Kept as the fallback — the channel is swappable behind the transport seam. |
| **matrix-nio** | Semi-stalled (last release 2024-10); reconnect must be self-built (`sync_forever` raises on non-timeout); bus-factor≈1. |
| **mautrix-python** | Bridge module deprecated 2024-07 (rewrite migrated to Go); sparse releases — adopting it bets on the maintainer's abandoned path. |

## References

- PR: #<NN>
- Resolves: `exploration/gateway-selection.md`; ROADMAP `salient push channel` gate.
- Related: [[adr-0005-public-private-split]], [[adr-0006-polyglot-ts-harness-python-cognition]]
- mautrix-go pure-client usage: `maunium.net/go/mautrix` `example/main.go` —
  `NewClient(hs, userID, token)` → `Syncer.OnEventType` → `SyncWithContext`;
  push via `SendText` / `SendMessageEvent` at any time.
