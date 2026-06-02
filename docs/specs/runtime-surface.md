# Runtime Surface

Date: 2026-04-07

## Goal

Define the current target runtime surface now that `$impl` is the public
build-phase orchestrator.

This spec answers two questions:

1. which existing `bin/` helpers still matter
2. which ones should stop being documented as the future primary control plane

## Control Plane

The primary control plane is now:

- `impl-plan` for ticket planning
- `$impl` for build-phase orchestration
- `$work` for Work Admission: classify one request, ticket, batch, board unit,
  epic, or metric loop before choosing Goal, compute, planning, proof, and the
  downstream skill
- `batch-work` for explicit operator-supplied ticket ranges or lists, aligned
  with `$work` proof policy
- native `/goal` for thread-scoped evidence-based continuation when the finish
  line, proof surface, constraints, iteration policy, and blocked stop
  condition can be expressed as a Goal
- `$ralph` for Goal-backed board context, eligible-ticket selection, and safe
  batch grouping over prepared filesystem tickets
- worker lanes and runtime helpers behind the canonical `$impl` surface
- `stop_hook.py` for mechanical active-ticket artifact, phase, review, and
  nonce gates

The primary control plane is not:

- `ralph_orchestrate.py`
- `ralph_worker.sh`
- direct binary-first orchestration docs

There is no separate public retired execution surface anymore.
Same-ticket repeats re-enter `$impl`.
Serial board drains enter through `$ralph`, which selects one eligible active
ticket or a safe related tiny-ticket batch and then hands that work unit to
`$work`. `$work` chooses `impl-plan`, `$impl`, `close-ticket`, direct local
work, reslicing, or autoresearch. Ralph does not revive retired binary-first
orchestration.

For same-ticket build looping, the runtime contract is:

- ticket `phase/status` says the work is still in a loopable build state
- ticket frontmatter may declare durable execution requirements such as `requires_qa` and `requires_demo`
- runtime `claim` says which session/lane currently owns that work
- session ownership is explicit: only control sessions that entered through a public skill invocation may own canonical current-turn intent
- explicit `$impl` control-session invocations must seed selected-ticket runtime ownership when ticket resolution is explicit or unambiguous; a session-only control stub is not sufficient
- `impl_loop_active` says this session is currently allowed to auto-continue the `$impl` loop
- runtime `execution_phase` plus `phase_requirements` define whether the active build loop is in `impl`, `qa`, or `demo`
- tmux `auto_continue` only says whether a visible follow-up lane may be spawned or reused; it is not the global activation gate

For native Goal preparation, use `goal-crafter` to turn fuzzy operator intent
into a strong `/goal` command with outcome, verification surface, constraints,
boundaries, iteration policy, and blocked stop condition. Goal mode should own
evidence-based continuation.

For Work Admission, use `$work` to decide whether a unit is tiny direct work, a
normal ticket, a Goal-backed ticket batch, a board drain, an epic that needs
reslicing, or a metric loop. Ticket `compute_target` and readiness fields are
context, not automatic run triggers.

For hook-backed skill-opportunity approval capture, the runtime contract is:

- `UserPromptSubmit` appends only control-session user turns to a bounded
  rolling conversation window under `.harness/state/self-improve/windows/`
- `Stop` appends the matching assistant response and trims the window to the
  configured maximum, defaulting to 10 exchanges
- every configured interval, defaulting to 10 captured user turns,
  `stop_hook.py` launches a detached background `codex exec` proposer by
  default; set `FARPLANE_SKILL_OPPORTUNITY_APPLY=0` to disable it
- proposer input includes the current window plus recent session windows,
  defaulting to 5 sessions, so repeated complaints and painful patterns can be
  recognized across nearby conversations
- proposer input and output live under
  `.harness/state/self-improve/applications/`
- Stop hook logs every self-improve sidecar readiness check as a named
  `skill-opportunity-review` hooklet row in `.harness/logs/stop-hook.jsonl`,
  including skipped checks that are not yet due. The row carries `status`,
  `readiness`, `reason`, trigger counts, project root, session id, and artifact
  handles.
- proposer side effects are bounded to Notion Tasks: it creates approval tasks
  tagged `agent self improvement` using the Notion-context Tasks data source
- the proposer must not mutate local repo files, including skills, docs,
  memory, tickets, install config, hooks, bin helpers, agents, or `.harness/`
- Stop-hook stdout remains reserved for the single hook JSON payload; proposer
  stdout and stderr are redirected to run-scoped files

For serial `$ralph`, the runtime contract is:

- ticket frontmatter and body remain the queue source of truth
- selector helpers are read-only and may not create claims, mutate tickets, or
  launch agents
- each selected ticket or safe batch is handed to `$work`
- batches require one proof row per ticket plus one batch-level regression row
- `$ralph` stops on no ready ticket, human gate, blocker, failed handoff, or
  loop limit
- parallel dispatch stays out of scope until worktrees, leases, merge policy,
  stale-worker handling, and batch QA are specified

For ticket-scoped isolated checkout and local QA targeting, runtime may also
persist ticket runtime records under:

- `.harness/state/tickets/TASK-XXXX.runtime.json`

Those records are runtime-only and may carry:

- branch
- checkout mode
- checkout path
- runtime mode
- declared frontend/backend targets
- reserved ports
- declared frontend/backend/compose commands
- launched process or compose metadata
- owner session alias

## Binary Decisions

| Binary | Decision | Reason |
| --- | --- | --- |
| `capture_user_turn.py` | `keep` | lightweight input-hook writer that stores bounded current-turn intent for later relevance checks |
| `notify.py` | `keep` | local utility with no orchestration overlap |
| `ticket_runtime.py` | `keep` | narrow local helper for ticket runtime records, optional isolated checkout creation, local runtime launch/stop, port reservation, and QA target publication |
| `tickets/scripts/check_ticket_metadata.py` | `keep` | canonical validator for the ticket surface and lives with the ticket system it validates |
| `stop_hook.py` | `keep` | thin runtime shim that evaluates active-ticket stop events, validates mechanical gates, and handles `$impl` re-entry decisions |
| `skills/impl/scripts/tmux_helper.py` | `keep` | skill-local operator visibility and lane recovery helper, not the control plane; it also writes the active runtime claim used by stop-hook consumers |
| `ralph_orchestrate.py` | `retired` | superseded by `$impl`; removed from `bin/` once no live surfaces depended on it |
| `ralph_worker.sh` | `retired` | old phase-launch wrapper removed in favor of direct prompt/`codex exec` worker lanes |
| `export_omx_team_input.py` | `retired` | removed with the OMX bridge path because it is not part of the current skill-first runtime |

## Documentation Rules

- Public docs should describe `$impl` as the build-phase orchestrator.
- Public docs should describe `$work` as the Work Admission layer before
  compute-heavy execution.
- Public docs should describe `batch-work` as a standalone explicit range/list
  skill that shares `$work` batch proof policy.
- Public docs should describe `.harness/` as the canonical live runtime root.
- `capture_user_turn.py`, `skills/impl/scripts/tmux_helper.py`, and `stop_hook.py` may be documented as operator/runtime shims.
- `ticket_runtime.py` may be documented as the narrow ticket-runtime shim for
  isolated checkout, declared runtime launch/stop, and live QA target setup.
- Public docs should describe `current-run.json` as control-session-owned state, not a generic sink for every prompt-bearing session.
- Public docs should describe `.harness/state/tickets/*.runtime.json` as
  runtime-only metadata, not as a durable replacement for ticket truth.
- Public docs should describe same-ticket `$impl` continuation as requiring both the session-scoped loop gate and the matching runtime claim.
- Public docs should describe native `/goal` as the preferred surface for
  evidence-based continuation and semantic stopping criteria.
- Public docs should describe `$ralph` as a Goal-backed board context and
  selector surface that hands work units to `$work`, not as a second executor
  or hidden runtime plane.
- Public docs should describe Stop hook as a mechanical protocol/artifact gate,
  not the autonomy brain for Goal-backed work.
- Public docs should describe tmux `auto_continue` as lane-follow-up plumbing, not as the source of truth for whether the `$impl` loop is active.
- internal Stop-hook role instructions should live under `agents/`, not as giant string literals in Python helpers.
- Any removed prototype binaries should remain only as historical references in
  archived tickets or older specs, not as live runtime files.
- Do not present `ralph_orchestrate.py` as the preferred future entrypoint.
- Do not present retired runtime directories or `docs/progress.md` as live queue state.

## Immediate Cleanup Scope

This cleanup does:

- relabel the primary runtime story
- document keep/remove/rewrite decisions
- remove the dead prototype wrappers that are no longer load-bearing
- keep skill behavior in tracked skills, not tracked prompt files

Follow-on cleanup can further simplify the remaining shims without reopening the
control-plane decision.
