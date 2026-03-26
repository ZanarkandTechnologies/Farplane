# Project Rules: Codex Harness

This repo versions the reusable parts of a Codex home directory while keeping machine-local runtime state out of Git.

## Tech Stack

- Framework: none
- Language: Markdown, TOML, Bash, Python
- Runtime target: Codex CLI home (`~/.codex`)
- Package manager: none required

## Folder Structure

- `agents/`: reusable agent presets
- `skills/`: custom skills and bundled skill docs
- `rules/`: command approval rules
- `bin/`: helper scripts used by the live Codex config
- `docs/`: PRD, memory, history, troubles, and specs
- `tickets/`: filesystem board for harness changes

## Conventions

- Never commit secrets, auth state, session history, logs, caches, or sqlite state.
- Keep `config.toml` local; version only `config.toml.example`.
- Prefer relative repo structure plus a small installer over hardcoding machine-specific paths into tracked files.

## Quick Commands

```bash
# Validate the installer
bash -n install.sh

# Validate the notify helper
python3 -m py_compile bin/notify.py

# Review tracked changes
git status --short

# Scan tracked files for obvious leaked secrets
rg -n "apiKey=|ref-[A-Za-z0-9]{8,}" README.md AGENTS.md PROJECT_RULES.md config.toml.example agents skills rules docs tickets install.sh bin
```
