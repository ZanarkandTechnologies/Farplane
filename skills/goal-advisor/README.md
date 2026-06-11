# goal-advisor

`goal-advisor` decides how to use native Codex Goal mode in Farplane and
generates the final native `/goal` prompt when Goal mode is warranted.

It chooses whether a request should become:

- a direct non-Goal task
- an active Goal
- a heartbeat
- a feedback loop
- a skill-improvement loop
- a rollout meta ticket
- a business/strategy loop

It owns both the architecture decision and the final Goal prompt so the metric,
state surfaces, drift policy, and continuation instructions stay coherent.

## Test

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
```
