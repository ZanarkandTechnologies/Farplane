---
name: automation-advisor
description: "Design or revise Farplane Codex automations using reviewable automations.md prompts and generic Pulse/Interval skill calls."
tier: 3
group: harness
source: local
workflow: true
template_uses:
  skill-template: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash

---

# Automation Advisor

## Context

Use this skill when creating, revising, or auditing Farplane Codex automations.
It is Farplane-specific authoring guidance for live Codex automation prompts.
Pulse belongs to the fast action loop; interval automations belong to reporting,
reflection, drift checks, and bounded replanning.

Do not reintroduce a project-local automation compiler or a hidden scheduler
thread. Keep the exact project-specific Codex prompts in
`farplane/automations.md`, and copy those prompt blocks into the Codex app
automation records. Keep skills generic and parameterized; the skills own
default Farplane paths and policies, while project-specific additions belong in
automation `context_refs`, workflow flags, or policy.

Prefer high-level operational prompts over fully resolved wiring. Canonical
files, report paths, boards, PM manifests, and standard side-effect gates are
resolved by the called skill. Automation prompts should name `project_root`,
the target skill, cadence, interval windows when relevant, and only the
configuration a human expects to edit.

## Skill Signature

```text
automation_advisor(intent, project_refs, current_automation?, activate?)
  -> automation_template_choice
   + prompt_delta
   + thread_delta?
   + automation_delta?
   + state_contract_check
   + proof_checklist

state:
  reads(docs/specs/steer-pulse-automation.md,
        farplane/automations.md?,
        farplane/pm.json?,
        skills/automation-advisor/qa_checklist.md?,
        skills/automation-advisor/templates/*,
        skills/interval-update/SKILL.md,
        skills/pulse-update/SKILL.md)
  writes(farplane/automations.md prompt updates,
         farplane/pm.json thread grouping when live activation succeeds)

gates:
  loop_choice_made; cadence_named; prompt_calls_skill_plainly;
  side_effect_gates_named; dated_report_path_used; no_lane_manifest_required;
  no_hidden_scheduler_config

routes:
  pulse-update | interval-update | goal-advisor | review

fails:
  creating another automation manifest compiler; mixing logs into tracked
  config; making Pulse own drift review; inventing a Steer scheduler thread;
  using latest.md as the canonical report
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Classify the automation request.
  - [ ] Choose `pulse-update`, `interval-update`, one-off ticket work, or no
        automation.
  - [ ] Use Pulse for frequent bounded action selection.
  - [ ] Use interval automations for scheduled reporting, drift checks, and
        replanning windows such as daily and weekly.
- [ ] 2. Bind the project surfaces.
  - [ ] Read the Pulse/Interval spec and current `farplane/automations.md`
        when present.
  - [ ] Read existing Codex automation prompt text when the task is an update.
  - [ ] Read [qa_checklist.md](qa_checklist.md) before material prompt edits
        or live automation updates.
- [ ] 3. Keep prompts reviewable and runtime state untracked.
  - [ ] Put project-specific automation prompt text in
        `farplane/automations.md`.
  - [ ] Let Codex automation records own cadence.
  - [ ] Do not add a tracked scheduler config or runtime run ledger unless a
        separate ticket proves the need.
  - [ ] Do not enumerate auto-resolved canonical paths unless they are real
        project-specific extensions.
- [ ] 4. Write or update the prompt.
  - [ ] Use the Pulse or Interval automation template as a starting point.
  - [ ] Ensure the prompt calls the owning skill in plain operational language
        with only project-specific context refs, workflow flags, policies, or
        side-effect gates that humans should edit.
  - [ ] Name side-effect gates and final state/report writebacks.
- [ ] 5. Activate live Codex loops only when requested.
  - [ ] Do not create live threads or automations during passive planning or
        substrate bootstrap.
  - [ ] When activation is requested and Codex app thread/automation tools are
        available, create or update the project loops named in
        `farplane/automations.md`, commonly Pulse, Daily Interval, and Weekly
        Interval.
  - [ ] Create dedicated project threads for loops that need context isolation.
  - [ ] Attach each Codex automation to the matching thread at the named
        cadence.
  - [ ] Append persistent loop and PM-owned worker thread IDs to
        `farplane/pm.json` so the UI renders them under the same employee.
  - [ ] If tools are unavailable, write the prompts and report
        `needs_automation_setup`.
- [ ] 6. Check the proof surface.
  - [ ] Apply [qa_checklist.md](qa_checklist.md) to the prompt or live
        automation delta.
  - [ ] Confirm interval report paths are date-stamped.
  - [ ] Confirm `farplane/automations.md` is the reviewable prompt source and
        no `farplane/automations.json`, `farplane/steer.config.toml`, or
        `compile_lane_automation` dependency remains.
  - [ ] Recommend review when the automation can create tickets, mutate goals,
        or spawn child work.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- recommended automation type.
- `farplane/automations.md` prompt text or concise prompt delta.
- created/reused thread and automation IDs when activation succeeds, plus the
  `farplane/pm.json` UI grouping delta.
- state contract check.
- proof checklist and review route.

## Live Activation Recipe

Use this only when the operator explicitly asks to activate live automations for
a project.

```text
activate_farplane_automations(project_root, project_id?, pm_manifest, automation_prompts)
  -> loop_thread_ids
   + loop_automation_ids
   + pm_json_thread_group_delta
```

1. Inspect existing Codex automations first and update matching project
   automations rather than creating duplicates.
2. Create or reuse the dedicated project threads named by
   `farplane/automations.md`, commonly:
   - `Project Pulse`
   - `Project Daily Interval`
   - `Project Weekly Interval`
3. Create or update `farplane/automations.md` with the exact prompt blocks.
4. Create or update each Codex automation by copying the matching prompt block
   exactly, attached to the matching thread at the named cadence.
5. Append visible loop thread IDs to `farplane/pm.json` so they render under
   the persistent PM employee:

```json
{
  "threads": {
    "chats": ["..."],
    "automations": ["..."]
  }
}
```

Risk guards:

- Do not create an extra Steer scheduler thread by default. Pulse owns fast
  ticket selection; interval automations own scheduled reports and plans.
- Do not activate live automations if project goals are placeholder or if the
  operator asked only for substrate setup.
- Do not store automation runtime IDs in `farplane/pm.json`; it is UI grouping
  glue for thread IDs.
- Do not hide PM-visible thread grouping in chat; write `farplane/pm.json`.
- If app automation tools are unavailable, stop at `needs_automation_setup`
  with the prepared prompts in `farplane/automations.md`.

## Reference Map

- [templates/interval-automation.md](templates/interval-automation.md)
- [templates/pulse-automation.md](templates/pulse-automation.md)
- [qa_checklist.md](qa_checklist.md) - prompt minimality, config hygiene,
  state-boundary, and no-legacy checks.
- [../../docs/specs/steer-pulse-automation.md](../../docs/specs/steer-pulse-automation.md)
