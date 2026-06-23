---
name: automation-advisor
description: "Design or revise Farplane Codex automations using reviewable automations.md prompts and generic Steer/Pulse skill calls."
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
It is Farplane-specific authoring guidance: Steer and Pulse belong to the
Farplane Framework, while this skill helps agents and humans write the live
Codex automation prompts and config cleanly.

Do not reintroduce a project-local automation compiler. Keep the exact
project-specific Codex prompts in `farplane/automations.md`, and copy those
prompt blocks into the Codex app automation records. Keep skills generic and
parameterized; project cadence, paths, thread IDs, policy, and schedule choices
belong in the automation prompt.

Prefer high-level operational prompts over fully resolved wiring. Canonical
files, state paths, report paths, boards, PM manifests, and standard
side-effect gates should be resolved by the Farplane project context,
dependency injection, or the called skill unless a project genuinely needs a
non-standard override.

## Skill Signature

```text
automation_advisor(intent, project_refs, current_automation?, steer_config?, activate?)
  -> automation_template_choice
   + prompt_delta
   + config_delta?
   + thread_delta?
   + automation_delta?
   + state_contract_check
   + proof_checklist

state:
  reads(docs/specs/steer-pulse-automation.md,
        farplane/steer.config.json?,
        farplane/automations.md?,
        farplane/pm.json?,
        skills/automation-advisor/templates/*,
        skills/steer-update/SKILL.md,
        skills/pulse-update/SKILL.md)
  writes(farplane/automations.md prompt updates, steer config patches when requested,
         farplane/pm.json thread grouping when live activation succeeds)

gates:
  loop_choice_made; config_state_separated; cadence_named; prompt_calls_skill_plainly;
  side_effect_gates_named; dated_report_path_used; no_lane_manifest_required

routes:
  steer-update | pulse-update | goal-advisor | review

fails:
  creating another automation manifest compiler; mixing logs into tracked
  config; making Pulse own long-horizon strategy; making Steer spawn unbounded
  leaf work; using latest.md as the canonical report
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Classify the automation request.
  - [ ] Choose `pulse-update`, `steer-update`, a Steer scheduled job, one-off
        ticket work, or no automation.
  - [ ] Use Pulse for frequent bounded action selection.
  - [ ] Use Steer for scheduled planning, drift checks, and recurring strategy
        or maintenance jobs.
- [ ] 2. Bind the project surfaces.
  - [ ] Read the Steer/Pulse spec and current `farplane/automations.md` when
        present.
  - [ ] Read existing Codex automation prompt text when the task is an update.
- [ ] 3. Keep config and state separate.
  - [ ] Put project-specific automation prompt text in
        `farplane/automations.md`.
  - [ ] Put `last_run_at`, `next_due_at`, `last_report`, and status in ignored
        scheduler state.
  - [ ] Do not enumerate auto-resolved canonical paths unless they are real
        project-specific overrides.
- [ ] 4. Write or update the prompt.
  - [ ] Use the Steer or Pulse automation template as a starting point.
  - [ ] Ensure the prompt calls the owning skill in plain operational language
        with only project-specific overrides that humans should edit.
  - [ ] Name side-effect gates and final state/report writebacks.
- [ ] 5. Activate live Codex loops only when requested.
  - [ ] Do not create live threads or automations during passive planning or
        substrate bootstrap.
  - [ ] When activation is requested and Codex app thread/automation tools are
        available, create or update exactly two project loops: Pulse and Steer.
  - [ ] Create dedicated project threads for Pulse and Steer when minute-level
        or thread-attached heartbeats are needed for context isolation.
  - [ ] Attach Pulse to the Pulse thread at the fast idle cadence.
  - [ ] Attach Steer to the Steer thread or project workspace at the minimum
        planning cadence supported by the automation tool.
  - [ ] Append persistent Pulse/Steer and PM-owned worker thread IDs to
        `farplane/pm.json` so the UI renders them under the same employee.
  - [ ] If tools are unavailable, write the prompts and report
        `needs_automation_setup`.
- [ ] 6. Check the proof surface.
  - [ ] Confirm report paths are date-stamped.
  - [ ] Confirm `farplane/automations.md` is the reviewable prompt source and
        no `farplane/automations.json` or `compile_lane_automation` dependency
        remains.
  - [ ] Recommend review when the automation can create tickets, mutate goals,
        or spawn child work.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- recommended automation type.
- `farplane/automations.md` prompt text or concise prompt delta.
- config patch when requested.
- created/reused thread and automation IDs when activation succeeds, plus the
  `farplane/pm.json` UI grouping delta.
- scheduler state contract.
- proof checklist and review route.

## Live Activation Recipe

Use this only when the operator explicitly asks to activate live automations for
a project.

```text
activate_farplane_automations(project_root, project_id?, pm_manifest)
  -> pulse_thread_id
   + steer_thread_id
   + pulse_automation_id
   + steer_automation_id
   + pm_json_thread_group_delta
```

1. Inspect existing Codex automations first and update matching Pulse/Steer
   automations rather than creating duplicates.
2. Create or reuse two dedicated project threads:
   - `Project Pulse`
   - `Project Steer`
3. Create or update `farplane/automations.md` with the exact Pulse and Steer
   prompt blocks.
4. Create or update the Pulse automation by copying the Pulse prompt block
   exactly, attached to the Pulse thread at the fast idle cadence.
5. Create or update the Steer automation by copying the Steer prompt block
   exactly, attached to the Steer thread or project workspace at the minimum
   planning cadence.
6. Append visible loop thread IDs to `farplane/pm.json` so they render under
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

- Do not create extra daily, weekly, strategy, ticket-drainer, quarterly, or
  yearly threads.
- Do not activate live automations if project goals are placeholder or if the
  operator asked only for substrate setup.
- Do not store automation runtime IDs in `farplane/pm.json`; it is UI grouping
  glue for thread IDs.
- Do not hide PM-visible thread grouping in chat; write `farplane/pm.json`.
- If app automation tools are unavailable, stop at `needs_automation_setup`
  with the two prepared prompts in `farplane/automations.md`.

## Reference Map

- [templates/steer-automation.md](templates/steer-automation.md)
- [templates/pulse-automation.md](templates/pulse-automation.md)
- [templates/steer.config.json](templates/steer.config.json)
- [../../docs/specs/steer-pulse-automation.md](../../docs/specs/steer-pulse-automation.md)
