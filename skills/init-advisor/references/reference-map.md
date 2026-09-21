# Init Advisor Reference Map


- [README.md](README.md) - load when the user asks what InitAdvisor sets up,
  how to run bootstrap manually, or how brownfield migration works.
- [references/project-profiles.md](references/project-profiles.md) - load when
  selecting project type, components, advice axes, prototype gates, and
  downstream handoff.
- [references/project-lifecycle.md](references/project-lifecycle.md) - load
  when recording the bootstrap route and next lifecycle phase.
- [references/MANIFEST_TEMPLATE.json](references/MANIFEST_TEMPLATE.json) -
  copied to `farplane/manifest.json` for the Farplane project spec instance.
- [references/FRAMEWORK_CHANGELOG.md](references/FRAMEWORK_CHANGELOG.md) -
  load before bumping `farplane-framework` versions or migrating projects
  between framework spec versions.
- [references/GITIGNORE_TEMPLATE](references/GITIGNORE_TEMPLATE) - appended to
  `.gitignore` so generated local runtime state and active ticket work stay out
  of commits while shared ticket and local-skill scaffold remains trackable.
- [references/FEATURES_README_TEMPLATE.md](references/FEATURES_README_TEMPLATE.md)
  - copied to `docs/features/README.md` for feature-spec guidance.
- [references/SYSTEMS_README_TEMPLATE.md](references/SYSTEMS_README_TEMPLATE.md)
  - copied to `docs/systems/README.md` for system/product grouping guidance.
- [references/automation-templates/](references/automation-templates/) - copied
  to `farplane/automations/` as one reviewable Markdown file per project-local
  Codex automation. Office-wide Daily/Weekly records are not project templates.
- [references/CODE_SCAFFOLD_RECIPES.md](references/CODE_SCAFFOLD_RECIPES.md) -
  load only when `include_code_scaffold == true`, the user asks which stack can
  be scaffolded, or stack setup commands need review.
- [references/FOUNDATION_FIND_CUSTOMER_TICKET_TEMPLATE.md](references/FOUNDATION_FIND_CUSTOMER_TICKET_TEMPLATE.md),
  [references/FOUNDATION_DELIVER_VALUE_TICKET_TEMPLATE.md](references/FOUNDATION_DELIVER_VALUE_TICKET_TEMPLATE.md),
  and [references/FOUNDATION_COLLECT_REVENUE_TICKET_TEMPLATE.md](references/FOUNDATION_COLLECT_REVENUE_TICKET_TEMPLATE.md)
  - copied to `TASK-0001` through `TASK-0003` as the dependency-ordered
    business foundation.
- [references/PROJECT_RULES_TEMPLATE.md](references/PROJECT_RULES_TEMPLATE.md)
  - copied to `PROJECT_RULES.md` for project stack, runtime, and QA commands.
- [references/TICKETS_README_TEMPLATE.md](references/TICKETS_README_TEMPLATE.md)
  and [references/TICKET_TEMPLATE.md](references/TICKET_TEMPLATE.md) - packaged
  ticket lifecycle/template scaffolds used by both source and installed runs.
- [references/qa/](references/qa/) - copied when creating the QA cookbook
  surface.
- [../harness-creator/SKILL.md](../harness-creator/SKILL.md) - call in full
  mode after substrate setup when static charter, capability workflows, metric objectives, feedback
  loops, missing systems, automation/binding deltas, or metric objectives
  need project-specific setup.
- [../../docs/farplane-framework/project-files.md](../../docs/farplane-framework/project-files.md)
  - load when the user asks why a Farplane project has these files or how the
  spec should evolve.
- [prompts/plan.md](prompts/plan.md) and [prompts/build.md](prompts/build.md) -
  load only when the user asks for reusable planning/build prompts.
