// Perception — a substrate-agnostic world snapshot.
// Canonical contract: ./schema/perception.schema.json (the source of truth).
// Keep this JSON-serializable: no methods, no class instances (ADR-0006).

/** A single thing the agent could do now, surfaced by the world. */
export interface ActionSpec {
  /** Stable id an Action references via its `affordance` field. */
  id: string;
  /** Human-readable name. */
  label?: string;
  /** Free-form description of the parameters this affordance accepts. */
  params?: Record<string, unknown>;
}

/**
 * One snapshot from `Bridge.observe()`.
 *
 * `state` is opaque at the bridge layer — an adapter specializes `TState` for
 * its world (e.g. Melvor in T2); `bridge/` itself never names a game field.
 */
export interface Perception<TState = unknown> {
  /** Which world produced this, e.g. "null", "melvor". */
  substrate: string;
  /** Epoch milliseconds at observation. */
  observedAt: number;
  /** Substrate-defined snapshot; opaque here. */
  state: TState;
  /** What the agent could do now — the menu the selector chooses from. */
  affordances: ActionSpec[];
}
