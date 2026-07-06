---
template_id: ticket-template
template_version: "0.1.8"
feature_refs:
  - FEAT-0007
  - FEAT-0008
  - FEAT-0029
  - FEAT-0065
ticket_id: TASK-0309
title: Move product loops into product-owned surfaces and split Pulse automations by product
phase: complete
status: done
owner: codex
claimed_by:
priority: high
depends_on:
  - TASK-0304
  - TASK-0306
blocked_by: []
ready: false
approval_required: false
requires_qa: true
requires_demo: false
human_gate: none
rewards.kpi:
  - accepted_harness_improvements
created_at: 2026-07-07T01:07:48+08:00
updated_at: 2026-07-07T01:42:00+08:00
next_action: archive after operator review
last_verification: "2026-07-07T01:42:00+08:00 pass: clean-state product-loop validator proof, JSON/TOML parse, check_skills.py, ticket metadata, targeted evals, and reviewer TAS-A pass-ready"
---

# TASK-0309: Move product loops into product-owned surfaces and split Pulse automations by product

## Summary

Farplane now has product-loop contracts, stronger generated-ticket QA, and
Pulse support for product-local loop invocation, but the product loop state
still lives under `.agents/skills/farplane-*/product-loop/` and the live
automation desired state still has one global Pulse heartbeat. This ticket
moves Farplane product-specific skill/state into product-owned project
surfaces and replaces the legacy portfolio Pulse with one product-scoped Pulse
automation per product.

The decisive path is to make automations tiny selectors (`product = "..."`),
make `farplane/products.md` and `farplane/products/<id>/program.md` own product
config, keep review/escalation behavior in `pulse-update` and
`worker-artifact-review-request`, and avoid adding extra automation params for
policy that the skill or bindings already owns.

## Scope

- In:
  - Move Farplane product-local operating doctrine out of `.agents/skills/`
    into `farplane/products/<product_id>/`.
  - Create this canonical product shape:
    - `farplane/products/<product_id>/skill.md`
    - `farplane/products/<product_id>/program.md`
    - `farplane/products/<product_id>/progress.md`
  - Remove `progress.template.md`; put the progress entry shape in each
    `program.md`.
  - Update `farplane/products.md` so product IDs map to product skill,
    program, progress, lane, primary reusable skills, and worker/review policy
    source.
  - Update `pulse-update` so product-scoped automation calls can pass only
    `product = "<id>"`; Pulse resolves product skill/program/progress from
    `farplane/products.md`.
  - Update `ticket-opportunity-generator` so lane-scoped generation reads the
    product-owned `skill.md`, `program.md`, and `progress.md` surfaces.
  - Update product-loop validators and evals for the new paths and no-template
    progress shape.
  - Update docs to explain the product-owned file equivalents for the
    Karpathy loop and the distinction between product loops and Taste Loop.
  - Update `farplane/automations.toml` to remove or pause the legacy portfolio
    Pulse and add one product-scoped Pulse heartbeat per product.
- Out:
  - Do not activate live Codex automations in this ticket unless the operator
    separately asks for activation.
  - Do not add review-channel, schedule, reminder, or phone-chaser params to
    every automation prompt.
  - Do not create `farplane/skills/` as a second skill namespace.
  - Do not add a new scheduler, hidden controller, automation compiler, or
    runtime ledger.
  - Do not generalize Taste Loop into a product lane in this slice.
  - Do not change external accounts, publish, deploy, spend, phone-call, or
    destructive behavior.

## Delta

```text
Before:
  - Product-loop policy and learning live under
    `.agents/skills/farplane-*/product-loop/`.
  - Each product has `program.md`, `progress.md`, and `progress.template.md`.
  - `.agents/skills` mixes reusable/invocable skill packages with
    Farplane-project product state.
  - `farplane/automations.toml` has one active global Pulse heartbeat:
    `farplane-ticket-update`.
  - Taste Loop has richer reminder cadence params than product Pulse, while
    Pulse owns only the general Telegram-first review/chase behavior.

After:
  - Product-specific doctrine and loop state live under
    `farplane/products/<product_id>/`.
  - Each product has `skill.md`, `program.md`, and `progress.md`; progress
    shape is documented inside `program.md`.
  - Reusable Codex skills stay in `skills/`; project product loops stay in
    `farplane/products/`.
  - Product Pulse automations pass only `product = "<id>"`; Pulse resolves
    lane, product skill, program, progress, worker budget, review cap, and
    review policy from project files.
  - Legacy portfolio Pulse is removed or paused after product-scoped records
    exist.

Why now:
  - TASK-0304 and TASK-0306 proved stronger product-loop review/writeback, but
    the file layout still suggests product state is skill package doctrine.
  - Kenji wants one Pulse per product with less global coordination and fewer
    automation params.
  - The next split should make product loops obvious to agents and humans
    without duplicating config in automation prompts.

First-principles basis:
  objective: Make Farplane product loops autonomous, inspectable, and
    product-owned without bloating automation prompts.
  need: Product loops need durable local program/progress state, while reusable
    skills should remain reusable and automations should stay reviewable.
  assumptions: Product IDs in `farplane/products.md` are stable enough to be
    the automation selector; Pulse can resolve product refs from that index.
  root_cause: `.agents/skills` is an autoload/invocation-oriented surface, but
    product-loop program/progress are project state and learning memory.
  constraints: No hidden scheduler, no extra config knobs in automation prompts,
    no activation side effects, and no broad Taste Loop/product merge yet.
  first_viable_slice: Move files and references, update validator/evals/docs,
    and write product-scoped automation desired-state records.
  proof_or_falsification: validators pass; product-loop evals pass; TOML parses;
    product-scoped Pulse prompt can resolve every product from one product ID;
    reviewer TAS-A before implementation closeout.
  tradeoff: Product-local `skill.md` becomes explicit project state rather than
    autoloaded Codex skill doctrine; Pulse/generator must read it via
    `farplane/products.md`.
  non_goals: live activation, new scheduler, WhatsApp support, new reminder
    policy, public posting, and generalized Taste Loop redesign.
```

## Change Plan

```text
architecture_signatures:
  module_level:
    - farplane/products.md / product_index(product_id): product refs + lane + primary skills + loop policy refs
    - farplane/products/<id>/skill.md / product_contract(product): artifact workflows + audience + review questions
    - farplane/products/<id>/program.md / product_loop_program(product): worker budget + review cap + progress entry shape
    - farplane/products/<id>/progress.md / product_loop_progress(product): append-only learning entries
    - skills/pulse-update/SKILL.md / pulse_update(project_root, product?): reconciliation + scoped product-loop invocation
    - skills/ticket-opportunity-generator/SKILL.md / generate_tickets(..., product_loop_context): executable ticket specs from one product context
    - farplane/automations.toml / automation_record(id): cadence + target + exact prompt
  main_flow:
    - automation(product) -> pulse-update(product) -> products.md lookup -> product program/progress -> ticket-opportunity-generator(product context) -> worker ticket/handoff
    - ticket completion/rejection -> worker-artifact-review-request/reviewer/Kenji verdict -> product progress entry
  data_flow:
    - automations.toml.prompt.Params.product -> products.md.Product.ID -> farplane/products/<id>/program.md
    - farplane/products/<id>/program.md.progress_entry_shape -> farplane/products/<id>/progress.md entry
    - ticket.learning_writeback.target -> farplane/products/<id>/progress.md
  builder_freeform_boundary:
    - Builder may choose exact Markdown wording and validator helper structure,
      but must not change ownership boundaries, add automation params beyond
      `product`, or activate live automations without explicit approval.
```

### Change 1: Product-Owned File Layout

```text
fixes:
  - Product-loop state currently lives under `.agents/skills`, which confuses
    autoloaded skill doctrine with project product memory.
before:
  - `.agents/skills/farplane-*/product-loop/program.md`
  - `.agents/skills/farplane-*/product-loop/progress.md`
  - `.agents/skills/farplane-*/product-loop/progress.template.md`
after:
  - `farplane/products/<product_id>/skill.md`
  - `farplane/products/<product_id>/program.md`
  - `farplane/products/<product_id>/progress.md`
read:
  - path: `.agents/skills/farplane-*/SKILL.md`
    reason: source for current product-specific workflow contracts
  - path: `.agents/skills/farplane-*/product-loop/*`
    reason: source for current product-loop policy and learning seed
  - path: `farplane/products.md`
    reason: product ID and lane source of truth
write:
  - path: `farplane/products/<id>/skill.md`
    change: create product-local contract extracted or linked from current product skill
  - path: `farplane/products/<id>/program.md`
    change: move product-loop policy and include progress entry shape
  - path: `farplane/products/<id>/progress.md`
    change: move ignored runtime learning entries
  - path: `.agents/skills/farplane-*/product-loop/*`
    change: delete after references and validation are updated
operation:
  - Move content with history-aware care; do not rewrite unrelated product
    skill behavior.
  - Keep `progress.md` ignored if product progress is runtime-local; update
    `.gitignore` to `farplane/products/*/progress.md`.
signature_or_type_impact:
  - Product loop refs change from skill-package paths to product-owned paths.
routes:
  docs: update_docs
  qa: validator + git check-ignore
  review: reviewer
qa:
  - `find farplane/products -maxdepth 2 -type f` shows each product has
    `skill.md`, `program.md`, `progress.md`.
  - `git check-ignore -v farplane/products/*/progress.md` proves runtime
    progress is ignored if the design keeps progress untracked.
failure_modes:
  - Losing current cycle-0 learning entries.
  - Accidentally autoloading project product state as reusable Codex skills.
  - Leaving stale `.agents/skills/.../product-loop` references.
```

### Change 2: Product Index and Resolver Contract

```text
fixes:
  - Automations should pass one product ID, not repeat lane, skill, policy,
    review, or path config.
before:
  - `farplane/products.md` maps product loops to `.agents/skills/...` paths.
after:
  - `farplane/products.md` maps product IDs to product-owned `skill.md`,
    `program.md`, `progress.md`, product lane, and primary reusable skill refs.
read:
  - path: `farplane/products.md`
    reason: current product catalog and product-loop table
  - path: `farplane/bindings.yaml`
    reason: shared human gates, KPI IDs, and future channel defaults
write:
  - path: `farplane/products.md`
    change: update Product Loop State table and state owner semantics
operation:
  - Treat product ID as the stable selector.
  - Keep review/escalation defaults out of `products.md` unless they are truly
    product-specific; shared review behavior remains in Pulse/review skills and
    bindings.
signature_or_type_impact:
  - product_index(product_id) must resolve all product-loop paths without
    automation-provided duplicates.
routes:
  docs: update_docs
  qa: product-loop validator
  review: reviewer
qa:
  - Validator fails if a Products row lacks `skill.md`, `program.md`, or
    `progress.md` paths.
failure_modes:
  - Duplicating policy between `products.md`, program files, and automation
    prompts.
```

### Change 3: Pulse and Generator Path Updates

```text
fixes:
  - Pulse/generator currently reference `.agents/skills/farplane-*/product-loop`
    as the product-loop owner surface.
before:
  - `pulse-update(product_loop_programs?)` reads `.agents/skills/.../product-loop`.
  - `ticket-opportunity-generator` expects collocated product-loop files under
    product skill packages.
after:
  - `pulse-update(project_root, product?)` resolves product program/progress
    via `farplane/products.md`.
  - `ticket-opportunity-generator` reads
    `farplane/products/<id>/skill.md`, `program.md`, and `progress.md`.
read:
  - path: `skills/pulse-update/SKILL.md`
    reason: Pulse owner contract
  - path: `skills/ticket-opportunity-generator/SKILL.md`
    reason: generated ticket context contract
  - path: `skills/*/eval_task.json`
    reason: existing product-loop and scoped Pulse evals
write:
  - path: `skills/pulse-update/SKILL.md`
    change: add product-scoped automation call contract and new product path refs
  - path: `skills/ticket-opportunity-generator/SKILL.md`
    change: update lane-scoped reads, examples, learning_writeback target, and no-invented-path guards
  - path: `skills/pulse-update/eval_task.json`
    change: update path expectations and add/adjust scoped product automation case
  - path: `skills/ticket-opportunity-generator/eval_task.json`
    change: update learning_writeback target expectations
operation:
  - Keep review policy in `pulse-update` and `worker-artifact-review-request`.
  - Do not add automation prompt params for review channel, schedule, or phone
    chaser.
signature_or_type_impact:
  - `product?: string` becomes the only automation-facing scoped Pulse selector.
routes:
  docs: update_docs
  qa: eval run
  review: reviewer
qa:
  - Targeted evals pass for product-scoped Pulse and generator learning
    writeback paths.
failure_modes:
  - Accidental backwards-compatible dual path that lets old `.agents/skills`
    product-loop refs linger.
  - Automation prompt grows policy knobs that Pulse should own.
```

### Change 4: Validator and Ignore Rules

```text
fixes:
  - Product-loop validation currently checks product-loop contracts under
    `.agents/skills`.
before:
  - `check_product_loops.py` validates Product Loop State rows pointing at
    `.agents/skills/.../product-loop/program.md`.
after:
  - Validator derives product IDs from `farplane/products.md` and validates
    `farplane/products/<id>/skill.md`, `program.md`, and ignored `progress.md`.
read:
  - path: `skills/ticket-opportunity-generator/scripts/check_product_loops.py`
    reason: current validator
  - path: `.gitignore`
    reason: runtime progress ignore policy
write:
  - path: `skills/ticket-opportunity-generator/scripts/check_product_loops.py`
    change: update path validation, progress shape checks, and stale-ref detection
  - path: `.gitignore`
    change: replace `.agents/skills/farplane-*/product-loop/progress.md` with
      `farplane/products/*/progress.md` if progress remains ignored
operation:
  - Add a stale-reference check for `.agents/skills/farplane-*/product-loop`
    across active skill/docs/automation surfaces.
signature_or_type_impact:
  - Validator remains a script, no new service.
routes:
  docs: no_docs beyond docs already touched in other changes
  qa: py_compile + validator
  review: reviewer
qa:
  - `python3 -m py_compile skills/ticket-opportunity-generator/scripts/check_product_loops.py`
  - `python3 skills/ticket-opportunity-generator/scripts/check_product_loops.py --project-root .`
  - stale-ref grep returns only archive/history/proof refs or none.
failure_modes:
  - Validator passes while stale docs/skills still point at old locations.
```

### Change 5: Product-Scoped Automation Desired State

```text
fixes:
  - One active global Pulse heartbeat still carries portfolio execution.
before:
  - `farplane-ticket-update` runs one unscoped Farplane Pulse beat every 30m.
after:
  - One product-scoped Pulse heartbeat per product:
    `farplane-pulse-experiments`,
    `farplane-pulse-ablations`,
    `farplane-pulse-productization`,
    `farplane-pulse-distribution`,
    `farplane-pulse-market-learning`.
  - Legacy `farplane-ticket-update` is removed or paused; recommendation is
    remove from desired state unless live Codex app migration needs a temporary
    paused record.
read:
  - path: `farplane/automations.toml`
    reason: current desired-state automation records
  - path: `skills/automation-advisor/qa_checklist.md`
    reason: automation prompt minimality and config hygiene
write:
  - path: `farplane/automations.toml`
    change: replace global Pulse with product-scoped records that pass only
      `project_root` and `product`
operation:
  - Keep cadence/target/status in TOML.
  - Keep policy out of prompt; Pulse resolves product config.
  - Do not create or update live Codex automations in this ticket.
signature_or_type_impact:
  - automation_prompt(product_id): `$pulse-update` + `project_root` + `product`
routes:
  docs: update_docs
  qa: TOML parse + automation-advisor checklist
  review: reviewer
qa:
  - TOML parser confirms every automation record has id/name/kind/status/prompt/target/schedule.
  - Prompts do not include duplicate `product_lane`, `product_skill`,
    `review_channel`, `reminder_after_hours`, or phone-chaser params.
failure_modes:
  - Removing legacy Pulse before live app automation records are manually
    migrated. Mitigate by documenting activation as a separate step.
```

### Change 6: Docs and Taste Loop Boundary

```text
fixes:
  - Docs still describe product-loop files beside product skills and do not
    clearly distinguish Taste Loop as a cross-product feedback optimizer.
before:
  - Product-loop file equivalents point to `.agents/skills/farplane-*/product-loop`.
  - Taste Loop is adjacent but not mapped against product-loop architecture.
after:
  - Docs point to `farplane/products/<id>/skill.md`,
    `program.md`, and `progress.md`.
  - Taste Loop is documented as a cross-product feedback optimizer that can
    write or feed product progress, not as a product lane in this slice.
read:
  - path: `docs/farplane-framework/pulse-and-interval-loop.md`
    reason: canonical Pulse/Product loop narrative
  - path: `farplane/products.md`
    reason: product catalog and artifact workflow table
write:
  - path: `docs/farplane-framework/pulse-and-interval-loop.md`
    change: update owner graph, file equivalents, automation shape, and Taste
      Loop boundary
  - path: `farplane/products.md`
    change: update Product Loop State and optionally add product-owned skill
      explanation
operation:
  - Keep detailed automation prompt policy in `automation-advisor`, not docs.
signature_or_type_impact:
  - docs only
routes:
  docs: update_docs
  qa: doc refs + reviewer
  review: reviewer
qa:
  - `python3 skills/skill-maintenance/scripts/check_skills.py`
  - grep confirms active docs no longer instruct new product loops under
    `.agents/skills/.../product-loop`.
failure_modes:
  - Over-claiming Taste Loop unification before a repeated writeback path is
    implemented.
```

## Done

```text
done_when:
  - Product-owned loop files exist under `farplane/products/<id>/` for all
    five current products.
  - `.agents/skills/farplane-*/product-loop/` no longer exists in active
    source state.
  - `progress.template.md` is removed; progress entry shape lives in each
    product `program.md`.
  - `farplane/products.md` resolves product ID to product skill, program,
    progress, lane, and primary reusable skill refs.
  - `pulse-update` accepts/product-documents a product-scoped automation call
    using only `product = "<id>"`.
  - `ticket-opportunity-generator` reads product-owned skill/program/progress
    and writes learning back to `farplane/products/<id>/progress.md`.
  - Product-loop validator passes and fails stale `.agents/skills/.../product-loop`
    refs in active owner surfaces.
  - `farplane/automations.toml` has product-scoped Pulse records and no active
    legacy portfolio Pulse record.
  - Review/escalation policy remains owned by Pulse, worker-artifact review,
    phone-chaser, and bindings; automation prompts do not repeat that policy.
  - Docs explain product-owned loop files, automation selector shape, and Taste
    Loop as a cross-product feedback optimizer.
  - Targeted evals pass before closeout.
  - Reviewer lane pass-ready receipt recorded before closeout.
```

## Proof

```text
proof_status: pass
checks:
  - pass: python3 -m py_compile skills/ticket-opportunity-generator/scripts/check_product_loops.py
  - pass: python3 skills/ticket-opportunity-generator/scripts/check_product_loops.py --project-root .
  - pass: python3 -m json.tool skills/ticket-opportunity-generator/eval_task.json
  - pass: python3 -m json.tool skills/pulse-update/eval_task.json
  - pass: python3 - <<'PY' ... tomllib.load(open("farplane/automations.toml", "rb")) ... PY
  - pass: git check-ignore -v farplane/products/{experiments,ablations,productization,distribution,market_learning}/progress.md
  - pass: rg ".agents/skills/farplane-.*/product-loop|product-loop/program.md|product-loop/progress.md|progress.template.md" farplane docs skills .gitignore --glob '!tickets/**' --glob '!skills/ticket-opportunity-generator/scripts/check_product_loops.py' returned no matches
  - pass: python3 skills/skill-maintenance/scripts/check_skills.py
  - pass: python3 tickets/scripts/check_ticket_metadata.py tickets/TASK-0309/ticket.md
evals:
  - pass A: ticket_opportunity_generator_requires_product_loop_writeback_01
    run: .farplane/evals/runs/20260706-173141-task-0309-product-owned-loops
  - pass A: pulse_invokes_product_loops_instead_of_portfolio_planning_01
    run: .farplane/evals/runs/20260706-173350-task-0309-product-owned-loops-rerun
  - pass A: pulse_product_scoped_automation_params_are_minimal_01
    run: .farplane/evals/runs/20260706-173527-task-0309-product-scoped-param-rerun
review:
  - revise TAS-B: reviewer agent 019f3880-fb01-7b33-865a-6e0b69dff195 found ignored runtime progress files were required by validation, making clean checkout proof incomplete
  - pass-ready TAS-A: reviewer agent 019f3884-26de-7c92-b4a5-0dd0fa3cf2ba confirmed the validator no longer depends on untracked progress files, reran clean-state proof, and found no blocking issues
residual_risk:
  - Desired-state automations were edited in farplane/automations.toml only; live Codex app automation activation/deletion was intentionally out of scope.
  - Worktree has unrelated dirty files in ingest/media/remotion/social/config surfaces; this ticket did not reconcile them.
```

## QA Strategy

```text
qa_strategy:
  proof_weight: tests + eval + review
  checks:
    - python3 -m py_compile skills/ticket-opportunity-generator/scripts/check_product_loops.py
    - python3 skills/ticket-opportunity-generator/scripts/check_product_loops.py --project-root .
    - python3 -m json.tool skills/ticket-opportunity-generator/eval_task.json
    - python3 -m json.tool skills/pulse-update/eval_task.json
    - python3 skills/eval/scripts/run_evals.py run --harness codex --judge-harness codex --target-root . --skill ticket-opportunity-generator --skill pulse-update --task-id <updated product-loop task ids> --label task-0309-product-owned-loops
    - python3 skills/skill-maintenance/scripts/check_skills.py
    - python3 tickets/scripts/check_ticket_metadata.py tickets/TASK-0309/ticket.md
    - python3 - <<'PY'
      import tomllib
      tomllib.load(open("farplane/automations.toml", "rb"))
      PY
    - rg ".agents/skills/farplane-.*/product-loop" farplane docs skills .agents || true
  manual:
    - Inspect one product, preferably `distribution`, and confirm
      `skill.md`, `program.md`, and `progress.md` tell a coherent loop story.
    - Inspect `farplane/automations.toml` and confirm product Pulse prompts
      pass only `project_root` and `product`.
    - Confirm review reminder/phone-chaser behavior is not duplicated in
      automation params.
  delegated_lanes:
    - reviewer
  review:
    - rubric: architecture
      required_tas: TAS-A
    - rubric: implementation-plan
      required_tas: TAS-A
    - rubric: integration-readiness
      required_tas: TAS-A
    - rubric: evidence-quality
      required_tas: TAS-A
    - rubric: documentation-quality
      required_tas: TAS-A
    - rubric: eval-quality
      required_tas: TAS-A
  evidence:
    - final file map of moved product surfaces
    - validator output
    - automation TOML parse output
    - targeted eval run summary
    - reviewer receipt
  goal_advisor_inputs:
    proof_route: local file move + validator + TOML parse + skill registry checks + targeted evals + reviewer lane
    final_evidence: changed file list, command outputs, eval summary, reviewer receipt, and ticket closeout notes
    final_checkpoint: before stop_complete, verify no active stale product-loop refs remain and reviewer TAS-A pass is recorded
  residual_risk:
    - Live Codex automation records still need a separate activation/sync step
      after this desired-state change.
    - Moving product-local skill docs out of `.agents/skills` may require
      one live Pulse smoke to prove agent discovery remains good.
    - Taste Loop writeback into product progress remains conceptual unless a
      later ticket explicitly wires it.
```

## Docs Strategy

```text
docs_strategy:
  outcome: update_docs
  doc_targets:
    - farplane/products.md
    - docs/farplane-framework/pulse-and-interval-loop.md
    - skills/pulse-update/SKILL.md
    - skills/ticket-opportunity-generator/SKILL.md
    - farplane/automations.toml
  no_docs_reason:
  validation:
    - python3 skills/skill-maintenance/scripts/check_skills.py
    - active docs grep for stale `.agents/skills/farplane-*/product-loop`
```

## Links

- `program:` create with `goal-advisor` after approval
- `progress:` create with `goal-advisor` after approval
- `visual companion:` `tickets/TASK-0309/diagrams.md`
- `artifacts:` `tickets/TASK-0309/artifacts/`
- `review:` pending reviewer lane after approval or before implementation closeout
- `refs:`
  - `farplane/products.md`
  - `farplane/automations.toml`
  - `skills/pulse-update/SKILL.md`
  - `skills/ticket-opportunity-generator/SKILL.md`
  - `skills/worker-artifact-review-request/SKILL.md`
  - `skills/phone-chaser/SKILL.md`
  - `docs/farplane-framework/pulse-and-interval-loop.md`
  - `skills/automation-advisor/qa_checklist.md`

## Notes

- `Blast radius:` material harness architecture and project-state move across
  products, Pulse, generator, automations, docs, validators, and evals.
- `Risks / rollback:` if product-owned skill files hurt discoverability, keep
  `farplane/products/<id>/skill.md` as source of truth and add short pointers
  from reusable skills rather than restoring product progress under
  `.agents/skills`.
- `Follow-ups:`
  - Activate or update live Codex app automations from the desired-state TOML.
  - Decide whether Taste Loop should write feedback outcomes into product
    progress after one product-scoped Pulse cycle proves the shape.
  - Consider an `init-advisor` product substrate template after this migration
    settles.
- `Grounding evidence:` local-only Farplane harness refactor based on current
  project files, tickets TASK-0304/TASK-0306, `automation-advisor`,
  `pulse-update`, and `ticket-opportunity-generator`.
- `Plan QA:`
  - `minimal_required_version:` pass - only moves current product-loop state,
    updates resolver contracts, and splits desired-state Pulse automations.
  - `reuse_before_new_surface:` pass - reuses `farplane/products.md`,
    `pulse-update`, `ticket-opportunity-generator`, and
    `farplane/automations.toml`.
  - `least_parameters:` pass - automation prompts add only `product`.
  - `new_files_functions_justified:` pass - `farplane/products/<id>/skill.md`
    is justified as product-owned doctrine separate from reusable skills.
  - `minimal_impl_plan_claim:` pass - no live activation, no new scheduler,
    no Taste Loop redesign.
  - `existing_service_fit:` pass - no new service; validator remains existing
    owner script.
  - `goal_advisor_ready:` pass after approval.
  - `clarifying_questions:` pass - assumptions recorded; no blocking unknowns.
  - `architecture_signatures:` pass.
  - `change_plan_signature_linkage:` pass.
  - `change_plan_locality:` pass.
  - `qa_strategy_explicit:` pass.
  - `docs_strategy:` pass.
  - `independent_plan_review:` pending.
  - `visual_companion_boundary:` pass.
  - `grounding_evidence:` local_only.
  - `highest_risk:` stale refs or automation prompt over-parameterization.
  - `fix_or_deferral:` reviewer lane and Goal Packet happen after operator
    approval.

## Run Hints

```text
Likely size: material
Goal recommendation: yes after operator approves this ticket
Budget hint: one focused implementation pass plus eval and reviewer rerun
Compute hint: local_shared
Planning hint: impl-plan complete; next owner is goal-advisor after approval
External side effects: none; do not activate live automations in this ticket
```
