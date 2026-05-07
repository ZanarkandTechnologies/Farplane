# Landing Page

## Purpose

Shape one-page, marketing, launch, portfolio, and cinematic frontend surfaces before implementation.

## Public API / Entrypoints

- `SKILL.md`: landing-page workflow
- `references/*`: scrolltelling, motion/media, and QA guidance
- `scripts/landing_spec_lint.py`: validates approved landing specs before build
- `scripts/section_quality_qa.cjs`: browser QA for section substance and visual carriers

## Minimal Example

1. Define the offer and audience.
2. Draft and approve `LANDING_SPEC.md`.
3. Validate it with `scripts/landing_spec_lint.py`.
4. Map assets, motion, and QA from the section matrix.
5. Hand off to `frontend-craft`.

## How to Test

- Confirm product app screens route away to `functional-ui`.
- Confirm cinematic/scroll requests do not duplicate GSAP API details.
- Run `python3 skills/skill-creator/scripts/quick_validate.py skills/landing-page`.
- Run `python3 skills/landing-page/scripts/test_landing_spec_lint.py`.
- Run `node --check skills/landing-page/scripts/section_quality_qa.cjs`.
