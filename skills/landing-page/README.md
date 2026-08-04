# Landing Page

## Purpose

Shape one-page, marketing, launch, portfolio, and cinematic frontend surfaces before implementation.

## Public API / Entrypoints

- `SKILL.md`: landing-page workflow
- `references/*`: research synthesis, product-demo media, scrolltelling, motion/media, asset evidence, and QA guidance
- `scripts/landing_spec_lint.py`: validates approved landing specs before handoff
- `scripts/asset_evidence_lint.py`: downstream validator named by premium specs
- `scripts/section_quality_qa.cjs`: downstream browser QA named by the proof plan
- `SKILL.md` Todo List: modern scroll-scrub landing recipe checklist
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
8. Resolve Asset Advisor outputs or blockers required for spec approval.
9. Return the approved spec to the calling `impl-plan` for one unified Change
   Plan.

## How to Test

- Confirm modern scroll-scrub requests follow the `SKILL.md` Todo List before
  spec handoff.
- Score a Terminal-style output with `python3 skills/landing-page/scripts/terminal_landing_score.py`.
- Confirm product app screens route away to `functional-ui`.
- Confirm JSON registries parse with `python3 -m json.tool`.
- Confirm cinematic/scroll requests do not duplicate GSAP API details.
- Confirm the skill returns `LANDING_SPEC.md` and never implements, renders, or
  deploys the page.
- Run `python3 skills/skill-creator/scripts/quick_validate.py skills/landing-page`.
- Run `python3 skills/landing-page/scripts/test_landing_spec_lint.py`.
- Run `python3 skills/landing-page/scripts/test_asset_evidence_lint.py`.
- Run `node --check skills/landing-page/scripts/section_quality_qa.cjs`.
