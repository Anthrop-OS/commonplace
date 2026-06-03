# exploration/ — open evaluations and discussion, *before* a decision

The home for thinking that is still in motion: option evaluations, substrate
surveys, MVP scoping, "what if we…" — anything weighed but **not yet decided**.

It completes the chain the other docs leave a gap in:

```
exploration/        →   decisions/ (ADR)   →   design/ + TASKS.md
"still weighing"        "decided, locked"      "building it"
```

## What goes where

| Dir | Holds | Tense |
|---|---|---|
| `exploration/` | open evaluations, trade-offs, surveys — **not binding** | in progress |
| `decisions/` | a decision **already made**, immutable (ADR) | past |
| `design/` | the rationale/skeleton of the **chosen** path | present |
| `ROADMAP.md` / `TASKS.md` | status / the ordered work | present → future |

If you're about to record a decision in `decisions/`, it should trace back to an
exploration (or an operator ack). An ADR records a decision; it is not where you
*make* one — you make it here, in the open.

## Lifecycle

Every note carries a `status`:

- **`open`** — options on the table, no lean yet.
- **`converging`** — a recommendation is forming; trade-offs mostly mapped.
- **`resolved`** — a decision was made. Set `resolves-to: adr-NNNN` and stop
  editing the analysis. The ADR cites this note; this note points at the ADR.

**Never delete a note**, even when resolved or abandoned — the reasoning trail is
itself part of the record (and, for a research instrument, potential data). To
revisit a resolved topic, open a *new* note that supersedes it.

## Authoring

Copy `TEMPLATE.md`. Frontmatter:

```yaml
---
topic: <kebab-case-slug>      # also the filename: <topic>.md
status: open                  # open | converging | resolved
date: 2026-06-03
related-adrs: []              # ADRs this informs or stems from, e.g. [adr-0003]
resolves-to:                  # adr-NNNN once resolved; blank until then
---
```

- Cite sources (`file:line`, URLs) for every non-obvious claim — same bar as ADRs.
- Tables/bullets over prose. State the trade-off, not just the options.
- Link related notes and ADRs with `[[name]]`.
