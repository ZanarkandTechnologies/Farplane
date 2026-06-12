# Adaptive Backoff

Date: 2026-06-02

## Goal

Give Farplane one small operating contract for waits that repeat: service
polling, retry loops, long-running media jobs, subagent first-write checks,
review watcher heartbeats, and remote status checks.

This is not a scheduler spec. Adaptive backoff chooses the next wait. It does
not authorize hidden daemons, always-on polling loops, automatic retries, or
background queues.

## Vocabulary

- `retry backoff`: waiting after a request failed, rate-limited, or returned an
  explicit retry hint.
- `polling backoff`: waiting after a request succeeded but the job, review,
  worker, render, or external service is still pending.
- `service hint`: provider-supplied timing such as `Retry-After`, rate-limit
  reset, estimated completion time, queue position, or next-check timestamp.
- `jitter`: a small random adjustment to avoid many agents polling at the same
  moment.
- `progress reset`: shortening the next wait after observable progress, such as
  a new status, artifact, log line, phase, or completed subtask.

## Contract

Use this shape when a workflow needs repeated waits:

```text
adaptive_backoff(
  start_delay,
  scale,
  cap,
  jitter,
  reset_on_progress,
  max_elapsed
)
```

The caller owns the workflow-specific values. The generic behavior is:

1. If the service returns a hint such as `Retry-After` or ETA, use that first
   unless it violates an explicit safety cap.
2. Start with short checks only when early feedback is useful.
3. Increase the delay by `scale` after each unchanged pending result.
4. Stop increasing at `cap`.
5. Reset or shorten the delay when progress is observed.
6. Add jitter when multiple agents, jobs, or retries might hit the same service.
7. Stop at `max_elapsed`, `max_attempts`, a terminal state, or a visible
   operator handoff.

## Default Profiles

Use these as starting points, then let the owning skill tighten them.

| Profile | Use | Suggested values |
| --- | --- | --- |
| `fast_feedback` | subagent first-write, process startup, short service warmup | `start_delay=5s`, `scale=1.5`, `cap=60s`, `jitter=10%`, `max_elapsed=10m` |
| `async_job` | images, short clips, uploads, queued transforms | `start_delay=30s`, `scale=2`, `cap=5m`, `jitter=10%`, `reset_on_progress=true` |
| `long_media` | video, upscales, large renders, batched media jobs | `start_delay=2m`, `scale=1.5`, `cap=10m`, `jitter=10%`, `reset_on_progress=true` |
| `human_review` | PR checks, reviewer comments, external approval waits | `start_delay=5m`, `scale=1.25`, `cap=15m`, `jitter=10%`, `reset_on_progress=true` |

## Workflow Rules

- Record enough state to resume: last check time, next check time, current
  delay, attempt count, status, and any service hint.
- Keep task IDs, result paths, PR numbers, worker names, and output artifacts
  in visible workspace files or ticket evidence, not terminal scrollback.
- Use a visible automation heartbeat when the workflow should resume later.
- For long waits, continue independent work instead of blocking the main agent.
- Treat repeated unchanged pending results as a signal to widen the interval.
- Treat new logs, artifacts, status changes, or partial completions as progress
  and reset or shorten the next interval.

## Boundaries

- Backoff does not create permission to launch Codex, own ticket queues, poll
  boards, retry failed phases, push code, merge PRs, deploy, or spend money.
- Backoff does not replace workflow-specific limits, Done / Proof contracts, or
  terminal-state notification rules.
- Hooks and scripts may calculate the next wait, but broad autonomy decisions
  still belong to the visible workflow, ticket, skill, or external runner.

## Consumers

- `templates/global/AGENTS.md` carries the always-loaded operating reflex.
- `skills/pr-review-watch` uses the `human_review` profile unless project
  memory declares a narrower policy.
- `skills/video-generation` and `skills/remotion-render` use `async_job` or
  `long_media` profiles for generated media and renders.
- Future deterministic scripts may add helper functions only when a concrete
  caller needs code-level enforcement.
