# commonplace

A human + AI-agent **dyad** inhabiting an open-ended game world together — not to optimize or win, but to explore and co-dwell. This repository is the reproducible **system**.

**Status:** early scaffold.

## What this is / isn't

- A research instrument for studying **operator–agent relationships**. The game is the method, not the goal.
- A three-layer runtime: bridges to game worlds (L1), a substrate-agnostic agent harness (L2), and a drive layer of identity + needs + memory/reflection (L3).
- It is **not** a companion product and **not** engagement-optimized. See [`ETHICS.md`](./ETHICS.md).

## Layout

```
commonplace/
├── LICENSE              AGPL-3.0-only  (code)
├── LICENSE-docs         CC-BY-SA-4.0   (docs & design)
├── ETHICS.md            non-binding ethical notice
├── AGENTS.md            binding rules for human or agent contributors
├── TASKS.md             ordered population plan (T1 → T5 → Milestone 0)
├── harness/             agent runtime (L2) + game bridge
├── drives/              identity + needs + memory/reflection (the core IP)
└── design/              design skeletons (informed symbiosis, autotelic drives)
```

## Quick start

This repo is currently scaffold-only — no runnable harness yet. To follow or
extend the build:

1. Read `AGENTS.md` for the binding contributor rules (licensing, IP boundary,
   drive-layer constraint, model routing).
2. Read `TASKS.md` for the ordered task plan; Milestone 0 (`T1` → `T5`) brings
   the dyad up end-to-end against a clean-room substrate.
3. Read `design/autotelic-drives.md` and `design/informed-symbiosis.md` for the
   load-bearing design stances before touching the drive or harness layers.

## Licensing

- **Code:** `AGPL-3.0-only` (see `LICENSE`). Network copyleft — if you run a
  modified version as a service, you must release your changes.
- **Docs & design:** `CC-BY-SA-4.0` (see `LICENSE-docs`).

## Ethics

This project ships an ethical **notice** ([`ETHICS.md`](./ETHICS.md)), **not** an
ethical-source *license*. It is a non-binding statement of intent and does **not**
modify or restrict the AGPL grant — the software stays genuinely open source. We
*ask*, not require, that you not repurpose this for engagement-maximization,
fostered dependency, or deceptive companionship. The real safeguards live in the
**design** (boundary scaffolding built into the system) and in the open
statement — not in the license.

## A note on game-world adapters

`harness/adapters/` holds perception↔action bridges. Bridges here are
substrate-agnostic. Some adapters are intentionally **not** in this public repo —
RuneScape-derived servers carry IP gray-areas; keep those private. See
`harness/README.md`.
