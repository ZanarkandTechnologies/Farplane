# Codex runtime adapter

Codex-only files. `bash install.sh` (default `--runtime codex`) installs the
shared sources into `~/.codex/`:

- `hooks/hooks.json` -> `~/.codex/hooks.json` (symlink; Codex reads the paths as written)
- `agents/*.toml` -> `~/.codex/agents/` (symlinks)
- `runtimes/AGENTS.md` -> `~/.codex/AGENTS.md` (copy)
- `runtimes/codex/config.toml.example` -> `~/.codex/config.toml` (rendered with skill profiles)
- `runtimes/codex/default.rules` -> `~/.codex/rules/default.rules` (Codex command approval rules)
- `runtimes/codex/notify.py` -> `~/.codex/bin/notify.py` (turn-complete sound; `farplane notify enable|disable`)

Skills install into `~/.codex/skills/`.
Only runtime-specific files live here; do not add a second hook or agent source.
