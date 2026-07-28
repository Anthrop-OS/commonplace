# logbook pipeline (T3)

Writer/reader for logbook entries — the **mechanism** of the record's capture
layer. It validates against [`../schema/entry.schema.yaml`](../schema/entry.schema.yaml),
routes by visibility tier, enforces the redaction gate, and offers a
transport-not-brain salient-push hook.

It provides the mechanism only. *What* to write and *what is salient* are the
drive layer's judgment (T4/T5), never this package's.

## Language

Python. The pipeline touches the **private record**, so it runs on a local model
host at runtime (AGENTS.md rule 6) and co-locates with the Python L3 cognition
layer (ADR-0006). The TypeScript harness (L2) stays on the world-facing side of
the JSON bridge seam; this is the record-facing side.

## Discipline this enforces

- **Visibility tiers** (AGENTS.md rule 3): every entry defaults to `private`.
  The writer **refuses** to emit a `shareable`/`narrative` entry without
  `redaction_checked: true` — a publication gate, raised as
  `RedactionRequiredError`. Validation and the gate are separate: a `shareable`
  entry with the flag unset is *well formed* but *not emittable*.
- **The record never enters this repo** (AGENTS.md rule 2 / ADR-0005). The store
  roots **outside** the working tree by default (`~/.commonplace/logbook`), so a
  stray entry can never be committed. The test suite asserts the repo tree holds
  no `*.entry.md`.
- **Transport, not brain** (`exploration/gateway-selection.md`): the salient-push
  sinks carry an already-chosen entry to the operator's channel; they contain no
  salience logic, LLM call, or filtering.

## Layout

```
src/commonplace_logbook/
  schema.py    parse entry.schema.yaml (a small DSL) into a typed SchemaSpec
  entry.py     Entry model + markdown frontmatter parse/serialize
  validate.py  structural validation; applies schema defaults
  store.py     visibility-tier -> on-disk path (env-overridable, out-of-repo)
  writer.py    validate -> redaction gate -> tier-routed write
  reader.py    read/loads an entry, validating against the schema
  salient.py   transport-not-brain push sinks (AstrBot / Discord / Null)
  cli.py       validate / route / emit
```

## Usage

```python
from commonplace_logbook import read_entry, write_entry, Entry, salient_push

entry = read_entry("note.entry.md")        # parse + validate
result = write_entry(entry)                  # validate, gate, route by tier
salient_push(entry, note="felt worth saying")  # only if the agent judged it salient
```

CLI:

```sh
commonplace-logbook validate note.entry.md   # schema check
commonplace-logbook route    note.entry.md   # show tier + target path (no write)
commonplace-logbook emit     note.entry.md   # validate, gate, write to the store
```

## Configuration (env)

| Variable | Purpose | Default |
|---|---|---|
| `COMMONPLACE_LOGBOOK_HOME` | store root for all tiers | `~/.commonplace/logbook` |
| `COMMONPLACE_OBSIDIAN_VAULT` | if set, `private` entries route here | unset |
| `COMMONPLACE_LOGBOOK_SCHEMA` | override the schema path | in-tree `../schema` |
| `COMMONPLACE_ASTRBOT_ENDPOINT` / `_TARGET` / `_TOKEN` | AstrBot push channel | unset |
| `COMMONPLACE_DISCORD_WEBHOOK` | thin Discord-webhook fallback channel | unset |

With no channel configured, the push hook resolves to a `NullSink` (no network),
so it is safe to call unconditionally.

## Develop

```sh
pip install -e ".[dev]"
pytest --cov --cov-report=term-missing   # 100% pipeline surface, mirrors logbook-ci
```
