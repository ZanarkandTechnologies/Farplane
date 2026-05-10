# Frontend Skill Scorecard

## Metric Card

Target user:

Codexter operators and frontend-building agents.

Job-to-be-done:

Produce frontend work that is less generic, more current with shadcn/registry capabilities, easier to verify, and still governed by Codexter's artifact-first skill topology.

Artifact being improved:

Frontend skill suite and references.

Primary behavior to improve:

Agents consistently make grounded frontend implementation choices before building instead of defaulting to generic components, stale registry assumptions, or underspecified visual direction.

Primary metric:

`frontend_skill_prebuild_completeness_rate`

Direction:

Increase.

Guard metric:

`frontend_skill_topology_sprawl_count` should not increase unless a new public skill earns a separate boundary.

Anti-metric:

`generic_ui_regression_rate`: number of frontend handoffs with uncustomized shadcn, missing states, stale package assumptions, or unsupported registry/theme commands.

Minimum meaningful delta:

For a small eval set of 8-12 frontend prompts, at least 80% should produce stack facts, visual dials/brief, registry/theme plan when relevant, state coverage, and QA gates before implementation.

Measurement method:

Create binary eval prompts for app UI, AI chat UI, dense dashboard, landing page, premium product page, redesign, visual polish, and delegated frontend run. Score output against required fields.

Judgement questions:

- Did the skill improve decision quality without bloating first-load instructions?
- Did it keep `frontend-craft` as orchestrator instead of creating competing entrypoints?
- Did registry/theme guidance stay official/current enough to trust?
- Did the preflight prevent actual build failures and visual slop?

## Manual Candidate Scores

| Candidate | User value | Evidence | Fit | Cost | Risk | Benchmarkability | Net |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| shadcn registry/CLI upgrade | 5 | 5 | 5 | 4 | 5 | 5 | 29 |
| frontend stack facts guard | 5 | 5 | 5 | 5 | 5 | 5 | 30 |
| durable design brief/design bible | 5 | 4 | 5 | 4 | 5 | 4 | 27 |
| component state/spec matrix | 5 | 4 | 5 | 4 | 5 | 5 | 28 |
| numeric taste dials | 4 | 5 | 5 | 5 | 4 | 4 | 27 |
| RSC/client motion isolation | 5 | 5 | 5 | 5 | 5 | 4 | 29 |
| image-first visual reference lane | 4 | 4 | 4 | 3 | 4 | 3 | 22 |
| searchable rule corpus | 3 | 3 | 4 | 2 | 4 | 3 | 19 |
| brand/logo/banner skill family | 3 | 4 | 3 | 2 | 3 | 2 | 17 |

## Recommended Eval Cases

1. Build an AI chat interface in an existing Next.js app with shadcn already configured.
2. Redesign a dense operations dashboard with existing tokens.
3. Create a premium product landing page requiring generated media and scroll proof.
4. Polish a form-heavy settings screen with missing error/loading/empty states.
5. Delegate a frontend repair phase to Pi/Kimi with an owned path and visual QA failure.
6. Add a component from a non-core shadcn registry and prove the registry/package path is valid.
7. Apply only a theme/font preset to an existing shadcn project without reinstalling components.
8. Implement motion in App Router without turning the whole page into a client component.
