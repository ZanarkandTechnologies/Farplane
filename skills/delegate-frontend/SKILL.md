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
5. For Terminal-style, cinematic, generated-media, or premium landing pages,
   delegate one phase at a time: `spec`, `assets`, `implementation`, then
   `visual-review`. Do not combine all phases in one live prompt.
6. Run `python3 bin/sync_frontend_pi_skills.py --json` or
   `python3 bin/delegate_cli_agent.py setup --profile frontend-pi-kimi --json`
   so the managed Pi profile receives the curated frontend/media skill bundle.
7. Run `doctor`, then `run --dry-run`.
8. Run live only after credentials/spend/filesystem gates are satisfied.
9. Send any resulting UI changes back through Codexter QA, `visual-qa`, and
   `review`.

## Core Decision Branches

- `workflow unclear` -> run `functional-ui` or `frontend-craft` first.
- `visual taste unclear` -> run `visual-design` before delegation.
- `landing page narrative` -> run `landing-page` before delegation.
- `cinematic landing build` -> require a `SPEC.md` or landing brief, then split
  the external run by phase and file ownership.
- `asset-heavy frontend` -> rely on the mounted inference.sh skills
  `image-generation`, `video-generation`, `remotion`, and `remotion-render`;
  do not require Codex-native `imagegen` in the external Pi profile.
- `implementation ready` -> call `delegate-cli --profile frontend-pi-kimi`.

## Judgement Questions

Use `advise` when deciding whether the UI work is ready for external build, or
whether Codexter should first produce a stronger UX/visual brief.

## Top Gotchas

1. Do not use this skill for final visual judgment; use `visual-qa`.
2. Do not bypass `delegate-cli`; this is a profile skill, not a second platform.
3. Do not call the frontend profile a general solution for all CLIs.
4. Do not attach gold-reference screenshots to broad implementation prompts
   after the spec exists; summarize the reference in the spec and reserve
   screenshots for visual-review prompts.
5. Do not accept a timed-out partial external run as a successful handoff.
6. Do not add Codex-native `imagegen` to the Pi profile bundle; Pi should use
   the repo-owned inference.sh asset skills for repeatable external CLI work.

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
