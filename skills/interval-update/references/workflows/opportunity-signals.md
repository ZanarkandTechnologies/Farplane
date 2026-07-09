---
title: "Opportunity Signals Workflow"
status: active
owner: interval-update
kind: workflow-reference
template_uses:
  skill-template: "0.3.2"
---

# Opportunity Signals Workflow

## Context

Use this workflow when an interval update needs to decide whether newly surfaced
opportunities deserve attention in the next planning window. Opportunities can
come from feed-scout reports, research notes, market scans, stakeholder input,
or explicitly enabled current-web research.

This workflow should not dominate obligations. It proposes candidates and
displacement decisions; the parent interval update decides whether to create
tickets or Goal Advisor handoffs.

## Workflow Signature

```text
opportunity_signals(context_bundle, review_window, planning_window,
                    opportunity_refs?, feedback_refs?, research_policy?)
  -> candidates + defer_or_displace_decisions + source_gaps

state: reads(context_bundle, opportunity_refs?, feedback_refs?);
       writes(parent_interval_update_report_section)
gates: source_refs_present_or_not_applicable; current_web_only_when_enabled;
       displacement_named; no_task_creation
fails: chasing shiny objects; using stale public claims as current evidence;
       creating tasks without plan fit; overriding commitments without saying so
```

## Source Contract

Preferred refs:

- `context_refs.workflow_refs.opportunity_refs`: feed-scout reports, research
  notes, market scans, tracked source exports, event/grant/company lists, or
  operator-provided opportunity docs.

Supporting refs:

- feedback refs and Codex attention findings, when already present in the
  context bundle.

Use web/current external search only when the automation explicitly enables it
or when the decision requires fresh public evidence.

## Phase Boundary

Enabled `opportunity_signals` runs as a read-only subagent lane by default. The
parent interval agent may handle only mechanical source binding inline; the
lane reads the context bundle, consumes summary context first, opens raw
evidence pointers only for cited proof or source gaps, and returns opportunity
decisions for the parent report. Current web remains allowed only when policy
enables it.

## Todo List

- [ ] 1. Bind inputs.
  - [ ] If no opportunity refs exist and mode is `when_sources_exist`, return
        `not_applicable`.
  - [ ] Confirm whether current web research is enabled.
- [ ] 2. Normalize and dedupe.
  - [ ] Cluster sources by opportunity thesis.
  - [ ] Dedupe by canonical URL, source ID, or clear same-thing match.
- [ ] 3. Score fit.
  - [ ] Compare each candidate against goals, current plan, feedback,
        available attention, and actual work.
  - [ ] Label evidence freshness and confidence.
- [ ] 4. Decide displacement.
  - [ ] Mark each candidate as `pursue`, `watch`, `defer`, `reject`, or
        `needs_one_more_proof`.
  - [ ] Name what existing priority it would displace, or say
        `displaces_none`.
- [ ] 5. Return planning implications.
  - [ ] Convert only strong candidates into ticket or Goal Advisor suggestions.
  - [ ] Do not create tasks directly.

## Templates

Read-only subagent handoff:

```text
Read <context_bundle>. Run opportunity_signals for <review_window> and
<planning_window>. Use configured opportunity refs first. Use current web only
if research_policy enables it. Return candidates with source links, fit,
displacement decision, confidence, next action, and source_gaps. Do not create
tasks.
```

## Gotchas

- A good opportunity is still bad if it displaces a stronger obligation.
- “Interesting” is not enough; require a next proof or a clear fit to goals.
- Current public facts require current grounding when they may have changed.

## Reference Map

- Parent interval update loads this file only when
  `report_workflows.opportunity_signals` is enabled.

## Output

```text
candidates:
  - thesis:
    source:
    why_now:
    fit_to_goals:
    displace_existing_priority:
    decision:
    confidence:
    next_action:
defer_or_displace_decisions:
  - candidate:
    decision:
    displaced_priority:
    rationale:
source_gaps:
```
