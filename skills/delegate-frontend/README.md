# Delegate Frontend

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
