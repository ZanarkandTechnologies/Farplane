---
ticket_id: TASK-0101
title: frontend skill topology
phase: complete
status: done
owner: codex
claimed_by:
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: false
requires_qa: false
requires_demo: false
created_at: 2026-05-03T14:58:45Z
updated_at: 2026-05-03T15:31:07Z
next_action: none; implementation and review complete
last_verification: 2026-05-03T15:31:07Z old cinematic landing package purged; validators and visible review pass
---

# TASK-0101: frontend skill topology

## Summary
Implement the agreed frontend skill split: keep `functional-ui` as a standalone UX/redesign entrypoint and make it a required planning lane inside a new `frontend-craft` orchestrator. Add granular `visual-design` and `landing-page` skills, fold stale cinematic/frontend implementation guidance behind references, and update durable docs so the shipped public capability is discoverable.

## Scope
- In: `frontend-craft`, `visual-design`, `landing-page`, `functional-ui` updates, compatibility routing for `frontend-design` and `cinematic-landing`, docs/memory/history inventory updates.
- Out: installing upstream community skills, adding external API credentials, changing hook/runtime behavior, or building a UI app.

## Plan
- `Change:` add a wrapper skill and granular frontend skills with clear routing.
- `Why:` the old frontend skill set mixed UX, taste, landing-page, GSAP, and asset-generation responsibilities, making it hard to know the right entrypoint.
- `Before -> After:` `frontend-design` plus `cinematic-landing` were the main public surfaces; now `frontend-craft` orchestrates implementation while `functional-ui`, `visual-design`, and `landing-page` remain directly invocable.
- `Touch:` `skills/frontend-craft/*`, `skills/visual-design/*`, `skills/landing-page/*`, `skills/functional-ui/*`, `skills/frontend-design/*`, `skills/cinematic-landing/*`, `skills/visual-qa/*`, `skills/testing/*`, `README.md`, `docs/specs/harness-techniques.md`, `docs/MEMORY.md`, `docs/HISTORY.md`, `AGENTS.md`.
- `Inspect:` local frontend skills, community repos under `/tmp/codexter-skill-research`, ticket/docs contracts, memory/troubles, skill-creator guidance.
- `Signature delta:`
  - `skills/frontend-craft/SKILL.md / route(request): FrontendSkillPath`
  - `skills/functional-ui/SKILL.md / redesign(current_ui, comparables): FunctionalUIHandoff`
  - `skills/visual-design/SKILL.md / shapeLook(functional_handoff): VisualBrief`
  - `skills/landing-page/SKILL.md / shapeOnePage(offer): LandingPageBrief`
- `Type Sketch:`
  - `FrontendSkillPath`: `mode`, `required_lanes`, `reference_files`, `handoff_target`
  - `FunctionalUIHandoff`: `users`, `diagnosis`, `comparables`, `recommended_model`, `states`, `implementation_notes`
  - `VisualBrief`: `register`, `scene_sentence`, `palette_strategy`, `typography`, `density`, `motion_taste`
  - `LandingPageBrief`: `offer`, `story_arc`, `sections`, `assets`, `scroll_motion`, `proof`
- `Typed flow example:` `"build dashboard"` -> `frontend-craft` -> `functional-ui` only if UX unsettled -> `visual-design` -> `frontend-design` references -> QA/review; `"functional-ui this bad settings panel"` -> `functional-ui` only -> implementation handoff.
- `Execution steps:`
  1. Add the new skill packages with first-load contracts and reference maps.
  2. Upgrade `functional-ui` for standalone broken-UI redesign and craft integration.
  3. Retarget `frontend-design` and `cinematic-landing` as compatibility/support surfaces.
  4. Update visual QA/testing references to the new landing-page surface.
  5. Update inventory, memory, history, and ticket evidence.
  6. Run validators plus a final review pass.
- `Recommendation:` wrapper plus granular skills, not one giant skill and not wholesale upstream replacement.
- `Options considered:` one giant `frontend-craft`; tiny standalone skills only; wrapper plus granular skills.
- `Blast radius:` skill discovery, frontend implementation routing, visual QA references, docs inventory.
- `Risks:` over-routing, stale old skill names, claiming external asset tooling is installed when it is not.

## Acceptance Criteria
- [x] `frontend-craft`, `visual-design`, and `landing-page` exist as discoverable skill packages.
- [x] `functional-ui` clearly supports both standalone broken-UI redesign and `frontend-craft` integration.
- [x] Existing `frontend-design` and `cinematic-landing` point to the new topology without deleting compatibility.
- [x] Motion, asset-generation, Pretext, HTML-in-Canvas, and upstream community skill learnings live as references, not scattered chat-only decisions.
- [x] Canonical docs/memory/history reflect the shipped capability.
- [x] Skill and ticket validators pass or any failures are documented.

## Verification
- `Tests:` `python3 skills/skill-creator/scripts/quick_validate.py` for touched/new skill packages; `python3 tickets/scripts/check_ticket_metadata.py`; doc/harness validators if available.
- `Manual checks:` re-read new `SKILL.md` files for first-load contract; grep for stale `cinematic-landing` routing.
- `Evidence required:` command results in this ticket.

## Refs
- Upstream evaluation repos:
  - https://github.com/pbakaus/impeccable
  - https://github.com/leonxlnx/taste-skill
  - https://github.com/greensock/gsap-skills
  - https://github.com/WICG/html-in-canvas
  - https://github.com/chenglou/pretext

## Evidence
- `Artifacts:`
  - [topology review artifact](artifacts/review/2026-05-03-frontend-skill-topology-review.json)
  - [cinematic landing purge review artifact](artifacts/review/2026-05-03-cinematic-landing-purge-review.json)
- `Commands:`
  - `python3 skills/skill-creator/scripts/quick_validate.py skills/frontend-craft` -> passed
  - `python3 skills/skill-creator/scripts/quick_validate.py skills/functional-ui` -> passed
  - `python3 skills/skill-creator/scripts/quick_validate.py skills/visual-design` -> passed
  - `python3 skills/skill-creator/scripts/quick_validate.py skills/landing-page` -> passed
  - `python3 skills/skill-creator/scripts/quick_validate.py skills/frontend-design` -> passed
  - `python3 skills/skill-creator/scripts/quick_validate.py skills/cinematic-landing` -> passed
  - `python3 skills/skill-creator/scripts/quick_validate.py skills/frontend-craft && python3 skills/skill-creator/scripts/quick_validate.py skills/functional-ui && python3 skills/skill-creator/scripts/quick_validate.py skills/visual-design && python3 skills/skill-creator/scripts/quick_validate.py skills/landing-page && python3 skills/skill-creator/scripts/quick_validate.py skills/frontend-design` -> all passed after deleting `skills/cinematic-landing`
  - `python3 tickets/scripts/check_ticket_metadata.py` -> `ticket metadata OK (8 ticket files checked)`
  - `python3 bin/check_harness_invariants.py` -> `harness invariants OK (5 files checked, 15 agents, 13 rules)`
  - `python3 bin/check_doc_parity.py` -> `structural doc parity OK (6 files checked, 29 rules)`
  - `rg -n "frontend-review|official GSAP skills|cinematic-landing.*owns|frontend-design.*visual execution|frontend-design handles visual" skills README.md AGENTS.md docs -g '*.md'` -> no stale matches
  - `rg -n "cinematic-landing|Cinematic Landing" . -g '*.md' -g '*.toml' -g '*.json' -g '!tickets/**' -g '!docs/HISTORY.md' -g '!docs/MEMORY.md'` -> no live references outside historical/memory trail
  - `find skills/cinematic-landing -maxdepth 3 -type f -print` -> no remaining files
  - `git diff --check -- AGENTS.md agents/frontend-designer.toml agents/qa-tester.toml docs/HISTORY.md docs/MEMORY.md docs/specs/harness-techniques.md skills/cinematic-landing skills/testing/references/index.md skills/visual-qa skills/landing-page/references/gotchas.md` -> passed
- `Result summary:` Added the frontend topology with a wrapper implementation entrypoint, standalone UX/redesign and visual/landing skill entrypoints, upstream reference files, docs inventory, memory, history, and visible review. Follow-up cleanup removed the old `skills/cinematic-landing` compatibility package and retargeted live agent, QA, testing, and docs references to `landing-page`. No UI visual QA was required because this ticket changed skills/docs rather than rendered UI.

## Blockers
- none
