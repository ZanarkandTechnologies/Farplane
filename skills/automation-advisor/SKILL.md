---
name: automation-advisor
description: "Design or revise Farplane Codex automations using project-owned automations.toml records and generic Pulse/Interval skill calls."
tier: 3
group: operations
source: local
eval: evals/evals.json
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.2.0"
qa_checklist: qa_checklist.md
allowed-tools: Read, Glob, Grep, Bash
---

# Automation Advisor

## Context

Use this skill to create, revise, or audit Farplane Codex automations. Work
Pulse is the only base heartbeat. Feed Scout, Daily/Weekly Interval, Dogfood,
and low-frequency maintenance remain separate `cron` records; Work Pulse is
the shared ticket executor.

Keep the full desired record in `farplane/automations.toml`: id, name, kind,
status, target, schedule, and the exact prompt copied into Codex. Runtime IDs,
logs, and mutable memory stay in the Codex automation store or ignored
`.farplane/` state. Do not add a compiler, scheduler thread, or second manifest.

Automation prompts call one owning `$skill-name`, name only human-editable
params and project-specific sources/gates, and leave generic workflow logic in
the skill. Daily and Weekly call `$interval-update`; Daily projects candidates
into one current weekly draft and Weekly owns selective promotion into
canonical knowledge owners.

## Skill Signature

```text
automation_advisor(intent, project_refs, current_automation?, activate?)
  -> template_choice + config_delta + automation_delta?
   + persistent_thread_delta? + state_contract_check + proof_checklist
state: reads(active feature/spec, farplane/automations.toml?, current prompts,
             target skill, templates, qa_checklist.md);
       writes(farplane/automations.toml and, only for an explicit persistent
              thread, farplane/pm.json)
gates: loop_choice; cadence; plain_skill_call; full_parseable_record;
  no_contract_duplication; side_effect_gates; dated_artifacts;
  one_heartbeat; no_hidden_scheduler
routes: pulse-update | interval-update | feed-scout | dogfood-review |
  goal-advisor | review
fails: logs in tracked config; generated prompt fragments; env-var schedules;
  second heartbeat; legacy orchestrator; bare receipt with no useful summary
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Classify the recurring job.
  - [ ] Choose Pulse, Interval, Feed Scout, Dogfood, optional scheduled skill
        work, one-off ticket work, or no automation.
  - [ ] Keep Pulse as the only heartbeat. Use cron for every scheduled report,
        source, self-improvement, knowledge, or maintenance pass.
  - [ ] Use Interval for Daily/Weekly reporting plus knowledge extraction;
        Daily stages source-fingerprinted candidates and Weekly dispositions and
        promotes them. Evidence-quality rules stay shared.
- [ ] 2. Bind current project surfaces.
  - [ ] Read the active feature/spec, current `farplane/automations.toml`, the
        exact existing prompt, target skill, template, and `qa_checklist.md`.
  - [ ] Read [prompt engineering](../../docs/fundamentals/prompt-engineering.md)
        before material prompt changes.
- [ ] 3. Keep desired config visible and runtime state untracked.
  - [ ] Use one complete `[[automations]]` record per Codex automation under
        template `1.0.0`; keep params in the prompt string.
  - [ ] Let the Codex record own live cadence and TOML own desired cadence,
        target, status, and exact prompt. Add no parallel scheduler or ledger.
- [ ] 4. Write the smallest reviewable prompt.
  - [ ] Invoke `$skill-name` and include only cadence, project root, source refs,
        workflow flags, local write policy, external side-effect gates, and
        human-editable overrides.
  - [ ] Do not restate scoring, routing algorithms, generic proof, output
        schemas, or safety rules already owned by the skill.
  - [ ] For Interval, name the shared evidence window, current weekly draft,
        Daily no-promotion boundary, Weekly promotion policy, dated report and
        receipt, and no-ticket-execution boundary.
  - [ ] Require a compact final response with report/draft/receipt links,
        ticket and candidate decisions, dispositions or upserts, changed owners,
        source gaps, operator needs, and next owner.
  - [ ] For every Interval revision, copy the exact receipt block under Output
        into the visible response after validation. Completion is invalid when
        any line is missing; TOML parsing or record counts do not imply it.
- [ ] 5. Activate only when requested.
  - [ ] Inspect existing Codex automations and update matching records instead
        of creating duplicates. Reuse the Pulse thread; cron jobs target the
        workspace unless an explicit persistent-thread exception exists.
  - [ ] Follow [live activation](references/live-activation.md). If the app
        tools are unavailable, stop at `needs_automation_setup` after writing
        the desired config.
- [ ] 6. Validate and review.
  - [ ] Reapply `qa_checklist.md`; parse TOML; verify all required fields,
        exactly one `$pulse-update` heartbeat, dated artifacts, prompt/config
        parity, and absence of legacy manifests or orchestrators.
  - [ ] Route material ticket, goal, external-source, or local knowledge-write
        automation changes through independent review.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

```toml
[[automations]]
id = "<id>"
name = "<name>"
kind = "cron"
status = "active"
prompt = '''
Use $<skill-name>.

Run one bounded pass with project-specific params and gates.

Config source:
farplane/automations.toml automation id="<id>"
'''
[automations.target]
workspace = "<project-root>"
[automations.schedule]
type = "daily | weekly | monthly | active_hours_interval"
timezone = "<timezone>"
```

## Gotchas

- A schedule is configuration, not runtime memory.
- One cron may own multiple phases only when one skill is their semantic parent.
- Local docs/Wiki/skill writes require route-specific validation; they do not
  grant deploy, publish, spend, account, or customer-contact authority.

## Reference Map

- [Interval automation template](templates/interval-automation.md)
- [Pulse automation template](templates/pulse-automation.md)
- [Live activation](references/live-activation.md) — load only when activation
  is explicitly requested.
- [Automation QA](qa_checklist.md) — prompt and config finish gate.
- [Active Interval feature](../../docs/features/FEAT-0067-daily-interval-review-reports.md)

## Output

Return the automation type, concise TOML/config delta, created or reused IDs
when activated, state-boundary checks, validation evidence, and review route.
For Interval changes, explicitly receipt: existing Daily/Weekly records updated;
one `$interval-update` parent and shared window per run; Daily draft projection
and zero canonical promotions; Weekly complete dispositions, finalized report,
authorized promotions, receipt, and next draft; external side-effect gates stay
separate; one Pulse heartbeat is preserved; and no ticket execution.

End Interval automation scenarios by copying this block exactly:

```text
interval_parent_calls_per_run: 1
bounded_evidence_windows_per_run: 1
daily_canonical_promotions: 0
weekly_dispositions_before_promotion: yes
promotion_policy_separate_from_external_side_effect_gates: yes
generic_routing_validation_owner: interval-update
pulse_heartbeat_count: 1
ticket_execution: none
```
