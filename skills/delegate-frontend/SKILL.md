---
name: delegate-frontend
version: 0.1.0
description: Delegate frontend implementation or design-polish work to the configured external CLI frontend profile, currently frontend-pi-kimi via delegate-cli, while preserving Codexter ticket, QA, visual review, and integration authority.
allowed-tools: Read, Grep, Glob, Bash
---

# Delegate Frontend

Use this profile skill when frontend implementation, page/component polish, or
visual craft should be built by an external CLI profile instead of the current
Codex lane.

## Trigger Conditions

- The user explicitly asks to delegate frontend work to another CLI/model.
- A ticket says the frontend builder should be external.
- `frontend-craft`, `visual-design`, or `landing-page` planning exists and the
  next step is implementation through a configured external agent.

## Workflow

1. Read the ticket or frontend brief.
2. Confirm the work is frontend build/polish, not UX-only planning or final
   visual QA.
3. Load `delegate-cli`.
4. Use profile `frontend-pi-kimi`.
5. Run `doctor`, then `setup`, then `run --dry-run`.
6. Run live only after credentials/spend/filesystem gates are satisfied.
7. Send any resulting UI changes back through Codexter QA, `visual-qa`, and
   `review`.

## Core Decision Branches

- `workflow unclear` -> run `functional-ui` or `frontend-craft` first.
- `visual taste unclear` -> run `visual-design` before delegation.
- `landing page narrative` -> run `landing-page` before delegation.
- `implementation ready` -> call `delegate-cli --profile frontend-pi-kimi`.

## Judgement Questions

Use `advise` when deciding whether the UI work is ready for external build, or
whether Codexter should first produce a stronger UX/visual brief.

## Top Gotchas

1. Do not use this skill for final visual judgment; use `visual-qa`.
2. Do not bypass `delegate-cli`; this is a profile skill, not a second platform.
3. Do not call the frontend profile a general solution for all CLIs.

## Outcome Contract

Return:

- profile used: `frontend-pi-kimi`,
- ticket or brief supplied,
- dry-run/live status,
- handoff/log paths,
- required QA and review follow-up.

## References

- [architecture.md](references/architecture.md)
- [workflows.md](references/workflows.md)
- [gotchas.md](references/gotchas.md)
