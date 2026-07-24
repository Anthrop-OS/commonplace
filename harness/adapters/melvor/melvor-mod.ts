// melvor-mod.ts — the mod glue: binds Melvor's in-process `game` global to the
// MelvorGameApi port that MelvorBridge consumes. This is the one place that
// names concrete game members, so all game-coupling (and its integration risk)
// lives here, isolated from the bridge logic.
//
// CLEAN-ROOM (AGENTS.md rule 4 · ADR-0003): the interfaces below declare only
// the *shape* of the small surface we touch — they are not copied from Melvor's
// source, and the game body is never vendored. Field/method names are confirmed
// against the live `game` object at integration time (the implementer runs a
// real Melvor + its mod toolchain; see issue #25 preconditions). Keeping the
// dependency this thin means a name change touches only this file.

import { MelvorBridge } from "./melvor-bridge";
import type { MelvorGameApi, MelvorSkillView } from "./melvor-bridge";

/** A skill object as exposed on the in-process `game`. Reads only, except `start`. */
export interface MelvorSkillObject {
  /** Namespaced id, e.g. "melvorD:Woodcutting". */
  readonly id: string;
  readonly name: string;
  readonly level: number;
  readonly xp: number;
  /**
   * The mod's start hook for this skill. Melvor has no single uniform "start a
   * skill" entrypoint — each skill begins differently (Woodcutting selects a
   * tree, Mining a rock, Fishing an area, …). The mod wires this per skill at
   * integration; an unwired skill leaves `start` absent and startSkill() reports
   * `rejected` rather than guessing. Returns false if the game itself refused
   * (e.g. level/requirement unmet).
   */
  start?: () => boolean;
}

/** The active action, when one is running. */
export interface MelvorActiveAction {
  readonly id: string;
  /** Halt this action. Present on Melvor's skill/action objects. */
  stop(): void;
}

/** The subset of the Melvor `game` global this adapter binds to. */
export interface MelvorGlobal {
  readonly skills: { readonly allObjects: readonly MelvorSkillObject[] };
  /** Currently active action, or null when the avatar is idle. */
  readonly activeAction: MelvorActiveAction | null;
}

/** Adapt the real `game` global to the port the bridge consumes. */
export function bindMelvorGlobal(game: MelvorGlobal): MelvorGameApi {
  const view = (s: MelvorSkillObject): MelvorSkillView => ({
    id: s.id,
    name: s.name,
    level: s.level,
    xp: s.xp,
  });
  return {
    listSkills: () => game.skills.allObjects.map(view),
    activeActionId: () => game.activeAction?.id ?? null,
    startSkill: (skillId) => {
      const skill = game.skills.allObjects.find((s) => s.id === skillId);
      if (!skill || !skill.start) return false;
      return skill.start();
    },
    stopActive: () => {
      game.activeAction?.stop();
    },
  };
}

/**
 * Mod entrypoint: build a MelvorBridge from the page's `game` global. Call this
 * from the loaded mod, where `game` is in scope. Throws off-page (e.g. in a
 * plain Node process) where no game exists — the adapter only works in-process.
 */
export function createMelvorBridge(): MelvorBridge {
  const g = (globalThis as { game?: MelvorGlobal }).game;
  if (!g) {
    throw new Error(
      "Melvor `game` global not found — load this adapter as a Melvor mod, in-page.",
    );
  }
  return new MelvorBridge(bindMelvorGlobal(g));
}
