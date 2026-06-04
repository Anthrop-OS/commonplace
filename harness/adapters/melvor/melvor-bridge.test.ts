// Tests for the Melvor adapter. Melvor itself is never loaded — a fake stands in
// for the in-process `game` global (issue #25: "tests as feasible — mock the
// game object"). Covers schema conformance, ≥1 real skill action through to a
// changed Perception, every rejection path, the mod glue binder, and the
// entrypoint's game-present / game-absent branches.

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import Ajv2020 from "ajv/dist/2020.js";
import { MelvorBridge } from "./melvor-bridge";
import { bindMelvorGlobal, createMelvorBridge } from "./melvor-mod";
import type { MelvorGlobal, MelvorSkillObject, MelvorActiveAction } from "./melvor-mod";

const here = dirname(fileURLToPath(import.meta.url));
const schema = (name: string): object =>
  JSON.parse(readFileSync(join(here, "..", "..", "bridge", "schema", name), "utf8")) as object;

const ajv = new Ajv2020({ strict: true, allErrors: true });
const validatePerception = ajv.compile(schema("perception.schema.json"));
const validateActionResult = ajv.compile(schema("action-result.schema.json"));

// A minimal fake of the in-process `game` global: one wired skill (Woodcutting,
// has a start hook) and one unwired skill (Fishing, no start hook). Starting
// Woodcutting sets the active action; stopping it clears it.
function makeFakeGame(): MelvorGlobal {
  let active: MelvorActiveAction | null = null;
  const woodcutting: MelvorSkillObject = {
    id: "melvorD:Woodcutting",
    name: "Woodcutting",
    level: 1,
    xp: 0,
    start: () => {
      active = { id: "melvorD:Woodcutting", stop: () => (active = null) };
      return true;
    },
  };
  const fishing: MelvorSkillObject = {
    id: "melvorD:Fishing",
    name: "Fishing",
    level: 1,
    xp: 0,
    // intentionally no start hook — an "unwired" skill
  };
  const skills = [woodcutting, fishing];
  return {
    skills: {
      get allObjects() {
        return skills;
      },
    },
    get activeAction() {
      return active;
    },
  };
}

test("observe() returns a populated Perception that conforms to the canonical schema", async () => {
  const bridge = new MelvorBridge(bindMelvorGlobal(makeFakeGame()));
  const p = await bridge.observe();

  assert.ok(validatePerception(p), ajv.errorsText(validatePerception.errors));
  assert.equal(p.substrate, "melvor");
  assert.ok(Number.isInteger(p.observedAt) && p.observedAt >= 0);
  assert.equal(p.state.activeActionId, null); // idle to start
  assert.deepEqual(
    p.state.skills.map((s) => s.id),
    ["melvorD:Woodcutting", "melvorD:Fishing"],
  );
  // one "train:" affordance per skill, plus the stop affordance
  assert.equal(p.affordances.length, 3);
  assert.deepEqual(
    p.affordances.map((a) => a.id),
    ["train:melvorD:Woodcutting", "train:melvorD:Fishing", "stop"],
  );
});

test("act() performs a skill action and the next observe() reflects it", async () => {
  const bridge = new MelvorBridge(bindMelvorGlobal(makeFakeGame()));

  const r = await bridge.act({
    affordance: "train:melvorD:Woodcutting",
    reason: "what does it feel like to gather wood rather than grind?",
  });
  assert.ok(validateActionResult(r), ajv.errorsText(validateActionResult.errors));
  assert.equal(r.status, "ok");
  assert.equal((await bridge.observe()).state.activeActionId, "melvorD:Woodcutting");

  const stop = await bridge.act({ affordance: "stop" });
  assert.equal(stop.status, "ok");
  assert.equal((await bridge.observe()).state.activeActionId, null);
});

test("stop on an idle world is an accepted no-op", async () => {
  const bridge = new MelvorBridge(bindMelvorGlobal(makeFakeGame()));
  const r = await bridge.act({ affordance: "stop" });
  assert.equal(r.status, "ok");
  assert.equal((await bridge.observe()).state.activeActionId, null);
});

test("training an unwired skill is rejected, leaving the world idle", async () => {
  const bridge = new MelvorBridge(bindMelvorGlobal(makeFakeGame()));
  const r = await bridge.act({ affordance: "train:melvorD:Fishing" });
  assert.equal(r.status, "rejected");
  assert.match(r.detail ?? "", /cannot start skill: melvorD:Fishing/);
  assert.equal((await bridge.observe()).state.activeActionId, null);
});

test("training an unknown skill id is rejected", async () => {
  const bridge = new MelvorBridge(bindMelvorGlobal(makeFakeGame()));
  const r = await bridge.act({ affordance: "train:melvorD:Nope" });
  assert.equal(r.status, "rejected");
  assert.match(r.detail ?? "", /cannot start skill: melvorD:Nope/);
});

test("an affordance the adapter does not recognize is rejected", async () => {
  const bridge = new MelvorBridge(bindMelvorGlobal(makeFakeGame()));
  const r = await bridge.act({ affordance: "teleport" });
  assert.equal(r.status, "rejected");
  assert.match(r.detail ?? "", /unknown affordance: teleport/);
});

test("bindMelvorGlobal reports the active action id when one is running", async () => {
  const game = makeFakeGame();
  const api = bindMelvorGlobal(game);
  assert.equal(api.activeActionId(), null);
  api.startSkill("melvorD:Woodcutting");
  assert.equal(api.activeActionId(), "melvorD:Woodcutting");
  api.stopActive();
  assert.equal(api.activeActionId(), null);
});

test("close() resolves", async () => {
  await assert.doesNotReject(() => new MelvorBridge(bindMelvorGlobal(makeFakeGame())).close());
});

test("createMelvorBridge builds a bridge from the page's game global", async () => {
  const slot = globalThis as { game?: MelvorGlobal };
  const prior = slot.game;
  try {
    slot.game = makeFakeGame();
    const bridge = createMelvorBridge();
    assert.ok(bridge instanceof MelvorBridge);
    assert.equal((await bridge.observe()).substrate, "melvor");
  } finally {
    if (prior === undefined) delete slot.game;
    else slot.game = prior;
  }
});

test("createMelvorBridge throws off-page where no game global exists", () => {
  const slot = globalThis as { game?: MelvorGlobal };
  const prior = slot.game;
  try {
    delete slot.game;
    assert.throws(() => createMelvorBridge(), /game` global not found/);
  } finally {
    if (prior !== undefined) slot.game = prior;
  }
});
