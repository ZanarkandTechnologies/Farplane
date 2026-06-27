# Taste Loop

`taste-loop` is the official optional active-hours human-feedback heartbeat for
Farplane. It selects high-compounding skills with the official Skill
Compounding Score from `docs/features/FEAT-0064-skill-compounding-score.md`; uses the
Codex automation schedule plus the `farplane/automations.md` TOML block for
active hours and feedback budget; and asks Codex to write local feedback cards
or Goal Advisor handoffs.

The runtime surface is a Codex automation prompt, not a local script. The
project-specific copy lives in `farplane/automations.md`; the reusable body
lives in `templates/heartbeat-prompt.md`.

Action beats write Markdown reports under `.farplane/reports/taste-loop/` and
any feedback-card or Goal-handoff artifacts under
`.farplane/automation/taste-loop/`. Ordinary no-op beats should avoid repo or
runtime artifacts unless diagnostic logging is enabled.

The heartbeat should derive an honest metric card before creating a benchmark
or Goal handoff. If the target needs taste, it routes through
`optimize-with-human`; if it needs measured improvement, it routes through
`goal-advisor` with `self-improve` context; if neither is honest, it blocks
rather than inventing a fake score.
