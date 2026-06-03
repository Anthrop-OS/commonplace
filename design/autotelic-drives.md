# Autotelic Drives — design skeleton (draft)

The agent's exploration should be an **end in itself**, not a means to skill
acquisition or task completion. The field's term for this is **autotelic agency**.

**Status:** skeleton. This is the project's most original — and least-charted — layer.

## Anchors (closest prior art)

- Autotelic agents / intrinsically-motivated goal-conditioned RL (Colas et al. 2020;
  Srivastava & Singh 2025). The nearest existing work — but framed in RL goal-
  conditioning, and still ultimately in service of *skill acquisition*.
- **The gap:** persistent *personality / internal needs* that sustain non-optimal,
  believable behavior over long horizons is essentially unstudied (the consensus
  review scored personality-modeling coverage as a near-total GAP). This is ours to fill.

## Design stance

- **Drive seeds, not reward functions.** Identity (direction) + needs/drives (engine)
  + memory/reflection (coherence). No single optimized objective.
- **Curiosity as purpose, not as instrumental bonus.** The agent may detour, dawdle,
  and follow questions that yield nothing useful. (cf. the *flâneur* — the deliberately
  aimless wanderer.)
- **"Purposeless exploration" is a failure mode in mainstream RL** (the noisy-TV
  problem, reward hacking). Here it is the *intended* behavior. Design and evaluation
  must reflect that inversion explicitly — we are running against the grain of the field.

## Evaluation (must be built, not borrowed)

The field lacks metrics for autotelic / non-task engagement (the consensus review
rated this the weakest-covered area). The logbook's `curiosity` block
(question / detour / surprise) is the seed of a homegrown measure — relational and
qualitative, not efficiency-based.
