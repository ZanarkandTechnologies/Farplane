# Frontend Skill Improvement Handoff

## Recommendation

Keep Codexter's frontend skill structure. Do not use either external repo as a base. Adapt the strongest techniques into the existing topology:

- `frontend-craft`: add stack facts and pre-build completeness gate.
- `frontend-design`: update shadcn/tweakcn/registry guidance to current official CLI/MCP behavior.
- `visual-design`: make taste dials numeric and add a durable design-brief output.
- `functional-ui` / `frontend-design`: add component state/spec matrix for reusable components.
- `landing-page`: borrow image-first section consistency ideas, but keep Codexter's stronger spec/media/QA gates.
- `delegate-frontend`: require delegate prompts to include design brief path, stack facts, registry/theme plan, and state/QA proof where relevant.
- `visual-qa`: add final preflight checks for small-phone, landscape, dynamic text, reduced motion, touch targets, contrast, theme parity, and no horizontal scroll.

## Proposed Ticket Slice

Title:

`TASK-frontend-skill-upgrade-current-registry-and-design-brief`

Scope:

1. Update `skills/frontend-design` references:
   - official shadcn MCP/Codex config caveat,
   - `components.json` advanced registries/auth,
   - registry index usage,
   - `shadcn search`, `view`, `docs`, `info`,
   - `shadcn apply --only theme/font`,
   - `preset` decode/resolve/open,
   - domain shortlist from current registry index:
     `@ai-elements`, `@assistant-ui`, `@agents-ui`, `@tool-ui`, `@auth0`, `@clerk`, `@billingsdk`, `@formcn`, `@better-upload`, `@evilcharts`, `@aceternity`, `@animate-ui`, `@cult-ui`, `@unlumen-ui`, `@8bitcn`, `@retroui`, `@boldkit`.
2. Update `skills/frontend-craft`:
   - stack facts card before implementation,
   - package/Tailwind/version checks,
   - RSC/client-leaf motion guidance,
   - preflight handoff requirement.
3. Update `skills/visual-design`:
   - numeric taste dials,
   - optional archetype recipe reference,
   - durable `DESIGN_BRIEF` output for substantial app UI.
4. Add `frontend-design` or `visual-design` reference for:
   - three-layer token architecture,
   - component state/spec matrix,
   - theme/preset/tweakcn workflow.
5. Update `delegate-frontend` prompt contract:
   - include design brief path,
   - stack facts,
   - registry/theme plan,
   - component state/QA proof expectation.
6. Update `visual-qa` or `frontend-craft/references/qa.md`:
   - small phone 375px,
   - landscape,
   - dynamic text/text-fit,
   - reduced motion,
   - touch targets,
   - dark/light contrast,
   - theme parity,
   - no hidden fixed content,
   - no horizontal scroll.

Out of scope:

- Creating a separate brandkit/logo/banner public skill.
- Importing external skill files wholesale.
- Building a searchable frontend rule CLI.
- Adding validators/scripts before a concrete eval or implementation ticket proves need.

## Production Expectation

A credible frontend skill pass should leave enough evidence that an agent:

- knows the user/job and functional states,
- knows the visual register and numeric taste dials,
- knows the actual stack and installed packages,
- knows whether Tailwind v3/v4 and shadcn are present,
- used current registry/theme discovery instead of stale assumptions,
- preserved or created a design brief,
- specified component states for reusable UI,
- planned browser/visual QA beyond desktop screenshots.

## Missing Gaps

Current Codexter does not consistently require:

- stack facts before frontend implementation,
- official shadcn current CLI/MCP registry flow,
- current registry index exploration,
- theme/font preset application via `shadcn apply`,
- durable design brief for app UI,
- component state/spec matrices,
- package/Tailwind/RSC motion guard,
- frontend-specific final preflight coverage.

## Implementation Order

1. Patch `frontend-design` docs first because registry/theme guidance is the most concrete and lowest risk.
2. Patch `frontend-craft` routing and QA references so the new guidance is actually invoked.
3. Patch `visual-design` dials/design-brief contract.
4. Patch `delegate-frontend` to pass the same constraints to external workers.
5. Add focused eval prompts or checklist tests only after the docs stabilize.

## Review Notes

Expected review families:

- skill routing clarity,
- no topology sprawl,
- official-doc accuracy for shadcn,
- first-load brevity,
- implementation handoff completeness,
- no external-source instruction leakage.
