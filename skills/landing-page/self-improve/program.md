# Self-Improve Program: landing-page

## Objective
make landing-page produce Terminal-quality spec-first cinematic industrial landing briefs with explicit asset generation, implementation, and QA contracts

## Current Contract
- Trigger: one-page, launch, homepage, hero-heavy, cinematic, scrolltelling, or brand/product landing requests.
- First-load workflow: define offer, select landing recipe/taste/effect records when applicable, map sections, plan assets/motion/proof, then hand off to frontend-craft.
- Outcome: a landing brief or implementation handoff with recipe route, story arc, section map, visual scenes/assets, motion plan, QA plan, and implementation instructions.
- Validation: binary evals require spec-first behavior, explicit asset generation contract, Terminal-style recipe/taste/effect selection, mobile/reduced-motion proof, and comparison-driven improvement notes.

## Eval Metric
- Primary: `skill_eval_pass_rate`
- Direction: higher
- Minimum meaningful delta: +0.10 pass rate on the smoke suite or one newly passing known-failure case.
- Simplicity guard: keep SKILL.md compact; prefer references/evals over duplicating long visual rules in the trigger file.

## Rubric
- Spec-first before build for cinematic/premium landing asks
- Explicit generated-asset and frame/fallback plan
- Gold-reference comparison against Terminal-style production quality
- Mobile, reduced-motion, and scroll-checkpoint QA
- Improvement hypotheses tied to observed failures

## Durable Evals
- `evals/test_cases.jsonl`
- `evals/assertions.md`

## Experiment Log
| Date | Run | Hypothesis | Result | Keep? | Lesson |
| --- | --- | --- | --- | --- | --- |
| 2026-05-05 | setup | Create skill-local memory | Baseline memory surface created | yes | Future runs should record durable lessons here. |
| 2026-05-05 | terminal-warehouse | Split Terminal-style landing work into spec/assets/implementation/visual-review phases | Pi/Kimi could create a spec and partial files, but broad and repair prompts timed out; rendered output remained below Terminal quality | yes | Terminal-quality pages need a hard spec gate, generated-media contract, and smaller external-builder prompts. |

## Accepted Learnings
- Terminal Industries quality is not just palette/nav imitation; it depends on
  physical-world media fidelity, object scale, deliberate mobile crop, and
  proof-ready visual restraint.
- Timed-out external CLI runs with partial files are benchmark failures even
  when the page can be repaired enough to render.
- Broad prompts that ask one agent to spec, build, generate assets, review, and
  repair a cinematic page should be replaced with phase-specific prompts.
- Code-native SVGs can be useful placeholders, but a Terminal-quality claim
  needs real or generated hero media, frame/poster fallbacks, and visual QA.

## Rejected Ideas
- None yet.

## Next Hypotheses
- Baseline the current skill/profile against the Terminal-style warehouse CV task.
- If the baseline builds before producing a spec, strengthen the landing-page workflow and delegate-frontend prompt contract around spec-first gates.
- If the baseline lacks generated asset/frame/fallback detail, add a spec-first cinematic asset checklist to landing-page references.
- Build 20-100 diverse cases before trusting overnight optimization.
- Add a visual-scoring runner that compares screenshot geometry: object fill
  ratio, nav containment, mobile overflow, first-viewport dead space, and asset
  404s.
