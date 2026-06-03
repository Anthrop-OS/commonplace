// Smoke test for the bridge contract.
// The point of T1: NullBridge's output validates against the CANONICAL JSON
// SCHEMA, not just against the TS types — proving the contract is language-
// neutral (ADR-0006), which is what lets the Python cognition layer bind to the
// same wire shape later (T4).

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import Ajv2020 from "ajv/dist/2020.js";
import { NullBridge } from "./null-bridge";

const here = dirname(fileURLToPath(import.meta.url));
const schema = (name: string): object =>
  JSON.parse(readFileSync(join(here, "schema", name), "utf8")) as object;

const ajv = new Ajv2020({ strict: true, allErrors: true });
const validatePerception = ajv.compile(schema("perception.schema.json"));
const validateAction = ajv.compile(schema("action.schema.json"));
const validateActionResult = ajv.compile(schema("action-result.schema.json"));

test("NullBridge.observe() conforms to the canonical Perception schema", async () => {
  const p = await new NullBridge().observe();
  assert.ok(
    validatePerception(p),
    ajv.errorsText(validatePerception.errors),
  );
  assert.equal(p.substrate, "null");
  assert.ok(Array.isArray(p.affordances));
});

test("act() accepts an offered affordance (with an autotelic reason) and returns ok", async () => {
  const bridge = new NullBridge();
  const p = await bridge.observe();
  const first = p.affordances[0];
  assert.ok(first, "NullBridge should offer at least one affordance");

  const action = {
    affordance: first.id,
    reason: "what happens if I do nothing?",
  };
  assert.ok(validateAction(action), ajv.errorsText(validateAction.errors));

  const result = await bridge.act(action);
  assert.ok(
    validateActionResult(result),
    ajv.errorsText(validateActionResult.errors),
  );
  assert.equal(result.status, "ok");
});

test("the schema rejects a Perception missing required fields", () => {
  assert.equal(validatePerception({ substrate: "null" }), false);
});

test("the schema rejects an Action with an unknown field", () => {
  assert.equal(
    validateAction({ affordance: "noop", payoff: 10 }),
    false,
    "additionalProperties:false should reject a reward-shaped field like 'payoff'",
  );
});

test("close() resolves (full Bridge surface is exercised)", async () => {
  const bridge = new NullBridge();
  await assert.doesNotReject(() => bridge.close());
});
