---
title: Project Code Review Guide
status: active
owner: project
updated: YYYY-MM-DD
---

# Project Code Review Guide

Use this guide for automated and human review. The local pre-push Codex
reviewer is a maintainability-first branch reviewer. It should load the
reusable `~/.codex/skills/code-review/SKILL.md` contract plus this
project-specific overlay. It does not replace the canonical Farplane reviewer
lane installed at `~/.codex/agents/reviewer.toml` or the TAS review contract in
`~/.codex/skills/review/SKILL.md`.

## Priorities

1. Maintainability: duplicated domain logic, hidden side effects, overlong new
   files, fragile ownership boundaries, missing shared modules, or code that
   bypasses the project module structure.
2. Branch consolidation: multiple commits that implement the same concept in
   different folders, helpers that should be shared, or related files that
   should move under one owning module before push.
3. Documentation: new durable modules or conventions without README/AGENTS
   notes, stale project docs, or rules left only in code.
4. Correctness and integration: broken runtime behavior, invalid data flow,
   stale state, missing null handling, wrong adapter behavior, failed
   persistence, or security-sensitive mistakes.
5. Product UX: confusing flows, inaccessible controls, broken loading/error
   states, layout overlap, and missing user feedback.

## Project Rules

- Read `AGENTS.md`, `PROJECT_RULES.md`, and the active ticket before judging
  broad implementation choices.
- Read nearest module `README.md` / `AGENTS.md` when changed files are under a
  module-like folder.
- Prefer deterministic check output and proof artifacts before reviewer
  judgment.
- New source files over 500 lines need an explicit ticket note or refactor.
- Existing large files may be touched narrowly, but do not add unrelated
  responsibility to them.
- If React component, hook, rendering, or data-fetching code changed, apply the
  installed `vercel-react-best-practices` skill when available.
- If a material review needs TAS gates, route it through the canonical
  Farplane `reviewer` lane rather than this local diff reviewer.

## Finding Format

Return only actionable findings introduced or exposed by the diff. Each finding
needs:

- severity: `critical`, `high`, `medium`, or `low`
- file path
- line number or narrow line range when possible
- concise issue
- concrete recommended fix

Use `patch_correct = true` only when there are no blocking maintainability,
modularity, documentation, correctness, security, or integration findings.
