---
name: pulse-update
description: "Run one bounded multi-phase Work Pulse: maintain state, service due reviews, dispatch executable tickets, refill low ready supply, and write one receipt."
tier: 3
group: operations
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.2.0"
eval: evals/evals.json
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Pulse Update

## Context

`pulse-update` is one bounded Work Pulse over a project board and shared worker
pool. Every wake runs maintenance, delayed-reward handling, dispatch, review
service, and low-supply refill in order; an earlier phase never suppresses a
later eligible phase. Pulse manages tickets but never implements them.

Load [references/work-pulse-runbook.md](references/work-pulse-runbook.md) before
operating a wake. It owns guard refresh, review chase, delayed reward, clean
worker creation, refill/materialization, circuit breaker, and receipt detail.

## Skill Signature

```text
work_pulse(project_root, wave_size = 1, worker_limit = 1, review_wip = 3,
           review_chase_limit = 1, ready_low_watermark = 1, extensions?)
  -> reconciliation + maintenance_actions[] + review_service_actions[]
   + review_area_pools[] + worker_handoffs[] + refill_result? + blockers[]
   + report_ref + next_wake?
state: reads(harness/metrics/bindings/automations, ticket Goal Packets and archive,
             Reward rows, task associations/circuit state, reports, Scout Brief,
             terminal reward preferences, project manager state)
       writes(ticket state when planner calls are materialized, Pulse report,
              decision/task-association/circuit rows, project manager state)
gates: reconcile first; current healthy guards before planning; due rewards use
       original Check-In Program; review actions consume no worker; worker/wave/
       review/chase caps enforced; clean task lineage verified before claim;
       configured planner calls validated before Pulse materializes them;
       side effects remain gated; one canonical JSON receipt written
routes: plan-next-wave | goal-advisor | worker-artifact-review-request |
        telegram-message | qa | review
fails: product controller; inline implementation; check-in ticket; invented
       reward policy; manager-task fork; claim before lineage verification;
       review queue as chase or global dispatch trigger; silent no-op
```

## Automation Preset

```text
pulse-update @30m
  wave_size = 1; worker_limit = 1; review_wip = 3
  review_chase_limit = 1; ready_low_watermark = 1
```

Cadence changes wake timing only; it grants no authority or capacity.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind project policy and read the complete
      [work-pulse runbook](references/work-pulse-runbook.md). Resolve harness
      problems/areas/planning skills, metrics, board/Goal Packets, task
      associations, current reports, review policy, and side-effect gates.
- [ ] 2. Reconcile all safe mechanical state. Refresh every selected stale
      hard guard exactly once with `scripts/guard_preflight.py`; reload it
      before fingerprinting planner input. A current failure blocks admission
      on the real gap; a failed/stale refresh returns a source gap and no
      planner calls. Maintenance consumes no wave slot.
- [ ] 3. Resume each `waiting_signal` ticket whose pending Reward rows matured.
      Hand all due IDs, timestamp, evidence, and original ticket/program/
      progress to one worker to execute its Check-In Program. Never create a
      check-in ticket or reimplement its accept/kill/monitor policy.
- [ ] 4. Service review state without workers. Repair malformed Review blocks,
      verify their task identity, pool distinct tickets by canonical area for
      presentation, release completed workers, and execute only the oldest due
      policy actions up to `review_chase_limit`. Queue size never triggers a
      chase; notification authority grants nothing else.
- [ ] 5. Dispatch eligible unclaimed tickets and due check-ins within
      `worker_limit`. New workers must use clean `create_thread` with the full
      handoff, verified project and first-turn lineage, canonical title, then
      claim/association. Probe and update `scripts/dispatch_circuit.py`; never
      fork the Pulse manager or claim an unverifiable task.
- [ ] 6. After dispatch, refill whenever remaining unclaimed ready supply is
      below `ready_low_watermark`. Build one post-preflight global planning
      envelope with configured skills, stable problems, all passive area ICPs,
      objective/metric movement, semantic time, global-first history, review
      pool/operator state, current context, optional Scout Brief loaded once,
      and terminal Reward accept/kill preference rows only. Use
      `scripts/plan_wave_guard.py` to dedupe/lock the call.
- [ ] 7. Call [plan next wave](../plan-next-wave/SKILL.md), validate its exact
      configured-skill response, reserve collision-free ticket IDs, and let
      Pulse alone materialize admitted calls up to `wave_size`. Tickets store
      the selected skill, bound arguments, objective contribution, evidence,
      proof, authority, and stop boundary—not copied skill workflows.
- [ ] 8. Write one dated Pulse report and exactly one bare JSON
      `pulse_receipt`. Record every phase, guard refresh, admission/exclusion,
      planner envelope and call IDs when refill ran, worker/review receipts,
      side-effect boundary, changed state rows, blocker/no-op reason, and next
      wake. Index the report when the CLI is available.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Worker Boundary

```text
create_ticket_worker(handoff, project_target, title)
  -> create_thread(initial_prompt = handoff, target = project_target)
  -> verify(target + clean first turn + no inherited manager history)
  -> set_title("[TASK-XXXX] <ticket title>")
  -> claim + register
reject: fork_thread | claim_before_verification | title_as_identity
```

Each handoff names `ticket.md`, optional `program.md`/`progress.md`, expected
output/proof, authority gates, stop, review route, and due Reward IDs/evidence.
Workers exit after producing proof and one review request or blocker.

## Gotchas

- `wave_size` caps backlog creation; `worker_limit` caps live Pulse workers.
  Human-active tickets are commitments, not Pulse workers.
- `review_wip` caps operator-facing area pools, not tickets or concurrency;
  saturation changes selection toward unattended-safe work but blocks neither
  dispatch nor planning.
- Daily/Weekly Interval and Dogfood reports may supply context but cannot
  materialize or dispatch refill calls. Goal Advisor compiles material tickets.
- Scout Brief supplies sourced context, never planning authority. Preference
  memory comes only from terminal AI-planned Reward accept/kill rows.
- A delayed experiment without an executable Check-In Program is a source gap,
  not permission for Pulse to invent a decision policy.

## Output

Return one bare valid JSON object, never YAML, a Markdown fence, or prose. The
receipt includes phase outcomes, guard preflight, admitted/excluded work,
worker/review actions, report/state refs, and next wake. If refill ran,
`planner_call` must expose the observed canonical input, configured skills,
history, state, proposed calls, admitted IDs, and provenance. See
[references/work-pulse-runbook.md](references/work-pulse-runbook.md) for the
required schema and outcome rules.
