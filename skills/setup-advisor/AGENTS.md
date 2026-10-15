# `skills/setup-advisor/AGENTS.md`

`skills/setup-advisor/` owns project bootstrap, framework migration, the split
charter, and external-service setup. Editing rules for this folder:

- Keep bootstrap docs-first and visible: intake answers live in the generated
  `docs/bootstrap-brief.md` and `AGENTS.md`, not in chat.
- Use one adaptive intake; never add a second long interview loop (`MEM-0054`).
- Ask explicitly about local hook activation, local validator routing, optional
  heavy local gates, and any separate CI/deploy gate (`MEM-0057`).
- Leave each generated repo with one canonical app run path, one QA/evidence
  run path, required services, and port/env assumptions on visible repo-owned
  surfaces (`MEM-0068`).
- UI-bearing projects default to shadcn plus the tweakcn darkmatter theme, with
  the theme plan, tooltip-over-explainer rule and visual QA path recorded;
  plain HTML only for static/throwaway artifacts or operator opt-out
  (`MEM-0116`, `MEM-0118`).
- Never scaffold a product catalog, per-category strategy or worker policy, or
  a controller index. A clean bootstrap creates no retired project file and
  needs none to validate; run an old-reference sweep after scaffolding.
- Never auto-enable git hooks; generated push gates must not depend on
  Farplane-owned helper paths; duplication heuristics stay advisory.
- `references/TICKETS_README_TEMPLATE.md` and `references/TICKET_TEMPLATE.md`
  are byte copies of the repo's `tickets/README.md` and
  `tickets/templates/ticket.md`; re-copy them when those change
  (`tests/test_bootstrap.py` checks this).
- Tests: `python -m unittest discover -s skills/setup-advisor/tests -p 'test_*.py'`
  and `-s skills/setup-advisor/scripts`.
