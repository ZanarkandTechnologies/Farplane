# Delegate Frontend

Profile skill for routing frontend implementation through `delegate-cli`.

The first profile is `frontend-pi-kimi`, which targets Pi with Kimi K2.6.

## Minimal Usage

```bash
python3 bin/delegate_cli_agent.py run --profile frontend-pi-kimi --ticket tickets/TASK-0106/ticket.md --dry-run --json
```

## How To Test

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/delegate-frontend
```
