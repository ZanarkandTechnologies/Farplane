# Landing Page

## Purpose

Shape one-page, marketing, launch, portfolio, and cinematic frontend surfaces before implementation.

## Public API / Entrypoints

- `SKILL.md`: landing-page workflow
- `references/*`: research synthesis, product-demo media, scrolltelling, motion/media, asset evidence, and QA guidance
- `scripts/landing_spec_lint.py`: validates approved landing specs before build
- `scripts/asset_evidence_lint.py`: validates generated/real media evidence after build
- `scripts/section_quality_qa.cjs`: browser QA for section substance and visual carriers
- `SKILL.md` Important Checklist: modern scroll-scrub landing recipe checklist
- `references/*`: scrolltelling, JSON registries, motion/media, and QA guidance
- `scripts/terminal_landing_score.py`: Terminal/Terminus-style self-improvement score runner

## Minimal Example

1. Define the offer and audience.
2. Research competitors/inspiration and synthesize best-of-worlds decisions.
3. Brainstorm the differentiated creative take.
4. Draft and approve `LANDING_SPEC.md`.
5. Validate it with `scripts/landing_spec_lint.py`.
6. For product/device/equipment pages, define realistic product shots,
   assembly/disassembly or exploded-view media, and feature callouts.
7. Map assets, motion, and QA from the section matrix.
8. Generate or collect required media assets for premium/cinematic pages.
9. Hand off to `frontend-craft` or `delegate-frontend`.
2. For modern cinematic or Terminal-style work, follow the `SKILL.md` Important Checklist.
3. Pick recipe, taste-profile, and effect-stack records when a reusable formula applies.
4. Map sections, story beats, and the ASCII page flow.
5. Plan assets and motion.
6. Hand off to `frontend-craft`.

## How to Test

- Confirm modern scroll-scrub requests follow the `SKILL.md` Important Checklist before implementation.
- Score a Terminal-style output with `python3 skills/landing-page/scripts/terminal_landing_score.py`.
- Confirm product app screens route away to `functional-ui`.
- Confirm JSON registries parse with `python3 -m json.tool`.
- Confirm cinematic/scroll requests do not duplicate GSAP API details.
- Run `python3 skills/skill-creator/scripts/quick_validate.py skills/landing-page`.
- Run `python3 skills/landing-page/scripts/test_landing_spec_lint.py`.
- Run `python3 skills/landing-page/scripts/test_asset_evidence_lint.py`.
- Run `node --check skills/landing-page/scripts/section_quality_qa.cjs`.
