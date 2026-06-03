// Tests for SyntheticBridge — the deterministic toy-world fixture.
// Covers every affordance branch, the rejection paths, schema conformance, and
// dual-control (operatorAct mutating the shared world the agent then perceives).

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import Ajv2020 from "ajv/dist/2020.js";
import { SyntheticBridge } from "./synthetic-bridge";

const here = dirname(fileURLToPath(import.meta.url));
const schema = (name: string): object =>
  JSON.parse(readFileSync(join(here, "schema", name), "utf8")) as object;

const ajv = new Ajv2020({ strict: true, allErrors: true });
const validatePerception = ajv.compile(schema("perception.schema.json"));
const validateActionResult = ajv.compile(schema("action-result.schema.json"));

test("observe() conforms to the canonical schema and is deterministic", async () => {
  const world = new SyntheticBridge();
  const p = await world.observe();
  assert.ok(validatePerception(p), ajv.errorsText(validatePerception.errors));
  assert.equal(p.substrate, "synthetic");
  assert.equal(p.observedAt, 0); // logical clock starts at 0
  assert.equal(p.affordances.length, 4);
  assert.deepEqual(p.state, { tick: 0, place: "meadow", energy: 100, gathered: 0 });
});

test("each affordance mutates state as expected; results validate", async () => {
  const world = new SyntheticBridge();

  const move = await world.act({ affordance: "move", reason: "what is over there?" });
  assert.ok(validateActionResult(move), ajv.errorsText(validateActionResult.errors));
  assert.equal(move.status, "ok");
  let s = (await world.observe()).state;
  assert.equal(s.place, "stream");
  assert.equal(s.energy, 95);
  assert.equal(s.tick, 1);

  await world.act({ affordance: "gather" });
  s = (await world.observe()).state;
  assert.equal(s.gathered, 1);
  assert.equal(s.energy, 85);
  assert.equal(s.tick, 2);

  await world.act({ affordance: "rest" });
  s = (await world.observe()).state;
  assert.equal(s.energy, 100); // capped at 100
  assert.equal(s.tick, 3);

  await world.act({ affordance: "look" });
  s = (await world.observe()).state;
  assert.equal(s.tick, 4); // look advances only the clock
  assert.equal(s.energy, 100);
});

test("move wraps around the ring of places", async () => {
  const world = new SyntheticBridge();
  for (let i = 0; i < 4; i++) await world.act({ affordance: "move" });
  assert.equal((await world.observe()).state.place, "meadow");
});

test("gather is rejected when energy is exhausted, leaving state unchanged", async () => {
  const world = new SyntheticBridge({ energy: 0 });
  const r = await world.act({ affordance: "gather" });
  assert.equal(r.status, "rejected");
  assert.match(r.detail ?? "", /tired/);
  const s = (await world.observe()).state;
  assert.equal(s.gathered, 0);
  assert.equal(s.tick, 0);
});

test("an unknown affordance is rejected", async () => {
  const world = new SyntheticBridge();
  const r = await world.act({ affordance: "teleport" });
  assert.equal(r.status, "rejected");
  assert.match(r.detail ?? "", /unknown affordance: teleport/);
});

test("operatorAct mutates the shared world — dual-control (agent perceives a change it didn't cause)", async () => {
  const world = new SyntheticBridge();
  const before = (await world.observe()).state;

  const r = world.operatorAct("gather");
  assert.equal(r.status, "ok");

  const after = (await world.observe()).state;
  assert.equal(after.gathered, before.gathered + 1);
  assert.equal(after.tick, before.tick + 1);
});

test("close() resolves", async () => {
  await assert.doesNotReject(() => new SyntheticBridge().close());
});
