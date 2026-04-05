# Ticket Index

Human summary only. Keep this synced with file moves, but automation truth still lives in each ticket file plus its folder path.

## Building

- `TASK-0001` `tickets/building/TASK-0001-codex-harness-bootstrap.md` - bootstrap a safe Git-backed Codex harness repo
- `TASK-0010` `tickets/building/TASK-0010-ralph-thin-prototype.md` - implement the first runnable Ralph worker/judge/orchestrator prototype around prompt files and ticket state
- `TASK-0011` `tickets/building/TASK-0011-ralph-hook-integration-and-evals.md` - simplify the runtime to ralphplan plus ralph, wire the stop hook, and capture toy eval findings
- `TASK-0012` `tickets/building/TASK-0012-deep-interview-and-brainstorm-skills.md` - add front-end discovery skills before PRD/spec/ticket execution
- `TASK-0013` `tickets/building/TASK-0013-rewrite-ralph-skills.md` - rewrite the installed $ralph and $ralplan skill surface to the harness-native behavior

## Review

- `TASK-0003` `tickets/review/TASK-0003-codexter-evaluator-scorecard.md` - define the normalized evaluator scorecard contract for round-level pass/fail results
- `TASK-0004` `tickets/review/TASK-0004-codexter-discovery-workflow.md` - add the explicit discovery workflow for ambiguous prompts

## Todo

- `TASK-0006` `tickets/todo/TASK-0006-codexter-orchestration-loop.md` - make planner -> builder -> evaluator an explicit Codexter loop
- `TASK-0007` `tickets/todo/TASK-0007-codexter-context-policy-and-handoff.md` - define ticket-based resume, documentation, and archive/delete rules
- `TASK-0008` `tickets/todo/TASK-0008-codexter-autonomy-modes.md` - park autonomy-mode policy outside v1 until the repo deliberately re-opens post-v1 autonomy work
- `TASK-0009` `tickets/todo/TASK-0009-codexter-assisted-stop-hook.md` - keep assisted continuation quarantined outside v1 and blocked on a future post-v1 autonomy decision
- `TASK-0005` `tickets/todo/TASK-0005-codexter-passive-runtime-telemetry.md` - keep passive telemetry parked until a future post-v1 slice defines an explicit active-ticket selector for hooks

## Done

- `TASK-0002` `tickets/done/TASK-0002-codexter-ticket-metadata-foundation.md` - lock the v1 ticket metadata contract and document that assisted continuation stays outside the foundation
