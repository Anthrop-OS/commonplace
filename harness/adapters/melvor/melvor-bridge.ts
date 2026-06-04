// MelvorBridge — a Bridge<MelvorState> over a running Melvor Idle instance.
// Mirrors the structure of bridge/synthetic-bridge.ts (the worked reference):
// observe() snapshots the world, act() applies one affordance via a private
// switch. The difference is the world is *external* — a live game — so instead
// of owning in-memory state, the bridge holds a reference to the game and reads
// through it on every observe().
//
// ── Act path: mod API (in-process), NOT CDP / headless-Chromium ───────────────
// This is already decided at the architectural level by ADR-0006 (polyglot:
// TypeScript harness, Python cognition), which chose the TS harness *precisely
// so the adapter can read the `game` global in-process* and rejected the
// single-language-Python alternative because it "forces the Melvor adapter
// through Playwright / CDP `eval`, making `Perception` extraction from the
// `game` global slower and more brittle than an in-process mod." So no new ADR
// is filed here — this comment records the act-path choice the ADR already made:
//
//   - In-process mod: direct property reads off `game` (no serialization, no
//     round-trip), synchronous control calls, and the richest perception — the
//     whole object graph is in scope. This is the path.
//   - CDP / headless-Chromium: every read is a `Runtime.evaluate` round-trip
//     returning a serialized snapshot; deep/cyclic game objects serialize
//     poorly and each observe() pays latency. Rejected for perception. (CDP/
//     OpenClaw remains a candidate for the *operator gateway*, an orthogonal
//     concern — see exploration/prior-art-l2-l3.md.)
//
// ── Runtime (ElizaOS / OpenClaw / Hermes) is NOT chosen here ──────────────────
// T2 is just an adapter implementing the Bridge contract; it does not need the
// L2 runtime selected. The lean (ElizaOS-core + OpenClaw-gateway + Hermes-
// fallback, exploration/prior-art-l2-l3.md) is committed via its own ADR when
// the loop needs it — deferred to T5 per issue #25.
//
// ── Shared-avatar concurrency (SURFACED, not solved) ──────────────────────────
// Melvor is single-avatar: there is exactly one active action on one save. If
// the operator and the agent both drive the same instance, their act() calls
// race on that single slot — start-skill is last-writer-wins, and the agent's
// next observe() will report an activeActionId it did not set (a change it
// didn't cause). This bridge does NOT arbitrate that: there is no lock, no
// turn-taking, no operator/agent identity on Action. Per ADR-0007 the dyad's
// operator-acts-in-world half is staged to Stardew (P1), whose native co-op
// gives separate avatars in one world and sidesteps this shared-avatar race
// entirely. On Melvor (P0) we only prove the agent-side loop. SyntheticBridge
// .operatorAct() is where dual-control is exercised deterministically meanwhile.
//
// ── IP boundary (AGENTS.md rule 4 · ADR-0003) ─────────────────────────────────
// Mod/bridge code only — the Melvor game body is never vendored. The types in
// melvor-mod.ts declare only the *shape* of the small in-process surface we
// bind to (clean-room), not Melvor's source.

import type { Bridge } from "../../bridge/bridge";
import type { Perception, ActionSpec } from "../../bridge/perception";
import type { Action, ActionResult } from "../../bridge/action";

/** One skill as seen by the agent. JSON-serializable, like any substrate state. */
export interface MelvorSkillView {
  /** Namespaced skill id, e.g. "melvorD:Woodcutting". */
  id: string;
  /** Display name, e.g. "Woodcutting". */
  name: string;
  level: number;
  xp: number;
}

/** Melvor's world snapshot — the typed `state` inside a Perception. */
export interface MelvorState {
  /** Id of the currently active action, or null if the avatar is idle. */
  activeActionId: string | null;
  /** Every skill, with its current level and xp. */
  skills: MelvorSkillView[];
}

/**
 * The minimal control+read surface the bridge needs from Melvor, implemented by
 * the mod over the in-process `game` global (see `bindMelvorGlobal` in
 * melvor-mod.ts). Stated as a port so the bridge logic is unit-testable with a
 * fake, and the brittle game-coupling is confined to one documented place.
 */
export interface MelvorGameApi {
  /** Snapshot every skill. */
  listSkills(): MelvorSkillView[];
  /** Id of the active action, or null when idle. */
  activeActionId(): string | null;
  /** Begin training a skill; false if the game refused (unknown / not wired / reqs unmet). */
  startSkill(skillId: string): boolean;
  /** Stop whatever is active; a no-op when already idle. */
  stopActive(): void;
}

const TRAIN_PREFIX = "train:";

export class MelvorBridge implements Bridge<MelvorState> {
  constructor(private readonly game: MelvorGameApi) {}

  async observe(): Promise<Perception<MelvorState>> {
    const skills = this.game.listSkills();
    const affordances: ActionSpec[] = [
      // One "train this skill" affordance per skill — the menu the autotelic
      // selector chooses from. The target skill is encoded in the id so an
      // Action needs no params (mirrors the bare-id affordances in synthetic).
      ...skills.map((s) => ({ id: `${TRAIN_PREFIX}${s.id}`, label: `Train ${s.name}` })),
      { id: "stop", label: "Stop the active action" },
    ];
    return {
      substrate: "melvor",
      // Melvor is real-time (unlike the synthetic fixture's logical tick), so
      // observedAt is the wall clock — an epoch-ms integer per the schema.
      observedAt: Date.now(),
      state: { activeActionId: this.game.activeActionId(), skills },
      affordances,
    };
  }

  async act(action: Action): Promise<ActionResult> {
    const { affordance } = action;
    if (affordance === "stop") {
      this.game.stopActive();
      return { status: "ok" };
    }
    if (affordance.startsWith(TRAIN_PREFIX)) {
      const skillId = affordance.slice(TRAIN_PREFIX.length);
      return this.game.startSkill(skillId)
        ? { status: "ok" }
        : { status: "rejected", detail: `cannot start skill: ${skillId}` };
    }
    return { status: "rejected", detail: `unknown affordance: ${affordance}` };
  }

  async close(): Promise<void> {
    // In-process: nothing to release (the mod shares the page's lifetime).
  }
}
