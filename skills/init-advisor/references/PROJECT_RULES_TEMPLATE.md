# Project Rules: [Project Name]

This file defines the project-specific technical rules, tech stack, and conventions.

## 🛠 Tech Stack
- **Framework**: [e.g., Next.js, FastAPI, Go]
- **Language**: [e.g., TypeScript, Python, Go]
- **Database**: [e.g., Convex, PostgreSQL, MongoDB]
- **Styling**: [e.g., Tailwind CSS, CSS Modules]
- **Package Manager**: [e.g., pnpm, npm, poetry]

## 📁 Folder Structure
- `ARCHITECTURE.md`: Top-level system map and canonical surface guide
- `src/`: Main source code
- `tests/`: Test files
- `docs/`: Canonical project state (`prd.md`, `features/README.md`, `features/FEAT-*.md`, `HISTORY.md`, `MEMORY.md`, `TASTE.md`, `TROUBLES.md`, `LESSONS.md`)
- `tickets/`: Ticket board (`TASK-*/ticket.md`, `archive/`, `templates/`)
- `...`: [Other key directories]

## 📜 Conventions
- **Naming**: [e.g., camelCase for functions, PascalCase for components]
- **Testing**: [e.g., Use Vitest for unit tests]
- **Documentation**: [e.g., Use JSDoc for all public exports]

## 🤖 Agent Workflow
- Agent lifecycle and ticket workflow rules live in `AGENTS.md`.
- This file owns technical stack, commands, runtime, conventions, and QA paths.
- Project profile, lifecycle route, prototype gates, and pipeline handoff live
  in `docs/bootstrap-brief.md`.

## 🧠 Learning Backpropagation
- **Raw feedback log**: `docs/TROUBLES.md`
- **Distilled lesson log**: `docs/LESSONS.md`
- **Cadence**: weekly interval review of recent troubles, lessons, ticket
  progress, proof failures, and interval reports.
- **Backprop action**: route actionable rows through
  `skill-maintenance(mode: harden_skill)` or the owning optimizer workflow such
  as `optimize-harness`, a repair ticket, or an eval.
- **Processed state**: `.farplane/state/skill-maintenance/processed-learning.jsonl`
  or the project-equivalent runtime path.
- **Dedupe rule**: do not delete ledger rows from `docs/TROUBLES.md` or
  `docs/LESSONS.md`; mark rows processed in runtime state with source refs and
  follow-up ticket/thread refs.
- **Spawn cap**: cap optimizer follow-ups per weekly run to avoid thread or
  ticket floods.

## 🎨 Frontend UI Initialization
- **UI applies to this repo**: [yes/no]
- **Component system**: [default `shadcn/ui` for app UI; existing design system only when already present; n/a only when no UI]
- **Theme baseline**: For UI-bearing app projects, initialize a shadcn-capable
  stack and apply the default tweakcn darkmatter theme before building unless
  the user explicitly disables it, the project has no UI, or an existing
  stronger design system already owns the theme:
  `pnpm dlx shadcn@latest add https://tweakcn.com/r/themes/darkmatter.json`
- **Skip reason when not applied**: [explicit user opt-out / no UI / existing design system / static throwaway artifact only]
- **Plain HTML exception**: Plain HTML/CSS/JS is not the default for app UI and
  does not satisfy this baseline unless the user explicitly asked for a
  static/throwaway artifact.
- **Tooltip rule**: Persistent explanatory text in the app chrome should become
  labels, tooltips, empty states, or progressive disclosure unless it is primary
  user content.
- **Visual QA expectation**: UI-bearing tickets must capture browser evidence
  and run visual QA against `docs/TASTE.md`, including checks for default-looking
  controls, text fit, responsive layout, and over-explaining copy.

## 🧩 Shared Utilities
- **Preferred shared utility location**: [e.g., `src/utils/`, `packages/shared/`, domain-scoped `src/lib/`]
- **Extract when**: [e.g., logic is reused across modules, would otherwise be copied, or is making feature files too large]
- **Keep local when**: [e.g., helper is private to one module or tightly coupled to one feature]

## ✅ Pre-Push Policy
- **Warn on large source files**: [default `500` raw lines]
- **Block on oversized source files**: [default `1000` raw lines]
- **Required local commands**:
  - Lint: `[command]`
  - Typecheck: `[command or n/a]`
  - Tests: `[command]`
  - Build: `[command or optional]`
- **Optional heavy checks**:
  - Reviewer agent: `[review command or disabled]`

## 🧹 Maintainability / Refactoring
- **Smell score target**: optimize changed or high-churn code first, using
  complexity, nesting, duplication, coverage gaps, lint/static issues, boundary
  violations, and churn as prioritization signals rather than absolute goals.
- **Complexity command**: `[command or n/a; e.g., eslint complexity, oxlint, radon]`
- **Duplication command**: `[command or n/a; e.g., jscpd, PMD CPD]`
- **Dependency boundary command**: `[command or n/a; e.g., dependency-cruiser, madge]`
- **Dead code command**: `[command or n/a; e.g., knip, depcheck, vulture]`
- **Static analysis dashboard**: `[SonarQube/SonarCloud/Code Climate/Qlty/n/a]`
- **Mutation testing**: `[command or high-budget only / n/a]`
- **Agent workflow**: use the `refactoring` skill for behavior-preserving
  structure cleanup after features, and keep behavior proof as the hard gate.

## 🛡 Hardening
- **Risk model**: map trust boundaries, input abuse, authz, secrets/data,
  dependencies, availability, concurrency, observability, recovery, and unsafe
  configuration before patching.
- **SAST command**: `[command or n/a; e.g., semgrep, codeql, sonar]`
- **Dependency audit command**: `[command or n/a; e.g., pnpm audit, npm audit, pip-audit, uv audit, osv-scanner]`
- **Secret scan command**: `[command or n/a; e.g., gitleaks, detect-secrets]`
- **Config validation command**: `[command or n/a]`
- **Resilience/failure tests**: `[command or n/a]`
- **Agent workflow**: use the `hardening` skill after major features to produce
  a risk map, mitigations, adversarial proof, and residual-risk note.

## 🧑‍⚖️ Review Policy
- **Canonical material reviewer**: Farplane reviewer lane from
  `~/.codex/agents/reviewer.toml` plus the TAS `review` skill.
- **Local pre-push reviewer**: `scripts/codex_review_agent.ts` reviews
  deterministic check logs and git diff as a lightweight second pair of eyes
  using `~/.codex/skills/code-review/SKILL.md` when installed.
- **Pre-push default**: advisory Codex SDK diff review after local validators.
- **Skip local diff review**: `FARPLANE_SKIP_AGENT_REVIEW=1`.
- **Strict local diff review**: `STRICT_AGENT_REVIEW=1`.
- **Required setup for Node projects**:
  - dev dependencies: `@openai/codex-sdk`, `tsx`
  - scripts: `review:agent`, `review:prepush`
- **Review artifacts**: `tickets/TASK-XXXX/artifacts/review/` under the ticket
  whose change and proof are being judged
- **When to route to canonical reviewer**: material ticket completion,
  TAS-gated review, evidence-bundle review, prompt/skill/eval changes, or
  completion receipts.

## ▶ Runtime / QA Commands
- **Authoritative app-only run path**: [e.g., `pnpm dev`, `npm run dev`, `uv run fastapi dev app/main.py`]
- **Authoritative QA / evidence run path**: [e.g., `pnpm run dev:qa`, `docker compose up app db`, `./scripts/qa_up.sh`]
- **Required local services**: [e.g., `postgres`, `redis`, `dagster`, `none`]
- **Launch shape**: [plain processes, compose, mixed]
- **Expected targets / base URLs**: [e.g., `http://127.0.0.1:3000`, `http://127.0.0.1:8000`]
- **Port / env contract**: [which vars may be overridden, such as `PORT`, `HOST`, `DATABASE_URL`]
- **Source of truth note**: [if package scripts or compose files are authoritative, say so here instead of adding wrappers]

## 🤖 Agent QA / Testability
- **Reusable QA runbooks live in**: `qa/cookbook/`
- **Stable browser regression tool**: [e.g., Playwright]
- **Interactive browser debugging tool**: [e.g., Codex in-app Browser]
- **Preferred fast-entry helpers**: [e.g., deep links, seeded states, keyboard shortcuts, debug routes]
- **Required state probes for complex UI**: [e.g., HUDs, DOM mirrors, overlays, event logs]

## 🚀 Quick Commands
```bash
# Install dependencies
[command]

# Run the preferred app-only path
[command]

# Run the preferred QA / evidence path
[command]

# Run tests
[command]

# Run the local pre-push gate
bash scripts/pre_push_check.sh

# Optional: stop or clean up the QA path
[command or n/a]

# Build project
[command]
```
