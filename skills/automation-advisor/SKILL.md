---
name: automation-advisor
description: "Design or revise Farplane Codex automations using project-owned automations.toml records and one owning skill per scheduled workflow."
tier: 3
group: operations
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash
---

# Automation Advisor

## Context

Use this skill to create, revise, or audit Farplane Codex automations. Work
Pulse is the only heartbeat and owns ticket execution. Company OS Daily and
Weekly, Feed Scout, Dogfood, and maintenance are separate `cron` records.

Keep each complete desired record in `farplane/automations.toml`: id, name,
kind, status, target, schedule, and exact prompt. Runtime IDs, logs, and mutable
memory stay in the Codex automation store or ignored `.farplane/` state. Do not
add a compiler, scheduler thread, or second manifest.

An automation prompt calls one owning skill. The automation owns integration
access, collection, pagination, frozen source caches, rendering, provider
effects, and readback. The skill reads only local inputs and writes exactly one
structured extraction. Company OS Daily fans out one `$pm-daily` call per
eligible Project; Weekly calls `$pm-weekly` once over the complete frozen set.
The former Interval workflow is removed and must not be restored or bound to
Daily or Weekly.

## Skill Signature

```text
automation_advisor(intent, project_refs, current_automation?, activate?)
  -> template_choice + config_delta + automation_delta?
   + state_contract_check + proof_checklist
state: reads(active feature/spec, farplane/automations.toml?, current prompts,
             target skill, templates, first-load Todo List guardrails);
       writes(farplane/automations.toml)
gates: loop_choice; cadence; one_owning_skill; full_parseable_record;
  file_in_file_out_boundary; side_effect_gates; one_heartbeat;
  no_hidden_scheduler
routes: pulse-update | pm-daily | pm-weekly | feed-scout | dogfood-review |
  goal-advisor | review
fails: logs in tracked config; provider access inside pm skills; generated
  prompt fragments; second heartbeat; active Daily/Weekly interval binding;
  ticket creation or execution from Company OS reviews
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Classify the recurring job.
  - [ ] Keep Pulse as the only heartbeat and ticket executor.
  - [ ] Use Company OS Daily/Weekly for project memory and money-linked review.
  - [ ] Use cron for every report, source, self-improvement, or maintenance pass.
- [ ] 2. Bind current project surfaces.
  - [ ] Read the active feature/spec, `farplane/automations.toml`, exact live
        prompt, target skill, template, and first-load Todo List guardrails.
  - [ ] Read [prompt engineering](../../docs/fundamentals/prompt-engineering.md)
        before material prompt changes.
- [ ] 3. Keep desired config visible and runtime state untracked.
  - [ ] Use one complete `[[automations]]` record per Codex automation.
  - [ ] Let the Codex record own live cadence and TOML own desired cadence,
        target, status, and exact prompt.
- [ ] 4. Write the smallest reviewable prompt.
  - [ ] Invoke one `$skill-name` and include only cadence, project bindings,
        sources, stages, write policy, side-effect gates, and final receipt.
  - [ ] For Company OS, name fetch/cache, local skill extraction, validation,
        and render/apply as four explicit stages.
  - [ ] Make provider access and effects automation-owned. Make skill inputs and
        its single JSON output exact.
  - [ ] Restrict Company OS actions to authorized existing issues; forbid task
        admission, strategy invention, broad promotion, and execution.
- [ ] 5. Activate when the accepted task includes live integration.
  - [ ] Inspect live Codex automations and update matching records instead of
        creating duplicates. Follow [live activation](references/live-activation.md).
  - [ ] Preserve IDs, cadence, target, model, reasoning, status, and the single
        Pulse heartbeat unless the accepted change explicitly alters one.
- [ ] 6. Validate and review.
  - [ ] Parse TOML; verify required fields, one `$pulse-update` heartbeat,
        Company OS prompt/skill parity, and no active Interval binding.
  - [ ] Verify Daily has one local skill call per eligible Project and Weekly
        has one call over a complete frozen set.
  - [ ] Route material workflow changes through independent review.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [Company OS automation](templates/company-os-automation.md)
- [Pulse automation](templates/pulse-automation.md)
- [Live activation](references/live-activation.md)

## Gotchas

- A schedule is configuration, not runtime memory.
- One cron may own multiple stages only when one skill is their semantic parent.
- A Company OS review observes and updates existing work; it does not start a
  Multica run or invent a new company strategy.
- Local report writes do not grant deploy, publish, spend, account, customer
  contact, or destructive authority.

## Output

Return the automation type, concise config delta, created or reused live IDs,
state-boundary checks, validation evidence, and review route. For a material
prompt revision, include the complete replacement TOML records with exact
prompts so the proposed change is reviewable before activation.

End Company OS automation changes with this receipt:

```text
daily_project_calls: one per eligible project
weekly_parent_calls: 1
skills_provider_reads: 0
skills_provider_writes: 0
automation_renders_and_applies: yes
existing_issue_actions_only: yes
multica_execution: none
pulse_heartbeat_count: 1
```
