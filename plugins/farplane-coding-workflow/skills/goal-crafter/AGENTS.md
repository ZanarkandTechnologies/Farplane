# goal-crafter

Use this module to maintain the `goal-crafter` skill only.

Keep the skill focused on preparing native Codex `/goal` prompts. Do not add
runtime hooks, hidden continuation state, or command dispatch here. `$work`
owns execution admission and `$ralph` remains the separate board-drain context
surface for prepared filesystem tickets.

For ticket-backed work, compile existing ticket metrics, proof, acceptance
criteria, blockers, and constraints into `GoalPrepState` before asking the
operator anything. Ask only missing execution-safety questions, capped at 3.
Route broad product discovery or unclear user value to PRD, `deep-interview`,
or `deep-system-design` instead of turning this skill into an interview loop.
See `MEM-0122`.
