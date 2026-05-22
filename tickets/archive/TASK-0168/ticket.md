---
ticket_id: TASK-0168
title: apply tier 3 pipeline model to video-production
phase: complete
status: done
owner: unassigned
claimed_by:
priority: medium
depends_on:
  - TASK-0165
  - TASK-0170
blocked_by: []
ready: true
approval_required: false
requires_qa: true
requires_demo: false
created_at: 2026-05-22T02:58:18+08:00
updated_at: 2026-05-22T03:14:00+08:00
next_action: none
last_verification: 2026-05-22 - skill maintenance, ticket metadata, and whitespace checks passed
---

# TASK-0168: apply tier 3 pipeline model to video-production

## Summary
Refactor `video-production` into the compact Tier 3 pipeline pattern while
preserving its existing method addresses and production boundaries. This skill
is a router over scripts, storyboards, ad specs, generated clips, Remotion
assembly, and frontend campaign handoffs, so it should expose a scannable
model instead of relying mainly on prose.

The base skill should own the domain router and short checklist. Method
references should remain method packets for marketing, explainer, storyboard,
talking-head, and ad-spec details rather than acting as independent subskills.

## Scope
- In:
  - add compact `VideoProduction := Brief + Audience + ChannelPlan + SceneMatrix + MethodSet + AssetPlan + DeliveryPlan + ProofPlan`
    model to `skills/video-production/SKILL.md`
  - add `skills/video-production/references/model.md` with scene/deliverable
    matrix, method selection, execution packets, and proof
  - shorten `skills/video-production/todos.md` so it points to the model and
    method refs
  - preserve existing method addresses:
    `video-production:marketing`, `video-production:explainer`,
    `video-production:storyboard`, `video-production:talking-head`, and
    `video-production:ad-spec`
  - add a method-selection smoke reference for choosing primary/supporting
    video methods
  - update generated registry and durable docs as required by `close-ticket`
- Out:
  - creating standalone subskills for each video method
  - changing model-native generation, Remotion, or render tooling
  - publishing, uploading, buying media, or approving likeness/identity assets
  - rewriting upstream references unless a method packet needs a small local
    proof checklist

## Plan
- `Change:` make `video-production` a model-first Tier 3 router with method
  packets and a short todo recipe.
- `Why:` video-production decomposes work into scenes, channels, methods,
  asset routes, and delivery proof. The current method list is strong, but the
  execution shape is easier to maintain as a matrix plus packets.
- `Before -> After:`
  - Before: the skill lists methods and a long sequence of production routing
    steps.
  - After: the skill defines `VideoProduction`, `Scene/Deliverable`,
    `VideoMethod`, and `ExecutionPacket`; todos become a compact
    anti-forgetting checklist.
- `Touch:`
  - `skills/video-production/SKILL.md`
  - `skills/video-production/todos.md`
  - `skills/video-production/references/model.md`
  - `skills/video-production/references/method-selection-smoke.md`
  - `docs/skills/registry.jsonl`
  - `docs/HISTORY.md`
- `Inspect:`
  - `skills/video-production/SKILL.md`
  - `skills/video-production/todos.md`
  - `skills/video-production/references/upstream-marketing.md`
  - `skills/video-production/references/prompting-marketing.md`
  - `skills/video-production/references/upstream-explainer.md`
  - `skills/video-production/references/upstream-storyboard.md`
  - `skills/video-production/references/upstream-talking-head.md`
  - `skills/video-production/references/upstream-ad-spec.md`
  - `skills/video-generation/references/domain-production.md`
  - `skills/skill-creator/references/tier3-pipeline-model.md`
- `Signature delta:`
  - `skills/video-production/SKILL.md / methods: video-production:*`
  - `skills/video-production/references/model.md / VideoProduction(brief): SceneMatrix`
  - `skills/video-production/references/model.md / MethodSelection(deliverable, methods, constraints): ExecutionPacket`
  - `skills/video-production/todos.md / checklist(model, method, route, proof): done`
- `Type Sketch:`
  - `VideoProduction`: `brief`, `audience`, `channel_plan`, `scene_matrix`,
    `method_set`, `asset_plan`, `delivery_plan`, `proof_plan`
  - `SceneOrDeliverable`: `id`, `job`, `channel`, `duration`, `format`,
    `source_assets`, `candidate_methods`, `chosen_method`, `asset_routes`,
    `delivery_outputs`, `proof`
  - `VideoMethod`: `id`, `use_when`, `avoid_when`, `inputs`, `outputs`,
    `routing`, `risk`, `proof`
  - `ExecutionPacket`: `deliverable_id`, `method_id`, `script_or_panel_steps`,
    `asset_routes`, `generation_route`, `delivery_specs`, `qa`
- `Typed flow example:`
  - User asks for a product explainer video plus TikTok ad cutdown.
  - The skill creates an explainer deliverable row and an ad-spec row.
  - It chooses `video-production:explainer` as primary and
    `video-production:ad-spec` as supporting for safe zones, duration, and
    platform deliverables.
  - Packets route script/storyboard planning through video-production,
    generated clips through `video-generation`, deterministic overlays through
    `remotion`, and final proof through `execute`.
- `Execution steps:`
  1. Add compact model prelude to `SKILL.md`.
  2. Add `references/model.md` with scene/deliverable matrix, method set,
     selection rule, execution packet, and proof plan.
  3. Add `references/method-selection-smoke.md` with marketing, explainer,
     storyboard, talking-head, and ad-spec cases.
  4. Shorten `todos.md` to ground, model, select method, draft, route assets,
     prove, and preserve publish/likeness boundaries.
  5. Keep upstream and prompting refs as method detail; add method-specific
     checklist snippets only when a method has extra proof obligations.
  6. Regenerate and validate skill registry.
  7. Run review and update evidence.
- `Recommendation:` base router owns the model and todos; method refs own
  method-specific production constraints. Do not create nested router skills.
- `Options considered:`
  1. Per-method subskills: rejected because shared production routing and proof
     would be duplicated.
  2. Base router plus method references: chosen because it preserves method
     addresses and keeps complex production choices scannable.
  3. Leave as-is: rejected because video-production is a high-fit candidate
     for the Tier 3 project/component/method model.
- `Blast radius:`
  - video production planning
  - video/image/remotion/frontend handoff routing
  - generated registry method visibility
  - future video workflow migrations
- `Risks:`
  - accidentally hiding consent/likeness/publish boundaries in a shorter todo
  - over-abstracting quick storyboard or script requests
  - breaking method-address clarity in the registry

## Gap Analysis
- `Current state:` `video-production` already has method addresses and many
  references, but no compact model file or selection smoke example.
- `Production expectation:` video projects should make audience, channel,
  duration, scene/deliverable matrix, asset routes, consent boundaries,
  delivery specs, and proof explicit before generation.
- `Missing gaps:` model reference, scene/deliverable matrix, execution packet
  shape, smoke examples, and shortened todos.
- `Comparable implementations:` `landing-page` model and `TASK-0165` Tier 3
  pipeline guide.
- `Recommendation:` land this as a docs/skill-structure migration only.

## Diagram
```mermaid
flowchart LR
  A["Video brief"] --> B["Scene/deliverable matrix"]
  B --> C["Method selection"]
  C --> D["Execution packets"]
  D --> E["video-generation / remotion / frontend routes"]
  E --> F["delivery proof + boundaries"]
```

## Acceptance Criteria
- [ ] `video-production` exposes compact model notation in `SKILL.md`.
- [ ] `references/model.md` defines scene/deliverable matrix, method set,
      selection rule, execution packets, and proof.
- [ ] `todos.md` is shorter and points to model/method refs.
- [ ] Smoke examples cover all five existing method addresses.
- [ ] Method addresses remain registry-visible.
- [ ] Skill registry, todo-tier, capability, and ticket metadata checks pass.

## Verification
- `Tests:`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 bin/sync_skill_registry.py --check`
  - `python3 bin/check_skill_todo_tiers.py --allow-peer-tier3`
  - `python3 bin/check_skill_capabilities.py validate`
  - `python3 tickets/scripts/check_ticket_metadata.py`
- `Manual checks:`
  - Confirm the shortened todos still preserve publish, spend, likeness, and
    external upload boundaries.
  - Confirm smoke examples choose primary/supporting methods based on complete
    deliverable directions.
- `Evidence required:`
  - model/smoke/todo diffs
  - regenerated registry diff
  - validation logs
  - review artifact

## Proof Contract
- `Metrics:`
  - `Primary metric:` video_production_pipeline_model_validation_passed
  - `Direction:` pass/fail
  - `Verify:` skill-system checks plus smoke reference inspection
  - `Guard:` no publish/upload/spend/likeness approval side effects
  - `Min acceptable result:` model, short todos, smoke, registry pass
  - `Autoresearch warranted:` no
  - `Autoresearch session:` none
- `Review Rubrics:`
  - `spec-contract >= 4.0`
  - `integration-readiness >= 4.0`
  - `evidence-quality >= 4.0`
- `Required Evidence:`
  - validation logs
  - method-selection smoke reference
  - review artifact

## Autonomy Readiness
- `Human inputs/assets:` none
- `Credentials / external access:` none
- `Compute/runtime needs:` local validators only
- `Tooling gaps:` no deterministic parser for smoke Markdown
- `QA risks:` shortened docs may omit important safety boundaries unless
  checked manually
- `Human gates:` approval before execution
- `Agent decision boundaries:` agent may edit video-production skill docs and
  references; agent may not run paid generation, publish, upload, or approve
  likeness use

## Closeout
- Added the video production model reference, method-selection smoke cases, and
  a shorter model-first todo list while preserving publish, spend, upload, and
  likeness boundaries.
- Verification passed:
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `git diff --check`

## Evidence
- Review:
  `tickets/archive/TASK-0170/artifacts/review/2026-05-22-profile-tier3-batch-review.md`

## Evidence Checklist
- [ ] Model reference:
- [ ] Method-selection smoke:
- [ ] Registry validation:
- [ ] Review report:

## Refs
- `skills/video-production/SKILL.md`
- `skills/video-production/todos.md`
- `skills/video-generation/references/domain-production.md`
- `skills/skill-creator/references/tier3-pipeline-model.md`
- `tickets/archive/TASK-0165/ticket.md`

## Evidence
- `Artifacts:`
- `Commands:`
- `Result summary:`

## Blockers
- none
