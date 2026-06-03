# drives/ — the drive layer (identity + needs + memory/reflection)

The project's core IP and most original layer. The design rationale lives in
`design/autotelic-drives.md`; this directory holds the implementation.

The drive layer is what keeps the agent from collapsing into a value-optimizing
grinder. It is **not** a reward function. It is:

- **identity** — direction (who this agent is, what it tends toward);
- **needs / drives** — the engine (curiosity, rest, novelty… rising and falling);
- **memory / reflection** — coherence and growth over time.

## Template-public, fill-private

Templates are public. The **personalized fills** — your agent's actual identity, your
operator profile, the specifics of your relationship — are **not**. They are gitignored
(`*.local.*`, `identity/*.filled.*`).

A public template plus a private fill keeps the *method* open and reproducible while
keeping your *relationship* out of the open repo. Anyone can stand up a dyad; no one
gets yours.
