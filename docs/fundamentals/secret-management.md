---
title: Secret Management
status: active
owner: farplane-core
updated: 2026-08-02
---

# Secret Management

Farplane uses Doppler as the project-scoped secret store and the process
environment as the only runtime credential interface.

```text
doppler project/config -> doppler run -> process environment -> skill or Core
```

## Ownership boundary

- Doppler owns API keys, access tokens, refresh tokens, client secrets,
  passwords, webhook secrets, and other rotatable credentials.
- Each project checkout owns its Doppler project/config selection. Running from
  Gagazet selects Gagazet; running from Farplane selects Farplane.
- `~/.farplane/config.toml` owns non-secret machine/operator settings only,
  such as local service URLs, policy toggles, public IDs, phone numbers, and
  model preferences. Farplane ignores credential fields there, and
  `farplane doctor` reports their key names for migration.
- `~/.codex/config.toml` is an existing Codex adapter surface. This migration
  does not alter it.
- Tracked skill packages do not own `config.toml`. Fixed defaults belong in
  `SKILL.md`, references, or deterministic code; per-run choices belong in the
  invocation.

## Project setup

From the project whose account or automation will run:

```bash
doppler setup
doppler secrets set KEY_NAME
doppler run -- python3 /absolute/path/to/skill/scripts/check_config.py
```

`doppler secrets set KEY_NAME` prompts for the value without putting it in
shell history. For an already configured project/config, pass `--project` and
`--config` explicitly when needed.

Use either wrapper for real work:

```bash
farplane run -- <command>
doppler run -- <command>
```

Both inject secrets only into the child process. A scheduled automation must
launch its credentialed command through one of these wrappers from the intended
project checkout; merely loading a skill does not fetch secrets.

## Verification

```bash
farplane doctor --json
doppler run -- python3 /absolute/path/to/skill/scripts/check_config.py
```

Readiness tools print key names and booleans only. They must never print secret
values. OAuth refreshes may be used in memory for the active operation, but
Farplane does not write rotated tokens into local TOML; rotate the Doppler
value through the human-owned credential flow when the result reports that
rotation is required.
