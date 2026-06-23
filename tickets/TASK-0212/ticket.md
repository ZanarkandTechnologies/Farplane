---
ticket_id: TASK-0212
title: Standardize template usage rollout tracking
phase: complete
status: done
owner: codex
claimed_by:
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
requires_qa: false
requires_demo: false
created_at: 2026-06-23T21:49:00+0800
updated_at: 2026-06-23T21:58:09+0800
next_action: optional reviewer/commit when ready
last_verification: 2026-06-23 full skill-maintenance check, project validator, template metadata check, registry tests, generator tests, project-file fallback tests, and targeted py_compile passed
---

# TASK-0212: Standardize Template Usage Rollout Tracking

## Summary

Create one simple rollout-tracking standard for template consumers:
`template_uses: { template_id: template_version }`. Extend the existing
template registry and skill-maintenance reports so Farplane can answer which
skills and projects are current, stale, or missing for each template.

This is a hard standardization, not a new schema-governance layer. Reuse the
current template registry, skill registry, project-file validator, and template
intelligence generator.

## Scope

- In:
  - Add `template_uses` extraction for Markdown front matter and JSON files.
  - Extend template registry rows with rollout metadata such as
    `applies_to` and `consumer_scope`.
  - Update `skills/skill-creator/references/SKILL_TEMPLATE.md` to emit
    `template_uses.skill-template` and bump the template version.
  - For skill rollout, focus only on skills that already declare a skill
    template version.
  - Track skill template, skill eval task, and skill QA checklist usage for
    skills where those surfaces exist.
  - Track Farplane framework/project template usage for the current Farplane
    repo and sibling Farplane-UI project.
  - Update generated rollout artifacts so template IDs link to feature refs and
    current/stale/missing consumer counts.
  - Keep legacy fields readable during this ticket, but stop treating them as
    the future-facing standard.
- Out:
  - No blind metadata pass over every doc.
  - No new broad schema registry.
  - No migration of archived tickets or historical research notes.
  - No cleanup of unrelated dirty worktree changes.
  - No live automation, deploy, push, or external account changes.

## Delta

- `Before:` Template usage is split across fields such as
  `skill_template_version`, `framework_template_version`, `spec_version`, and
  `version`. Template source metadata exists, but rollout reporting is
  template-specific and cannot answer generic "who uses template X?" questions.
- `After:` Template consumers use one field:
  `template_uses.<template_id> = <version>`. Existing reports show template
  current/stale/missing counts by consumer scope and feature refs.
- `Why now:` Changing core templates currently creates uncertainty about which
  skills, evals, QA checklists, and projects need rollout. The operator needs a
  confidence radius before making template changes.
- `First-principles basis:`
  - `objective:` make template changes traceable across the system.
  - `need:` show who is on the latest skill/eval/QA/project templates.
  - `assumptions:` current rollout targets are mostly skills plus the Farplane
    and Farplane-UI project framework files.
  - `root_cause:` version fields are individually meaningful but not generic
    enough to power one tracker.
  - `constraints:` reuse current registries and validators; avoid extra
    taxonomy; protect unrelated user edits.
  - `first_viable_slice:` template registry metadata + extractor + rollout
    matrix + migration for current skills/projects.
  - `proof_or_falsification:` generated rollout artifact reports expected
    counts, validators pass, and selected stale/missing consumers are visible.
  - `tradeoff:` migrate metadata now and keep legacy readers temporarily.
  - `non_goals:` all-doc versioning, schema registry, historical rewrite.

## Program

```text
signature:
  template_rollout_tracking(template_registry, skill_registry, project_files)
    -> template_usage_matrix + registry_delta + migrated_consumers + validation_evidence

vars:
  source_registry = docs/templates/registry.jsonl
  source_config = rules/template-registry.toml
  skill_template = skills/skill-creator/references/SKILL_TEMPLATE.md
  skill_consumers = skills/*/SKILL.md with existing skill_template_version/template_uses
  project_consumers = farplane/manifest.json + ../Farplane-UI/farplane/manifest.json

program:
  ground_current_metadata(vars)
    -> template_ids + legacy_fields + current_rollout_gaps

  extend_template_registry()
    -> applies_to + consumer_scope + feature_refs per template

  add_template_uses_extractor()
    -> Markdown and JSON consumer metadata

  migrate_current_consumers()
    -> skills and project manifests with template_uses

  generate_rollout_matrix()
    -> current/stale/missing consumers by template_id

  verify(done_when, proof)
    -> validators + generated artifact + progress evidence
```

## Map

- `Touch:`
  - `bin/validators/sync_template_registry.py`
  - `bin/validators/check_template_version_metadata.py`
  - `bin/validators/check_farplane_project_files.py`
  - `bin/validators/test_sync_template_registry.py`
  - `bin/validators/test_check_farplane_project_files.py`
  - `skills/skill-maintenance/scripts/check_skills.py`
  - `skills/skill-maintenance/scripts/generate_template_intelligence.py`
  - `skills/skill-maintenance/scripts/test_generate_template_intelligence.py`
  - `skills/skill-creator/references/SKILL_TEMPLATE.md`
  - `rules/template-registry.toml`
  - `rules/template-version-watch.toml`
  - `docs/templates/README.md`
  - `docs/templates/registry.jsonl`
  - current skill front matter for skills with existing `skill_template_version`
  - `farplane/manifest.json`
  - `../Farplane-UI/farplane/manifest.json`
- `Inspect:`
  - `docs/features/registry.jsonl`
  - `docs/skills/registry.jsonl`
  - `docs/farplane-framework/project-files.md`
  - `skills/deep-init-project/references/*`
  - `tickets/TASK-0211/ticket.md`
- `Signature delta:`
  - `extract_template_uses(path, metadata) -> dict[str, str]`
  - `build_template_rollout(template_rows, consumers) -> rollout_rows`
  - `template_rollout_summary(rows) -> counts`
- `Type Sketch:`

```text
TemplateRegistryRow = {
  template_id: string,
  template_version: string,
  path: string,
  feature_refs: string[],
  consumer_scope?: "skill" | "project" | "mixed",
  applies_to?: string[]
}

TemplateConsumer = {
  consumer_id: string,
  path: string,
  consumer_scope: "skill" | "project",
  template_uses: dict[template_id, version],
  legacy_template_uses: dict[template_id, version]
}

TemplateRolloutRow = {
  template_id: string,
  current_version: string,
  consumer_id: string,
  consumer_scope: string,
  used_version?: string,
  status: "current" | "stale" | "missing",
  feature_refs: string[]
}
```

## Done / Proof

```text
done_when:
  - `template_uses` is the standard consumer field documented for skills and projects.
  - Skill template source emits `template_uses.skill-template` and its template version is bumped.
  - Existing skills with `skill_template_version` are migrated or read into template rollout as `skill-template` consumers.
  - Skill eval and QA checklist template rollout can be counted for skills that have eval_task.json or qa_checklist.md surfaces.
  - Farplane and Farplane-UI project manifests declare project-level template usage.
  - Generated template intelligence includes template rollout rows grouped by template_id, feature refs, and consumer scope.
  - Validators/tests cover extraction, registry metadata, rollout counts, and current project manifests.

proof:
  checks:
    - `python3 bin/validators/sync_template_registry.py --write`
    - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
    - `python3 bin/validators/check_farplane_project_files.py`
    - `python3 skills/skill-maintenance/scripts/test_generate_template_intelligence.py`
    - `python3 -m unittest bin/validators/test_sync_template_registry.py`
    - `python3 -m unittest bin/validators/test_check_farplane_project_files.py`
  manual:
    - Inspect generated template rollout counts for `skill-template`, `skill-eval-task`, `skill-qa-checklist`, and `farplane-framework`.
    - Inspect Farplane-UI manifest update without touching unrelated dirty files.
  review:
    - rubric: skill-system / registry-governance / framework-contract
      required_tas: TAS-A or explicit blocker
  evidence:
    - `skills/skill-maintenance/graph/skill-template-intelligence.json`
    - command output summarized in `tickets/TASK-0212/progress.md`
```

## Run Hints

- `Likely size:` large
- `Goal recommendation:` required
- `Budget hint:` one active local implementation window; no spend/deploy/push
- `Compute hint:` local_shared
- `Planning hint:` direct Goal execution from this ticket
- `Proof weight:` tests + review
- `Proof route:` mechanical validators first; reviewer if available before final completion

## State

- `result:` done
- `blocked:` no
- `latest_verification:` `python3 skills/skill-maintenance/scripts/check_skills.py --write`, `python3 bin/validators/check_farplane_project_files.py`, `python3 bin/validators/check_template_version_metadata.py --all`, registry/generator tests, project-file fallback tests, and targeted `py_compile` passed.
- `review:` formal reviewer lane not available in the current toolset; mechanical validators and ticket-scoped proof completed.
- `notes:` Farplane-UI is intentionally recorded as a stale `farplane-framework` consumer and missing `farplane-steer-config` until that project is migrated.
- `Final evidence:` progress log + generated rollout artifact summary + command results
- `Batchability:` single-ticket
- `Human inputs/assets:` none; operator pre-approved implementation
- `Credentials / external access:` none
- `Compute/runtime needs:` local Python only
- `Tooling gaps:` none expected
- `QA risks:` dirty worktree and sibling Farplane-UI local changes require scoped edits only
- `Human gates:` none; operator said get to work and run the created goal
- `Agent decision boundaries:` do not invent a new schema registry; do not rewrite unrelated docs; do not revert user changes

## Goal Packet

- `Goal packet:` active
- `Program:` `tickets/TASK-0212/program.md`
- `Progress:` `tickets/TASK-0212/progress.md`
- `Files:`
  - `tickets/TASK-0212/ticket.md`
  - `tickets/TASK-0212/program.md`
  - `tickets/TASK-0212/progress.md`
  - `docs/templates/registry.jsonl`
  - `rules/template-registry.toml`
  - `skills/skill-creator/references/SKILL_TEMPLATE.md`
  - `skills/skill-maintenance/scripts/generate_template_intelligence.py`
  - `skills/skill-maintenance/scripts/check_skills.py`
  - `bin/validators/sync_template_registry.py`
  - `bin/validators/check_farplane_project_files.py`
  - `farplane/manifest.json`
  - `../Farplane-UI/farplane/manifest.json`
- `Generated Goal prompt:` `tickets/TASK-0212/generated-goal-prompt.md`
- `Metric provider:` mechanical
- `Feedback preset:` none
- `Drift reviewer:` inline
- `Heartbeat:` none
- `Stop condition:` complete after done/proof checks pass or blocked by unrelated dirty worktree conflict
- `Final report:` concise changed files, rollout counts, checks, blockers, and next step

## State

- `next_action:` implement the active Goal Packet.
- `blocked:` no.
- `latest_verification:` none yet.
- `result:` in progress.

## Links

- `program:` `tickets/TASK-0212/program.md`
- `progress:` `tickets/TASK-0212/progress.md`
- `artifacts:` none yet
- `review:` pending
- `refs:`
  - `docs/templates/README.md`
  - `docs/features/registry.jsonl`
  - `docs/skills/registry.jsonl`
  - `docs/farplane-framework/project-files.md`
  - `tickets/TASK-0211/ticket.md`

## Notes

- Treat the sibling Farplane-UI worktree as user-owned and only edit
  `farplane/manifest.json` there.
