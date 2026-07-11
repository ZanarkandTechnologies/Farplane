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
   - Pass: `farplane/harness.md` names mission, human thesis, static leverage
     commitments, non-tradeoffs, agent authority, and change rule.
   - Fail: the project can drift its thesis or commitments silently.

4. `capability_workflow_ownership`
   - Pass: recurring artifact production is owned by an existing reusable
     skill, a project-local `.agents/skills/<capability>/SKILL.md`, or an
     explicit refinement ticket; `farplane/harness.md` references only the
     stable capabilities the project depends on.
   - Fail: project outputs depend on an undocumented workflow or a product
     catalog/controller file.

5. `goals_and_capabilities_split`
   - Pass: value direction, goal axes, and KPI IDs live in
     `farplane/goals.yaml`; stable policy and capability refs live in
     `farplane/harness.md`; executable work and proof live in tickets.
   - Fail: a capability skill becomes a planning controller or duplicates
     goals, ticket state, or worker policy.

5a. `metric_contract_split`
   - Pass: `farplane/metrics.yaml` owns provider-independent metric meaning,
     every goal KPI ID resolves there, and `farplane/bindings.yaml` owns only
     connector/provider refresh coordinates.
   - Fail: metric meaning remains embedded in bindings or is duplicated across
     goal, capability, and provider files.

6. `goals_operating_model`
   - Pass: `farplane/goals.yaml` captures North Star, 3-month outcome, success
     criteria, non-goals, decision boundaries, current milestone, holds, and
     structured YAML for parseable goals, value function, axes, projects, and
     milestones.
   - Fail: file existence is treated as enough when the operating model is
     stale, placeholder, or not grounded in the operator's current intent.

7. `human_intake_gate`
   - Pass: for new or migrated meaning-heavy files, `init-advisor` records
     `human_intake=skip|offer|required`; uses destination skill signatures as
     the question inventory; asks direct signature questions for factual or
     narrow gaps; and escalates to `deep-interview --quick` only for
     intent-heavy, contradictory, or risky canonical-file gaps. The
     `deep-interview --quick` handoff is constrained to missing signature
     params plus intent, outcome, non-goals, decision boundaries, and success
     criteria; the human intake decision, missing answers, and any interview
     summary are written to `docs/bootstrap-brief.md`.
   - Fail: it always runs a generic long interview, invents file content from
     placeholders, or bypasses `deep-interview` when mission, non-goals,
     decision boundaries, success criteria, North Star, value function, or
     milestone intent are unclear. It also fails if the Deep Interview loop is
     duplicated inside `init-advisor`, `harness-creator`, or
     `horizon-advisor`.

9. `full_mode_readiness`
   - Pass: full mode audits `farplane/harness.md` for human thesis, static
     leverage commitments, non-tradeoffs, agent authority, and change rule; it
     audits `docs/bootstrap-brief.md`, capability workflow ownership, and
     `farplane/goals.yaml` for team archetype, recurring outputs, North Star,
     3-month outcome, success criteria, non-goals, and decision boundaries.
     Readiness state and missing answers are written to
     `docs/bootstrap-brief.md`.
   - Fail: full mode claims the project is initialized while these fields are
     missing, stale, placeholder, or ungrounded in operator intent.

10. `split_file_delta_boundary`
   - Pass: `farplane/goals.yaml` stays structured YAML for the North Star,
     value function, goal axes, outcome targets, KPI refs, current bets,
     milestone, and holds; split-file deltas are proposed or applied only after
     operator intent is known; `goal-advisor` is used only after the current
     milestone is concrete enough for a ticket-backed Goal Packet.
   - Fail: InitAdvisor treats `farplane/goals.yaml` existence as enough,
     rewrites split-file strategy without operator intent, or invokes
     `goal-advisor` before there is a concrete milestone.

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
   - Pass: Pulse dispatches executable tickets up to the worker limit, makes
     due original-ticket check-ins eligible, and calls the BAU-only next-wave
     planner when refill is allowed; Feed Scout, Interval maintenance, and
     Dogfood remain separate ticket sources.
   - Fail: selection, execution, or check-in dispatch is split into another
     automation, or Pulse refill invents self-improvement work.

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
