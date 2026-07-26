---
template_id: ticket-template
template_version: "0.2.5"
feature_refs:
  - FEAT-0007
ticket_id: TASK-0414
title: "Purge unused runtime and standalone binary surfaces"
status: done
priority: high
created_at: 2026-07-26T18:00:00+08:00
updated_at: 2026-07-26T15:53:38.440251Z
---
# TASK-0414: Purge unused runtime and standalone binary surfaces

## Summary

Make `farplane` the only user-facing executable installed by Core. Retain only
the Python launchers that Codex hooks or the notify configuration technically
call. Remove the unused PR/Ticket Runtime workflow and the retired invocation,
board, and compute command family rather than moving dead abstractions behind
new subcommands.

## Scope

- In:
  - inventory every `INSTALL_BIN_FILES` entry against active callers
  - remove `pr-runtime`, Ticket Runtime, and their tests/docs/install paths
  - remove the retired standalone invocation/board/compute command family
  - preserve required hook and notification launchers
  - update active registries and documentation
- Out:
  - remote compute, schedulers, per-ticket compute servers, or worktree runtime
    orchestration
  - compatibility aliases for removed pre-public commands
  - changes to native Codex task/worktree selection

## Delta

```text
before:
  install:
    - farplane
    - ticket-runtime
    - farplane_invocation.py
    - farplane_boards.py
    - farplane_compute.py
    - hook and notification launchers
  unused_workflows:
    - pr-runtime
    - ticket-scoped runtime records and port/process orchestration
    - retired explicit invocation envelope and future compute selector
after:
  public_cli:
    - farplane
  required_technical_edges:
    - capture_user_turn.py
    - notify.py
  internal_dependencies:
    - runtime_telemetry.py
    - user_turn.py
    - _compat.py
  removed:
    - pr-runtime
    - ticket-runtime
    - retired invocation/board/compute wrappers and implementations
example:
  local_ticket:
    - Codex opens the current checkout or its native worktree
    - QA receives an explicit target when an app must run
    - no Farplane runtime record or port broker is involved
```

## Program

```yaml
mode: refactor
owner_surface: installer_and_bin
behavior_lock:
  keep:
    - farplane CLI
    - UserPromptSubmit hook
    - turn-complete notification configuration
  delete:
    - unused runtime workflow
    - retired invocation command family
```

## Done / Proof

- [x] Every installed binary is classified by an active caller or removed.
- [x] `ticket-runtime`, `pr-runtime`, runtime-record orchestration, and their
      active references are absent.
- [x] Retired invocation/board/compute wrappers, implementations, tests, skill,
      workflow policy, and active registry references are absent.
- [x] Installer retires removed live paths and installs no dead executable.
- [x] Hook, notify, installer, skill-registry, and full Core test suites pass.

## Links

- `install.sh`
- `bin/README.md`
- `hooks.json`
- `docs/features/FEAT-0015-symphony-compatible-farplane-invocation-contract.md`
- `tickets/archive/TASK-0414/artifacts/validation/binary-cleanup-proof.json`
- `tickets/archive/TASK-0414/artifacts/review/completion-receipt.json`

## Notes

- Current policy is local development only. A future remote-compute need must
  earn a new ticket and interface from current requirements.
