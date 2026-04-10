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
- Keep live repo-owned skills and docs Codexter-native. Retired OMX instructions belong only in archive or research material, not active surfaces.
- Prefer `.harness/` for live runtime state.
- Keep root `AGENTS.md` local and navigational. Global install policy belongs in `templates/global/AGENTS.md`.
- When changing harness behavior, prefer the smallest lever that fixes the real failure:
  - review loop and proof requirements first
  - ticket/task-shaping contracts next
  - skills and subagent boundaries after that
  - root prompt rewrites last
- Do not treat Codexter like an app repo with one central runtime to extend by default. Most work here is about better orchestration surfaces, not more orchestration code.

## Durable Truth

- `tickets/`: active task object, plan, evidence, blockers, handoff
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
