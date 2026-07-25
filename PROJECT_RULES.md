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
- `docs/`: PRD, memory, history, troubles, lessons, and specs
- `farplane/`: tracked project harness, metrics, automations, bindings, hooks, and PM config
- `.farplane/`: ignored project runtime state, reports, eval runs, logs, and ledgers
- `tickets/`: filesystem board for harness changes
- `qa/`: reusable QA guidance and cookbook workflows

## Conventions

- Never commit secrets, auth state, session history, logs, caches, or sqlite state.
- Keep `config.toml` local; version only `config.toml.example`.
- Keep generated `.farplane/` runtime state out of Git.
- Keep canonical project config in tracked `farplane/`, not ignored `.farplane/`.
- Do not enable local git hooks or live automations unless the operator explicitly asks.
- Prefer relative repo structure plus a small installer over hardcoding machine-specific paths into tracked files.
- Keep top-level `bin/` narrow: public wrappers, live hook/runtime shims, the
  global Farplane CLI edge, shared cross-skill commands, and repo-wide validator
  wrappers only. Core implementations belong under `bin/core/`, hook/runtime
  implementations under `bin/runtime/`, Core-owned tests under `bin/tests/`,
  skill-specific scripts and tests under `skills/<owner>/scripts/`, and
  repo-wide validators/tests under `bin/validators/`. Do not add generated
  `__pycache__` as tracked source.

## Quick Commands

```bash
# Validate the installer
bash -n install.sh

# Validate the notify helper
python3 -m py_compile bin/notify.py

# Validate Farplane project substrate
python3 bin/validators/check_farplane_project_files.py

# Validate core harness invariants
python3 bin/validators/check_harness_invariants.py

# Validate doc references
python3 bin/validators/check_doc_refs.py

# Validate focused bin/skill script ownership after moving helpers
python3 -m unittest skills/delegate-cli/scripts/test_delegate_cli_agent.py
python3 -m unittest skills/skill-maintenance/scripts/test_install_selected_skills.py
python3 -m unittest skills/skill-maintenance/scripts/test_import_installed_skills.py
python3 -m unittest skills/skill-maintenance/scripts/test_sync_skill_plugins.py

# Validate skill metadata and generated registry shape
python3 skills/skill-maintenance/scripts/check_skills.py --write

# Review tracked changes
git status --short

# Scan tracked files for obvious leaked secrets
rg -n "apiKey=|ref-[A-Za-z0-9]{8,}" README.md AGENTS.md PROJECT_RULES.md config.toml.example agents skills rules docs tickets install.sh bin
```
