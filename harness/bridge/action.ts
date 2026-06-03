// Action / ActionResult — a substrate-agnostic intent and its outcome.
// Canonical contract: ./schema/action.schema.json, ./schema/action-result.schema.json.
// Keep JSON-serializable (ADR-0006).

/** One intent to act, consumed by `Bridge.act()`. */
export interface Action {
  /** The `ActionSpec.id` this targets, from a Perception's affordances. */
  affordance: string;
  /** Parameters for the chosen affordance. */
  params?: Record<string, unknown>;
  /**
   * The autotelic *why*: a question, a novelty, a surprise — NOT a payoff or
   * expected reward (ADR-0004). The bridge ignores it; the logbook records it.
   */
  reason?: string;
}

/** Whether an action applied, was refused by the world, or failed in transit. */
export type ActionStatus = "ok" | "rejected" | "error";

/** The outcome of `Bridge.act()`. The next `observe()` reflects any change. */
export interface ActionResult {
  status: ActionStatus;
  /** Human-readable detail, especially for `rejected` / `error`. */
  detail?: string;
}
