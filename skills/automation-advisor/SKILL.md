---
name: automation-advisor
description: "Design or revise Farplane Codex automations using full project-owned automations.toml configs and generic Pulse/Interval skill calls."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash

---

# Automation Advisor

## Context

Use this skill when creating, revising, or auditing Farplane Codex automations.
It is Farplane-specific authoring guidance for live Codex automation configs.
Pulse belongs to the fast executor loop; interval automations belong to
reporting, reflection, drift checks, work-lane allocation, and bounded
replanning.

Do not reintroduce a project-local automation compiler or a hidden scheduler
thread. Keep the full desired Codex automation records in
`farplane/automations.toml`, including id, name, kind, status, target, schedule,
and the exact prompt copied into the Codex app automation record. Keep runtime
state in the Codex app automation store or ignored `.farplane/` files. Keep
skills generic and parameterized; the skills own default Farplane paths and
policies, while project-specific additions belong in the automation `prompt`
field as visible params, overrides, workflow flags, or policy.

Prefer high-level operational prompts over fully resolved wiring. Canonical
files, report paths, boards, PM manifests, and standard side-effect gates are
resolved by the called skill. Automation prompts should name `project_root`,
the target skill, cadence, interval windows when relevant, and only the
configuration a human expects to edit.

When the target workflow is already a Codex skill, prefer the `$skill-name`
operator-facing invocation over function-signature prose. Function signatures
belong in `SKILL.md`; automation records should stay close to the operator
instruction the Codex app actually runs.

Current automation template shape is `framework_template_version: "1.0.0"`:

```toml
schema = "farplane_project_automations"
framework_template_version = "1.0.0"
updated_at = "YYYY-MM-DD"
owner = "automation-advisor"

[[automations]]
id = "<automation-id>"
name = "<human name>"
kind = "heartbeat | cron"
status = "active | paused"
prompt = '''
Use $<skill-name>.

Write the exact Codex automation prompt here. Include the project root, skill
params, project-specific reads/runs/gates, and overrides that a human expects
to review and copy into the live Codex automation record.

Config source:
farplane/automations.toml automation id="<automation-id>"
'''

[automations.target]
workspace = "<project-root>"
thread_id = "<optional-thread-id>"

[automations.schedule]
type = "interval | active_hours_interval | daily | weekly | monthly"
timezone = "<timezone>"
```

Each `[[automations]]` record owns the full desired Codex automation config:
identity, kind/status, schedule, workspace/thread target, and prompt. The
prompt remains a string because it is the exact human-authored instruction the
Codex app runs; it should not be split into Markdown tables or adjacent prompt
blocks. Do not put runtime run IDs, last-run status, logs, or automation memory
in tracked TOML.

## Skill Signature

```text
automation_advisor(intent, project_refs, current_automation?, activate?)
  -> automation_template_choice
   + config_delta
   + thread_delta?
   + automation_delta?
   + state_contract_check
   + proof_checklist

state:
  reads(docs/features/FEAT-0065-pulse-and-interval-automation.md,
        farplane/automations.toml?,
        farplane/pm.json?,
        skills/automation-advisor/qa_checklist.md?,
        skills/automation-advisor/templates/*,
        skills/interval-update/SKILL.md,
        skills/pulse-update/SKILL.md)
  writes(farplane/automations.toml config updates,
         farplane/pm.json thread grouping when live activation succeeds)

gates:
  loop_choice_made; cadence_named; prompt_calls_skill_plainly;
  config_parseable; prompt_field_present;
  schedule_owned_by_codex_automation; no_skill_contract_duplication;
  side_effect_gates_named; dated_report_path_used; no_lane_manifest_required;
  no_hidden_scheduler_config

routes:
  pulse-update | interval-update | goal-advisor | review

fails:
  creating another automation manifest compiler; mixing logs into tracked
  config; making Pulse own drift review; inventing a Steer scheduler thread;
  using latest.md as the canonical report; duplicating schedule in env vars
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Classify the automation request.
  - [ ] Choose `pulse-update`, `interval-update`, one-off ticket work, or no
        automation.
  - [ ] Use Pulse for frequent bounded action selection.
  - [ ] Use interval automations for scheduled reporting, drift checks, and
        replanning windows such as daily and weekly.
  - [ ] Use monthly consolidation automations for low-churn registry or
        artifact-compression reviews that should not run inside weekly
        self-learning.
- [ ] 2. Bind the project surfaces.
  - [ ] Read the Pulse/Interval spec and current `farplane/automations.toml`
        when present.
  - [ ] Read existing Codex automation `prompt` text when the task is an update.
  - [ ] Read [qa_checklist.md](qa_checklist.md) before material prompt edits
        or live automation updates.
- [ ] 3. Keep prompts reviewable and runtime state untracked.
  - [ ] Put project-specific automation config and prompt text in
        `farplane/automations.toml`.
  - [ ] Let Codex automation records own live cadence and
        `farplane/automations.toml` own desired cadence, target, status, and
        exact prompt for review and UI editing.
  - [ ] Put user-editable automation metadata in TOML, not in
        `config.toml.example` env vars, unless the value is machine-local,
        secret, or not tied to a Codex automation.
  - [ ] Keep skill invocation params inside the record's `prompt` string unless
        a future UI explicitly defines a structured skill-param editor.
  - [ ] Do not add a tracked scheduler config or runtime run ledger unless a
        separate ticket proves the need.
  - [ ] Do not enumerate auto-resolved canonical paths unless they are real
        project-specific extensions.
- [ ] 4. Write or update the prompt.
  - [ ] Use the Pulse or Interval automation template as a starting point.
  - [ ] Ensure the prompt calls the owning skill in plain operational language,
        preferably `$skill-name` when the skill is directly invocable,
        with only project-specific context refs, workflow flags, policies, or
        side-effect gates that humans should edit.
  - [ ] Use `farplane/automations.toml` template `1.0.0`.
  - [ ] Use one `[[automations]]` record per Codex automation.
  - [ ] Ensure each record has the actual Codex automation prompt in `prompt`,
        including `Params` and `Overrides` sections when the called skill needs
        them.
  - [ ] Ensure the prompt uses `$skill-name` but includes the cadence-specific
        instruction text that would be useful to a human reviewer.
  - [ ] Reject prompt prose that restates the called skill's scoring,
        selection, proof, benchmark, output-shape, or safety contract.
  - [ ] Name side-effect gates and final state/report writebacks.
- [ ] 5. Activate live Codex loops only when requested.
  - [ ] Do not create live threads or automations during passive planning or
        substrate bootstrap.
  - [ ] When activation is requested and Codex app thread/automation tools are
        available, create or update the project loops named in
        `farplane/automations.toml`, commonly Pulse, Daily Interval, Weekly
        Interval, and any explicitly requested monthly consolidation loop.
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
  - [ ] Confirm `farplane/automations.toml` parses.
  - [ ] Confirm every record has id, name, kind, status, schedule, target, and
        prompt fields needed to sync to live Codex automation records.
  - [ ] Confirm interval report paths are date-stamped.
  - [ ] Confirm `farplane/automations.toml` is the reviewable config source and
        no `farplane/automations.json`, `farplane/steer.config.toml`, or
        `compile_lane_automation` dependency remains.
  - [ ] Recommend review when the automation can create tickets, mutate goals,
        or spawn child work.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- recommended automation type.
- `farplane/automations.toml` config text or concise config delta.
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
   `farplane/automations.toml`, commonly:
   - `Project Pulse`
   - `Project Daily Interval`
   - `Project Weekly Interval`
   - explicitly requested monthly consolidation loops
3. Create or update `farplane/automations.toml` with the exact desired records.
4. Create or update each Codex automation by copying the matching record's
   `prompt` exactly, attached to the matching thread at the named cadence.
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
  with the prepared configs in `farplane/automations.toml`.

## Reference Map

- [templates/interval-automation.md](templates/interval-automation.md)
- [templates/pulse-automation.md](templates/pulse-automation.md)
- [qa_checklist.md](qa_checklist.md) - prompt minimality, config hygiene,
  state-boundary, and no-legacy checks.
- [../../docs/features/FEAT-0065-pulse-and-interval-automation.md](../../docs/features/FEAT-0065-pulse-and-interval-automation.md)
