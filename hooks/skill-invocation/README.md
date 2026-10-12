# Skill invocation

- **Event:** `PostToolUse`, matched to `Skill` (Claude) or `Bash` (Codex).
- **Entrypoint:** `skill_invocation.py` (five-second timeout).
- **Purpose:** Record each real skill invocation as one `skill_invoked` row on
  the bunker Convex hook stream `skill-invocation-listener`. Skill heat
  (`skills/skill-maintenance/scripts/generate_skill_graph.py`) counts only
  these rows.

## What counts

| Runtime | Counted | Not counted |
| --- | --- | --- |
| Claude | Every `Skill` tool call (`source: skill_tool`). A plugin prefix such as `farplane:commit` is stored as `plugin`; heat counts only rows with no plugin or `farplane`. | `Read` or `Bash` of a `SKILL.md`, and `/name` typed in a prompt (that is a request). |
| Codex | The first `Bash` read (`cat`, `sed`, `head`, ...) of an installed `<root>/<name>/SKILL.md` in a turn, where the path runs through `.codex/`, `.agents/` or `.claude/` (`source: skill_read`). | Reads of a source tree (`skills/<name>/SKILL.md`): that is skill maintenance. Later skill reads in the same turn: composition and intelligest's skill level-up. Any read in a turn whose prompt named a `$skill`: Codex injected that skill itself. |

Prompt mentions are posted by [user turn](../user-turn/README.md) to the same
stream as `skill_requested` (hookType `UserPromptSubmit`); heat reports them as
`requested_count_*`, never as invocations. Codex `$skill` and Claude `/skill`
invocations typed by the operator therefore show as requests, not invocations.

## Install and failure behavior

Registration lives only in [`hooks/hooks.json`](../hooks.json); `farplane hooks
install` (Codex) and `install.sh --runtime claude` link this folder and render
the entry for both runtimes. Rows go to `FARPLANE_TELEMETRY_HOOKS_URL`, else
`FARPLANE_CONVEX_SITE_URL` + `/telemetry/hooks`, with the telemetry token.
Convex drops a repeated `eventKey`, so a replayed payload counts once. No
endpoint, a network error or malformed JSON means no row; the hook never prints
to the agent and never blocks. Eval and judge runs are skipped. The per-turn
Codex claim lives in `~/.farplane/state/skill-invocations/<session>.json`.

Check: `python3 -m unittest bin/tests/test_skill_invocation_hook.py`.
