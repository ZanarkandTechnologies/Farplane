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
- `docs/`: Canonical project state (`prd.md`, `specs/README.md`, `specs/*`, `HISTORY.md`, `MEMORY.md`, `TASTE.md`, `TROUBLES.md`)
- `tickets/`: Ticket board (`TASK-*/ticket.md`, `archive/`, `templates/`)
- `...`: [Other key directories]

## 📜 Conventions
- **Naming**: [e.g., camelCase for functions, PascalCase for components]
- **Testing**: [e.g., Use Vitest for unit tests]
- **Documentation**: [e.g., Use JSDoc for all public exports]

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
  - Desloppify: `[command or disabled]`
  - CodeRabbit: `coderabbit review --plain --type committed --base [branch]`

## 🤖 Agent QA / Testability
- **Reusable QA runbooks live in**: `qa/cookbook/`
- **Stable browser regression tool**: [e.g., Playwright]
- **Interactive browser debugging tool**: [e.g., agent-browser]
- **Preferred fast-entry helpers**: [e.g., deep links, seeded states, keyboard shortcuts, debug routes]
- **Required state probes for complex UI**: [e.g., HUDs, DOM mirrors, overlays, event logs]

## 🚀 Quick Commands
```bash
# Install dependencies
[command]

# Run development server
[command]

# Run tests
[command]

# Run the local pre-push gate
bash scripts/pre_push_check.sh

# Build project
[command]
```
