# Delegate Frontend

## Purpose

Delegate bounded frontend phases to the configured Pi/Kimi frontend profile while
keeping Farplane responsible for final integration, QA, and claims.

## Public API / Entrypoints

- `SKILL.md`: delegation contract and command pattern.
- `.harness/external-cli/profiles/frontend-pi-kimi`: mounted Pi skill profile.
- `.harness/external-cli/runs/<run-id>`: prompt, command, sessions, and handoff.

## Minimal Example

1. Pick a phase: `spec`, `assets`, `implementation`, `repair`, or `visual-review`.
2. Write a prompt with owned files, first-write path, and acceptance criteria.
3. Run `pi` with the frontend profile skills.
4. Read `handoff.md` and decide keep, repair, or reject.

## How to Test

- Run a startup probe that writes one known file and exits.
- Inspect `command.json` to confirm the Pi adapter, Kimi model, and mounted
  frontend/review/QA skills.
- Require the handoff to list loaded and actually used skills.
Profile skill for routing frontend implementation through `delegate-cli`.

The first profile is `frontend-pi-kimi`, which targets Pi with Kimi K2.6.
The managed profile mounts frontend/media skills plus `agent-browser`,
`visual-qa`, `review`, and `web-design-guidelines` so the delegated builder can
capture runnable browser evidence in the same thread before handoff.

## Minimal Usage

```bash
python3 bin/sync_frontend_pi_skills.py --json
python3 bin/delegate_cli_agent.py run --profile frontend-pi-kimi --ticket tickets/TASK-0106/ticket.md --dry-run --json
```

## How To Test

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/delegate-frontend
```
