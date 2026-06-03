// SyntheticBridge — a deterministic in-memory toy world. NOT a game: a test
// fixture / synthetic substrate for developing the loop (T3/T4/T5) and the drive
// layer before a real adapter exists, and for deterministically exercising
// dual-control (the operator acting on the shared world — the Stardew P1 model).
//
// Determinism: there is no wall clock and no RNG. `observedAt` is a logical tick,
// so a given sequence of actions always yields the same Perceptions — which is
// what makes it usable in CI and in assertions.

import type { Bridge } from "./bridge";
import type { Perception, ActionSpec } from "./perception";
import type { Action, ActionResult } from "./action";

/** The toy world's state. JSON-serializable, like any substrate's state. */
export interface SyntheticState {
  /** logical clock — advances by one per applied action */
  tick: number;
  /** current location (one of PLACES) */
  place: string;
  /** 0..100; falls on move/gather, rises on rest */
  energy: number;
  /** resources collected so far */
  gathered: number;
}

const PLACES = ["meadow", "stream", "grove", "ridge"] as const;

const AFFORDANCES: ActionSpec[] = [
  { id: "move", label: "move to the next place" },
  { id: "gather", label: "gather here" },
  { id: "rest", label: "rest" },
  { id: "look", label: "look around" },
];

export class SyntheticBridge implements Bridge<SyntheticState> {
  private state: SyntheticState;

  constructor(init?: Partial<SyntheticState>) {
    this.state = { tick: 0, place: PLACES[0], energy: 100, gathered: 0, ...init };
  }

  async observe(): Promise<Perception<SyntheticState>> {
    return {
      substrate: "synthetic",
      observedAt: this.state.tick,
      state: { ...this.state },
      affordances: AFFORDANCES.map((a) => ({ ...a })),
    };
  }

  /** The agent acts. */
  async act(action: Action): Promise<ActionResult> {
    return this.applyAffordance(action.affordance);
  }

  /**
   * Dual-control: the operator acts on the *same* world (the co-op model — two
   * actors, one world). The agent perceives the change on its next observe(),
   * having not caused it. Synchronous because the fixture has no transport.
   */
  operatorAct(affordance: string): ActionResult {
    return this.applyAffordance(affordance);
  }

  async close(): Promise<void> {
    // nothing to release
  }

  private applyAffordance(id: string): ActionResult {
    switch (id) {
      case "move": {
        const idx = Math.max(0, PLACES.indexOf(this.state.place as (typeof PLACES)[number]));
        this.state.place = PLACES[(idx + 1) % PLACES.length]!;
        this.state.energy = Math.max(0, this.state.energy - 5);
        this.state.tick++;
        return { status: "ok" };
      }
      case "gather": {
        if (this.state.energy <= 0) {
          return { status: "rejected", detail: "too tired to gather" };
        }
        this.state.gathered++;
        this.state.energy = Math.max(0, this.state.energy - 10);
        this.state.tick++;
        return { status: "ok" };
      }
      case "rest": {
        this.state.energy = Math.min(100, this.state.energy + 20);
        this.state.tick++;
        return { status: "ok" };
      }
      case "look": {
        this.state.tick++;
        return { status: "ok" };
      }
      default:
        return { status: "rejected", detail: `unknown affordance: ${id}` };
    }
  }
}
