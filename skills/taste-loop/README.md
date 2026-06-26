# Taste Loop

`taste-loop` is the official optional active-hours human-feedback heartbeat for
Farplane. It selects high-compounding skills with the official Skill
Compounding Score from `docs/specs/skill-compounding-score.md`; gates on
Kenji's work hours and feedback budget; and asks Codex to write local feedback
cards or Goal Advisor handoffs.

The runtime surface is a Codex automation prompt, not a local script. The
project-specific copy lives in `farplane/automations.md`; the reusable body
lives in `templates/heartbeat-prompt.md`.

Each beat should write a Markdown report under `.farplane/reports/taste-loop/`
and any feedback-card or Goal-handoff artifacts under
`.farplane/automation/taste-loop/`.

The heartbeat should derive an honest metric card before creating a benchmark
or Goal handoff. If the target needs taste, it routes through
`optimize-with-human`; if it needs measured improvement, it routes through
`goal-advisor` with `self-improve` context; if neither is honest, it blocks
rather than inventing a fake score.
