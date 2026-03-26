# Codex Harness

Portable Git repo for the reusable parts of this live `~/.codex` home.

## What This Tracks

- `agents/` agent role configs
- `skills/` custom/local skills
- `rules/` approval rules
- `bin/notify.py` local notification helper
- `AGENTS.md` and `PROJECT_RULES.md`
- repo docs/tickets for evolving the harness
- `config.toml.example` as the sanitized bootstrap config

## What This Does Not Track

- auth or API keys
- `config.toml` with machine-local values
- session history, logs, sqlite files, caches, snapshots, or archived sessions

## Recommended Setup

### Option A: Clone straight into `~/.codex`

```bash
git clone <your-remote-url> ~/.codex
cp ~/.codex/config.toml.example ~/.codex/config.toml
```

Then edit `~/.codex/config.toml` and replace the placeholder paths, API keys, and trusted project entries.

### Option B: Keep the repo elsewhere and link it into `~/.codex`

```bash
git clone <your-remote-url> ~/src/codex-harness
cd ~/src/codex-harness
bash install.sh
```

`install.sh` symlinks tracked config into `~/.codex` without touching ignored live state. It also seeds `config.toml` from `config.toml.example` if no config exists yet.

## First Push

```bash
cd ~/.codex
git init
git add .
git commit -m "chore(codex): bootstrap config harness"
git branch -M main
git remote add origin <your-remote-url>
git push -u origin main
```

## Bootstrap Checklist

1. Copy `config.toml.example` to `config.toml`.
2. Replace `__CODEX_HOME__` with the real absolute path to your Codex home.
3. Add any secret-bearing MCP URLs locally only.
4. Add machine-specific `[projects."..."]` trust entries locally only.
5. Run `python3 -m py_compile bin/notify.py` and `bash -n install.sh` after edits.
