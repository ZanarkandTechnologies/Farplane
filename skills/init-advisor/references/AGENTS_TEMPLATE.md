# Project AGENTS.md (Template)

This file is loaded every loop. Keep it operational and project-specific. It is
the project's only rules file: stack, commands, runtime, QA paths, and
conventions live here, not in a second root rules file.

## Stack

- Framework: `[e.g., Next.js, FastAPI, Go]`
- Language: `[e.g., TypeScript, Python, Go]`
- Database: `[e.g., Convex, PostgreSQL, none]`
- Styling: `[e.g., Tailwind CSS, n/a]`
- Package manager: `[e.g., pnpm, uv]`

## Build & Run

- Install: `[your command]`
- Dev (authoritative app-only path): `[e.g., pnpm dev]`
- QA path (authoritative QA / evidence path): `[e.g., pnpm run dev:qa, docker compose up app db]`
- Stop or clean up the QA path: `[command or n/a]`
- Required local services: `[e.g., postgres, redis, none]`
- Expected targets / base URLs: `[e.g., http://127.0.0.1:3000]`
- Port / env contract: `[which vars may be overridden, such as PORT, DATABASE_URL]`
- Source of truth: `[if package scripts or compose files are authoritative, say so here instead of adding wrappers]`

## Validation (Backpressure)

- Tests: `[your command]`
- Typecheck: `[your command or n/a]`
- Lint: `[your command]`
- Build: `[your command or optional]`
- Pre-push gate: `bash scripts/pre_push_check.sh` (warn at `[500]` raw source
  lines, block at `[1000]`)
- Quality tools (record only adopted commands; `n/a` otherwise):
  - complexity `[cmd]`, duplication `[cmd]`, dependency boundaries `[cmd]`,
    dead code `[cmd]`, mutation testing `[cmd or high-budget only]`, static
    analysis dashboard `[SonarQube / Qlty / n/a]`;
  - SAST `[cmd]`, dependency audit `[cmd]`, secret scan `[cmd]`, config
    validation `[cmd]`, resilience/failure tests `[cmd]`.
  The `code-health` skill's clean and harden modes read these slots.

## Where Files Go

One home per job. A file with no row here belongs to the owner that writes or
reads it, not to a new top-level folder.

| Path | Holds | Git |
| --- | --- | --- |
| `AGENTS.md`, `ARCHITECTURE.md`, `README.md` | Rules, system map, setup | tracked |
| `[src/]` | Main source code | tracked |
| `[tests/]` | Test files | tracked |
| `[src/lib/]` | Shared utilities, once a second real caller exists | tracked |
| `docs/` | `prd.md`, `features/`, `systems/`, `HISTORY.md`, `MEMORY.md`, `TASTE.md`, review docs | tracked |
| `farplane/` | Committed Farplane config: harness, metrics, bindings, automations | tracked |
| `docs/qa/` | One page per long repeatable QA flow; created only when the first exists | tracked |
| `tickets/` | Ticket templates and the archive | tracked |
| `.farplane/` | Everything generated or private: runs, output, scratch, media | ignored |

- Never write output, downloads, or scratch to a new root folder (`output/`,
  `tmp/`, `<tool>_output/`). Use `.farplane/<owner>/`.
- A file that should never be committed lives under `.farplane/`, not behind an
  extra ignore rule elsewhere.
- Keep helpers local until reuse appears; extract when logic would otherwise be
  copied or makes a feature file too large.

## Docs State

- Architecture: `ARCHITECTURE.md`
- PRD: `docs/prd.md`
- Specs index: `docs/features/README.md`
- Specs: `docs/features/FEAT-*.md`
- History: `docs/HISTORY.md`
- Memory: `docs/MEMORY.md`
- Taste: `docs/TASTE.md`
- Code review: `docs/code_review.md` and `docs/review-agent.md`
- Tickets: active `tickets/TASK-*/ticket.md`, new closed-ticket locators in
  `tickets/archive-index.jsonl`, and legacy local archives in
  `tickets/archive/TASK-*/ticket.md`

## Project Lifecycle

Work flows through:
`bootstrap -> deep interview -> PRD -> ticket breakdown -> per-ticket plan -> implementation -> proof/review -> closeout`.

- Use `docs/bootstrap-brief.md` for project profile, lifecycle route,
  prototype gates, and pipeline handoff.
- Use `docs/prd.md` for requirements, first SLC slice, constraints, and
  autonomy readiness.
- Use active `tickets/TASK-*/ticket.md` files as the work objects.
- Plan each ticket before build; prove and review before closeout.

## Context First (Always)

- Read relevant specs/PRD before proposing edits.
- Read nearest module `README.md` + `AGENTS.md`.
- Search for existing patterns and inspect related files.
- Identify affected interfaces first.
- No blind edits.

## Always-On Code Rules

- Conventions: naming `[e.g., camelCase functions, PascalCase components]`,
  testing `[e.g., Vitest unit tests]`, docs `[e.g., JSDoc on public exports]`.
- New non-obvious logic files need a concise top-of-file orientation comment
  that names ownership, inputs/outputs, side effects, and key invariants.
- Keep helpers module-local until a second real caller exists; avoid catch-all
  `utils.ts` files for domain behavior.
- New source files over 500 raw lines need a ticket note or split plan; do not
  add unrelated responsibility to existing oversized files.
- For UI-bearing changes, capture browser evidence and check the relevant
  Agent QA entry below instead of relying only on compile/build.

## Code Ownership Defaults

- For TypeScript projects, prefer strict types, no `any`, explicit exported API
  return types, and tests colocated when practical.
- Prefer modular, feature-owned files over catch-all helpers.
- Keep root entrypoints focused; push detailed workflow logic into owning
  modules.
- When code grows custom behavior, state, or variants, extract the owning
  feature/module instead of growing one oversized file.
- Maintainability: use `code-health` clean mode for behavior-preserving cleanup
  after features; optimize changed or high-churn code first and keep behavior
  proof as the hard gate.
- Hardening: use `code-health` harden mode after major features for a risk map,
  mitigations, adversarial proof, and a residual-risk note.

## UI Baseline

- UI applies to this repo: `[yes/no]`; component system: `[default shadcn/ui;
  existing design system when present; n/a when no UI]`.
- UI-bearing app projects start on a shadcn-capable stack with the tweakcn
  darkmatter theme unless the user opts out, there is no UI, or an existing
  design system owns the theme:
  `pnpm dlx shadcn@latest add https://tweakcn.com/r/themes/darkmatter.json`.
  Skip reason when not applied: `[opt-out / no UI / existing system / throwaway static artifact]`.
- Plain HTML/CSS/JS does not satisfy this baseline unless the user asked for a
  static or throwaway artifact.
- Persistent explanatory chrome text becomes labels, tooltips, empty states, or
  progressive disclosure unless it is primary user content.
- UI-bearing tickets capture browser evidence and run visual QA against
  `docs/TASTE.md` (default-looking controls, text fit, responsive layout,
  over-explaining copy).

## Agent QA / Testability

- Short QA entry notes live in this section; a long repeatable flow gets
  `docs/qa/<flow>.md`. The shared method is the `qa` skill's guide.
- Stable browser regression tool: `[e.g., Playwright]`; interactive debugging:
  `[e.g., in-app Browser]`.
- Fast-entry helpers: `[deep links, seeded states, keyboard shortcuts, debug routes]`.
- State probes for complex UI: `[HUDs, DOM mirrors, overlays, event logs]`.
- Before launching the app for QA or evidence capture, use the Build & Run
  commands above and the entry notes here (or the matching `docs/qa/` page) instead of guessing
  commands or ports.

## Review Policy

- Material reviewer: the Farplane reviewer lane plus the TAS `review` skill, for
  material ticket completion, TAS-gated review, evidence bundles,
  prompt/skill/eval changes, and completion receipts.
- Local pre-push reviewer: `scripts/codex_review_agent.ts` gives an advisory
  diff review after local validators. Skip with `FARPLANE_SKIP_AGENT_REVIEW=1`;
  make it strict with `STRICT_AGENT_REVIEW=1`. Node projects need dev
  dependencies `@openai/codex-sdk`, `tsx` and scripts `review:agent`,
  `review:prepush`.
- Review artifacts: `tickets/TASK-XXXX/artifacts/review/` under the ticket
  being judged.

## First-Principles Planning

Before specs, tickets, or implementation plans, reduce the work to: objective,
user/system need, constraints, assumptions, root cause, smallest valuable
slice, proof/falsification, tradeoffs, and non-goals.

## Operating Modes

- Discovery mode: expand options inline and stop for ambiguity-gated operator clarification before PRD/spec writing.
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
  follow the shared-utility row in Where Files Go.
- If the same helper logic is appearing across multiple modules, extract it to
  the approved shared utility surface instead of copying it again.
- Update ticket status, phase, blockers, and spawned follow-ups in the ticket
  file as work progresses. When a ticket is complete and its writeback is done,
  run `farplane ticket finalize TASK-XXXX` with one `--media <path>` per
  selected file. Core creates or resumes, verifies, and
  closes the configured-repository issue before mining and cleanup; do not
  create the issue or move the packet into `tickets/archive/` manually.
- Route a repeated failure to the smallest owner: a skill, eval, validator,
  canonical doc, or ticket artifact. Promote only a durable project invariant
  to `docs/MEMORY.md`.
- During weekly skill hardening, inspect relevant ticket evidence and
  owner-local evals, then route actionable findings to `skill-maintenance`,
  `eval`, the owning optimizer workflow, or a ticket. Cap optimizer follow-ups
  per weekly run to avoid thread or ticket floods.
