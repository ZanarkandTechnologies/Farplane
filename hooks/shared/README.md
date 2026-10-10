# Shared hook code

Not a hook: nothing in [`hooks/hooks.json`](../hooks.json) runs a file here.
These modules are imported by more than one hook, so they live once, beside the
hooks that use them:

- `hook_delivery.py` — reports a gate's block and sends lifecycle pings
  (every hook).
- `skill_suggestion.py` — the small-model client used to suggest a skill and to
  judge continuation (`user-turn`, `stop-gate`, `continuation`).
- `response_format.py` — the final-answer format checks (`stop-gate`,
  `continuation`).

Code used by one hook lives in that hook's folder. Code the `farplane` CLI also
uses lives in `bin/core/` (for example `user_turn.py`, `skill_registry.py`).
The installer links this folder under `~/.codex/hooks/shared/` with the others.
