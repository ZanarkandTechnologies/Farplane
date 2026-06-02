# Delegate CLI

Route bounded work to external coding-agent CLIs while Farplane keeps ticket,
artifact, QA, review, and integration authority.

## Minimal Usage

```bash
python3 bin/delegate_cli_agent.py doctor --profile frontend-pi-kimi --json
python3 bin/sync_frontend_pi_skills.py --json
python3 bin/delegate_cli_agent.py run --profile frontend-pi-kimi --ticket tickets/TASK-0106/ticket.md --dry-run --json
```

## How To Test

```bash
python3 -m unittest bin.test_delegate_cli_agent
python3 skills/skill-creator/scripts/quick_validate.py skills/delegate-cli
```
