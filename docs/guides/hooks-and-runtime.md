---
title: "Farplane Hooks and Runtime"
status: active
owner: harness
created_at: 2026-06-23
updated_at: 2026-10-15
framework_template_version: "0.4.0"
tags:
  - farplane
  - hooks
  - runtime
  - lifecycle
refs:
  - hooks/hooks.json
  - hooks/README.md
  - install.sh
  - docs/guides/work-loop.md
  - docs/guides/project-files.md
---

# Farplane Hooks and Runtime

Farplane has one hook surface. `hooks/hooks.json` is the single hook
registration for both runtimes: `farplane hooks install` links it into
`~/.codex`, and `install.sh --runtime claude` renders it into a local
`farplane` Claude Code plugin. It holds small lifecycle telemetry commands,
edit/response gates, skill-invocation telemetry, and a bounded Jev
continuation check. Hooks do not infer durable state transitions from
arbitrary writes.

```text
hook(event, transcript/runtime_state)
  -> telemetry | mechanical_gate | bounded_continuation_advice
```

## Lifecycle Hooks

Each active hook lives in a [documented folder](../../hooks/README.md). Its README
owns entrypoint usage, configuration, failure behavior, and focused checks:
[stop gate](../../hooks/stop-gate/README.md),
[continuation](../../hooks/continuation/README.md),
[response length](../../hooks/response-length/README.md),
[lifecycle telemetry](../../hooks/lifecycle-telemetry/README.md),
[skill length](../../hooks/skill-length/README.md),
[skill invocation](../../hooks/skill-invocation/README.md),
[foreground wait](../../hooks/foreground-wait/README.md), and
[user turn](../../hooks/user-turn/README.md).
`farplane hooks install` links these complete folders. Temporary installed-only
migration links keep old flat command paths usable by active Codex sessions with
cached registrations; remove them only after those sessions retire or reload.
`hooks/hooks.json` remains the single registration source and uses the new paths.

`hooks/hooks.json` currently defines:

| Event | Commands | Purpose |
| --- | --- | --- |
| `UserPromptSubmit` | `capture_user_turn.py`, `farplane_console_ping.py` | classify the current user turn, append lightweight conversation windows, resolve native/ticket display metadata locally, and send sanitized `turn_start` hook telemetry |
| `PreToolUse` (`Bash`) | `foreground_wait.sh` | Claude only: deny a foreground Bash call that sleeps 30 s or more or polls in an `until`/`while`/`for` sleep loop, with the reason naming `run_in_background`, Monitor, or `timeout` ≤ 30000 for a short wait |
| `PostToolUse` (`apply_patch`, `Edit`, `Write`) | `skill_file_line_gate.py` | return repair feedback when a touched `skills/**/SKILL.md` exceeds 200 physical lines; the edit remains applied |
| `PostToolUse` (`Skill`, `Bash`) | `skill_invocation.py` | record each real skill invocation as one `skill_invoked` row on the telemetry stream (a Claude `Skill` call, or Codex's first `Bash` read of an installed `SKILL.md` in a turn); observation only, never blocks |
| `Stop` | `stop_gate.py`, `farplane_console_ping.py --expect-event Stop` | one blocking gate checks length, then continuation, then response format (at most one nudge per stop), and telemetry observes stop attempts; neither certifies task completion |
| `SubagentStart` | `farplane_console_ping.py` | send sanitized subagent-start lifecycle telemetry |
| `SubagentStop` | `farplane_console_ping.py` | send sanitized subagent-stop lifecycle telemetry |

The user-turn capture has a 30-second timeout; every other command has five
seconds. These are graphable as `hook:*` nodes that `triggers` command nodes.

### Inspecting Stop behavior

Run `farplane hooks list` to see each managed command, event, status message,
timeout, and source owner. Add `--json` for structured output, or use
`farplane hooks doctor` to check installed links. This inventory describes
Farplane's managed configuration, not the runtime's effective trust decisions
or other project/plugin hooks. Codex `/hooks` (or Claude Code's hook settings)
owns the effective hook controls.

Two Stop handlers are registered:

| Handler | Reads / effects | Can request continuation? |
| --- | --- | --- |
| `hooks/stop-gate/stop_gate.py` | Runs, in order: the length check (500 prose words and 50 nonblank prose lines by default, configurable through `FARPLANE_FINAL_RESPONSE_MAX_PROSE_WORDS` and `FARPLANE_FINAL_RESPONSE_MAX_PROSE_LINES`); then one Jev request through `farplane run` that scores continuation (threshold 0.5, at most three nudges per real user turn) and classifies the answer's shape and missing sections (threshold 0.6, at most two, once per user turn). A completed change that edited files and cites nothing gets one proof nudge. `FARPLANE_STOP_CHECKS` selects checks. Unknown provenance or provider failure allows stopping. | Yes, at most one block per stop: length, else continuation, else format. |
| `hooks/lifecycle-telemetry/farplane_console_ping.py` | Resolves task/project metadata and existing local ticket bindings; sends a `turn_end` event to the configured telemetry endpoint with a two-second HTTP timeout. No endpoint means no send; network errors are logged and allowed. Stop does not create ticket bindings. | No; no block response is emitted. |

The `continuation_gate.py` and `final_response_gate.py` entrypoints stay installed,
unregistered, for sessions with cached commands; the stop gate reuses their logic.

Both Stop handlers have five-second timeouts. The response accountant
(`bin/core/farplane_response.py`) excludes supported diagram blocks, media
embeds, labeled proof lines of at most 30 words, and trailing link-only
references from prose counts. Closed Mermaid and `wireframe` blocks, exact
image/video embed lines, marker-only Markdown blockquote spacer lines, and
trailing link-only references are classified separately; blockquote content,
four-space-indented code, and malformed or mixed forms count as prose. The
prose word and line ceilings are hard. The gate receives
`last_assistant_message` directly, so agents need no response draft file;
`farplane response check PATH|--stdin --json` is only an inspectable
preflight. The gate never truncates or owns task completion. Telemetry contains metadata, not the final
answer or full transcript. A Stop event can precede another continuation, so
`turn_end` must not be read as Goal or ticket completion.

Telemetry remains separate from the stop gate. Blocking feedback uses a
level-four Markdown hook name followed by labeled instruction bullets. The length
check owns rewrites; continuation and format recognize their own versioned
feedback and exact length feedback before reassessing a revised response. No hook
certifies native Goal completion.

The continuation reader uses Codex desktop actual-user metadata, preserves the
opening and latest request plus a bounded dialogue tail, and excludes tool
outputs, reasoning, and commentary. Long rollouts read complete JSONL rows from
a 1 MiB opening window and an 8 MiB recent window; the middle is neither loaded
nor sent. Transcript format and hook-feedback provenance are implementation
details, so unknown forms allow stopping. Redaction reduces common credentials
and identifiers, but is not anonymization: authorized conversation text goes to
the configured provider. Its stderr diagnostic reports only a fixed decision
status.
Enable/disable it through Codex's hook control; credentials stay in Doppler and
are injected by `farplane run` from the installed Farplane source directory, not
the calling project. The registered command invokes Python directly; the hook
captures credential bootstrap failures and allows stopping without exposing setup
errors to other Codex projects. Bootstrap has a four-second deadline.

### Classified telemetry and delivery diagnostics

Each lifecycle command uses `--expect-event` with its registered event.
The sender validates that argument against stdin `hook_event_name` before
sending; it never overwrites the event. Mismatches emit a diagnostic and do not
send. The existing `turn_start`, `turn_end`, `subagent_start`, and `subagent_stop`
classifications remain. Every Stop occurrence gets a fresh event key so a final
Stop after continuation is not deduplicated against an earlier attempt; replay
of the same payload retains its key.

Latest per-event receipts live at
`~/.farplane/state/hook-delivery/<EVENT>.json` (respecting `FARPLANE_STATE_DIR`).
`farplane hooks list` shows observed delivery status and timestamp:
`unconfigured`, `attempted`, `accepted`, or `failed`. Receipts contain fixed
metadata/reason codes and HTTP status only, never credentials or payloads.
Accepted means HTTP 2xx, not a verified UI projection. These are shared latest
observations across tasks, not per-task execution truth.

The UI (now the bunker's Convex backend) projects Stop as idle / "stop
attempted", and newer observed
tool activity restores running. SubagentStop stops the child, not its parent.
Selective activity publishers cannot reveal silent continuation. Existing
agent-hours accounting retains Stop as a measured turn boundary.

### Optional JEV entry-skill suggestion

`capture_user_turn.py` may apply TypeSafe's official two-pass Skill suggestion
cookbook through TypeSafe, OpenRouter or Featherless before the model starts. The first request runs one `Choice` across the
generated registry plus three skill-need `Noul` gates. When the gate passes, a
second request reranks the top three using each skill's description and a
bounded opening excerpt from its `SKILL.md`; independent fit Nouls may reject
the entire shortlist. A surviving Choice winner is injected as one advisory
`<skill_relevance>` block. Explicit `$skill` mentions bypass JEV, and the hook
never invokes a skill itself.

The integration is off unless `FARPLANE_JEV_SKILL_SUGGESTION=1`.
`FARPLANE_JEV_PROVIDER` defaults to `typesafe`, which requires Doppler to
inject `TYPESAFE_API_KEY` and defaults to `jev-1.13.0` at
`https://api.typesafe.ai/v1/systemone`. Selecting `openrouter` uses
`OPENROUTER_API_KEY` and `typesafe/jev-1.13` at
`https://openrouter.ai/api/alpha/decisions`. Selecting `featherless` requires
Doppler to inject `FEATHERLESS_API_KEY` and defaults to
`featherless-ai/gemma-4-26B-A4B-classifier` at
`https://api.featherless.ai/v1/classifier`. The public demo is not used because
its 2k-token context cannot hold Farplane's full generated skill registry.
`FARPLANE_JEV_ENDPOINT` can override either endpoint, and `FARPLANE_JEV_MODEL`
overrides either provider default. Missing setup, invalid registry,
timeouts, API failures, malformed answers, low need, and low absolute fit all
fail open with empty hook output. API keys are never stored in tracked config
or telemetry. Enabling this feature sends the current user prompt, registry
descriptions, and bounded shortlisted skill excerpts to the selected provider.

## Issue Completion

An issue closes in the run that finishes it: one proof comment, then `gh issue
close` (`tickets/README.md`). Core has no close command, completion event,
outbox, or completion mining; the 2026-10-13 removal found that mining had not
run since tickets moved to GitHub Issues and that nothing read its findings.
Lessons from finished work are routed in the closing session to their owner
(skill, eval, validator), and the daily `report-gen` automation reads issues
closed since its last run.

## Runtime State Boundaries

Runtime state lives under ignored `.farplane/` when it is generated, mutable,
local, or too noisy for tracked config. Hooks write only small bounded records:

```text
.farplane/state/message-windows/   user-turn conversation windows
.farplane/events/                  local lifecycle events
.farplane/logs/                    hook diagnostics
.farplane/evals/runs/              eval run output
~/.farplane/state/hook-delivery/<EVENT>.json     latest telemetry delivery receipt
~/.farplane/state/stop-gate/decisions.jsonl      stop-gate decisions (metadata only)
~/.farplane/state/skill-invocations/<session>.json   per-turn skill-read claim (Codex)
```

`UserPromptSubmit` does not write singleton current-run or execution-ownership
files, and prompt text never enters hook telemetry. Work lives in GitHub
Issues, so no hook binds a thread to an issue. `farplane_console_ping.py` still
carries a `thread_id` binding for non-archived filesystem tickets under
`tickets/`; none remain, so that path never fires.

The lifecycle publisher reads the latest exact-id `thread_name` from the
append-only Codex `session_index.jsonl`. Telemetry sends only sanitized native
title metadata; a native rename is observed on the next lifecycle hook without
the Codex app server or a background watcher. Subagent and eval hooks create no
thread ownership.

Scheduled jobs keep their prompt in `farplane/automations/<job>.md`, whose
front matter names the `runtime` (`claude` or `codex`) and `runtime_task` that
runs it; the runtime's scheduler (Claude scheduled tasks today) owns cadence
execution and runtime IDs. `farplane/pm.json` only groups PM-visible thread IDs
for display; it never stores automation runtime IDs.

## Telemetry Config

Lifecycle telemetry is defined by the installed hook config.
`hooks.json` calls `hooks/lifecycle-telemetry/farplane_console_ping.py` on all four lifecycle events.
The final-response gate uses the same runtime-config precedence for its two
non-secret prose ceilings: process env, then `~/.farplane/config.toml` `[env]`,
then rendered `~/.codex/config.toml`.

`farplane_console_ping.py` loads config through Farplane Core runtime config in
this order:

1. process env
2. non-secret local settings from `~/.farplane/config.toml`
3. rendered adapter fallback `~/.codex/config.toml`

This keeps Farplane compatible with Doppler-style secret injection:
`doppler run -- farplane install`, `doppler run -- codex`, or any equivalent
runtime env source can supply API keys without making Doppler a required
Farplane dependency. `~/.farplane/config.toml` may hold local bootstrap or
UI-managed settings, but Core does not read rotatable secrets from it. See
[secret management](../fundamentals/secret-management.md).

In this Farplane checkout, use `farplane run -- <command>` as the standard
project wrapper for credentialed scripts. It checks the current project's
Doppler setup and runs `doppler run -- <command>` so skill scripts can live
under `skills/` while resolving secrets from the project scope.

Readiness and repair stay on the existing verbs: `farplane doctor` reports
Core, hook, UI, local-config, and Doppler readiness; `farplane install` performs
safe mechanical render/link/repair work and wraps its installer subprocess with
Doppler when this checkout declares Doppler and the shell is not already
Doppler-injected. Do not add a separate setup/sync command for this lifecycle.

Endpoint selection:

1. `FARPLANE_TELEMETRY_HOOKS_URL` when explicitly set
2. `FARPLANE_CONVEX_SITE_URL` plus `/telemetry/hooks`

The bunker or its setup flow may own the `~/.farplane/*` values; the Codex
install path owns symlinking `hooks.json`, the hook folders, and required Core
Python command targets into `~/.codex`, and `install.sh --runtime claude`
renders the same registration into the Claude Code plugin. `farplane hooks list`
inventories every managed command and `farplane hooks doctor --json` validates
each target and interpreter.

## Hook Rules

Global installation is primary-checkout-only. `farplane install`,
`farplane hooks install`, and direct `install.sh` execution reject linked Git
worktrees so `~/.codex` cannot be repointed at an ephemeral task checkout.

- Detect or capture cheaply.
- Keep PostToolUse checks path-scoped and deterministic. The skill-file gate
  checks only `SKILL.md` paths named by the completed patch; pre-commit repeats
  the exact 200-line invariant as the hard repository backstop.
- Keep live Stop behavior observational except for bounded continuation advice and small deterministic gates
  with explicit evidence. The final-response gate may continue a turn only to
  compress an over-limit user-facing message; it may not judge completion,
  rewrite artifacts, start new work, or treat budget-exempt presentation as
  permission to introduce more topics.
- Write only small, bounded runtime records unless an issue or skill owns the
  durable write.
- Route judgment-heavy work to skills, issues, or reviewers.
- Never auto-rewrite durable memory/context files from a hook.
- Do not use Stop hooks for completion review. Put QA evidence review and
  reviewer-lane completion review in the issue `Done / Proof` block or Goal
  program final checkpoint.

The skill-file gate may trigger the repair loop but never rewrites the file.
`harness` maintain mode owns source-preserving, responsibility-based compaction and
review; default-path behavior cannot be hidden merely to meet the envelope.

The lifecycle graph tags hook, command, runtime, and automation nodes from
`skills/harness/scripts/farplane_lifecycle_catalog.py` and the parsed
`hooks/hooks.json`; see [Graphs](graphs.md). The tags show hook boundaries
without implying that hooks are a central orchestrator.
