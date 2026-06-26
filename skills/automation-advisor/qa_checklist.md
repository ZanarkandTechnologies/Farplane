---
title: "Automation Advisor QA Checklist"
owner: automation-advisor
status: active
kind: qa-checklist
created_at: 2026-06-24
---

# Automation Advisor QA Checklist

Use this checklist when creating or revising `farplane/automations.md` prompt
blocks or live Codex automation records.

```text
automation_prompt_qa(automation_prompt, called_skill, project_context)
  -> pass | fail | needs_review
```

## Checks

1. `skill_boundary`
   - Pass: the prompt calls one owning skill plainly.
   - Fail: the prompt reimplements the skill's workflow instead of passing
     parameters, context refs, workflow flags, or policy.

2. `operator_skill_invocation`
   - Pass: when a target is a Codex skill, the prompt uses the operator-facing
     `$skill-name` invocation plus the minimum params a human should see.
   - Fail: the prompt uses function-signature prose such as
     `skill_name(project_root=...)` when `$skill-name` would be clearer, or
     copies the skill signature into the automation record.

3. `minimal_project_config`
   - Pass: the prompt includes only information that cannot live in the called
     skill: cadence identity, project root, interval windows, project-specific
     read/write refs, enabled workflows, project-specific sources, and
     side-effect gates.
   - Fail: the prompt restates default Farplane paths, generic report shapes,
     default ticket board rules, or skill-owned implementation details.

3. `read_write_contract`
   - Pass: interval automation prompts describe project-specific sources and
     side effects as `Call`, `Reads`, `Writes`, `Runs`, and `Gates`
     instructions that visually match skill signatures.
   - Fail: the prompt exposes raw internal config objects such as empty
     `context_refs.workflow_refs` arrays when plain read/write instructions
     would be clearer.

4. `config_ownership`
   - Pass: config key names, defaults, fallback order, and validation rules live
     in the called skill, config template, or runtime config source. The
     automation record only names explicit overrides.
   - Fail: `farplane/automations.md` lists every env/config key, duplicates
     defaults from `config.toml.example`, or becomes a second config reference.

5. `skill_contract_duplication`
   - Pass: scoring, selection, proof, benchmark, output-shape, and generic
     safety behavior live in the called skill or skill references.
   - Fail: the automation prompt restates the called skill's normal checklist,
     scoring formula, generic gates, benchmark rules, or output contract.

6. `context_ref_fit`
   - Pass: cross-interval dependencies, private docs, external source refs, and
     optional telemetry refs are described in the `Reads` block with clear
     source-gap behavior.
   - Fail: the prompt tells the skill to infer cadence-specific parent context
     or bakes source paths into a generic skill.

7. `workflow_flag_fit`
   - Pass: optional analysis work is expressed under `Runs`.
   - Fail: optional workflows are described as always-on skill behavior or as a
     separate hidden scheduler.

8. `prompt_size`
   - Pass: the prompt is short enough to review and edit in the Codex app.
   - Fail: the prompt contains long background, rationale, duplicated docs, or
     exhaustive operational prose better owned by a skill reference.

9. `runtime_state_boundary`
   - Pass: cadence lives in the Codex automation record, runtime logs live in
     ignored `.farplane/`, reports are dated files, and `pm.json` is only UI
     thread grouping glue.
   - Fail: tracked config stores mutable last-run state or automation runtime
     IDs.

10. `side_effect_gates`
   - Pass: the prompt names project-specific external side-effect gates only
     when they matter.
   - Fail: the prompt permits push, deploy, publish, spend, account mutation,
     destructive cleanup, or external mutation without explicit operator
     policy.

11. `no_legacy_orchestrator`
   - Pass: no Steer scheduler, cadence alias skill, lane compiler, or
     automation JSON manifest is reintroduced.
   - Fail: the prompt calls retired compatibility surfaces or creates a hidden
     orchestration layer.

12. `copyability`
   - Pass: the prompt block in `farplane/automations.md` can be copied into the
     Codex app record with only schedule/workspace metadata supplied by the app.
   - Fail: the file and live automation prompt diverge in behavior.

13. `review_route`
   - Pass: automations that can create tickets, change goals, spawn workers, or
     use external sources get review or source-gap handling.
   - Fail: material automation behavior self-approves without evidence or a
     review handoff.

14. `workflow_source_routing`
   - Pass: optional workflows that need telemetry, feedback, opportunity,
     metric, or status inputs receive explicit source refs in the `Reads` block
     or record source gaps.
   - Fail: workflows infer project-specific sources from cadence name, operator
     identity, private context, or generic extra refs with unclear ownership.
