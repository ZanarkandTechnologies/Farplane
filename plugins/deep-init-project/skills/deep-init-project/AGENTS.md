# `skills/deep-init-project/AGENTS.md`

Rules for the `deep-init-project` skill surface.

## Purpose

`skills/deep-init-project/` owns project bootstrap scaffolding and the generated
artifact defaults for new or migrated repos.

## Keep

- bootstrap as a docs-first, visible-artifact workflow
- `deep-interview` as the canonical intake engine for ambiguous bootstrap work
- `docs/bootstrap-brief.md` as the visible bootstrap brief surface
- bootstrap-owned agent-experience/testability decisions captured in
  `docs/bootstrap-brief.md` and scaffolded `qa/` surfaces
- bootstrap-owned runtime and evidence-capture command guidance captured in
  `docs/bootstrap-brief.md`, `PROJECT_RULES.md`, and scaffolded `qa/` surfaces
- bootstrap-owned frontend UI initialization guidance captured in
  `docs/bootstrap-brief.md`, `PROJECT_RULES.md`, and `docs/TASTE.md` when the
  generated or migrated repo has a UI surface
- bootstrap-owned decisions about local hooks, optional heavy local gates, and
  separate CI/deploy protection captured in `docs/bootstrap-brief.md`
- optional `.githooks/` plus repo-local `scripts/pre_*_check.sh`
- manual hook activation and explicit project-owned validator commands

## Do Not

- duplicate the `deep-interview` loop inside `deep-init-project`
- auto-enable git hooks during bootstrap
- make generated repos depend on Codexter-owned helper paths for push gates
- turn utility-duplication heuristics into hard blockers in the default template

## Invariants

- `MEM-0054`: `deep-init-project` should reuse `deep-interview`-quality intake and
  generate a visible bootstrap brief rather than inventing a second shallow
  bootstrap interview flow.
- `MEM-0057`: `deep-init-project` bootstrap must ask explicitly about local
  hook activation, local validator routing, optional heavy local gates, and any
  separate CI/deploy gate instead of implying those choices.
- `MEM-0068`: `deep-init-project` bootstrap should leave each repo with one
  canonical app run path, one canonical QA/evidence run path, required local
  services, and the relevant port or environment-variable assumptions on
  visible repo-owned surfaces instead of relying on remembered shell commands.
- `MEM-0116`: UI-bearing project bootstrap should leave a visible shadcn/tweakcn
  theme plan, default darkmatter command or skip reason, tooltip-over-explainer
  rule, and visual QA evidence path in generated project artifacts.
- `MEM-0118`: UI-bearing app bootstrap defaults to shadcn plus tweakcn
  darkmatter. Plain HTML is only acceptable for explicit static/throwaway
  artifacts or user opt-out, not because the agent decided shadcn was
  unnecessary.
