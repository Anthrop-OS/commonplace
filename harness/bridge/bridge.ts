// Bridge — the substrate-agnostic perception↔action interface.
// An adapter (harness/adapters/, T2+) implements this for one world.
// The IPC transport that carries these JSON values between the TS harness and
// the Python cognition layer is NOT here — it is orchestration (T5, ADR-0006).

import type { Perception } from "./perception";
import type { Action, ActionResult } from "./action";

export interface Bridge<TState = unknown> {
  /** Read the world: current state plus the affordances available now. */
  observe(): Promise<Perception<TState>>;
  /** Attempt one action. The next `observe()` reflects its effect. */
  act(action: Action): Promise<ActionResult>;
  /** Release the connection, if the adapter holds one. */
  close?(): Promise<void>;
}
