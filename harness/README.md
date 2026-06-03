# harness/ — agent runtime (L2) + game bridge

The world-agnostic runtime and the perception↔action bridge that connects it to a
game world. The runtime is *not* the world (L1) and *not* the drive layer (L3 — see
`drives/`); it is the executor in between.

```
harness/
├── bridge/      substrate-agnostic perception↔action interface
└── adapters/    per-substrate adapters  (see IP boundary below)
```

## Runtime candidates (evaluated)

- **OpenClaw** — gateway + CDP browser harness. Fastest path for a single-machine,
  human-in-the-loop prototype: its browser harness drives a web game directly (no
  game-bridge glue), and its messaging gateway gives the operator an async channel.
- **ElizaOS** — the only candidate with a working "agent-as-player-in-world"
  precedent (provider → LLM → action → evaluator loop). Best for a long-lived,
  inhabited deployment.
- **Hermes Agent** — general, local-first (Ollama). The steady fallback brain when a
  gateway-style harness is too heavy or stronger local memory/planning is needed.

## IP boundary — read before adding an adapter

Bridges in `bridge/` stay substrate-agnostic. Adapters carry the substrate-specific
risk, and some must **not** live in this public repo:

- **RuneScape-derived servers (e.g. 2004scape)** carry IP gray-areas. Keep their
  adapter private: `harness/adapters/private/` (gitignored).
- **Closed buy-to-play games (e.g. Melvor):** ship mod code only, never the game body.
- **MIT-licensed substrates (e.g. AI Town derivatives):** fine to include here.
- **Copyleft substrates (e.g. Stendhal):** may impose their license on derivatives —
  verify the terms before vendoring anything.
