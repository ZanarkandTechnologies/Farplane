---
schema: farplane_project_automation
framework_template_version: 1.0.0
owner: automation-advisor
id: project-work-pulse
name: Project Work Pulse
kind: heartbeat
status: paused
target:
  thread_id: <pulse-thread-id>
schedule:
  type: interval
  interval_minutes: 30
---
Use $pulse-update.

Run one bounded multi-phase Work Pulse: maintenance, due review service,
dispatch, low-watermark refill, then one combined receipt. Reconcile all safe
terminal state, route at most the review chase limit without consuming a
worker, dispatch unclaimed executable tickets up to the worker limit, and call
the one adaptive next-wave planner whenever unclaimed ready supply ends below
the configured watermark. Review WIP backpressures dispatch, not planning.
Human-active tickets do not consume Pulse worker capacity. Workers execute
ticket programs and produce proof; do not implement ticket bodies or wait for
workers inside the heartbeat.
When the configured Feed Scout Brief exists, load it once and pass relevant
complete source-backed facts plus canonical per-area ICPs into Plan Next Wave.
Outward-facing tickets must copy selected facts into `audience_context`, name a
baseline/default and intended belief or workflow delta; Scout Brief is
evidence, not authority.

Params:
project_root = "<project-root>"
wave_size = 3
worker_limit = 1
review_wip = 3
review_chase_limit = 1
ready_low_watermark = 1

Final response:
- State the action taken or no-op reason.
- List tickets dispatched, chased, admitted, completed/reconciled, or blocked.
- Summarize refill outcome, worker/review limits, source gaps, and next owner.
- Link any report, ticket, worker, or receipt artifacts created by the beat.

Config source:
farplane/automations/work-pulse.md id="project-work-pulse"
