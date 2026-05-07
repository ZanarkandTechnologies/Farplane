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
- Artifact score: `terminal_landing_score_percent >= 80` for generated Terminal/Terminus pages
- Direction: higher
- Minimum meaningful delta: +0.10 pass rate on the smoke suite or one newly passing known-failure case.
- Simplicity guard: keep SKILL.md compact; prefer references/evals over duplicating long visual rules in the trigger file.

## Rubric
- Spec-first before build for cinematic/premium landing asks
- Explicit generated-asset and frame/fallback plan
- Gold-reference comparison against Terminal-style production quality
- Mobile, reduced-motion, and scroll-checkpoint QA
- Improvement hypotheses tied to observed failures
- Terminal scroll review score across strategy/spec, asset pipeline,
  scroll-scrub mechanics, visual craft proxy, mobile/reduced motion, and
  delegation evidence

## Durable Evals
- `evals/test_cases.jsonl`
- `evals/assertions.md`

## Experiment Log
| Date | Run | Hypothesis | Result | Keep? | Lesson |
| --- | --- | --- | --- | --- | --- |
| 2026-05-05 | setup | Create skill-local memory | Baseline memory surface created | yes | Future runs should record durable lessons here. |
| 2026-05-05 | terminal-warehouse | Split Terminal-style landing work into spec/assets/implementation/visual-review phases | Pi/Kimi could create a spec and partial files, but broad and repair prompts timed out; rendered output remained below Terminal quality | yes | Terminal-quality pages need a hard spec gate, generated-media contract, and smaller external-builder prompts. |
| 2026-05-07 | scroll-scrub-todo-recipe | Add a loaded checklist that forces competitor analysis, user-story section planning, ASCII flow, nested `advise`, hero media generation, scroll-scrub conversion, and QA before implementation | Added `todos.md` and wired it into landing-page first-load and spec-first references | yes | The missing behavior was not only stricter QA; the skill needed an ordered pre-build recipe agents can follow without inference. |
| 2026-05-07 | terminal-scroll-review-score | Add a domain review rubric and score runner so Terminal/Terminus self-improvement can chase an 80-point observable artifact target | Added `terminal-scroll-review.md` and `terminal_landing_score.py`; baseline scoring should drive the next prompt/profile repair | yes | Human taste still matters, but the loop needs a mechanical score that combines spec, assets, scroll, mobile, and delegation evidence. |
| 2026-05-07 | warehouse-cv-score-loop | Run Pi/Kimi and a local sidecar control through the Terminal score | Pi/Kimi code-native output improved from `43` stub score to `61/100` after QA but failed Terminal gates; the local sidecar control wired generated videos and passed the pre-offer-gate content score at `90/100` | yes | The recipe target is reachable when generated hero/support media are wired as a sidecar, but delegation success requires Pi/Kimi to produce that sidecar plus a complete handoff. |
| 2026-05-07 | initial-offer-gate | Add a first-viewport hero-offer visibility gate after a mechanically passing sidecar still felt weak at first paint | `scroll_scrub_qa.cjs` now reports `hasInitialHeroOfferVisible`; the hidden-headline Pi sidecar dropped to revise, and the direct Pi repair restored a `99/100` Terminal score | yes | Terminal-quality scroll pages must communicate the offer before scroll; dominant media without visible copy is a real failure, not just a taste nit. |

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
- Modern scroll-scrub landing work should start with competitor/reference
  analysis, user-story section selection, an ASCII page flow, and nested
  `advise` decisions per section before any asset generation or implementation.
- Terminal/Terminus self-improvement should report `terminal_landing_score.py`
  results. A sub-80 score should name the weakest dimension as the next
  hypothesis instead of broadly asking the builder to "make it better."
- A media sidecar can convert an otherwise weak code-native prototype into a
  Terminal-ready mechanics artifact by wiring generated videos, mediaTime
  scrub, support videos, and large checkpoint deltas. Treat this as the target
  pattern for external builders, not as proof that Pi/Kimi produced it.
- A hero can pass media and scroll mechanics while still failing first
  impression. Require `hasInitialHeroOfferVisible` so the main headline or
  offer is visible at first paint, before any scroll-scrub reveal.

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
