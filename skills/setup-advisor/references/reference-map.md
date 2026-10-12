# Setup Advisor Reference Map

## Init and migrate

- [migration.md](migration.md) - what bootstrap writes, brownfield upgrade
  steps, and the finish checklist.
- [phase-boundary.md](phase-boundary.md) - `human_intake` choices and when the
  operating model counts as initialized.
- [project-profiles.md](project-profiles.md) - project type, components,
  advice axes, prototype gates, downstream handoff.
- [project-lifecycle.md](project-lifecycle.md) - lifecycle phase owners
  recorded in the bootstrap brief.
- [FRAMEWORK_CHANGELOG.md](FRAMEWORK_CHANGELOG.md) - read before bumping
  `farplane-framework` or migrating between spec versions.
- [CODE_SCAFFOLD_RECIPES.md](CODE_SCAFFOLD_RECIPES.md) - only when a code or
  app scaffold is in scope or stack commands need review.
- [../prompts/plan.md](../prompts/plan.md), [../prompts/build.md](../prompts/build.md)
  - only when the operator asks for reusable plan/build prompts.

## Scaffold templates (copied by `scripts/bootstrap.sh`)

| Template | Target |
| --- | --- |
| `AGENTS_TEMPLATE.md`, `ARCHITECTURE_TEMPLATE.md` | `AGENTS.md`, `ARCHITECTURE.md` |
| `FARPLANE_README_TEMPLATE.md`, `MANIFEST_TEMPLATE.json` | `farplane/README.md`, `farplane/manifest.json` |
| `HARNESS_TEMPLATE.yaml`, `METRICS_TEMPLATE.yaml`, `BINDINGS_TEMPLATE.yaml` | the split charter in `farplane/` |
| `PM_TEMPLATE.json`, `LOCAL_SKILLS_README_TEMPLATE.md` | `farplane/pm.json`, `.agents/skills/README.md` |
| `BOOTSTRAP_BRIEF_TEMPLATE.md`, `TASTE_TEMPLATE.md` | `docs/bootstrap-brief.md`, `docs/TASTE.md` |
| `FEATURES_README_TEMPLATE.md`, `SYSTEMS_README_TEMPLATE.md` | `docs/features/README.md`, `docs/systems/README.md` |
| `CODE_REVIEW_TEMPLATE.md`, `REVIEW_AGENT_TEMPLATE.md` | `docs/code_review.md`, `docs/review-agent.md` |
| `TICKETS_README_TEMPLATE.md`, `TICKET_TEMPLATE.md` | byte copies of the repo's `tickets/README.md` and `tickets/templates/ticket.md` |
| `FOUNDATION_*_TICKET_TEMPLATE.md` | `tickets/TASK-0001..0003` foundation drafts |
| `GITHOOKS_README_TEMPLATE.md`, `PRE_*_HOOK_TEMPLATE.sh` | opt-in `.githooks/` |
| `PRE_*_CHECK_TEMPLATE.sh`, `COLLECT_REVIEW_CONTEXT_TEMPLATE.sh`, `CODEX_REVIEW_AGENT_TEMPLATE.ts`, `RUN_PRE_PUSH_REVIEW_TEMPLATE.sh` | `scripts/` gates and diff reviewer |
| `GITIGNORE_TEMPLATE` | appended to `.gitignore` |

## Charter (`charter` mode)

- [../templates/project-harness.md](../templates/project-harness.md) - transient
  review worksheet, never the charter.
- [../templates/capability-map.md](../templates/capability-map.md) - large
  capability inventory only.
- [../templates/missing-primitive-plan.md](../templates/missing-primitive-plan.md)
  - a material missing feedback or KPI primitive.
- [../templates/goal-advisor-handoff.md](../templates/goal-advisor-handoff.md) -
  a selected ticket ready for Goal Advisor.
- [goal-advisor metric card](../../goal-advisor/references/metrics.md) - deep
  metric or guard design.
- [project-files contract](../../../docs/farplane-framework/project-files.md) -
  why a Farplane project has these files.

## Deploy (`deploy` mode)

- [../templates/setup-wizard.sh](../templates/setup-wizard.sh) - copy only for
  irreducible human gates; never edit its library section in the copy.
