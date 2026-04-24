# Codexter AGENTS.md

This file is the project-local context for developing Codexter itself.

The install-time global harness contract now lives at `templates/global/AGENTS.md` and is what `install.sh` links into the live Codex home as `~/.codex/AGENTS.md`.

## Repo Purpose

Codexter is a harness repo for orchestrating Codexes through visible artifacts.

The main surfaces are:

- tickets as durable task memory
- docs as the canonical system of record
- skills as reusable workflows
- subagents as bounded specialists
- hooks and scripts as small control points

Prefer improving review loops, ticket contracts, skill packaging, and evidence surfaces before inventing more hidden orchestration code.

Do not describe a workflow as a shipped public capability until the repo
actually contains the discoverable `skills/<name>/` package and the canonical
inventory/docs point to it. See `MEM-0044`.

When the operator explicitly wants audit-then-fix recovery mode after a likely
assistant miss, use the `repent` skill rather than inventing ad hoc recovery
behavior.

When planning a missing or partially implemented feature depends on understanding
what a production-grade version should include, use `gap-analysis` before
locking the ticket plan so current-state gaps and external comparables are
explicit instead of implied.

## Project Structure

- `README.md`: current product shape, setup, and canonical entry points
- `agents/`: subagent role configs and prompt contracts
- `bin/`: hook and runtime scripts
- `docs/`: durable specs, history, memory, troubles, and research
- `experiments/`: smoke runs, eval outputs, and prototype evidence
- `rules/`: reusable policy fragments
- `skills/`: operational playbooks, references, scripts, and templates
- `templates/global/`: install-only template artifacts shipped into the live Codex home
- `tickets/`: active task board and archived work history

## Read First

Choose the smallest relevant reading set before editing.

For general repo orientation:

- `README.md`
- `ARCHITECTURE.md`
- `docs/specs/README.md`
- active ticket under `tickets/`
- `docs/MEMORY.md`
- `docs/TROUBLES.md`

For harness tuning and repo-shape changes:

- `docs/specs/harness-engineering-doctrine.md`
- `docs/specs/harness-engineering-quickstart.md`
- `docs/specs/harness-techniques.md`
- `docs/specs/spec-first-execution-loop.md`
- `docs/specs/orchestrator-subagent-loop.md`
- `docs/specs/review-gates.md`

For install and bootstrap work:

- `install.sh`
- `templates/global/AGENTS.md`
- `PROJECT_RULES.md`
- `config.toml.example`
- `skills/init-project/SKILL.md`

For harness-design research and external patterns:

- `docs/research/web-research/2026-04-02_anthropic-harness-comparison.md`
- `docs/research/web-research/2026-04-02_codexter-change-proposal.md`
- `docs/research/web-research/2026-04-02_codexter-vs-omx-gap-analysis.md`

## Local Operating Rules

- No blind edits. Read the relevant spec, ticket, and nearby module docs first.
- Tickets and docs are the source of truth; do not hide state in chat.
- Keep chat concise and put deep detail into visible repo artifacts such as the active ticket and canonical docs.
- When summarizing implemented feature changes to the operator, prefer `Before` / `After` / `Example` bullets over one dense prose block. See `MEM-0051`.
- Keep QA and completion proof artifact-first: link ticket-scoped evidence from `tickets/artifacts/TASK-XXXX/`, and for UI/user-visible work keep browser capture separate from final `visual-qa` judgment. See `MEM-0048`.
- Treat `$impl` as the public execution surface, with internal `execution_phase` progression through `impl`, `qa`, and `demo` when required. Stop-hook should advance those phases mechanically before final completion review. See `MEM-0049`.
- Auto-run `review` at the end of `impl-plan` and at the end of `impl` when working inside Codexter.
- Keep live repo-owned skills and docs Codexter-native. Retired OMX instructions belong only in archive or research material, not active surfaces.
- Prefer `.harness/` for live runtime state.
- Keep root `AGENTS.md` local and navigational. Global install policy belongs in `templates/global/AGENTS.md`.
- For Codexter harness brainstorming, explicitly compare repo-local `AGENTS.md`, `templates/global/AGENTS.md`, `skills/*`, `agents/*.toml`, and hooks / `bin/*`, then explain why the chosen surface should change now and why the others should not be the primary change surface.
- For harness-surface placement decisions, use `docs/specs/harness-engineering-doctrine.md` before expanding root policy, subagents, hooks, or validators.
- When changing harness behavior, prefer the smallest lever that fixes the real failure:
  - review loop and proof requirements first
  - ticket/task-shaping contracts next
  - skills and subagent boundaries after that
  - root prompt rewrites last
- Do not treat Codexter like an app repo with one central runtime to extend by default. Most work here is about better orchestration surfaces, not more orchestration code.
- For early skill-todo experiments, prefer plain `todos.md` checkbox templates with Markdown links to related skills before inventing parser syntax or persisted workflow state.

## Durable Truth

- `tickets/`: active task object, plan, evidence, blockers, and any short
  resume notes when needed
- `docs/HISTORY.md`: append-only change log
- `docs/MEMORY.md`: curated invariants and constraints
- `docs/TROUBLES.md`: repeated misses and prevention ideas
- `experiments/`: proof artifacts and smoke outputs

Transient execution state stays outside this file. Keep this file short enough that an agent can use it as a map.

## Stop If

- scope conflicts or is unclear
- API or interface contract is ambiguous
- migration is risky with no rollback
- circular dependency appears

No silent architectural drift.
