# Farplane AGENTS.md

This file is the project-local context for developing Farplane itself. It is a
routing kernel. The global Codex contract is
[templates/global/AGENTS.md](templates/global/AGENTS.md).
Keep this file navigational: a rule belongs here only when every Farplane task
needs it before a ticket, skill, or owner document can take over.

## Operating model

- Farplane is a harness built from visible tickets, skills, docs, bounded
  subagents, and small deterministic control points. Prefer those surfaces to
  hidden orchestration.
- The active ticket is the task contract, scope boundary, proof scoreboard, and
  handoff. Do not keep durable state only in chat.
- For material work, a Goal Packet adds `program.md` for loop policy,
  `progress.md` for observations, and `artifacts/` for proof. `ticket.md`
  remains the executable contract.
- A direct `impl` on a ready material ticket authorizes `goal-advisor` execution
  unless required inputs, an approval gate, or destructive/external side effects
  block. Keep ticket body and metadata current. Material completion requires its
  `Done / Proof`, QA/reviewer receipts, and the `farplane ticket finalize
  TASK-XXXX` close route. Compare ticket, program, and progress at material
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
- Before changing this file or `templates/global/AGENTS.md`, apply
  `docs/templates/global-agents-qa-checklist.md`. Preserve a concrete
  before/after/example and name the destination of removed behavior.
- Put reusable procedure in its skill, task-local decisions and proof in the
  ticket, cross-surface policy in its canonical doc, and deterministic checks
  in validators. Link to an owner; do not copy its contract here.
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
- Credentialed commands run through `farplane run -- <command>` or
  `doppler run -- <command>`. `farplane doctor` reports readiness and
  `farplane install` owns safe render/link/repair work.
- Farplane is local Codex orchestration. Do not add a daemon, hosted control
  plane, scheduler, or per-ticket runtime without a ticketed need.

## Durable truth

- `tickets/` holds active task state, proof, blockers, and archived tickets.
- `docs/HISTORY.md` records meaningful milestones and migrations.
- `docs/MEMORY.md` holds current project invariants that are worth retrieving
  outside their owner surface.
- Prefer `.farplane/` for live runtime state. It also holds generated state.
- `docs/` holds current contracts and references; stale content is folded into
  its owner or deleted rather than preserved as live guidance.

## Map

- `README.md` — product entry points and setup.
- `ARCHITECTURE.md` — system boundaries and canonical workflow map.
- `tickets/` — task contracts and proof.
- `skills/` — progressively loaded workflows and their local references.
- `docs/features/` and `docs/systems/` — capability and system contracts.
- `bin/` — live CLI, runtime, and shared validators.
- `templates/global/` — install-time global Codex contract.

## Stop and surface a decision

- scope or interface contract conflicts;
- migration has no safe rollback;
- a circular dependency appears; or
- the required owner surface cannot be identified.

Do not silently create architectural drift.
