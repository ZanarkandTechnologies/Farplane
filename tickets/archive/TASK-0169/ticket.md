---
ticket_id: TASK-0169
title: apply tier 3 pipeline model to product-photography
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

# TASK-0169: apply tier 3 pipeline model to product-photography

## Summary
Refactor `product-photography` into the compact Tier 3 pipeline pattern and add
registry-visible method addresses for common product image jobs. Unlike
`social-content` and `video-production`, this skill currently has no `methods`
frontmatter, so this ticket should introduce a method set as part of the model
rollout.

The base skill should own the shot-set router, product facts, asset/source
constraints, generation route, and proof. Upstream references should stay as
supporting constraints and examples rather than becoming independent subskills.

## Scope
- In:
  - add compact `ProductPhotography := ProductFacts + Channel + ShotMatrix + MethodSet + AssetRoute + ProofPlan`
    model to `skills/product-photography/SKILL.md`
  - add registry-visible method addresses for product-photo jobs, such as
    `product-photography:hero`, `product-photography:packshot`,
    `product-photography:lifestyle`, `product-photography:detail`,
    `product-photography:marketplace`, and
    `product-photography:cutout-upscale`
  - add `skills/product-photography/references/model.md` with shot matrix,
    method selection, execution packet, and proof rules
  - shorten `skills/product-photography/todos.md` to point to model/method
    refs and preserve spend/upload/listing boundaries
  - add a method-selection smoke reference for product shot routing
  - update generated registry and durable docs as required by `close-ticket`
- Out:
  - generating product photos in this ticket
  - changing `imagegen`, `image-generation`, or background-removal tooling
  - uploading to Amazon, Shopify, marketplaces, ads platforms, or storefronts
  - turning upstream refs into subskills

## Plan
- `Change:` convert `product-photography` into a model-first Tier 3 router and
  add method addresses for product image shot families.
- `Why:` product photography decomposes a brief into product facts, channel
  constraints, shot sets, asset routes, and commercial proof. Method addresses
  make these routes visible in the registry and easier to select.
- `Before -> After:`
  - Before: the skill lists a short product-photo recipe and shot-set words but
    has no registry-visible method set.
  - After: the skill exposes product-photo method addresses, a compact model,
    a shot matrix, an execution packet shape, and short todos.
- `Touch:`
  - `skills/product-photography/SKILL.md`
  - `skills/product-photography/todos.md`
  - `skills/product-photography/references/model.md`
  - `skills/product-photography/references/method-selection-smoke.md`
  - `docs/skills/registry.jsonl`
  - `docs/HISTORY.md`
- `Inspect:`
  - `skills/product-photography/SKILL.md`
  - `skills/product-photography/todos.md`
  - `skills/product-photography/references/upstream-product-photography.md`
  - `skills/product-photography/references/upstream-ai-product-photography.md`
  - `skills/image-generation/references/domain-production.md`
  - `skills/frontend-craft/references/asset-generation.md`
  - `skills/skill-creator/references/tier3-pipeline-model.md`
- `Signature delta:`
  - `skills/product-photography/SKILL.md / methods: product-photography:*`
  - `skills/product-photography/references/model.md / ProductPhotography(brief): ShotMatrix`
  - `skills/product-photography/references/model.md / MethodSelection(shot, methods, constraints): ExecutionPacket`
  - `skills/product-photography/todos.md / checklist(model, method, route, proof): done`
- `Type Sketch:`
  - `ProductPhotography`: `product_facts`, `source_assets`, `channel`,
    `shot_matrix`, `method_set`, `asset_route`, `handoff_packets`,
    `proof_plan`
  - `Shot`: `id`, `job`, `channel`, `aspect_ratio`, `background`,
    `source_asset`, `candidate_methods`, `chosen_method`, `generation_route`,
    `output`, `proof`
  - `ProductPhotoMethod`: `id`, `use_when`, `avoid_when`, `inputs`,
    `outputs`, `commerce_constraints`, `risk`, `proof`
  - `ExecutionPacket`: `shot_id`, `method_id`, `required_inputs`,
    `prompt_or_edit_steps`, `generation_route`, `postprocess_route`,
    `handoff`, `qa`
- `Typed flow example:`
  - User asks for Amazon listing images from one product photo.
  - The skill builds shot rows for packshot, scale, detail, lifestyle, and
    cutout/upscale.
  - Method selection picks `product-photography:marketplace` as the primary
    method, with `product-photography:packshot` and
    `product-photography:cutout-upscale` supporting specific rows.
  - Packets route bitmap creation/editing through `imagegen` or
    `image-generation`, product-page integration through `frontend-craft` when
    needed, and proof through `execute`.
- `Execution steps:`
  1. Add method addresses to `SKILL.md` frontmatter and first-load method notes.
  2. Add compact model prelude to `SKILL.md`.
  3. Add `references/model.md` with shot matrix, method set, selection rule,
     execution packet, proof plan, and upload/listing boundaries.
  4. Add `references/method-selection-smoke.md` for hero, packshot,
     lifestyle, detail, marketplace, and cutout/upscale cases.
  5. Shorten `todos.md` to ground, model, select method, route generation,
     prove, and preserve spend/upload/listing boundaries.
  6. Regenerate and validate skill registry.
  7. Run review and update evidence.
- `Recommendation:` add method addresses in product-photography because this
  skill currently lacks registry-visible routes but clearly owns multiple
  reusable shot-family workflows.
- `Options considered:`
  1. Keep one generic product-photography route: rejected because shot families
     have different inputs, proof, and risk.
  2. Add method addresses under one base skill: chosen because the workflows
     share product facts, channel constraints, generation routes, and proof.
  3. Create subskills per shot family: rejected because that would fragment a
     single product-photo planning surface.
- `Blast radius:`
  - product-photo planning and generation routes
  - image-generation handoffs
  - frontend/product-page handoffs
  - generated registry method visibility
- `Risks:`
  - choosing too many method addresses and making the skill look heavier than
    it is
  - weakening commercial/listing boundaries by shortening todos
  - implying product images were generated or marketplace-compliant without
    actual visual proof

## Gap Analysis
- `Current state:` `product-photography` is a useful Tier 3 domain skill but
  lacks method addresses, model reference, execution packet shape, and smoke
  method-selection examples.
- `Production expectation:` product-photo workflows should state product
  facts, source assets, commerce channel, shot set, generation/postprocess
  route, output dimensions, and proof before claiming commercial quality.
- `Missing gaps:` method frontmatter, shot matrix, model reference, smoke
  examples, and shorter todos.
- `Comparable implementations:` `social-content`, `video-production`, and the
  `TASK-0165` landing/frontend pilot.
- `Recommendation:` add a concise method set and model now; do not generate
  assets in this ticket.

## Diagram
```mermaid
flowchart LR
  A["Product brief + source assets"] --> B["Shot matrix"]
  B --> C["Product-photo method selection"]
  C --> D["Execution packets"]
  D --> E["imagegen / image-generation / frontend routes"]
  E --> F["commercial proof + upload boundary"]
```

## Acceptance Criteria
- [ ] `product-photography` exposes registry-visible method addresses.
- [ ] `SKILL.md` includes compact model notation and method notes.
- [ ] `references/model.md` defines shot matrix, method set, selection rule,
      execution packet, and proof plan.
- [ ] `todos.md` is shorter and points to model/method refs.
- [ ] Smoke examples cover every new method address.
- [ ] Skill registry, todo-tier, capability, and ticket metadata checks pass.

## Verification
- `Tests:`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 bin/sync_skill_registry.py --check`
  - `python3 bin/check_skill_todo_tiers.py --allow-peer-tier3`
  - `python3 bin/check_skill_capabilities.py validate`
  - `python3 tickets/scripts/check_ticket_metadata.py`
- `Manual checks:`
  - Confirm method set is small enough to be useful and not a taxonomy dump.
  - Confirm shortened todos preserve spend, upload, listing, and marketplace
    proof boundaries.
- `Evidence required:`
  - model/smoke/todo diffs
  - regenerated registry diff showing methods
  - validation logs
  - review artifact

## Proof Contract
- `Metrics:`
  - `Primary metric:` product_photography_pipeline_model_validation_passed
  - `Direction:` pass/fail
  - `Verify:` skill-system checks plus smoke reference inspection
  - `Guard:` no generation/upload/spend/listing side effects
  - `Min acceptable result:` method frontmatter, model, short todos, smoke,
    registry pass
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
- `QA risks:` docs-only change may imply generated-image quality without
  visual proof; keep this ticket structural
- `Human gates:` approval before execution
- `Agent decision boundaries:` agent may edit product-photography skill docs

## Closeout
- Added product-photography method addresses, the product photo model
  reference, method-selection smoke cases, and a shorter model-first todo list.
- Verification passed:
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `git diff --check`

## Evidence
- Review:
  `tickets/archive/TASK-0170/artifacts/review/2026-05-22-profile-tier3-batch-review.md`
  and references; agent may not generate assets, upload listings, or spend

## Evidence Checklist
- [ ] Model reference:
- [ ] Method-selection smoke:
- [ ] Registry validation:
- [ ] Review report:

## Refs
- `skills/product-photography/SKILL.md`
- `skills/product-photography/todos.md`
- `skills/image-generation/references/domain-production.md`
- `skills/skill-creator/references/tier3-pipeline-model.md`
- `tickets/archive/TASK-0165/ticket.md`

## Evidence
- `Artifacts:`
- `Commands:`
- `Result summary:`

## Blockers
- none
