---
title: Init Advisor QA Checklist
owner: init-advisor
status: active
kind: qa-checklist
created_at: 2026-06-26
---

# Init Advisor QA Checklist

Use this checklist when dogfooding `init-advisor`, reviewing an initialized
Farplane project, or changing init behavior.

```text
init_advisor_qa(project_root, init_mode, activation_requested?)
  -> readiness_verdict + gaps + proof_refs
```

## Checks

1. `human_status_language`
   - Pass: chat, reports, and checklists use plain status language such as
     "Ready" or "Operating model still missing".
   - Fail: the operator only sees internal labels such as
     `needs_operating_model_intake`.

2. `substrate_files`
   - Pass: tracked files in `farplane/`, `.agents/skills/README.md`, `docs/`,
     `tickets/`, and `qa/` exist according to `farplane/manifest.json`.
   - Fail: required project files are absent or replaced by legacy filenames.

3. `static_charter`
   - Pass: `farplane/harness.yaml` names mission, human thesis, static leverage
     commitments, non-tradeoffs, agent authority, and change rule.
   - Fail: the project can drift its thesis or commitments silently.

4. `capability_workflow_ownership`
   - Pass: recurring artifact production is owned by an existing reusable
     skill, a project-local `.agents/skills/<capability>/SKILL.md`, or an
     explicit refinement ticket; `farplane/harness.yaml` references only the
     stable capabilities the project depends on.
   - Fail: project outputs depend on an undocumented workflow or a product
     catalog/controller file.

5. `objectives_and_capabilities_split`
   - Pass: selected objective/guard refs, stable human policy, descriptive
     planning areas and capability refs live in `farplane/harness.yaml`; reusable
     metric meaning, direction, freshness, and guard rules live in
     `farplane/metrics.yaml`; executable work and proof live in tickets.
   - Fail: a capability skill becomes a planning controller or duplicates
     goals, ticket state, or worker policy.

5a. `metric_contract_split`
   - Pass: `farplane/metrics.yaml` owns provider-independent metric meaning,
     every selected metric ref resolves there, and `farplane/bindings.yaml` owns only
     connector/provider refresh coordinates.
   - Fail: metric meaning remains embedded in bindings or is duplicated across
     goal, capability, and provider files.

6. `objective_operating_model`
   - Pass: `farplane/harness.yaml` captures mission, human thesis, non-tradeoffs,
     decision boundaries, authority, planning areas, and selected metric refs;
     `farplane/metrics.yaml` captures metric definitions, directions,
     freshness, and guard rules.
   - Fail: file existence is treated as enough when the operating model is
     stale, placeholder, or not grounded in the operator's current intent.

7. `human_intake_gate`
   - Pass: for new or migrated meaning-heavy files, `init-advisor` records
     `human_intake=skip|offer|required`; uses destination skill signatures as
     the question inventory; asks direct signature questions for factual or
     narrow gaps; and stops for focused operator clarification only for
     intent-heavy, contradictory, or risky canonical-file gaps. Clarification
     is constrained to missing signature params plus intent, outcome, non-goals,
     decision boundaries, and success criteria; the human intake decision,
     missing answers, and summary are written to `docs/bootstrap-brief.md`.
   - Fail: it always runs a generic long interview, invents file content from
     placeholders, or bypasses operator clarification when mission, non-goals,
     decision boundaries, success criteria, North Star, value function, or
     metric-objective intent is unclear. It also fails if a generic long
     interview loop is duplicated inside the owning skills.

9. `full_mode_readiness`
   - Pass: full mode audits `farplane/harness.yaml` for human thesis, static
     leverage commitments, non-tradeoffs, agent authority, and change rule; it
     audits `docs/bootstrap-brief.md`, capability workflow ownership,
     `farplane/harness.yaml` for human meaning and boundaries, and
     `farplane/metrics.yaml` for honest metric meaning, directions, freshness,
     and guard rules.
     Readiness state and missing answers are written to
     `docs/bootstrap-brief.md`.
   - Fail: full mode claims the project is initialized while these fields are
     missing, stale, placeholder, or ungrounded in operator intent.

10. `split_file_delta_boundary`
   - Pass: `farplane/harness.yaml` keeps human meaning, planning areas, hard
     constraints, and selected metric refs while `farplane/metrics.yaml` keeps
     reusable metric meaning, direction, freshness, and guard rules; split-file
     deltas are applied only after operator intent is known; `goal-advisor` is
     used only after a ticket is concrete enough for a Goal Packet.
   - Fail: InitAdvisor treats file existence as enough, invents metric
     objectives without operator intent or evidence, or invokes
     `goal-advisor` before there is a concrete executable ticket.

11. `automation_source`
   - Pass: `farplane/automations.toml` contains one reviewable Work Pulse
     heartbeat plus separate Feed Scout, Daily BAU, Weekly BAU,
     self-improvement, and optional cron configs that call
     generic skills directly; it does not require `farplane/steer.config.toml`,
     `.farplane/state/steer-scheduler.json`, or `latest.md` as canonical
     interval state.
   - Fail: a hidden scheduler, lane compiler, automation JSON manifest, or
     retired Steer thread is required.

12. `pulse_selection`
   - Pass: Pulse dispatches unclaimed executable tickets up to the Pulse worker
     limit, does not count human-active tickets as Pulse workers, makes due
     original-ticket check-ins eligible, and calls one adaptive next-wave
     planner when refill is allowed; Feed Scout, Interval, and Dogfood provide
     report/candidate context plus bounded evidence-backed recovery tickets;
     they never independently admit opportunities or experiments.
   - Fail: selection, execution, or check-in dispatch is split into another
     automation, area planner subagents are required, or scheduled report
     automations independently admit proactive tickets.

13. `live_automation_activation`
   - Pass: when activation was requested, live Codex automation records match
     `farplane/automations.toml` and PM-visible thread IDs are in
     `farplane/pm.json`; runtime automation IDs stay in the Codex app
     automation store.
   - Fail: live prompts drift from the reviewed source, or runtime automation
     IDs are stored in `pm.json`.

14. `quality_tooling_slots`
    - Pass: optional PROJECT_RULES slots cover maintainability/refactoring
      commands such as lint, complexity, duplication, dependency boundaries,
      dead code, static analysis dashboard, and mutation testing, plus hardening
      commands such as SAST, dependency audit, secret scan, config validation,
      and resilience/failure tests. Cleanup routes to `refactoring`; risk
      reduction routes to `hardening`.
    - Fail: quality tooling is auto-installed, universalized, or lacks routing.

15. `qa_cookbook`
   - Pass: `qa/cookbook/` has at least one concrete project page beyond the
     template for the repo's normal evidence path.
   - Fail: agents must infer validation, ticket metadata checks, skill checks,
     or browser proof paths from chat.

16. `runtime_boundaries`
   - Pass: generated reports, eval runs, logs, and local run state live in
     ignored `.farplane/`; active ticket work under `tickets/TASK-*` is ignored
     by default while `tickets/README.md` and `tickets/templates/` remain
     available as tracked scaffold.
   - Fail: mutable run state or active ticket work is added to tracked project
     config by default.

17. `proof_commands`
   - Pass: the final init or dogfood result names the exact validator,
     checklist, eval, or manual evidence used.
   - Fail: completion is claimed with "looks good" and no proof ref.

18. `business_foundation_tickets`
   - Pass: a fresh bootstrap creates exactly `TASK-0001` `find_customer`,
     `TASK-0002` `deliver_value`, and `TASK-0003` `collect_revenue`; sequences
     are `1..3`, later tickets depend on the preceding ticket, and no live work
     or automation starts. External-action approvals stay in the ticket program,
     not retired ticket metadata.
   - Fail: bootstrap emits the retired starter PRD ticket, omits or duplicates
     a foundation step, weakens approval/dependency ordering, or activates work.

19. `foundation_ticket_preservation`
   - Pass: without `--force`, each existing foundation ticket path is preserved
     byte-for-byte, missing sibling tickets are still created, and every
     collision is reported with its exact destination path.
   - Fail: a brownfield collision is silently overwritten, suppresses creation
     of unrelated missing tickets, or is reported as a clean three-ticket init.
