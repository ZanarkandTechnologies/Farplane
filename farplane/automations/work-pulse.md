---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: farplane-ticket-update
name: Farplane Work Pulse
kind: heartbeat
status: active
target:
  thread_id: 019ed47a-3182-73f3-879f-a53797759b2a
schedule:
  type: interval
  interval_minutes: 30
---
Task storage override: follow tickets/README.md. Multica is dashboard-only;
resolve project bindings, keep issues unassigned, and use --no-start for updates.
Create/update task records through the existing Multica CLI, never ticket.md.
Do not invoke filesystem materializers, finalizers or dispatch based on local
migration snapshots. If a phase requires such a legacy adapter, report that
phase as unavailable; continue independent read-only reporting. Never start
Multica agents, squads, autopilots or runs.

Use $pulse-update.

Run one bounded multi-phase Work Pulse: maintenance, due review service,
dispatch, low-watermark refill, then one combined receipt. Reconcile all safe
terminal state, route at most the review chase limit without consuming a
worker, dispatch unclaimed executable tickets up to the worker limit, and call
the one adaptive next-wave planner whenever unclaimed ready supply ends below
the configured watermark. Review WIP caps operator-facing area pools; when
those pools are full, keep safe workers productive by preferring machine-
verifiable or delayed-feedback work with low immediate human load.
Human-active tickets remain unavailable but do not consume Pulse worker
capacity. Workers execute ticket programs and produce proof; do not implement
ticket bodies or wait for workers inside the heartbeat. Use Farplane V1
terminology rather than retired product or v-next language.

Overrides:
- Treat the operator as unavailable unless current context explicitly proves
  availability. Do not admit work whose positive output depends on a human
  decision, dirty cross-project mutation, publication, outreach, credentials,
  or destructive authority during an unattended window.
- Self-improvement must prevent a recurring failure through a durable forward
  mechanism and name its next-run proof. One-off historical cleanup is
  maintenance, not compounding leverage.
- After two consecutive worker create/lookup failures, open a dispatch circuit
  for that mechanism until a later successful health check. Continue safe
  planning/refill, but do not repeat the same failed launch every wake.
- Apply the structured `farplane/bindings.yaml#operator.review_chase_policy`.
  An awaiting-review ticket without a valid Review block is repair work, not a
  silent wait. Initial Telegram, due Telegram reminders, and policy-selected
  Phone Chaser calls use automation-owned credentials and are not blocked by a
  worker ticket's no-credentials boundary. Record every send/dispatch receipt
  and never infer a chase from queue size.
- Treat blocked and awaiting-review ownership narrowly. They dedupe the same
  output or prerequisite, not an entire area, KPI, audience, or objective;
  continue admitting independent non-interfering artifact work.
- Pass stable identity problems, selected objective movement, passive area
  context, and configured planning skill refs. Do not invent project goals or
  duplicate strategy state outside tickets.
- Let configured planning skills propose evidence-bound calls, then rank at
  most `wave_size` globally. Skills and areas never receive quotas.
- Query ticket/Reward history by problem, area, or configured skill when needed. For content/distribution
  hypotheses, use a relevant Tasty Pack as optional taste evidence without
  creating a content Pulse.
- Load `farplane/bindings.yaml#feed_scout.scout_brief` once when it exists and
  pass relevant complete facts, freshness/confidence, source refs, and source
  gaps to the planner. Every outward-facing admitted ticket must bind its canonical
  area ICP, a specific job or pain, a named baseline/default, the belief or
  workflow delta it should cause, and copy the selected facts into its
  `audience_context.source_facts`. A trend name or generic ICP pain is not
  enough. Self-improvement may use local
  ticket/Reward/eval evidence when external memory is irrelevant.
- Keep review tickets distinct but summarize pending review in bounded
  per-area pools. Pass review_wip to the board projection, expose active versus
  queued pools plus one deterministic digest per active area, and never drop
  underlying ticket review refs or decisions. Full pools never globally block
  unattended-safe dispatch.
- Include derived semantic_time_state in the planner input for metric
  freshness/movement, ticket delivery deadlines, matured Reward IDs, and operator
  availability validity. Serialization timestamps alone do not create novelty,
  but crossing one of those planning boundaries must change the fingerprint.

Params:
project_root = "/Users/kenjipcx/Zanarkand Technologies/projects/Farplane"
wave_size = 10
worker_limit = 4
review_wip = 3
review_chase_limit = 1
ready_low_watermark = 20

Final response:
- State the action taken or no-op reason.
- List tickets dispatched, chased, admitted, completed/reconciled, or blocked.
- Summarize refill outcome, worker/review limits, source gaps, and next owner.
- Link any report, ticket, worker, or receipt artifacts created by the beat.

Config source:
farplane/automations/work-pulse.md id="farplane-ticket-update"
