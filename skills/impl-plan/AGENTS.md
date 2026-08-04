# Impl Plan Maintenance

## Scope

- `SKILL.md`
- `prompts/plan.md`
- `qa_checklist.md`
- `references/examples.md`
- `references/visual-companion-template.md`
- `scripts/validate_visual_companion.py`
- `README.md`

## Ownership

- Keep one public planner: `impl-plan`.
- Keep the sole ticket-body schema in `tickets/templates/ticket.md`.
- Keep `references/template.md` as a superseded pointer for historical links,
  never as an active planning surface.
- Keep repo policy in root `AGENTS.md`; keep planning mechanics here.
- Keep Goal runtime configuration in `goal-advisor` and Goal sidecars.

## Contract

- Treat a selected coherent ticket as the planning boundary. Split only across
  a real proof, reusable-foundation, migration, external-blocker, or runtime
  boundary.
- Inspect existing code, tests, docs, components, assets, accepted briefs, and
  implementation evidence before adding surfaces.
- Reuse sufficient planning context. Advisors resolve only a named
  `targeted_refresh` or `create` gap; they do not produce child plans.
- Use Change Plan units as the executable file map. Include real files,
  operation, material contract/type impact, local proof, and failure boundary;
  do not repeat global Delta, QA, Docs, or route policy in every unit.
- Add architecture signatures and typed movement only when they improve
  ownership or interface review.
- Keep Done and QA concrete. Preserve Agent Testability Briefs and require
  independent review for material claims.
- Use inline text/Mermaid only when it replaces prose. Use a linked
  `diagrams.md` only for complex multi-view or independently reviewed visual
  needs; validate it when present.
- Keep bulky execution evidence in `progress.md` or ticket artifacts.

## Checks

- `SKILL.md`, prompt, README, examples, QA checklist, and validators agree.
- The canonical ticket template is the only active section catalogue.
- Simple backend plans do not manufacture advisor work, diagrams, services,
  configuration, or broad research.
- Complex plans remain executable without transcript memory.
- The ticket validator reports raw first-load context plus Markdown categories;
  raw context remains the gate.
- Optional companions pass only when link, file, metadata, sections, legends,
  and semantic Mermaid classes agree.
- Every edited authored skill file stays within the repository line budget.
- Material skill changes receive independent review and a dated audit.

## Testing

- Run focused validator and companion tests.
- Run skill quick validation, eval query checks, skill registry generation and
  tests, document-reference checks, and skill surface-budget checks.
- Validate a simple ticket without a companion and a linked valid companion.
- Re-read the canonical ticket template and this skill once for drift.
