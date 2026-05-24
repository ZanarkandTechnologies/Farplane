# goal-crafter

Use this module to maintain the `goal-crafter` skill only.

Keep the skill focused on preparing native Codex `/goal` prompts. Do not add
runtime hooks, hidden continuation state, or command dispatch here. `$work`
owns execution admission and `$ralph` remains the separate board-drain context
surface for prepared filesystem tickets.
