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

4. `product_catalog`
   - Pass: `farplane/products.md` names the team archetype, primary/supporting
     products, expected outputs, work lanes, and constraints.
   - Fail: product direction is implicit or mixed into dynamic planning files.

5. `products_to_local_skills`
   - Pass: every active product row in `farplane/products.md` either has a
     local `.agents/skills/<product-skill>/SKILL.md` owner or an explicit
     refinement ticket.
   - Fail: product rows exist but tickets have no callable workflow to invoke.

6. `goals_operating_model`
   - Pass: `farplane/goals.md` captures North Star, 3-month outcome, success
     criteria, non-goals, decision boundaries, current milestone, holds, and a
     fenced `goal-program` block with parseable goals, value function, axes,
     projects, and milestones.
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

8. `full_mode_readiness`
   - Pass: full mode audits `farplane/harness.md` for human thesis, static
     leverage commitments, non-tradeoffs, agent authority, and change rule; it
     audits `docs/bootstrap-brief.md`, `farplane/products.md`, and
     `farplane/goals.md` for team archetype, product outputs, North Star,
     3-month outcome, success criteria, non-goals, and decision boundaries.
     Readiness state and missing answers are written to
     `docs/bootstrap-brief.md`.
   - Fail: full mode claims the project is initialized while these fields are
     missing, stale, placeholder, or ungrounded in operator intent.

9. `split_file_delta_boundary`
   - Pass: `farplane/goals.md` stays Markdown with a fenced `goal-program`
     block for parseable goals, value function, axes, projects, and milestones;
     split-file deltas are proposed or applied only after operator intent is
     known; `goal-advisor` is used only after the current milestone is concrete
     enough for a ticket-backed Goal Packet.
   - Fail: InitAdvisor treats `farplane/goals.md` existence as enough,
     rewrites split-file strategy without operator intent, or invokes
     `goal-advisor` before there is a concrete milestone.

10. `automation_source`
   - Pass: `farplane/automations.md` contains reviewable Pulse, Daily Interval,
     and Weekly Interval prompt blocks that call generic skills directly; it
     does not require `farplane/steer.config.toml`,
     `.farplane/state/steer-scheduler.json`, or `latest.md` as canonical
     interval state.
   - Fail: a hidden scheduler, lane compiler, automation JSON manifest, or
     retired Steer thread is required.

11. `pulse_selection`
   - Pass: Pulse selects at most one bounded action per beat, prefers local
     ready/unblocked tickets, reads `farplane/harness.md` and
     `farplane/products.md` for product refill work, defines refill tickets with
     project type, baseline/comparison, expected artifact, and proof signal, and
     avoids a separate ticket-drainer automation.
   - Fail: ticket selection is split into another automation or refill work has
     no product/proof shape.

12. `live_automation_activation`
   - Pass: when activation was requested, live Codex automation records match
     `farplane/automations.md` and PM-visible thread IDs are in
     `farplane/pm.json`; runtime automation IDs stay in the Codex app
     automation store.
   - Fail: live prompts drift from the reviewed source, or runtime automation
     IDs are stored in `pm.json`.

13. `quality_tooling_slots`
    - Pass: optional PROJECT_RULES slots cover maintainability/refactoring
      commands such as lint, complexity, duplication, dependency boundaries,
      dead code, static analysis dashboard, and mutation testing, plus hardening
      commands such as SAST, dependency audit, secret scan, config validation,
      and resilience/failure tests. Cleanup routes to `refactoring`; risk
      reduction routes to `hardening`.
    - Fail: quality tooling is auto-installed, universalized, or lacks routing.

14. `qa_cookbook`
   - Pass: `qa/cookbook/` has at least one concrete project page beyond the
     template for the repo's normal evidence path.
   - Fail: agents must infer validation, ticket metadata checks, skill checks,
     or browser proof paths from chat.

15. `runtime_boundaries`
   - Pass: generated reports, eval runs, logs, and local run state live in
     ignored `.farplane/`; active ticket work under `tickets/TASK-*` is ignored
     by default while `tickets/README.md` and `tickets/templates/` remain
     available as tracked scaffold.
   - Fail: mutable run state or active ticket work is added to tracked project
     config by default.

16. `proof_commands`
    - Pass: the final init or dogfood result names the exact validator,
      checklist, eval, or manual evidence used.
    - Fail: completion is claimed with "looks good" and no proof ref.
