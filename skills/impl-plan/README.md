# Impl Plan

## Purpose

`impl-plan` turns one selected software or product request into one
approval-ready canonical ticket. It inventories repository leverage and
accepted planning context, resolves only material gaps, and produces an
executable Change Plan plus proof contract before `goal-advisor` compiles
execution.

The sole ticket-body schema is
[`tickets/templates/ticket.md`](../../tickets/templates/ticket.md). The skill
owns reasoning and context resolution, not a second template.

## Entrypoints

- `SKILL.md`: planning workflow and decision contract.
- `prompts/plan.md`: compact operator prompt.
- `qa_checklist.md`: readiness and maintenance checks.
- `references/examples.md`: optional output calibration.
- `references/visual-companion-template.md`: optional detailed diagram
  companion.
- `scripts/validate_visual_companion.py`: validates a companion when linked or
  present; no companion is required for a simple ticket.
- `AGENTS.md`: maintenance rules.

`references/template.md` is a historical migration pointer only. Do not load
it as an active schema.

## Minimal Flow

1. Read `SKILL.md`, its checklist, and the selected ticket.
2. Inspect relevant code, tests, docs, accepted briefs, assets, and evidence.
3. Resolve required context as `reuse`, `targeted_refresh`, `create`, `block`,
   or `not_applicable`; call advisors only for a real refresh or creation gap.
4. Populate the canonical ticket template with compact Change Plan units.
5. Use an inline map only when it replaces prose; create `diagrams.md` only
   for complex multi-view or independently reviewed visual context.
6. Run the ticket validator, apply `qa_checklist.md`, and reconcile a material
   reviewer receipt before `approval_ready`.
7. After human approval, hand the same ticket to `goal-advisor`.

## Testing

- The canonical ticket template is the only active body schema.
- Plans reuse accepted context and existing code surfaces before adding new
  work or calling advisors.
- Change units identify files, operation, material contract impact, local
  proof, and failure boundary without repeating global sections.
- Done and QA are observable and proportional to risk.
- Simple tickets pass without diagrams; linked or orphaned companions are
  validated; inline Mermaid is allowed when useful.
- `farplane validate ticket ... --phase planning` reports raw first-load
  context plus prose, Mermaid, media, and reference categories.
- Material plans have independent review; Goal compilation happens only after
  ticket approval.
