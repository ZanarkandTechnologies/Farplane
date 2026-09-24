# Claude runtime adapter

Plugin metadata for Claude Code. `bash install.sh --runtime claude` renders the
installable plugin into `~/.claude/farplane/` from the shared sources:

- root `hooks.json` -> `plugin/hooks/hooks.json` (Codex paths rewritten, `FARPLANE_AGENT_RUNTIME=claude`)
- `agents/*.toml` -> `plugin/agents/*.md` (invoked as `farplane:<name>`)
- `templates/global/AGENTS.md` -> `~/.claude/farplane/AGENTS.md`, imported from `~/.claude/CLAUDE.md`

Skills install unprefixed into `~/.claude/skills/` so names match Codex.
Only runtime-specific metadata lives here; do not add a second hook or agent source.
