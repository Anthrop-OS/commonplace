// NullBridge — the contract's reference no-op. Connects to no world.
// Proves the bridge interface is implementable and the JSON contract holds with
// no game attached (the T1 acceptance bar).

import type { Bridge } from "./bridge";
import type { Perception } from "./perception";
import type { Action, ActionResult } from "./action";

/** State of a world with nothing in it. */
export type NullState = Record<string, never>;

export class NullBridge implements Bridge<NullState> {
  async observe(): Promise<Perception<NullState>> {
    return {
      substrate: "null",
      observedAt: Date.now(),
      state: {},
      affordances: [{ id: "noop", label: "do nothing" }],
    };
  }

  async act(_action: Action): Promise<ActionResult> {
    return { status: "ok" };
  }

  async close(): Promise<void> {
    // nothing to release
  }
}
