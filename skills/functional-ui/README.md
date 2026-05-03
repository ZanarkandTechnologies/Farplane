# Functional UI

## Purpose

Guide agents to design or repair product workflows from user stories, current UI diagnosis, and adjacent-product patterns before visual styling starts.

## Public API / Entrypoints

- `SKILL.md`: main workflow contract
- `references/*`: redesign diagnosis, comparable pattern extraction, and implementation handoff
- `AGENTS.md`: maintenance rules

## Minimal Example

1. Identify the user and top stories.
2. Diagnose the current UI when one exists.
3. Compare similar/latest examples and their proven workflows.
4. Produce 3 viable UI options.
5. Recommend one workflow.
6. Hand the result to `visual-design` or `frontend-craft`.

## How to Test

- Confirm the output starts with user stories.
- Confirm broken-UI requests include a diagnosis.
- Confirm the artifact compares similar/latest examples.
- Confirm one workflow is explicitly recommended.
