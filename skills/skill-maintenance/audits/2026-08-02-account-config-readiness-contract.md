---
title: "Account config readiness contract"
status: accepted
owner: skill-maintenance
created_at: 2026-08-02
updated_at: 2026-08-02
tags:
  - configuration
  - doppler
  - social-accounts
refs:
  - docs/skills/system.md
  - skills/instagram-account/scripts/check_config.py
  - skills/x-account/scripts/check_config.py
---

# Account Config Readiness Contract

## Decision

Credential-bearing account skills use one package-local `check_config.py`
command that checks read and publish readiness together. It does not accept a
capability selector and does not put secret fields in skill frontmatter.
Successful output is intentionally limited to `skill`, `ready`, `read_ready`,
`publish_ready`, and `redacted`; blocked output adds only `missing`.

## Delta

- Before: the Instagram and X checkers reported both branches but returned
  success when only read credentials were available, leaving the meaning of a
  successful check ambiguous.
- After: both emit a shared `skill`, `ready`, and `redacted` envelope; `ready`
  and exit `0` require both read and publish readiness, while existing branch
  fields explain partial configuration.
- Example: an Instagram Login token without an Instagram user ID returns
  `read_ready: true`, `publish_ready: false`, `ready: false`, and exit `1` in a
  single redacted report.
- Follow-up refinement: removed config paths, API mode, optional app/refresh
  diagnostics, duplicated auth-mode fields, and empty missing lists from the
  default output after live use showed they obscured the decision.

## Proof

- Instagram checker tests cover token-only partial readiness, complete
  readiness, exit status, and value redaction.
- X checker tests cover bearer-only partial readiness, OAuth 2.0 complete
  readiness, exit status, and value redaction.
- Both scripts compile under the local Python runtime.
- Skill-config validation, todo-tier validation, Tier 0 validation, registry
  validation, and `git diff --check` pass.
- The selected Instagram and X skills were reinstalled into the live Codex
  skill directory, where both checker test suites pass.
- A live redacted Gagazet Doppler run reports read-ready but publish-blocked
  because neither supported Instagram user-ID key is stored.
- `check_skills.py --write` completed all config-contract-related checks but
  remains nonzero because `content-impl-plan` already exceeds its enrolled QA
  and eval surface budgets.

## Boundary

Optional Meta app credentials and X refresh credentials remain diagnostic and
do not block `ready`. Provider-specific setup detail remains in conditional
references. The checker never fetches or prints secret values itself; commands
that need live credentials continue to run through Doppler.

## Residual Evidence

The first live retry exposed that both account loaders parsed the optional
private fallback before using valid Doppler environment values. Because the
operator's `~/.farplane/config.toml` contains invalid TOML, that fallback
raised before readiness could be reported. Both loaders now treat malformed
fallback/cache TOML as empty, leaving runtime environment credentials
authoritative. The private file itself was not modified.

Proof after repair:

- Complete Instagram script suite: 5 tests pass.
- Complete X script suite: 7 tests pass.
- Successful-output tests enforce the exact five-field contract; partial
  readiness tests enforce conditional missing-key guidance and redaction.
- Both repaired loaders and checker tests compile; `git diff --check` passes.
- The installed skills were refreshed. The operator's exact command now exits
  `0` with `ready: true` from the Farplane checkout despite the malformed
  fallback.
- The same command from Gagazet exits `1` with `read_ready: true` and
  `publish_ready: false`, proving that checkout's Doppler config still lacks an
  Instagram user-ID key.
- Eval comparison skipped: this is deterministic loader error handling covered
  by focused unit and live command tests.
