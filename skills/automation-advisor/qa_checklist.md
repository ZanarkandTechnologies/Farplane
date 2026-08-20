---
title: "Automation Advisor QA Checklist"
owner: automation-advisor
status: active
kind: qa-checklist
created_at: 2026-06-24
---

# Automation Advisor QA Checklist

Use this checklist when creating or revising `farplane/automations.toml`
desired-state records or live Codex automation records.

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

3. `full_toml_config`
   - Pass: `farplane/automations.toml` contains one `[[automations]]` record
     per live Codex automation, with id, name, kind, status, schedule,
     workspace/thread target, and exact prompt text.
   - Fail: the desired state is split across Markdown tables, adjacent prompt
     blocks, env vars, or prose that an agent must interpret before syncing.

4. `toml_contract`
   - Pass: the TOML parses, declares `schema = "farplane_project_automations"`,
     and each automation record can be synced without touching prose.
   - Fail: config is stored as custom XML/HTML, prose-only tables, invalid
     TOML, or hidden generated state.

5. `prompt_field_contract`
   - Pass: each automation record has one non-empty `prompt` field containing
     the actual human-authored Codex prompt, including skill params and
     skill-specific overrides when needed.
   - Fail: the prompt is generated from Markdown prose, collapsed to a bare
     skill call when real instruction is needed, or stored outside TOML.

6. `read_write_contract`
   - Pass: interval automation prompts describe project-specific sources and
     side effects in a shape matching the skill signature. Daily/Weekly
     Interval prompts name the current weekly draft, Daily no-promotion
     boundary, Weekly promotion policy, dated report, and receipt.
   - Fail: the prompt exposes raw internal config objects such as empty
     `context_refs.workflow_refs` arrays when plain read/write instructions
     would be clearer.

7. `config_ownership`
   - Pass: user-editable automation metadata and exact prompt text live in
     `farplane/automations.toml` and sync to the Codex automation record;
     machine-local, secret, runtime, or non-automation config lives outside
     this file.
   - Fail: active-hours schedule or automation params are duplicated as
     `FARPLANE_*` env vars, or runtime state is stored in the tracked TOML.

8. `skill_contract_duplication`
   - Pass: scoring, selection, proof, benchmark, output-shape, and generic
     safety behavior live in the called skill or skill references.
   - Fail: the automation prompt restates the called skill's normal checklist,
     scoring formula, generic gates, benchmark rules, or output contract.

9. `context_ref_fit`
   - Pass: cross-interval dependencies, private docs, external source refs, and
     optional telemetry refs are described in the `Reads` block with clear
     source-gap behavior.
   - Fail: the prompt tells the skill to infer cadence-specific parent context
     or bakes source paths into a generic skill.

10. `workflow_flag_fit`
   - Pass: optional analysis work is expressed under `Runs`; Interval's two
     required sibling phases remain one parent skill call rather than two jobs.
   - Fail: optional workflows are described as always-on skill behavior or as a
     separate hidden scheduler.

11. `prompt_size`
   - Pass: the prompt is short enough to review and edit in the Codex app.
   - Fail: the prompt contains long background, rationale, duplicated docs, or
     exhaustive operational prose better owned by a skill reference.

12. `runtime_state_boundary`
   - Pass: desired cadence lives in `farplane/automations.toml`, live cadence
     is synced to the Codex automation record, runtime logs live in ignored
     `.farplane/`, reports are dated files, and `pm.json` is only UI thread
     grouping glue.
   - Fail: tracked config stores mutable last-run state or automation runtime
     IDs.

13. `side_effect_gates`
   - Pass: the prompt separates local knowledge write policy from deploy,
     publish, spend, account, customer-contact, destructive, and other external
     side-effect gates.
   - Fail: the prompt permits push, deploy, publish, spend, account mutation,
     destructive cleanup, or external mutation without explicit operator
     policy.

14. `no_legacy_orchestrator`
   - Pass: no Steer scheduler, cadence alias skill, lane compiler, or
     automation JSON manifest is reintroduced.
   - Fail: the prompt calls retired compatibility surfaces or creates a hidden
     orchestration layer.

15. `syncability`
   - Pass: each TOML record contains enough structured data to compile the
     Codex automation schedule/target/status update, and `prompt` contains the
     exact prompt to copy into the live automation.
   - Fail: the file requires humans or agents to interpret prose tables before
     updating the live automation, or the live prompt diverges from the prompt
     block.

16. `review_route`
   - Pass: automations that can create tickets, change goals, spawn workers, or
     use external sources get review or source-gap handling.
   - Fail: material automation behavior self-approves without evidence or a
     review handoff.

17. `single_heartbeat`
   - Pass: exactly one desired-state record uses `kind = "heartbeat"`, it
     invokes `$pulse-update`, and Feed Scout, Interval, Dogfood, and
     maintenance records use `kind = "cron"`.
   - Fail: another workflow becomes a heartbeat or ticket execution is split
     across scheduled jobs.

18. `workflow_source_routing`
   - Pass: optional workflows that need telemetry, feedback, opportunity,
     metric, or status inputs receive explicit source refs in the `Reads` block
     or record source gaps.
   - Fail: workflows infer project-specific sources from cadence name, operator
     identity, private context, or generic extra refs with unclear ownership.

19. `final_response_contract`
   - Pass: scheduled report-producing prompts include a compact final response
     contract that surfaces key findings, tickets created or updated, candidate
     decisions with reasons, draft/disposition result, knowledge receipt and
     changed owners, source gaps, operator-needed items, and next owner or
     no-ticket-execution receipts.
   - Fail: the prompt allows a receipt that only says the report was written,
     the index was regenerated, or no ticket was created without summarizing
     the report and admission decisions.

20. `interval_lifecycle_receipts`
   - Pass: Interval revisions explicitly receipt one parent call and bounded
     window per run, Daily zero promotions, Weekly disposition-before-promotion,
     separate promotion/external gates, Interval-owned generic routing and
     validation, one Pulse heartbeat, and no ticket execution.
   - Fail: these boundaries are merely implied by a TOML parse or record count.
