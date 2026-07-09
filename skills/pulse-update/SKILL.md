---
name: pulse-update
description: "Run the Farplane fast executor loop: reconcile outcomes, invoke product-local loops, delegate ready tickets, request planning when blocked, and update ledgers."
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

Use this skill for the Farplane Pulse loop: the fast manager heartbeat that
reconciles worker outcomes, admits reward-bearing ready tickets, invokes
product-local loops when new product work is needed, creates or records worker
handoffs, and writes decision state. Pulse does not own drift review, scrum
reflection, long-horizon strategy, product-boundary decisions, product workflow
contracts, product-specific next-move selection, worker implementation, or
scheduled planning. It may read Weekly and Daily strategy only as tactical
constraints.

Pulse has founder-like ambition inside hard gates, but it is no longer the
all-product idea brain. When the reward-bearing board has capacity, Pulse
chooses which product-local loops are eligible to run and lets those loops rank
the next product move from `farplane/products/<product>/product.md`,
and ignored runtime `farplane/products/<product>/progress.md`. The detailed idea compiler remains
[ticket-opportunity-generator](../ticket-opportunity-generator/SKILL.md), now
called with one product-loop context when a product loop is active. Generated
tickets must already be concrete worker work with product-backed rewards,
output artifacts, stop conditions, review surfaces, and product-loop learning
writeback; `farplane/products/<product>/product.md` owns product identity,
KPI refs, gates, and artifact workflows, while
`farplane/products/<product>/skill.md` owns workflow-specific output contracts.

Pulse itself is the manager, not a worker. It may reconcile state, repair
mechanical admission metadata on AI-planned reward-bearing tickets, write ticket
specs returned by the generator, and create worker handoffs. It must not
implement worker ticket bodies inline in the parent heartbeat. If a
worker-thread tool is unavailable, Pulse records the handoff packet in
`.farplane/automation/spawned-threads.jsonl` with a non-spawned status such as
`handoff_recorded`, leaves the ticket ready and unclaimed, and writes the reason.

Worker artifact review is also owner-routed. Pulse handoffs require workers to
use [worker-artifact-review-request](../worker-artifact-review-request/SKILL.md)
when artifacts are ready for Kenji, unless the ticket explicitly says
`review_notify: none` with a reason. Pulse reconciliation requires a Telegram
message id, skipped-duplicate receipt, or explicit blocker for completed
artifacts waiting on human review; the review skill owns the phone-readable
message contract and fallback proof.

Every Pulse mode ends with visible state writeback: decision row, report,
reward/outcome rows when applicable, spawned-thread or handoff rows when
applicable, and ticket deltas made. Do not describe a Pulse beat as complete
without naming decision/reward writeback or the reason no reward row applies.
Interval controls when Pulse wakes; policy controls what it may do.

Every Pulse mode selection begins with reconciliation. State the board
classification, worker status, review counts by product loop, each eligible
loop's `worker_budget`, each loop's `max_tickets_in_review`, and skipped-loop
reasons before invoking product loops, planning next-wave work, or creating
handoffs.

Every product-loop decision produces an explicit receipt row. For each product
loop considered, write or report `product_loop_invocation` with:
`product`, `product_ref`, `progress_ref`, `worker_budget`,
`tickets_in_review`, `max_tickets_in_review`, `decision: invoked | skipped`,
`reason`, and the resulting handoff, blocker, or review-support action.

## Product-Scoped Automation Input Contract

Product-scoped Pulse automations pass only:

```text
project_root = "<Farplane checkout>"
product = "<product id from farplane/products/<product>/product.md>"
```

Pulse must validate `product`, resolve the product config/skill/progress
paths from `farplane/products/<product>/product.md` or the generated
`farplane/products.json` registry, reconcile board and workers globally, and invoke
only that product loop for new work. Pulse must explicitly reject or ignore
automation-level `product_lane`, skill path, progress path, `review_channel`,
schedule, phone chaser behavior, or worker policy params; those belong to
`pulse-update`, product `product.md`, project bindings,
and the live automation scheduler.

## Automation Presets

`pulse-update.executor @30m -> reports.pulse`

Pulse resolves the standard Farplane project refs by default: the static
project charter, long-term goals, project bindings, local
tickets, recent interval guidance, project products, product-local
`farplane/products/<product>/skill.md` files, execution policy, spawned
threads, outcomes, rewards, reports, and `farplane/pm.json`. The live Codex
automation supplies cadence and true project extensions only. Product-scoped
automations may pass `product = "<id>"`; Pulse then reconciles globally but
invokes only that product loop for new work. Do not require automation params
for `product_lane`, skill path, progress path, `review_channel`, schedule,
phone chaser behavior, or worker policy; Pulse resolves those from product
`product.md`, generated `farplane/products.json`, project bindings, and this skill
contract. Product worker budgets come from product-loop policy rather than a
single global worker cap. Pulse owns reward reconciliation, proceedable ticket
admission, execution handoff shape, product-loop invocation receipts,
planning-request reporting, and decision/outcome ledger writes.

Empty-board behavior is bounded. If no proceedable ticket exists and no
mechanical admission repair is available, Pulse checks goals, bindings,
latest Weekly/Daily reports, product strategies, worker state, and
manual-ticket diagnostics. When those inputs are fresh and safe, Pulse invokes
eligible product loops. A product loop may call `ticket-opportunity-generator`
with its own product-loop context to produce executable specs. Pulse writes
only specs that pass the generator QA/reviewer contract and the normal
admission gates, records the product loop and reward signal being tested, and
immediately creates worker handoffs when tooling is available. If a
manager-level note, product-strategy correction, ticket closure receipt, or
prioritization judgment is required, Pulse does that directly in the parent
beat or writes `request_planning`; it must not delegate manager thinking as
worker throughput.

A human-gated final action is not an idle reason. Pulse should first search for
safe local prep, proof, research, packaging, draft, ranking, experiment,
ablation, or review-request work that can proceed while Kenji is unavailable.
Only when product strategy is missing, stale, unsafe, requires
product/goal judgment, or the safe-local-prep scan is exhausted should Pulse
write `request_planning` with the source gap, idle reason, and board evidence.

Open human-review workers are not board-wide blockers. If a worker has finished
local artifacts, AI review, QA, or a prep packet and is waiting on Kenji for
review or a final human-gated action, Pulse leaves that thread open, records the
waiting reason and last notification when visible, and asks the worker thread to
use `worker-artifact-review-request` for useful, non-noisy reminders. Pulse
records the message id, skipped-duplicate receipt, or fallback blocker and
continues safe local work when product-loop capacity remains. Review throttling
is product-local: a product loop stops creating new review-producing work when
its own `max_tickets_in_review` is reached. Pulse does not add a global review
cap in this first slice.

Review chasing is project-bound policy, not automation prompt sprawl. Pulse
reads the freeform `farplane/bindings.yaml#operator.review_chase_policy`
prompt. Pulse owns the
workflow mechanics; the binding is only Kenji's plain-language preference:
Telegram first during active hours, then phone-chaser if still stale, with
receipts or blockers instead of silence. There is no global daily phone cap in
Pulse; the repeat guard is one phone escalation per feedback item unless a new
artifact/review cycle is created. A due review wait must never end as quiet
`DONT_NOTIFY` or `request_planning`: it must produce a Telegram message id,
phone dispatch receipt, skipped-fresh/queued receipt, or blocker.

When a product loop is at `max_tickets_in_review`, Pulse skips new
review-producing work for that loop and routes the capped loop toward review
packaging, a concise Kenji chase, or existing
`worker-artifact-review-request`/Telegram reminder paths when useful. Other
product loops with capacity continue normally.

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
or has product-loop capacity after open Pulse workers are reconciled. A
manual/operator ticket like an active Taste Loop feedback ticket must not stop
Pulse from invoking product-local loops for safe product-backed autonomous
work.

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
at least one `kpi_id` must appear in a product `product.md` `kpis.*` list and
resolve to `farplane/bindings.yaml#metrics`. Human-created
tickets without that field are manual/operator tickets, not Pulse throughput.
KPI presence is necessary but not sufficient: the ticket scope must produce the
named product output or artifact workflow. Tooling, metadata, Pulse, generator,
or maintenance cleanup is admitted only as `repair_ticket_admission_state` when
it belongs to a reward-bearing AI-planned ticket or is explicitly opted in and
directly unblocks an existing product-backed ticket; do not create or delegate
it as the main next-wave product work.
New generated tickets must satisfy the `ticket-opportunity-generator`
executable spec contract, including big-claim/reach, artifact-level, dedupe,
review-surface, lifecycle metadata, and product-backed reward gates. Worker
handoffs must include `review_notify: worker-artifact-review-request` or an
explicit `review_notify: none` reason.

## Skill Signature

```text
pulse_update(project_root, product?, extensions?, pulse_policy?)
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
        farplane/bindings.yaml#operator.review_chase_policy?,
        farplane/products.json?,
        farplane/products/*/product.md?,
        farplane/products/*/skill.md?,
        farplane/products/*/progress.md?,
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
  default_refs_resolved; product_strategy_resolved_or_gap_labeled;
  strategy_inputs_resolved_or_gap_labeled;
  bindings_resolved_or_gap_labeled; product_loop_product_files_resolved_or_gap_labeled;
  product_filter_valid_or_gap_labeled;
  open_worker_threads_reconciled;
  review_chase_policy_prompt_resolved_or_gap_labeled;
  due_human_review_chases_sent_queued_or_blocked;
  extensions_merged; board_loaded; pulse_board_classified; rewards_reconciled;
  proceedable_ticket_admission_checked; product_backed_reward_checked;
  big_claim_and_artifact_level_checked_for_generated_tickets;
  worker_review_notification_recorded_for_completed_artifacts;
  done_active_tickets_archived_or_recorded; product_loop_capacity_checked;
  next_wave_tickets_rewarded_when_created; product_worker_policy_respected;
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
  Reward.kpi_rewards with expected_reward, check_in_at, and guard; planning every possible project instead of the active
  frontier; duplicating caps or cadence from heartbeat policy into interval reports;
  treating open human-review threads as board-wide blockers; using a single
  global worker or review cap as the primary product-throughput model; bundling local
  artifact creation with post/publish/spend/deploy/external-contact final
  actions when a safe prep ticket would keep throughput moving; creating worker
  tickets whose main deliverable is to plan, prioritize, refresh strategy,
  choose future tickets, or otherwise hand planning back to Pulse; creating
  generic execution tickets whose title/scope does not already name the
  concrete hypothesis, target surface, evidence source, and expected product
  contribution; selecting human-created tickets without frontmatter
  rewards.kpi and parseable Reward.kpi_rewards with check_in_at; treating manual/operator tickets as refill blockers;
  repairing manual ticket metadata without explicit operator request;
  treating generic maintenance/tooling cleanup as product throughput when it
  does not directly produce a product-lane output or unblock an existing
  product-backed ticket; writing `request_planning` only because final action
  approval is waiting; finishing worker artifacts without a Telegram review
  request receipt or explicit fallback; returning quiet `DONT_NOTIFY` when a
  human-review chase is due; treating archived completed tickets with pending
  review-cycle receipts as unchaseable; creating mid-but-valid tickets whose
  claim, surprise, baseline, artifact level, or review value is weak; bypassing
  product-loop learning writeback for generated tickets
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind policy and context.
  - [ ] Resolve standard Farplane refs for ticket board, latest interval
        guidance, latest Weekly and Daily
        strategy inputs, `farplane/goals.yaml`, `farplane/bindings.yaml`, static
        project charter, project products and lane weights, product-loop
        `product.md`/progress when present, execution policy, local product skill refs from admitted tickets, spawned thread rows,
        recent outcomes, report paths, and `farplane/pm.json`.
  - [ ] Read `farplane/bindings.yaml` for operator behavior inputs such as
        human gate tags, active-time or notification preferences when present,
        and product-loop worker policy supplied by the caller or product loop.
  - [ ] Resolve the freeform
        `farplane/bindings.yaml#operator.review_chase_policy` prompt before
        reconciling waiting review items. The binding owns Kenji's preference
        in plain language; Pulse owns cadence and receipt workflow.
  - [ ] Merge caller-supplied extensions for product budgets, gates, or
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
  - [ ] For every waiting review item, including archived completed tickets with
        a pending review-cycle receipt, classify the chase state:
        `fresh`, `queued_until_active_hours`,
        `telegram_reminder_due`, `stale_telegram_due`, `phone_due`,
        `already_phone_chased`, or `blocked`.
  - [ ] During human active hours, send or request the due worker-owned
        Telegram reminder first. If stale Telegram escalation was already sent
        and remains unanswered, follow the review chase policy prompt by
        routing one `phone-chaser` call for that feedback item or recording the
        blocker. Do not use a global daily phone cap. Outside active hours,
        record the queued chase and next active window.
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
        from product `product.md` KPI refs that resolve into
        `farplane/bindings.yaml#metrics`; each reward item should include
        `expected_reward` and `check_in_at`; the ticket scope must produce that
        product output or artifact workflow. Tickets without product-backed rewards are
        skipped as manual/operator work and do not block refill.
  - [ ] Exclude maintenance, Pulse, generator, metadata, or tooling cleanup as
        autonomous product throughput unless it directly unblocks an existing
        reward-bearing product-backed ticket. Such cleanup belongs in
        `repair_ticket_admission_state`, not a delegated worker ticket.
  - [ ] Interpret `human_gate: none | [tag, "reason"]` as a final-action gate.
        Do not execute the tagged final action without Kenji, but do not block
        local prep, artifacts, research, proof, QA, packaging, or draft work
        merely because the final action is gated.
  - [ ] Respect product-loop worker budgets, `max_tickets_in_review`, open
        child-thread limits, parallelizability notes, side-effect gates, and
        action authority.
  - [ ] Prefer tickets that match the latest interval guidance, but do not
        perform strategy ranking inside Pulse.
- [ ] 4. Choose execution mode.
  - [ ] Before selecting any mode, state the reconciled board/worker/review
        facts that justify it: proceedable ticket count, open worker count,
        tickets in review by product loop, each eligible loop's
        `worker_budget`, each loop's `max_tickets_in_review`, and any skipped
        loop reason.
  - [ ] If proceedable tickets exist, choose `delegate_ready_tickets` and spawn
        or hand off every admitted ticket up to the relevant product-loop
        worker policy.
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
        generated `farplane/products.json`,
        product configs/progress, recent Feed Scout refs when distribution may be
        selected, open Pulse worker state, manual ticket diagnostics, and
        reward-bearing AI-planned board state.
  - [ ] Invoke eligible product loops rather than scanning every product lane
        inline. Each product loop checks its own current opportunity, safe
        autonomous work, human-gate cost, worker budget, and
        `max_tickets_in_review`.
        In the Pulse report, record `product_loop_invocation` rows with
        `worker_budget`, `tickets_in_review`, `max_tickets_in_review`,
        `decision`, and `reason` for every invoked or skipped loop.
  - [ ] Check each eligible product's current strategy, active focus,
        hypothesis, constraints, and next moves before creating tickets. If a
        product strategy is missing, stale, or contradicted by fresh interval
        evidence, record the gap or override in the Pulse report.
  - [ ] Name the product loop, product-loop cycle, frontier, bottleneck, or
        reward signal being tested. Avoid creating a separate strategy ledger; the
        product-loop progress entry, Pulse report, and generated ticket
        `Reward` block are the evidence trail.
  - [ ] Run
        [ticket-opportunity-generator](../ticket-opportunity-generator/SKILL.md)
        with one product-loop context before execution-ticket creation when no
        proceedable ticket exists or the product loop's frontier is broad.
        Accept only returned executable specs that pass the generator's
        product-backed reward, lifecycle metadata, big claim/reach,
        artifact-level, dedupe, review-surface, learning-writeback, and
        no-worker-ideation gates.
  - [ ] Create only small tactical execution tickets that ladder to a current
        focus, strategy move, active project, frontier step, lane, bottleneck, or reward
        signal. Do not create tickets whose main deliverable is a plan,
        candidate ticket list, prioritization decision, strategy refresh, vague
        first proof, recommendation for what Pulse should do next, or "call the
        product skill with an idea." A generated product ticket is the concrete
        artifact sample; it uses the product skill as the process contract.
  - [ ] Do manager work in the parent beat. If the next useful move is
        product-strategy refresh, ticket closure reconciliation, frontier selection,
        or queue prioritization, apply the bounded writeback directly in the
        Pulse report/state when policy allows, or write a
        `request_planning` for Daily/Weekly when it needs product or goal
        judgment.
  - [ ] Prefer safe local work when Kenji is asleep/unavailable, review backlog
        is high, or worker threads are waiting on human feedback: local
        artifacts, research, experiment design/run, proof, QA, packaging, draft
        video/content, ranking packets, and decision packets.
  - [ ] Avoid blocky tickets that combine reversible preparation with final
        human-gated actions. Prefer `make/rank/prepare drafts` separately from
        `post/publish/spend/deploy/contact`.
  - [ ] Use product lane weights to derive product-loop worker budgets; Daily
        strategy, blockers, freshness, and proof urgency may override which
        product loop runs when the reason is recorded.
  - [ ] Every generated ticket must include frontmatter `rewards.kpi`,
        parseable `Reward.kpi_rewards[]` with `expected_reward` and
        `check_in_at` plus `guard`, and a product
        KPI/workflow contribution. Cross-product coordination KPIs are not
        enough by themselves.
  - [ ] Prefer this priority ladder:
        delegate ready unblocked work; continue the active product frontier;
        continue the main daily focus; unblock the main daily focus; improve
        proof, review, or instrumentation for the focus; prepare downstream
        work for the weekly strategy; support
        product/marketing only when it ladders to the weekly strategy; improve the
        harness only when it improves future throughput or proof; no-op only
        when safe support work would be fake progress.
  - [ ] If maintenance is selected, name the active frontier it unblocks.
  - [ ] For each admitted ticket, create a named child-thread handoff with
        objective, context refs, local product skill ref when present, gates,
        expected outputs, reward horizon, stop condition, and
        `review_notify: worker-artifact-review-request` plus
        `learning_writeback` unless review is explicitly disabled with a
        reason. Do not start implementing the ticket in the Pulse parent thread
        after creating it.
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
- product-loop invocation, skip, or review-cap reasons for next-wave planning.
- explicit statement that Pulse did not implement worker ticket bodies inline.
- side-effect and no-mutation boundary for the beat.
- expected outputs and reward horizon.
- report and state paths.

## Execution Modes

- `delegate_ready_tickets`: delegate all reward-bearing AI-planned or freshly generated
  ready, unblocked, unclaimed,
  dependency-satisfied, approval-free, non-parked, non-complete,
  parallelizable tickets to named worker threads under product-loop worker
  policy. The parent
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
- `plan_next_wave_when_empty`: when the reward-bearing AI-planned board has no
  proceedable ticket and current strategy inputs are fresh, invoke eligible
  product-local loops. Each product loop uses its collocated
  `farplane/products/<product>/product.md`,
  `farplane/products/<product>/progress.md`, recent
  tickets, open worker state, bindings, and board evidence to pick the next
  concrete move. Manual/operator tickets may be reported as diagnostics but do
  not block this mode. Treat this as a bounded test of the product loop's
  current belief, not as long-horizon strategy or a separate idea ledger.
  Worker tickets created by this mode must be pure execution tickets with a
  concrete deliverable, stop condition, explicit product KPI or artifact
  workflow contribution, and product-loop learning writeback. They must not be planning
  tickets, generic artifact tickets, "call the skill with an idea" tickets, or
  ticket generators. If the current
  frontier is broad, the product loop calls
  [ticket-opportunity-generator](../ticket-opportunity-generator/SKILL.md) with
  its product-loop context, then creates execution tickets only for selected
  concrete premises that pass big-claim/reach, artifact-level, dedupe, reward,
  review-surface, and learning-writeback gates. Immediately delegate admitted
  tickets to worker threads when tooling is available. This mode must not
  change goals, KPIs, product boundaries, external systems, cadence, spend,
  publishing, or customer contact. If the frontier points at a gated final
  action, create or select a safe local prep/research/proof/draft/ranking
  ticket instead of the final action.
- `request_planning`: write a planning request for Daily or Weekly Interval
  when the board lacks executable work, needs product/goal judgment, or the
  safe-local-prep scan is exhausted. Do not request planning merely because a
  final human gate is waiting. Include queue evidence, idle reason, safe-local
  alternatives considered, and suggested planning scope.
- `no_op_blocked`: stop only when execution, repair, and planning request are
  all blocked, unsafe, or would create noisy work.
