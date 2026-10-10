# Farplane AGENTS.md

This file is the project-local context for developing Farplane itself. It is a
routing kernel. The global Codex contract is
[runtimes/AGENTS.md](runtimes/AGENTS.md).
Keep this file navigational: a rule belongs here only when every Farplane task
needs it before a ticket, skill, or owner document can take over.

## Operating model

- Farplane is a harness built from visible tickets, skills, docs, bounded
  subagents, and small deterministic control points. Prefer those surfaces to
  hidden orchestration.
- The active GitHub issue in the project's own repository is the task
  contract, scope boundary, proof scoreboard, and handoff; execution stays in
  Codex. The repository is public, so issues carry engineering facts only.
  Multica is archived read-only; don't read or write it. Follow
  `tickets/README.md` and do not keep durable state only in chat.
- For material work, the issue body holds Goal program policy and the current
  checkpoint; top-level comments hold append-only progress. Repository files
  hold structured designs and proof when useful, not a second writable task.
- A direct `impl` on a ready material ticket authorizes `goal-advisor` to compile
  the Goal Packet and native Goal prompt; native Goal executes the accepted scope
  unless required inputs, an approval gate, or destructive/external side effects
  block. Keep issue body and metadata current. Material completion requires its
  `Done / Proof`, QA/reviewer receipts, and `$close-ticket` updating the same
  GitHub issue without starting a run. Compare ticket, program, and progress at material
  continuations; use drift review when self-approval risk is high. Ticket
  lifecycle and thread mechanics stay in `tickets/README.md`.
- Every implementation ticket needs a compact Contract Diagram. UI tickets also
  need `design.md`; QA compares the operated result with that baseline.
- A workflow is not shipped until its `skills/<name>/` package and canonical
  inventory are present.
- Active Farplane surfaces use one current name and path. Do not retain aliases,
  shims, fallback parsers, or old commands without an explicit public-contract
  or migration need.
- Human-facing shortcuts are not implicit workflow dependencies; native phases
  own generic planning and execution, while skills own named work products.

## Context budget

```text
context_budget(task) -> request_or_ticket + owner_surface + local_proof_surface
```

Start with the request or active ticket, then load one owner and one nearby
implementation or proof surface:

- ticket work: `tickets/README.md` or the ticket template;
- skill work: that skill's `SKILL.md` and its nearby tests or checklist;
- code work: the owning module and its closest test;
- docs work: the canonical owner and the relevant reader-facing page;
- harness placement: `harness-engineering-doctrine.md` and the relevant
  registry; and
- install work: the touched installer or template and its validation path.

Load another file only to answer a named question the current set cannot answer.
Do not preload history or memory logs. Read `docs/HISTORY.md` or
`docs/MEMORY.md` only when the ticket, a source reference, or a known invariant
makes one relevant.

## Local boundaries

- Before proposing a new Farplane policy, skill, agent, hook, validator, or
  template, use `harness-advisor` to select the smallest owner surface. Root
  prompt text is the last lever, not the default.
- Before changing this file or `runtimes/AGENTS.md`, apply
  `docs/templates/global-agents-qa-checklist.md`. Preserve a concrete
  before/after/example and name the destination of removed behavior.
- Put reusable procedure in its skill, task-local decisions and proof in the
  ticket, cross-surface policy in its canonical doc, and deterministic checks
  in validators. Link to an owner; do not copy its contract here.
- Keep one executable entrypoint per lifecycle boundary. New harness workflow
  surfaces may own dedicated folders only under `skills/` or `hooks/`. For
  validators, migrations, CLI checks, and similar repository automation, prefer
  fewer scripts in the existing owner directory: add related checks as named
  functions behind the existing runner and one `main()` instead of creating a
  folder or executable file per check. Split reusable or domain-heavy logic into
  helper modules only when the runner remains the single public entrypoint.
- Browser/user-visible proof uses the project QA lane and ticket proof policy:
  use in-app Browser for public or unauthenticated browsing, reproducible browser
  extraction, and normal QA; use Chrome or Computer Use only when existing
  authenticated state (cookies, extensions, or native-app state) is required;
  use Playwright only for requested regression coverage or an existing suite.
- Architecture owns the complete system map. The README routes readers to it;
  do not maintain two independent canonical diagrams.
- Do not modify installed or external skills under `~/.codex/skills/` unless the
  operator explicitly requests that target. Change the repo-owned source and
  use its install or sync path.
- Stay in the operator-selected checkout. Do not silently create or switch
  worktrees. Native subagents share the checkout and require a single-writer
  boundary.
- The normal Farplane shared checkout is `main` only. Do not create or switch
  local branches. Serialize writers. Publishing means pushing `main` straight to
  `origin/main` through the project commit workflow; open a `codex/*` PR only
  when the operator asks for one.
- Credentialed commands run through `farplane run -- <command>` or
  `doppler run -- <command>`. `farplane doctor` reports readiness and
  `farplane install` owns safe render/link/repair work.
- Farplane is local Codex orchestration. Do not add a daemon, hosted control
  plane, scheduler, or per-ticket runtime without a ticketed need.

## Durable truth

- GitHub Issues hold active task state and blockers. `tickets/` retains local proof,
  migration snapshots, templates, and legacy records.
- `docs/HISTORY.md` records meaningful milestones and migrations.
- `docs/MEMORY.md` holds current project invariants that are worth retrieving
  outside their owner surface.
- Prefer `.farplane/` for live runtime state. It also holds generated output.
- `docs/` holds current contracts and references; stale content is folded into
  its owner or deleted rather than preserved as live guidance.

## Where files go

One home per job. If a file has no row here, it belongs to the owner that
writes or reads it (usually a skill), not a new top-level folder.

| Path | Holds | Git |
| --- | --- | --- |
| `AGENTS.md`, `ARCHITECTURE.md`, `README.md` | Project rules, system map, setup. No other root rules file. | tracked |
| `agents/`, `hooks/`, `skills/` | Shared harness sources; `hooks/hooks.json` is the one hook registration. | tracked |
| `config/` | Farplane's own settings files: skill groups and profiles, validation and git-gate checks, template registry. | tracked |
| `bin/` | CLI, runtime, validators; placement rules in `bin/AGENTS.md`. | tracked |
| `docs/` | Current contracts and references. | tracked |
| `runtimes/<name>/` | What one runtime (`codex`, `claude`) needs beyond the shared sources, e.g. Codex `default.rules`. | tracked |
| `runtimes/AGENTS.md` | Install-time global contract shared by both runtimes. | tracked |
| `farplane/` | This project's committed config only: harness, metrics, bindings, automations. Bunker strategy docs (`farplane/strategy/`) belong only in private business repos, never here. | tracked |
| `tickets/` | Issue templates and the frozen legacy archive. | tracked |
| `.agents/skills/` | Project-local skills (Codex convention). | tracked |
| `.farplane/` | Everything generated or private: runs, output, scratch, caches, media. | ignored |
| `.agent-office/` | The bunker's runtime state for this checkout (upstream agent-office's folder name; see Farplane-UI-v2 `docs/prd.md`). | excluded |

- Never write output, downloads, or scratch to a new root folder (`output/`,
  `tmp/`, `<tool>_output/`). Use `.farplane/<owner>/`, or the session
  scratchpad for throwaway files. A skill that writes files names its
  `.farplane/` subfolder.
- A file that should never be committed lives under `.farplane/`, not behind
  an extra ignore rule elsewhere. Keep `config.toml` local; version
  `runtimes/codex/config.toml.example`.
- Do not enable local git hooks or live automations unless the operator asks.
- Delete empty folders, `.DS_Store`, and stray caches when you see them.
- Checks: `python3 bin/validators/check_farplane_project_files.py`,
  `python3 bin/validators/check_harness_invariants.py`,
  `python3 bin/validators/check_doc_refs.py`, and
  `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
  Push mechanics live in `skills/commit/references/push-main.md`; PR mechanics,
  for requested PRs only, in `skills/commit/references/single-worktree-pr.md`.

## Stop and surface a decision

- scope or interface contract conflicts;
- migration has no safe rollback;
- a circular dependency appears; or
- the required owner surface cannot be identified.

Do not silently create architectural drift.
