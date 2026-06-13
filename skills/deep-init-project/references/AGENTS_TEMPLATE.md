# Project AGENTS.md (Template)

This file is loaded every loop. Keep it operational and project-specific.

## Build & Run

- Install: `[your command]`
- Dev: `[authoritative app-only command from PROJECT_RULES.md]`
- QA path: `[authoritative QA or evidence command from PROJECT_RULES.md]`

## Validation (Backpressure)

- Tests: `[your command]`
- Typecheck: `[your command]`
- Lint: `[your command]`
- Build: `[your command]`

## Docs State

- Architecture: `ARCHITECTURE.md`
- PRD: `docs/prd.md`
- Specs index: `docs/specs/README.md`
- Specs: `docs/specs/*`
- History: `docs/HISTORY.md`
- Memory: `docs/MEMORY.md`
- Troubles: `docs/TROUBLES.md`
- Lessons: `docs/LESSONS.md`
- Taste: `docs/TASTE.md`
- Code review: `docs/code_review.md` and `docs/review-agent.md`
- Tickets: active `tickets/TASK-*/ticket.md`, completed `tickets/archive/TASK-*/ticket.md`

## Project Lifecycle

Work flows through:
`bootstrap -> deep interview -> PRD -> ticket breakdown -> per-ticket plan -> implementation -> proof/review -> closeout`.

- Use `docs/bootstrap-brief.md` for project profile, lifecycle route,
  prototype gates, and pipeline handoff.
- Use `docs/prd.md` for requirements, first SLC slice, constraints, and
  autonomy readiness.
- Use active `tickets/TASK-*/ticket.md` files as the work objects.
- Plan each ticket before build; prove and review before closeout.
- Technical commands, stack rules, runtime, and QA paths live in
  `PROJECT_RULES.md`.

## Context First (Always)

- Read relevant specs/PRD before proposing edits.
- Before code edits, read `PROJECT_RULES.md`; do not rely on this file to
  carry every technical rule.
- Read nearest module `README.md` + `AGENTS.md`.
- Search for existing patterns and inspect related files.
- Identify affected interfaces first.
- No blind edits.

## Always-On Code Rules

- New non-obvious logic files need a concise top-of-file orientation comment
  that names ownership, inputs/outputs, side effects, and key invariants.
- Keep helpers module-local until a second real caller exists; avoid catch-all
  `utils.ts` files for domain behavior.
- New source files over 500 raw lines need a ticket note or split plan; do not
  add unrelated responsibility to existing oversized files.
- For UI-bearing changes, capture browser evidence and check the relevant
  `qa/` cookbook instead of relying only on compile/build.
- Use `PROJECT_RULES.md` for exact technical standards, commands, shared
  utility placement, and review policy.

## Code Ownership Defaults

- Follow the project's language, style, and quality gates in
  `PROJECT_RULES.md`.
- For TypeScript projects, prefer strict types, no `any`, explicit exported API
  return types, and tests colocated when practical.
- Prefer modular, feature-owned files over catch-all helpers.
- Keep root entrypoints focused; push detailed workflow logic into owning
  modules.
- Keep local helpers near the owning feature; promote them to the shared utility
  surface in `PROJECT_RULES.md` only after real reuse appears.
- When code grows custom behavior, state, or variants, extract the owning
  feature/module instead of growing one oversized file.

## First-Principles Planning

Before specs, tickets, or implementation plans, reduce the work to: objective,
user/system need, constraints, assumptions, root cause, smallest valuable
slice, proof/falsification, tradeoffs, and non-goals.

## Operating Modes

- Discovery mode: use `brainstorm` for options and `deep-interview` for ambiguity-gated clarification before PRD/spec writing.
- Planning mode: create/refresh plan first; get confirmation before implementation.
- Build mode: execute approved plan, then test/review.

## Delegation Guardrails

- Use specialized QA delegation only when corresponding surface changed.
- Docs/markdown/rule-text-only changes: `visual-qa` is not needed.
- If delegating, include one-line reason and expected artifact.

## Prototype-First Delivery

- Start smallest possible slice first.
- Ramp intentionally: `1 -> 10 -> 100`.
- Use dry-runs/checkpoints for risky or stateful operations.

## Notes

- Don’t assume not implemented: search first.
- Prefer local patterns, then docs, then external examples.
- Before adding new helper logic, search for existing shared utilities and
  follow the utility-placement rule in `PROJECT_RULES.md`.
- Before launching the app for QA or evidence capture, read `PROJECT_RULES.md`
  and the relevant `qa/` cookbook page instead of guessing commands or ports.
- If the same helper logic is appearing across multiple modules, extract it to
  the approved shared utility surface instead of copying it again.
- Update ticket status, phase, blockers, and spawned follow-ups in the ticket file as work progresses. When a ticket is complete and its writeback is done, move it into `tickets/archive/`.
- If the same failure or user correction happens more than once, append a short raw entry to `docs/TROUBLES.md` with the miss, correction, and prevention idea.
- If that raw entry produces a reusable prompt, skill, eval, or policy improvement, distill it into `docs/LESSONS.md`.
- During weekly learning drains, read recent `docs/TROUBLES.md` and
  `docs/LESSONS.md`, route actionable rows to the owning optimizer workflow,
  ticket, eval, or skill update, and record processed rows in runtime state
  rather than deleting ledger history.
