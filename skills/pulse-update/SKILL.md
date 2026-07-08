---
name: pulse-update
description: "Run the Farplane fast executor loop: reconcile outcomes, delegate ready tickets up to policy cap, request planning when blocked, and update ledgers."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.1.0"
eval: eval_task.json
allowed-tools: Read, Write, Glob, Grep, Bash

---

# Pulse Update

## Context

Use this skill for the Farplane Pulse loop: immediate attention, worker
portfolio management, reward reconciliation, ready-ticket delegation, tactical
next-wave planning, and worker handoff writeback. It does not own drift review,
scrum reflection, strategy, product-boundary decisions, or scheduled planning.
It may read Weekly and Daily strategy as constraints. Its job is to keep useful
worker throughput high inside policy: delegate the board, manage open worker
threads, remind or record waiting human-review workers when useful, and when the
board is empty instantiate the next safe tactical wave from already-accepted
strategy.
Pulse should have founder-like ambition inside these gates: generate bold,
bounded tactical ideas from the current `farplane/ops-memory.md` belief state,
fresh strategy inputs, and board evidence, then let Daily and Weekly intervals
challenge that belief from observed outcomes. Do not add a separate idea ledger;
use Pulse reports, interval reports, tickets, rewards, metrics, and ops memory.
Planning stays in the parent Pulse beat. Worker tickets are for execution: every
ticket Pulse creates or admits must be immediately actionable by a worker and
must produce a concrete artifact, proof packet, local state change, QA result,
draft, rendered asset, dataset, or reviewable packet that advances a named
`farplane/products.md` product, lane, or artifact workflow. An artifact is not
enough by itself; it must contribute to the product portfolio instead of being
generic busywork. Do not create tickets whose main output is planning more
tickets, choosing a direction, refreshing strategy, or deciding what should be
done next.
Reviewer receipts, human-review reminders, and approval pings are manager or
worker follow-up lanes; they are not product throughput by themselves.
Pulse itself is the manager, not a worker. It may reconcile state, repair
mechanical metadata on AI-planned reward-bearing tickets, create ticket specs,
and create worker handoffs, but it must not implement a worker ticket inline in
the parent heartbeat. Once a ticket is created or admitted, the next action is
a named worker-thread handoff up to policy cap. If a worker-thread tool is
unavailable, Pulse records the handoff packet in
`.farplane/automation/spawned-threads.jsonl` with a non-spawned status such as
`handoff_recorded`, leaves the ticket ready and unclaimed, and writes the
reason instead of doing the implementation itself.
Every Pulse mode ends with visible state writeback: decision row, report,
reward/outcome rows when applicable, spawned-thread or handoff rows when
applicable, and the ticket deltas that were made. Do not describe a Pulse beat
as complete without naming decision/reward writeback or the reason no reward
row applies.
Before creating execution tickets, Pulse must call or follow
[ticket-opportunity-generator](../ticket-opportunity-generator/SKILL.md), or
delegate bounded scout/research workers whose output is an opportunity packet,
not the final ticket wave. The final worker tickets must already contain the
specific idea: named feature, code area, artifact, evidence source, hypothesis,
baseline/variant or audience/hook, expected reward, and stop condition. They
must also carry the generator's big-claim/reach gate: audience or operator
tension, why the result might surprise, dedupe status, artifact level, and
review surface.
Generic tickets like "create first ablation proof", "write evidence content",
or "find experiment candidates" are failures. Good tickets look like "Ablate
proof-ticket template against no template on recent closeouts" or "Draft content
on how ticket structure prevents false completion, grounded in TASK-0275 and
closure-gate evidence."
Next-wave planning scans product lanes before ticket creation and returns a
portfolio wave, not a default single ticket. Size the wave by worker cap, useful
lane diversity, and specificity. A one-ticket wave needs an explicit reason:
worker cap is one, or only one premise survived the evidence, specificity, and
autonomy gates. Pulse must not mutate goals, KPIs, product boundaries, external
accounts, spend, publishing, deploys, customer contact, cadence, or caps during
that wave; it creates local prep/proof/draft/research tickets instead.
When asked what Pulse should do, answer with operational receipts, not only the
conceptual route. Minimum answer/report fields are: admitted/excluded tickets;
selected/skipped product lanes with lane-weight or Daily/Weekly override
reasons; generated ticket specs with frontmatter `rewards.kpi`, parseable body
`Reward.kpi_rewards[]`, and `guard`; normal admission gates before delegation,
named as ready true,
approval false, blockers empty, dependencies satisfied, claim empty,
not complete/done, not parked, and no external credential blocker; execution
mode; named worker-thread handoffs or blocked-handoff reason; explicit
no-inline-implementation statement for worker tickets; side-effect/no-mutation
boundary; and decision/reward/report writeback paths or the reason a row does
not apply.

This skill should be easy to pilot by changing cadence and extensions, without
rewriting the action logic. Interval controls when Pulse wakes; policy controls
what it may do.

## Automation Presets

`pulse-update.executor @30m -> reports.pulse`

Pulse resolves the standard Farplane project refs by default: the static
project charter, long-term goals, project bindings, active ops memory, local
tickets, recent interval guidance, project products, local product skill refs
under `.agents/skills/`, execution policy, spawned threads, outcomes, rewards,
reports, and
`farplane/pm.json`. The live Codex automation supplies cadence, concurrency cap,
and true project extensions only. Pulse owns reward reconciliation, proceedable
ticket admission, execution handoff shape, planning-request reporting, and
decision/outcome ledger writes.

Empty-board behavior is bounded. If no proceedable ticket exists and no
mechanical admission repair is available, Pulse first checks
`farplane/goals.yaml`, `farplane/bindings.yaml`, `farplane/ops-memory.md` when
present, the latest Weekly and Daily strategy inputs, and
`farplane/products.md` lane weights. Ops memory supplies the active focus,
active projects, managed open worker notes, critical paths, next frontier,
constraints, and parking lot. When those inputs are fresh and safe, Pulse may
create a small next wave of tactical tickets from the active frontier and
immediately admit them through the same hard gates. Each next-wave decision
should name the active belief, frontier, bottleneck, or reward signal being
tested so the next Daily or Weekly report can keep, revise, or drop that
belief. If a manager-level note, ops-memory correction, ticket closure receipt,
or prioritization judgment is required, Pulse should do that directly in the
parent beat or write `request_planning`; it should not delegate that thinking
as a worker ticket. A human-gated final action is not, by itself, an idle
reason. Pulse should first search for safe local prep, proof, research,
packaging, draft, ranking, experiment, ablation, or review-request work that
can proceed while Kenji is away. Only when strategy or ops memory is missing,
stale, unsafe, requires product/goal judgment, or the safe-local-prep scan is
exhausted should Pulse write `request_planning` with the source gap, idle
reason, and board evidence.
When the frontier points to experiments, ablations, market learning, or
distribution, Pulse should use
[ticket-opportunity-generator](../ticket-opportunity-generator/SKILL.md) to
mine current goals, products, ops memory, recent completed tickets, artifacts,
code/skill hotspots, rewards, metrics, and reports before ticket creation. It
may ask bounded scout workers to return ranked premises, but the execution
ticket it finally creates must name the selected premise and must be runnable
without further ideation.

Open human-review workers are not board-wide blockers. If a worker has finished
local artifacts, AI review, QA, or a prep packet and is waiting on Kenji for
review or a final human-gated action, Pulse should leave that thread open,
record the waiting reason in the report or ops memory, ask the worker thread to
send a phone-viewable Telegram reminder through
[worker-artifact-review-request](../worker-artifact-review-request/SKILL.md)
or [telegram-message](../telegram-message/SKILL.md) when the reminder is useful
and not noisy, record the message id or fallback receipt, and escalate through
[phone-chaser](../phone-chaser/SKILL.md) when the Telegram request is unanswered
past the configured chase window or is an urgent Kenji-facing blocker. Then
continue safe local work when capacity remains. Human review backlog should
bias Pulse away from spawning more human-review-heavy tickets and toward local
artifact, research, experiment, proof, QA, packaging, or draft content work.

Pulse board state is not the same as the active ticket directory. Tickets do
not need `created_by`: AI-planned work is identified by frontmatter
`rewards.kpi`. The body `## Reward` block carries expected reward details and
guards. The spawned-thread ledger is worker state, not ticket-origin state. At
the start of board admission, run or emulate
`python3 skills/pulse-update/scripts/list_pulse_board.py --project-root <root>`
and separate:

- `ai_generated_active_tickets`: active tickets with frontmatter
  `rewards.kpi`; `pulse_managed_active_tickets` is a compatibility alias for
  this set.
- `manual_active_tickets`: active tickets without frontmatter `rewards.kpi`.
  They
  may be reported as operator work, but they are not Pulse throughput, do not
  block refill, and must not be repaired unless Kenji explicitly asks or they
  are opted into AI planning by adding a valid reward block.
- `open_pulse_workers`: spawned ledger rows still waiting for reward,
  completion, human review, final action, or unblock, and whose ticket still
  exists on the active board.
- `stale_open_worker_rows`: spawned ledger rows that look open but whose ticket
  is no longer active. They are reconciliation diagnostics, not refill
  blockers.

`plan_next_wave_when_empty` means the reward-bearing AI-planned board is empty
or has spare capacity after open Pulse workers are reconciled. A manual/operator
ticket like an active Taste Loop feedback ticket must not stop Pulse from
planning safe product-backed autonomous work.

Proceedable ticket selection is a hard gate. Pulse must not select local ticket
implementation work unless the ticket is `ready: true`,
`approval_required: false`, `blocked_by: []`, `claimed_by:` empty, dependency
satisfied, not `phase: complete` or `status: done`, not parked, and not waiting
on external credentials or other non-computer-actionable input. A compact
`human_gate` frontmatter value is a final-action gate, not a ticket-start gate:
`human_gate: none` means the worker can finish normally; `human_gate: [tag,
"reason"]` means the worker may prepare local artifacts and proof but must stop
before the tagged final action. Gate tags are project policy from
`farplane/bindings.yaml` `human_gates`, such as `post`, `publish`, `spend`,
`deploy`, `external_contact`, `account_mutation`, or `destructive_cleanup`.
Autonomous Pulse selection also requires frontmatter `rewards.kpi` or explicit
operator opt-in plus product-backed reward attribution. The ticket body must
also contain a parseable `## Reward` fenced YAML block with `kpi_rewards[]`, and
at least one `kpi_id` must appear in
`farplane/bindings.yaml` `metrics` with a `product` that maps to a product,
work lane, or artifact workflow in `farplane/products.md`. Human-created
tickets without that field are manual/operator tickets, not Pulse throughput.
KPI presence is necessary but not sufficient: the ticket scope must produce the
named product output or artifact workflow. Tooling, metadata, Pulse, generator,
or maintenance cleanup is admitted only as `repair_ticket_admission_state` when
it belongs to a reward-bearing AI-planned ticket or is explicitly opted in and
directly unblocks an existing product-backed ticket; do not create or delegate
it as the main next-wave product work.
New generated tickets must also name `big_claim`, `audience_tension` or
operator tension, `surprise_factor`, `dedupe_status`, `artifact_level`, and
`review_surface`. Worker handoffs must tell the worker to send or record a
Telegram review request with archive-safe artifact links when the artifact is
ready, then use `phone-chaser` if that review request is ignored past the
configured chase window, unless the ticket explicitly says `review_notify: none`
with a reason.

## Skill Signature

```text
pulse_update(project_root, extensions?, pulse_policy?)
  -> reward_update
   + execution_mode
   + child_thread_handoffs?
   + next_wave_ticket_deltas?
   + planning_request?
   + decision_row
   + ledger_delta

state:
  reads(farplane/harness.md?,
        farplane/goals.yaml?,
        farplane/bindings.yaml?,
        farplane/products.md?,
        farplane/ops-memory.md?,
        .agents/skills/**/SKILL.md?,
        .farplane/reports/interval/**?,
        .farplane/feed-scout/daily/*.json?,
        .farplane/reports/feed-scout/*?,
        .farplane/feed-scout/ledger.jsonl?,
        .farplane/automation/heartbeat-policy.json,
        .farplane/automation/spawned-threads.jsonl,
        .farplane/automation/action-outcomes.jsonl,
        tickets/TASK-*/ticket.md,
        skills/pulse-update/scripts/list_pulse_board.py?,
        farplane/pm.json?)
  writes(.farplane/reports/pulse/<YYYY-MM-DDTHHMMSSZ>.md,
         .farplane/automation/decisions.jsonl,
         .farplane/automation/spawned-threads.jsonl,
         .farplane/automation/rewards.jsonl,
         tickets/TASK-*/ticket.md when plan_next_wave_when_empty creates safe tactical tickets,
         farplane/pm.json when persistent PM-owned worker threads are spawned)

gates:
  default_refs_resolved; ops_memory_resolved_or_gap_labeled;
  strategy_inputs_resolved_or_gap_labeled;
  bindings_resolved_or_gap_labeled; open_worker_threads_reconciled;
  extensions_merged; board_loaded; pulse_board_classified; rewards_reconciled;
  proceedable_ticket_admission_checked; product_backed_reward_checked;
  big_claim_and_artifact_level_checked_for_generated_tickets;
  worker_review_notification_recorded_for_completed_artifacts;
  done_active_tickets_archived_or_recorded; lane_weight_bias_checked;
  next_wave_tickets_rewarded_when_created; delegation_cap_respected;
  side_effect_gates_respected; decision_recorded; report_ref_frontmatter_written;
  pm_thread_grouping_updated_when_persistent

routes:
  ticket-opportunity-generator | goal-advisor | impl-plan | feed-scout | skill-maintenance |
  worker-artifact-review-request | telegram-message | eval | qa | review

fails:
  performing drift review or weekly scrum planning; rediscovering strategy
  every beat; creating strategy-shaped or unsafe refill tickets in Pulse;
  implementing worker tickets in the parent heartbeat; treating goal-advisor as the
  default empty-board fallback; treating interval as authority;
  skipping reward/outcome writeback; using planner-level exploration before
  reward learning proves value; generating tickets without parseable
  Reward.kpi_rewards plus guard; planning every possible project instead of the active
  frontier; duplicating caps or cadence from heartbeat policy into ops memory;
  treating open human-review threads as board-wide blockers; bundling local
  artifact creation with post/publish/spend/deploy/external-contact final
  actions when a safe prep ticket would keep throughput moving; creating worker
  tickets whose main deliverable is to plan, prioritize, refresh strategy,
  choose future tickets, or otherwise hand planning back to Pulse; creating
  generic execution tickets whose title/scope does not already name the
  concrete hypothesis, target surface, evidence source, and expected product
  contribution; selecting human-created tickets without frontmatter
  rewards.kpi and parseable Reward.kpi_rewards; treating manual/operator tickets as refill blockers;
  repairing manual ticket metadata without explicit operator request;
  treating generic maintenance/tooling cleanup as product throughput when it
  does not directly produce a products.md output or unblock an existing
  product-backed ticket; writing `request_planning` only because final action
  approval is waiting; finishing worker artifacts without a Telegram review
  request receipt or explicit fallback; creating mid-but-valid tickets whose
  claim, surprise, baseline, artifact level, or review value is weak
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind policy and context.
  - [ ] Resolve standard Farplane refs for ticket board, `farplane/ops-memory.md`
        when present, latest interval guidance, latest Weekly and Daily
        strategy inputs, `farplane/goals.yaml`, `farplane/bindings.yaml`, static
        project charter, project products and lane weights, execution policy,
        local product skill refs from admitted tickets, spawned thread rows,
        recent outcomes, report paths, and `farplane/pm.json`.
  - [ ] Read `farplane/bindings.yaml` for operator behavior inputs such as
        human gate tags, active-time or notification preferences when present,
        and worker-cap extensions supplied by the caller or policy.
  - [ ] Merge caller-supplied extensions for delegation caps, budgets, gates, or
        extra context refs.
  - [ ] Treat Weekly/Daily strategy as constraints and tactical inputs only; do
        not perform drift review, KPI mutation, product-boundary decisions, or
        weekly scrum planning inside Pulse.
- [ ] 2. Reconcile previous outcomes.
  - [ ] Inspect prior spawned thread rows and expected outputs.
  - [ ] Inspect open worker/thread rows or app-visible worker state when
        available. Classify completed, active, waiting-human-review, waiting
        final-action, blocked, stale, and missing-output workers.
  - [ ] Move or record active tickets that are already `phase: complete` or
        `status: done` for archiving before board selection. They are not
        proceedable work. If safe filesystem archive is available, move
        `tickets/TASK-XXXX/` to `tickets/archive/TASK-XXXX/`; otherwise write
        the exact archive-needed receipt.
  - [ ] For waiting human-review or final-action workers, record the ticket,
        thread id, waiting reason, last notification when visible, and whether
        a worker-context Telegram reminder is useful or noisy. Do not let those
        workers block safe unrelated work.
  - [ ] If a finished worker artifact has no review notification receipt, use
        `worker-artifact-review-request` or ask the worker thread to send one:
        archive-safe artifact refs, phone-readable summary, one reply action,
        and message id or fallback receipt.
  - [ ] Apply immediate rewards for completed, partial, blocked, noisy, or
        missing-output child work.
  - [ ] Avoid double-counting already rewarded outcomes.
- [ ] 3. Admit ready tickets.
  - [ ] Run or emulate
        `python3 skills/pulse-update/scripts/list_pulse_board.py --project-root <root>`
        and classify active tickets into reward-bearing AI-planned,
        manual/operator, and
        archive-needed sets before admission.
  - [ ] Build the proceedable set from reward-bearing AI-planned ticket state
        plus any freshly generated tickets in this beat. Treat `ready: false`,
        `approval_required: true`, nonempty `blocked_by`, nonempty
        `claimed_by`, incomplete dependencies, `phase: complete`,
        `status: done`, parked next actions, external credential blockers, and
        non-computer-actionable blockers as hard exclusions.
  - [ ] Require frontmatter `rewards.kpi` plus product-backed
        `Reward.kpi_rewards[]` before autonomous delegation. Each admitted
        ticket must already have the frontmatter marker plus parseable reward
        block, be freshly generated by Pulse with both fields, or be explicitly
        opted in by operator instruction; it must name at least one `kpi_id`
        from `farplane/bindings.yaml` metrics whose product maps into
        `farplane/products.md`; the ticket scope must produce that product
        output or artifact workflow. Tickets without product-backed rewards are
        skipped as manual/operator work and do not block refill.
  - [ ] Exclude maintenance, Pulse, generator, metadata, or tooling cleanup as
        autonomous product throughput unless it directly unblocks an existing
        reward-bearing product-backed ticket. Such cleanup belongs in
        `repair_ticket_admission_state`, not a delegated worker ticket.
  - [ ] Interpret `human_gate: none | [tag, "reason"]` as a final-action gate.
        Do not execute the tagged final action without Kenji, but do not block
        local prep, artifacts, research, proof, QA, packaging, or draft work
        merely because the final action is gated.
  - [ ] Respect `maxChildThreadsPerBeat`, open child-thread limits,
        parallelizability notes, side-effect gates, and action authority.
  - [ ] Prefer tickets that match the latest interval guidance, but do not
        perform strategy ranking inside Pulse.
- [ ] 4. Choose execution mode.
  - [ ] If proceedable tickets exist, choose `delegate_ready_tickets` and spawn
        or hand off every admitted ticket up to policy cap.
  - [ ] If no ticket is proceedable but a purely mechanical ticket metadata or
        proof-state repair would make an existing reward-bearing AI-planned ticket
        executable, choose `repair_ticket_admission_state`.
  - [ ] If no reward-bearing AI-planned executable work exists and fresh Weekly/Daily
        strategy can be converted into safe tactical work, choose
        `plan_next_wave_when_empty`.
  - [ ] If no executable work exists because the queue is empty, vague, stale,
        blocked by product/goal judgment, unsafe, or undersupplied, first run a
        safe-local-prep scan for artifact, proof, research, packaging, draft,
        ranking, experiment, ablation, or review-request work that can proceed
        without Kenji. Choose `request_planning` only when that scan is
        exhausted or would create fake progress.
  - [ ] Choose `no_op_blocked` only when execution, mechanical repair, and
        planning request are all blocked or unsafe.
- [ ] 5. Plan, spawn, or record.
  - [ ] For `plan_next_wave_when_empty`, read the latest Weekly strategy, Daily
        strategy, `farplane/goals.yaml`, `farplane/bindings.yaml`,
        `farplane/ops-memory.md` when present, `farplane/products.md` lane
        weights, recent Feed Scout reports or daily JSON when distribution may
        be selected, open Pulse worker state, manual ticket diagnostics, and
        reward-bearing AI-planned board state.
  - [ ] Scan every product lane or artifact workflow in `farplane/products.md`
        for progress blockers, current opportunity, safe autonomous work, and
        human-gate cost. Record selected and skipped lanes with compact reasons.
        Do not create exactly one ticket by default; create a wave sized by
        worker cap, useful diversity, and specificity. A one-ticket wave is
        valid only when worker cap is one or only one premise survives the
        specificity and autonomy gates.
  - [ ] Check the active focus, active projects, critical paths, next frontier,
        constraints, and parking lot before creating tickets. If ops memory is
        missing, stale, or contradicted by fresh interval strategy, record the
        gap or override in the Pulse report.
  - [ ] Name the current ops-memory belief, frontier, bottleneck, or reward
        signal being tested. Avoid creating a new idea ledger; the Pulse report
        and generated ticket `Reward` block are the evidence trail.
  - [ ] Run
        [ticket-opportunity-generator](../ticket-opportunity-generator/SKILL.md)
        before ticket creation when the frontier is broad. Use it to mine
        recent completed tickets, artifacts, rewards, metrics, reports,
        Feed Scout trend tensions, leverage-advisor style compounding bets,
        code/skill hotspots, and product goals for concrete premises. If
        needed, delegate bounded scout workers to return ranked premises, but
        do not treat scout output as the final execution ticket wave.
  - [ ] Create only small tactical tickets that ladder to a current focus, bet,
        active project, frontier step, lane, bottleneck, or reward signal.
        Generated tickets must be pure execution tickets: immediately
        actionable, scoped to a concrete output, and able to finish with an
        artifact, proof packet, local state change, QA result, draft, rendered
        asset, dataset, or reviewable packet that advances a named product, lane,
        product reward, or artifact workflow from `farplane/products.md`.
        Require the ticket summary, scope, or reward block to name that
        products.md contribution.
  - [ ] Require the big-claim/reach gate for every generated worker ticket:
        external or operator-facing claim, why it matters now, what would make
        the result surprising, baseline or contrast, dedupe status, artifact
        level, and review surface. Reject specific-but-boring tickets rather
        than handing them to workers.
  - [ ] Require specificity in generated ticket premises:
        - ablation tickets name the feature/behavior under test, baseline,
          variant, measurement surface, and expected decision.
        - experiment tickets name the code/skill/process area to tighten,
          proposed change, measurement, and expected reward.
        - content tickets name the harness-engineering insight, source evidence,
          target audience, hook angle, and produced format.
        - market-learning tickets name the source/entity/question and the
          decision the artifact will inform.
        Do not create tickets whose main deliverable is a plan, candidate
        ticket list, prioritization decision, strategy refresh, vague first
        proof, or recommendation for what Pulse should do next.
  - [ ] Do manager work in the parent beat. If the next useful move is
        ops-memory refresh, ticket closure reconciliation, frontier selection,
        or queue prioritization, apply the bounded writeback directly in the
        Pulse report/state/ops-memory when policy allows, or write a
        `request_planning` for Daily/Weekly when it needs product or goal
        judgment.
  - [ ] Prefer safe local work when Kenji is asleep/unavailable, review backlog
        is high, or worker threads are waiting on human feedback: local
        artifacts, research, experiment design/run, proof, QA, packaging, draft
        video/content, ranking packets, and decision packets.
  - [ ] Avoid blocky tickets that combine reversible preparation with final
        human-gated actions. Prefer `make/rank/prepare drafts` separately from
        `post/publish/spend/deploy/contact`.
  - [ ] Use product lane weights as selection bias when several equally safe
        slices are available; Daily strategy, blockers, freshness, and proof
        urgency may override the bias when the reason is recorded.
  - [ ] Every generated ticket must include frontmatter `rewards.kpi` and
        parseable `Reward.kpi_rewards[]` plus `guard`, using KPI IDs from
        `farplane/bindings.yaml` metrics and a products.md product/workflow
        contribution. Do not use cross-product coordination KPIs as the only
        justification for a worker ticket.
  - [ ] Prefer this priority ladder:
        delegate ready unblocked work; continue the active ops-memory frontier;
        continue the main daily focus; unblock the main daily focus; improve
        proof, review, or instrumentation for the focus; prepare downstream
        work for the weekly bet; support
        product/marketing only when it ladders to the weekly bet; improve the
        harness only when it improves future throughput or proof; no-op only
        when safe support work would be fake progress.
  - [ ] If maintenance is selected, name the active frontier it unblocks.
  - [ ] For each admitted ticket, create a named child-thread handoff with
        objective, context refs, local product skill ref when present, gates,
        expected outputs, reward horizon, stop condition, and `review_notify`
        instruction to use `worker-artifact-review-request` when the artifact
        is ready. The worker must bind `feedback_channel=telegram`,
        `feedback_policy=ask_when_artifact_ready`, and its worker-thread reply
        route; send a Telegram review request with a phone-readable teaser and
        archive-safe artifact refs; write the review-cycle receipt; and satisfy
        the turn exit gate before stopping. Fallback is allowed only after
        `telegram-message` proves the send route, credentials, or
        phone-readable review surface is unavailable and records the exact
        blocker; do not write tickets where "archive-safe fallback" is the
        normal review deliverable. Do not start implementing the ticket in the
        Pulse parent thread after creating it.
  - [ ] For every new next-wave ticket, immediately create the worker-thread
        handoff in the same beat when tooling is available. When tooling is not
        available, write a spawned-thread ledger row with `status:
        handoff_recorded`, leave the ticket ready, unclaimed, and waiting for
        worker spawn; do not consume the ticket inline as a fallback.
  - [ ] For managed waiting workers, leave the worker thread open and let that
        worker own follow-up when Kenji replies. Pulse may ask the worker thread
        to send a reminder or summarize state, but should not create a duplicate
        approval queue.
  - [ ] If the child is a persistent PM-owned worker chat that should appear
        under the project employee in the UI, append its thread ID to
        `farplane/pm.json` `threads.chats`.
  - [ ] If no child is needed, write the repair or planning request result
        directly.
- [ ] 6. Write decision state.
  - [ ] Append decision, spawned-thread, reward, and report rows.
  - [ ] Write a date-stamped Pulse report and keep newest-report pointers in
        state when needed.
  - [ ] Include minimal Core report frontmatter: `ref:
        reports/pulse/<YYYY-MM-DDTHHMMSSZ>`, `kind: pulse`, `created_at`, and
        `ui_summary`.
  - [ ] Run `farplane reports index --project-root <project_root>` after
        writing the report when the CLI is available.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- execution mode.
- reward update summary.
- child thread ids, repair result, planning request, or blocked reason.
- admitted/excluded ticket summary and named worker-thread handoffs.
- worker artifact review notification receipts or fallback reasons for
  completed artifacts awaiting Kenji.
- selected/skipped product lane reasons for next-wave planning.
- explicit statement that Pulse did not implement worker ticket bodies inline.
- side-effect and no-mutation boundary for the beat.
- expected outputs and reward horizon.
- report and state paths.

## Execution Modes

- `delegate_ready_tickets`: delegate all reward-bearing AI-planned or freshly generated
  ready, unblocked, unclaimed,
  dependency-satisfied, approval-free, non-parked, non-complete,
  parallelizable tickets to named worker threads up to policy cap. The parent
  Pulse beat may prepare context, spawn or record handoffs, and write state, but
  it must not implement the ticket body inline.
- `execute_ready_tickets`: legacy alias for `delegate_ready_tickets` in old
  reports only. New Pulse decisions should use `delegate_ready_tickets`.
- `manage_worker_portfolio`: reconcile open workers, reward finished workers,
  leave human-review/final-action workers open, send or request bounded
  worker-context reminders through `worker-artifact-review-request` or
  `telegram-message` when useful, record message id or fallback receipt, and
  keep selecting safe local work rather than no-oping behind human review.
- `repair_ticket_admission_state`: perform only mechanical repair that can make
  an existing reward-bearing AI-planned ticket executable, such as stale
  ready/approval/phase metadata or missing proof-state links. Do not repair
  manual/operator tickets here unless Kenji explicitly opted them in with a
  valid reward block, and do not make product or strategy decisions here.
- `plan_next_wave_when_empty`: when the reward-bearing AI-planned board has no proceedable
  ticket and current strategy inputs are fresh, scan product lanes and create a
  small wave of tactical tickets from ops-memory active frontier, Weekly/Daily
  strategy, product lane weights, open Pulse worker state, bindings, and board
  evidence. Manual/operator tickets may be reported as diagnostics but do not
  block this mode. Treat
  this as a bounded test of Pulse's current operating belief, not as
  long-horizon strategy or a separate idea ledger. Planning and prioritization
  happen inside this parent beat; worker tickets created by this mode must be
  pure execution tickets with a concrete deliverable, stop condition, and
  explicit `farplane/products.md` contribution, not planning tickets, generic
  artifact tickets, or ticket generators. They must pass the big-claim/reach
  gate: audience or operator tension, surprise factor, strong baseline or
  contrast, dedupe status, sufficient artifact level, and review surface. The
  expected output is a portfolio
  wave sized by worker cap and useful lane diversity, with selected and skipped
  lane reasons. A one-ticket wave is allowed only when the cap is one or only
  one premise survives specificity, evidence, and autonomy gates. If the
  current frontier is broad, this mode first performs or delegates opportunity
  discovery through
  [ticket-opportunity-generator](../ticket-opportunity-generator/SKILL.md),
  then creates execution tickets only for the selected concrete premises and
  immediately delegates them to worker threads. The
  mode must not change goals, KPIs, product
  boundaries, external systems, cadence, caps, spend, publishing, or customer
  contact. Generated tickets require frontmatter `rewards.kpi`, parseable
  `Reward.kpi_rewards[]` plus `guard`, and must pass normal admission gates
  before delegation. If the frontier
  points at a gated final action, create or select a safe local prep/research/
  proof/draft/ranking ticket instead of the final action.
- `request_planning`: write a planning request for Daily or Weekly Interval
  when the board lacks executable work, needs product/goal judgment, or the
  safe-local-prep scan is exhausted. Do not request planning merely because a
  final human gate is waiting. Include queue evidence, idle reason, safe-local
  alternatives considered, and suggested planning scope.
- `no_op_blocked`: stop only when execution, repair, and planning request are
  all blocked, unsafe, or would create noisy work.
