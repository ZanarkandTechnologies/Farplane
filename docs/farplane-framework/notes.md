---
title: "Thread Notes"
status: active
owner: farplane-framework
created_at: 2026-10-06
updated_at: 2026-10-06
tags:
  - farplane
  - notes
  - memory
refs:
  - runtimes/AGENTS.md
  - install.sh
  - docs/farplane-framework/project-files.md
  - docs/systems/wiki.md
---

# Thread Notes

Notes let one thread hand its research to another without redoing the work.
They are plain Markdown in one local-only git repo, found with `rg`. There is
no index, schema, database, or projection.

```text
~/.farplane/notes/                  local git repo, no remote, pre-push guard
  README.md
  2026-10-06-<slug>.md              useful to any project
  projects/<project>/2026-10-06-<slug>.md
```

## When To Use Notes

| Knowledge | Owner |
| --- | --- |
| Scoped research one thread found and another thread would reuse | Notes |
| Ingested source data about people, companies, and other entities | [Wiki](../systems/wiki.md) through `manage-wiki` |
| Task state, decisions, and proof for one piece of work | The active ticket |
| Durable project invariants worth retrieving outside their owner | `docs/MEMORY.md` |
| Who the operator is and what they are focused on | `~/.farplane/USER.md` |

## Contract

- One file per finding, named `YYYY-MM-DD-<slug>.md`, with `title` and a
  one-line `summary` in front matter. Put the finding first, then sources.
- Project-scoped notes go under `projects/<project>/`, where `<project>` is the
  project folder name. Everything else goes at the top level.
- Before researching, search the notes: `rg -il "<topic>" ~/.farplane/notes`.
- After writing or changing a note, commit it in the notes repo:
  `git -C ~/.farplane/notes add -A && git -C ~/.farplane/notes commit -m "note: <slug>"`.
- Correct a wrong note in place; git keeps the old version.
- Never add a remote. Notes may hold client names, strategy, and private
  research, so they stay on this machine. The repo sits outside every
  pushable checkout, and its `pre-push` hook refuses any push.

## Setup

`farplane install` creates the repo if it is missing and keeps the `pre-push`
guard in place on every install. It never touches existing notes.

The folder also opens as an Obsidian vault; `.obsidian/workspace*.json` is
gitignored. A later pass may add `[[Name]]` links for named entities so the
vault graph and backlinks work; notes do not depend on it.
