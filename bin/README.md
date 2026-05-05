# Bin

Executable helpers for the Codex harness.

## Purpose

This folder contains small scripts used by the live Codex config plus a few
transitional runtime helpers from earlier prototype iterations.

Primary control plane:

- `impl-plan`
- `$impl`
- persistent builder lanes
- `stop_hook.py`

Stop-hook role instructions are canonical TOML configs under `agents/`.
`stop_hook.py` reads those TOML files directly and injects their exact
`developer_instructions` into `codex exec`.

The `bin/` directory is now mostly shim/utility territory, not the main
orchestration story.

## Entrypoints

- `check_harness_invariants.py` - narrow validator for high-value root/runtime/ticket-boundary invariants
- `check_doc_parity.py` - narrow canonical-doc parity validator for README/spec/ticket surfaces
- `capture_user_turn.py` - turn-start user-intent writer for the hook surface
- `delegate_cli_agent.py` - external CLI delegation helper for profile setup,
  dry-run command rendering, execution logs, and ticket evidence copyback
- `codexter_boards.py` - board adapter contract plus the filesystem
  `FileTicketAdapter` that normalizes `tickets/TASK-*/ticket.md` into a
  `WorkItem`
- `codexter_invocation.py` - contract helper for `WORKFLOW.md`,
  `CodexterRunEnvelope`, board-backed `WorkItem`, compute selection, skill
  routing, and `ProofPacket` validation; it does not launch Codex
- `notify.py` - local notification helper
- `stop_hook.py` - thin stop-hook/runtime shim
- `ticket_runtime.py` / `ticket-runtime` - local helper for ticket runtime
  records, optional isolated checkouts, port reservation, runtime
  launch/teardown, and QA target lookup

## Runtime Decisions

- `stop_hook.py`: keep
- `capture_user_turn.py`: keep
- `ticket_runtime.py`: keep

Runtime state stays lightweight and machine-facing. The grouped `claim` object
tracks the active ticket/run/session ownership for hook consumers, while
`last_user_turn` carries the saved current-turn user ask.

For live multi-session coordination:

- `session_id` remains the transport/runtime identity
- `session_name` is the human-facing session alias, such as `agent-03`
- `session_origin` records whether a session is `control`, `internal`, or `non_owning`
- ticket frontmatter may mirror only the human-facing alias as `claimed_by`
- raw `session_id` should stay runtime-only

Delegated worker metadata is additive:

- `worker_name` identifies the lane role for the current live path
- `main_artifact_path` points at the worker's canonical work object
- `grounding_summary` captures the worker's explicit artifact-grounding line when available
- `worker_started_at`, `last_checkpoint_at`, and `checkpoint_summary` support stale-wait backpressure reads

The live `status` surface now derives a first advisory backpressure signal:

- `backpressure_state`: `within_budget`, `over_budget`, `inactive`, or `unknown`
- `stale_for_secs`: elapsed seconds since the latest checkpoint when available
- `recommended_action`: present for over-budget waits

Runtime routing is session-first for parallel Codex usage:

- explicit run-state selector when a managed lane exports one
- hook `session_id` for lane-scoped session state
- `.harness/state/current-run.json` as the live current-run pointer / last-active selector
- only `session_origin=control` sessions may persist canonical `last_user_turn` and advance the live current-run pointer

See [the runtime-surface spec](/Users/kenjipcx/coding-harness/Codexter/docs/specs/runtime-surface.md) for the canonical decision table.

## Preferred Agent-Facing Command Surfaces

Use the existing helpers directly, but prefer output modes that keep routine
success quiet and make failure output the thing that stands out.

- `python3 skills/impl/scripts/tmux_helper.py followup ...`
  Default mode: one-line success summary for operator/agent scans
- `python3 skills/impl/scripts/tmux_helper.py followup ... --json`
  Use when a script or hook needs the structured payload
- `python3 skills/impl/scripts/tmux_helper.py status`
  Current mode: full JSON because this is still primarily a machine/state read surface
- `python3 bin/ticket_runtime.py ensure ...`
  Use when a skill or operator needs a ticket-scoped runtime record, optional
  isolated checkout path, declared commands, and QA targets without launching yet
- `python3 bin/ticket_runtime.py up ...`
  Use when the ticket runtime should actually start configured frontend/backend
  processes or a compose-backed runtime
- `python3 bin/ticket_runtime.py qa ...`
  Use when QA needs the current runtime status plus only the live targets that
  are actually open for the ticket right now
- `python3 bin/ticket_runtime.py down ...`
  Use when the helper should stop tracked processes or run the declared
  compose-down command, then release reserved ports
- `python3 bin/delegate_cli_agent.py doctor --profile frontend-pi-kimi --json`
  Use before a live external CLI run to check the profile templates, copied
  skill sources, executable, and required environment variables
- `python3 bin/delegate_cli_agent.py run --profile frontend-pi-kimi --ticket <ticket> --dry-run --json`
  Use to render the Pi/Kimi frontend delegation prompt, command, runtime logs,
  and durable ticket artifacts without spending tokens or editing files
- `python3 -m unittest bin/test_codexter_boards.py`
  Use to prove the filesystem BoardAdapter path containment and ticket
  normalization contract before changing invocation or Ralph selection behavior
- `python3 bin/codexter_invocation.py prepare --ticket <ticket> --phase planning --proof .harness/results/<ticket>.proof.json`
  Use to validate a local Codexter invocation envelope and inspect the selected
  skill route without launching Codex
- `python3 tickets/scripts/check_ticket_metadata.py`
  Current mode: already near the desired quiet-success shape; keep the single-line pass output

Examples:

```text
followup ok: TASK-0033 -> building pane=%42 session=main run=.harness/runs/task-0033-building-20260410T091500000000Z.json dry-run
```

```text
followup failed: TASK-0033 -> building | tmux send-keys failed | pane=%42
no current client
```

## Minimal Example

```bash
python3 skills/impl/scripts/tmux_helper.py launch \
  --ticket tickets/TASK-0014/ticket.md \
  --phase building \
  --dry-run

python3 skills/impl/scripts/tmux_helper.py followup \
  --ticket tickets/TASK-0014/ticket.md \
  --phase documenting \
  --reason "hook-driven follow-up"

python3 skills/impl/scripts/tmux_helper.py followup \
  --ticket tickets/TASK-0014/ticket.md \
  --phase documenting \
  --reason "hook-driven follow-up" \
  --json

python3 skills/impl/scripts/tmux_helper.py status

python3 bin/ticket_runtime.py up \
  --ticket TASK-0014 \
  --branch pr-123 \
  --checkout-mode worktree \
  --runtime-mode branch-runtime \
  --create-worktree \
  --reserve frontend \
  --reserve backend \
  --frontend-cmd "npm run dev" \
  --backend-cmd "npm run api" \
  --json

python3 bin/ticket_runtime.py qa --ticket TASK-0014 --json
python3 bin/ticket_runtime.py down --ticket TASK-0014 --json

python3 bin/delegate_cli_agent.py doctor --profile frontend-pi-kimi --json
python3 bin/delegate_cli_agent.py run \
  --profile frontend-pi-kimi \
  --ticket tickets/TASK-0014/ticket.md \
  --dry-run \
  --json

```

In the live interactive path, `$impl` is the orchestrator contract and
`skills/impl/scripts/tmux_helper.py` is only a visibility/recovery helper.
Same-lane continuations come from the normal Stop-hook block/continue flow.
`followup` is the fallback path when a lane must be recreated or resumed from
stored session metadata. `status` centralizes the active lane plus the latest
hook verdict, falling back to the Stop-hook log when the live run state has
already advanced.

## How To Test

- `python3 bin/check_harness_invariants.py`
- `python3 bin/check_doc_parity.py`
- `python3 -m unittest bin/test_harness_invariants.py`
- `python3 -m unittest bin/test_doc_parity.py`
- `python3 -m unittest bin/test_delegate_cli_agent.py`
- `python3 -m unittest bin/test_ticket_metadata.py`
- `python3 -m unittest bin/test_ticket_runtime.py`
- `python3 -m py_compile bin/stop_hook.py`
- `python3 -m py_compile bin/ticket_runtime.py bin/test_ticket_runtime.py`
- `python3 -m py_compile bin/capture_user_turn.py bin/user_turn.py`
- `python3 -m py_compile bin/check_harness_invariants.py bin/test_harness_invariants.py`
- `python3 -m py_compile bin/check_doc_parity.py bin/test_doc_parity.py`
- `python3 -m py_compile bin/delegate_cli_agent.py bin/test_delegate_cli_agent.py`
- `python3 -m py_compile skills/impl/scripts/tmux_helper.py`
- `python3 -m unittest discover -s bin -p 'test_*.py'`
- `python3 skills/impl/scripts/tmux_helper.py launch --ticket <ticket> --phase building --tmux-session <session> --dry-run`
- `python3 skills/impl/scripts/tmux_helper.py followup --ticket <ticket> --phase documenting --run-state <run-state> --dry-run`
- `python3 skills/impl/scripts/tmux_helper.py followup --ticket <ticket> --phase documenting --run-state <run-state> --dry-run --json`
- `python3 skills/impl/scripts/tmux_helper.py status`
