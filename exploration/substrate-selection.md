---
topic: substrate-selection
status: converging
date: 2026-06-03
related-adrs: [adr-0003]
resolves-to:
---

# Substrate selection — which world(s) the dyad inhabits

> Status: **converging**. Not binding. `adr-0003` already locked *Melvor as the
> clean-room first substrate*; this note evaluates the substrate **ladder** beyond
> it and surfaces a strong new entrant (Stardew Valley). Resolves into a new ADR.

## Question

Beyond the clean-room start (Melvor, `adr-0003`), what is the right sequence of
L1 substrates — and does the **full Milestone 0 with dual-control** (operator and
agent both acting in one world) change the answer?

## Guiding principle

**Substrate complexity is a tax that does not directly buy research value** — the
value lives in L3 (the autotelic drive layer). Pick the *least* complex world that
still affords the *kind* of depth being studied. What matters is the **kind** of
depth (progression / social / spatial / emergent), not raw depth.

## Criteria

| Criterion | Why it matters |
|---|---|
| Depth **kind** | must afford the autotelic behavior we study; social depth is closest to the *relationship* research core |
| Substrate complexity | integration cost competes with L3 (the real IP) for budget |
| Determinism / reproducibility | the research record + CI need repeatable runs |
| Single-avatar "inhabit" fit | the dyad inhabits *a* character, not a god-view |
| **Dual-control fit** | MVP = full M0 *with* dual-control — operator + agent in one world |
| Programmable API / MCP | an existing API/MCP server collapses adapter (T2) cost |
| IP | some adapters must stay private (gitignored) |

## Evaluation

| World | Depth (kind) | Complexity | Determinism | Inhabit | Dual-control | API / MCP | IP |
|---|---|---|---|---|---|---|---|
| **Melvor** | low–med (progression) | **low** | **high** (idle/single/pausable) | ✓ you are the player | weak (no co-presence) | mod API + `game` global | mod-only |
| **Stardew Valley** | **med–high (social + progression + spatial)** | low–med | med (seeded RNG) | ✓ a farmer | **native** (co-op: P1+P2, separate avatars) | **SMAPI + several MCP servers** | proprietary; ship mod only |
| **AI Town** | med (social/conversational) | low–med | med (other agents are LLMs) | ✓ a townsperson agent | possible (multi-agent) | agent-native (MIT) | MIT, public OK |
| **2004scape** | **high (spatial+social+progression, full MMO)** | **high** | **low** (real-time, multiplayer) | ✓ but shared world | yes (separate chars) | MMO client/protocol | **gray — private adapter only** |
| **Dwarf Fortress** | **very high (emergent)** | **very high** | low (chaotic) | ⚠ adventure mode only; fortress = god-view | weak | DFHack RPC + `dfhack-mcp` | proprietary; via DFHack |

### Notes per candidate

- **Melvor** — its "clean" *is* its low complexity (no space/social/real-time,
  single-player, readable `game` global). Best for standing up the research
  apparatus (T3/T4/T5) deterministically + in CI. But depth is "a menu of skills";
  the autotelic detour is thin (fish instead of grind), and it has **no
  co-presence**, so it cannot exercise dual-control. Correct as the *first* rung
  (`adr-0003`), not necessarily the M0 rung.
- **Stardew Valley** — the surprise. **Native co-op** = operator is Player 1, agent
  is Player 2, **same farm, separate avatars** → native dual-control that **sidesteps
  the shared-avatar concurrency problem**. Depth is social/relational (NPC hearts,
  seasons) — closest to the *relationship* research core — yet far more tractable
  than 2004scape/DF. Mature **SMAPI** + multiple existing **MCP servers**, including
  one that drives an AI companion as Player 2/3. Strong candidate for the
  full-M0-with-dual-control MVP, possibly *ahead of* Melvor for that milestone.
- **AI Town** — not a game; an agent-native social sandbox (MIT). Low integration,
  social depth. A good second substrate for the social dimension, but Stardew now
  covers social depth *and* dual-control with more "game" texture.
- **2004scape** — the "inhabit a living world" dream (true flâneur wandering), but
  real-time + multiplayer (non-deterministic), MMO integration (high), and IP-gray
  → **private adapter only**. A later rich-world milestone, kept private.
- **Dwarf Fortress** — depth ceiling (emergent storytelling), but integration would
  eat the L3 budget. `dfhack-mcp` lowers *reading* state; *acting* + spatial
  reasoning stay hard, and fortress mode is god-view (only adventure mode
  "inhabits"). Research stretch, not near-term.

## Architecture implication: MCP-backed adapters

Existing game MCP servers do **not** replace the `Bridge` (T1) — they give an
adapter a ready transport. An **MCP-backed adapter** implements `observe()` /
`act()` by calling the game's MCP tools. For Stardew (and partly DF) this turns T2
from "build integration from scratch" into "thin adapter over an existing MCP
server," materially lowering substrate complexity.

## Current lean

A complexity ladder, not a single pick:

1. **Melvor — first rung (locked, `adr-0003`).** Stand up T3/T4/T5 deterministically.
2. **Stardew Valley — strong candidate for the M0 rung** *because* MVP now includes
   dual-control: native co-op gives operator+agent co-presence with separate avatars,
   plus social/relational depth and a ready SMAPI/MCP path. Possibly replaces Melvor
   as the M0 substrate, or follows immediately.
3. **AI Town** — social-dimension option; now partly subsumed by Stardew.
4. **2004scape** — later rich-world milestone, **private adapter**.
5. **Dwarf Fortress** — research stretch (adventure mode + DFHack), de-prioritized.

**Key trade-off:** Melvor minimizes complexity but *cannot* exercise dual-control
(no co-presence); Stardew adds modest complexity but is the lowest-cost world that
satisfies the chosen MVP (full M0 + dual-control) and aligns with the relationship
research core.

## Open items

- Operator decision: does Stardew **replace** Melvor as the M0 substrate, or sit as
  rung 2 after a Melvor clean-room proof? → a new ADR (substrate ladder / M0 substrate).
- Validate the Stardew MCP servers' action coverage + stability before committing.
- Confirm `dfhack-mcp` is read-only or also actuates, if DF is ever revisited.
- Separate exploration may be warranted for **MVP scope** (full M0 + dual-control)
  as its own note.

## Sources

- `decisions/adr-0003-melvor-clean-room-first.md`; `TASKS.md` (T1–T5); `harness/README.md` (IP boundary)
- DF: [dfhack-mcp](https://github.com/oleksiy-korniychuk/dfhack-mcp); [DFHack docs](https://docs.dfhack.org/); [Utility:DFHack wiki](https://dwarffortresswiki.org/index.php/Utility:DFHack); [Autonomous DF agent writeup](https://earezki.com/ai-news/2026-03-14-teaching-an-ai-to-play-dwarf-fortress-the-idea/)
- Stardew: [StardewMCP (Nexus)](https://www.nexusmods.com/stardewvalley/mods/46320); [StardewValley-MCP (companion as P2/P3)](https://github.com/amarisaster/StardewValley-MCP); [stardew-mcp (Go/WebSocket)](https://github.com/Hunter-Thompson/stardew-mcp); [SMAPI](https://www.nexusmods.com/stardewvalley/mods/2400)
