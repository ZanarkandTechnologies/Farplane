---
title: Farplane Framework Changelog
owner: init-advisor
status: active
kind: framework-changelog
updated_at: 2026-07-22
---

# Farplane Framework Changelog

## 2.0.9

Date: 2026-07-22

Primary change: add one ignored local named-view config over canonical entity
IDs and expose those views through generated projections and World UI.

Changed surfaces:

- `.farplane/views.yaml` owns multiple named views as `name + entity_ids`;
- duplicate YAML/view keys, malformed membership, duplicates, and unresolved
  entity IDs fail `farplane entities compile`;
- `index.json`, `world.json`, and `crm.json` carry identical normalized views
  and one shared fingerprint;
- Farplane World reads the entity-owned projection path and intersects the
  selected named view with query, kind, and location filters;
- Feed Scout groups remain source-owner buckets and do not own view membership.

Migration steps:

1. Add `.farplane/views.yaml` with `views: {}` or one or more named views.
2. Add `.farplane/views.yaml` to ignored standard paths while keeping shared
   source/connector configuration in `farplane/bindings.yaml`.
3. Run `farplane entities compile --project-root <project>` and update World
   consumers to `.farplane/entities/world.json` plus `index.json`.
4. Do not add `.farplane/config.yaml`, duplicate entity records, or a second
   Feed Scout membership list.

## 2.0.8

Date: 2026-07-21

Primary change: make flat entity memory the single source of truth and derive
World and CRM as views.

Changed surfaces:

- canonical entities move to `.farplane/entities/<id>.md` with no kind/type
  subdirectories;
- `kind` remains the classification field and optional non-empty `funnel`
  frontmatter promotes the same entity into the CRM view;
- `farplane entities compile` generates adjacent `index.json`, `world.json`,
  and `crm.json` projections;
- paragraph-backed links use `entity:<id>` while question footnotes, source
  references, claims, and optional session provenance remain intact;
- schema version 3 removes storage paths and entity-link URI spelling from
  semantic claim and edge key material.

Migration steps:

1. Flatten `.farplane/crm/entities/**/*.md` into `.farplane/entities/*.md` and
   fail on filename collisions.
2. Replace body links from `crm:<id>` to `entity:<id>` without changing other
   entity content.
3. Remove old generated CRM projections and run
   `farplane entities compile --project-root <project>`.
4. Update consumers to `.farplane/entities/index.json`, `world.json`, and
   `crm.json`; do not keep a dual-read compatibility path.

## 2.0.7

Date: 2026-07-20

Primary change: add question-level provenance to Markdown-owned CRM knowledge
without retaining turn-level conversation history.

Changed surfaces:

- entity claim blocks may cite stable `q-*` footnotes whose definitions retain
  exact question text and optional local session provenance;
- CRM schema version 2 compiles question-backed claims plus question refs on
  nodes and associations, while keeping questions out of the default node set;
- unresolved, empty, or conflicting question definitions fail compilation;
- semantic claim and edge keys ignore question/session markers;
- bootstrap stops seeding generated schema-v1 CRM JSON; the canonical compiler
  creates both projections after first use.

Migration steps:

1. Bump `farplane/manifest.json` `spec_version` and
   `template_uses.farplane-framework` to `2.0.7`.
2. Remove any bootstrap-seeded `.farplane/crm/entities.json`; generated
   `entities.json` and `world.json` remain disposable compiler output.
3. Add `[^q-*]` citations only to durable factual claim blocks and define exact
   matching questions under each entity's `## Question index`.
4. Keep `session=<id>` optional and local; do not migrate or store turn IDs.
5. Run `farplane crm compile --project-root <project>` and update consumers for
   schema-version-2 `questions`, `claims`, and `question_refs` fields.

## 2.0.5

Date: 2026-07-17

Primary change: make stable problems and current product bets explicit in the
typed project charter without duplicating metric definitions.

Changed surfaces:

- `identity.problems` names each durable problem and references canonical
  metrics from `metrics.yaml`;
- `identity.product_bets` names current audience-facing solution hypotheses
  and links each bet to one or more problem IDs;
- metric definitions, direction, refresh, observations, baselines, and ticket
  targets remain outside the problem and bet records.

Migration steps:

1. Add a small `identity.problems` list with stable IDs, one-sentence problem
   statements, and canonical `metric_refs`.
2. Add `identity.product_bets` with audience-facing promises and
   `problem_refs`.
3. Keep missing direct measurements explicit instead of inventing metric
   observations.

## 2.0.4

Date: 2026-07-14

Primary change: make each `harness.yaml` planning area own its canonical
candidate-generation instruction and require next-wave planning to consume it.

Changed surfaces:

- every `areas.<area_id>` keeps one non-empty `planner_instruction` beside its
  description, capability refs, and metric refs;
- Plan Next Wave receives complete area records, applies every scope-relevant
  instruction, and returns instruction-use receipts before ranking;
- admitted specs trace `ranking.area_instruction_ref` to the selected area and
  explain `ranking.area_instruction_applied`;
- Pulse and scheduled allocators pass canonical area records instead of
  reconstructing area policy;
- self-improvement planning covers create, refine, shorten, refactor,
  consolidate, retire, repair, and rollout decisions with invocation, Reward,
  health, duplication, and maintenance evidence.

Migration steps:

1. Ensure every project area has a non-empty singular `planner_instruction`.
2. Pass complete `harness.areas` records to Plan Next Wave.
3. Add exact area-instruction refs and application explanations to admitted
   planner specs.
4. Remove caller-local area-policy paraphrases and reject typo aliases such as
   `planner_instrcuitions`.

## 2.0.3

- CRM relationship entities are now authored as Markdown under
  `.farplane/crm/entities/**/*.md`.
- `farplane crm compile` validates IDs and references, then generates
  `.farplane/crm/entities.json` for machine consumers.
- Bootstrap and the framework manifest now include the Markdown-owned CRM
  standard.

This file tracks changes to `farplane-framework` project manifests generated by
`init-advisor`. Use it as the quick migration reference before changing
`skills/init-advisor/references/MANIFEST_TEMPLATE.json`, bootstrap scaffolding,
or project-level documentation guidance.

```text
framework_bump(old_version, new_version, project_root)
  -> manifest_delta + migration_steps + proof_commands
```

## 2.0.2

Date: 2026-07-12

Primary change: turn accepted ticket-completion learning into immediate local
ticket supply instead of waiting for the weekly Dogfood review.

Changed surfaces:

- `core:ticket-completion-learning@1.1.0` still produces a privacy-validated,
  read-only semantic report;
- after report acceptance, deterministic Core projects at most the strongest
  high/medium-confidence finding into one deduped ticket, using a source or
  self-improvement KPI for `todo` and falling back to `awaiting_review` when no
  declared KPI exists;
- report schema 2 requires a locally validated semantic dedupe key, Core ranks
  confidence/direct-fix strength independently of model order, and generated
  learning-ticket completions are report-only to prevent recursive supply;
- known corrections receive a direct-fix program and uncertain improvements
  receive a prove-or-reject program;
- no-signal, source-gap, low-confidence, replay, and duplicate paths create no
  additional ticket;
- Dogfood consumes the report plus created/existing/no-ticket receipt and never
  recreates the projected ticket.

Migration steps:

1. Update the completion-learning route to
   `core:ticket-completion-learning@1.1.0`.
2. Keep the semantic executor read-only; ticket writes belong only to the Core
   projector after validation.
3. Count projected tickets in Pulse/Dogfood through the normal ticket board.
4. Prove one accepted finding creates one ticket and delivery, replay,
   paraphrase, unrelated-KPI, and generated-ticket recursion cannot admit
   another.

## 2.0.1

Date: 2026-07-12

Primary change: replace every-N-turn learning review with one bounded,
event-driven ticket-completion learning program.

Changed surfaces:

- `farplane.ticket.completed` fans out to lean coverage and structured learning
  programs through the existing local Core drain;
- learning freezes only the completed ticket packet and bounded operator-turn
  window named by event provenance; assistant replies are excluded because the
  ticket packet owns completion truth;
- Core ignores user config/rules for the read-only executor and validates the
  report schema, evidence refs, sensitive patterns, and raw-source overlap;
- missing thread/window or local Codex execution becomes a replayable source
  gap rather than a broad thread scan;
- completion learning emits compact evidence reports and never edits docs,
  skills, tickets, or external systems;
- Weekly Dogfood consumes accepted findings as recovery or experiment evidence.

Migration steps:

1. Add `ticket-completion-learning-v1` beside the lean completion route in
   `farplane/bindings.yaml`.
2. Remove any N-turn/Stop-hook learning reviewer and obsolete
   `.farplane/state/learning-reviews` consumer.
3. Preserve bounded operator-turn capture in
   `.farplane/state/message-windows/`; remove obsolete assistant-response and
   turn-cadence state.
4. Reinstall, validate routes, and prove one completion produces two immutable
   runs while a missing window produces a visible source gap.

Proof commands:

```bash
farplane install
farplane mining routes validate --project-root . --json
python3 bin/tests/test_farplane_mining.py
python3 bin/tests/test_runtime_state.py
```

## 2.0.0

Date: 2026-07-12

Primary change: replace descriptive `products` with planning `areas` and make
one adaptive Work Pulse planner the only proactive ticket-admission point.

Changed surfaces:

- `farplane/harness.yaml#areas` names recurring investment areas, planner
  instructions, capability skills, and local metric refs;
- `plan_next_wave` reads a recent global ticket-history sample first, then may
  progressively filter by AI origin, area, KPI, Reward, or wider time range;
- human-active tickets remain unselectable but consume no Pulse worker capacity
  and do not block empty-board refill;
- Feed Scout, Daily/Weekly Interval, and Dogfood write reports and bounded
  candidates; they may create capped direct recovery tickets for evidenced
  known failures but cannot admit uncertain fixes, new direction, or experiments;
- self-improvement competes as an evidence-gated area rather than operating as
  a second ticket-admission controller;
- project objectives, area diagnostics, and guards are separate snapshot roles.

Migration steps:

1. Replace `harness.yaml#products` with `areas`; give every area a description,
   planner instruction, capability refs, and metric refs.
2. Choose a small project-level objective set and hard guards. Keep local area
   diagnostics out of the global objective priority list.
3. Set Feed Scout, Interval, and Dogfood automation write policy to bounded
   direct recovery only; route opportunities, uncertain fixes, and experiments
   through the global planner.
4. Install the latest skills/hooks, regenerate primitive and project snapshots,
   and verify a human-active ticket does not block Pulse refill.
5. Observe planner admissions and use terminal Reward evidence plus rejected
   AI-ticket counts to refine area instructions.

Proof commands:

```bash
farplane install
farplane doctor --json
farplane project snapshot --project-root . --json
python3 bin/validators/check_farplane_project_files.py --root .
python3 -m unittest skills.pulse-update.scripts.test_list_pulse_board
```

## 1.9.1

Date: 2026-07-12

Primary change: make the V1 contract safe to propagate into existing Farplane
projects without adding another orchestration layer. This is a patch release
over `1.9.0`; the project-file schema is unchanged.

Changed surfaces:

- downstream migrations must remove retired project files and active readers,
  not merely add `harness.yaml` beside them;
- every project uses exactly one Work Pulse heartbeat, while Feed Scout,
  Daily/Weekly BAU review, Dogfood, and consolidation remain separate cron
  sources when relevant;
- automation activation is gated on a project-specific typed charter,
  selected measurable objectives, honest metric providers, and stable
  capability-skill ownership;
- installed source skills and hooks must match the repo-owned release before a
  live Pulse is judged.

Migration steps:

1. Apply the `1.9.0` typed charter, metric, Reward, and Core mining migration.
2. Delete retired charter, goals, product-controller, bindings Markdown, and
   compatibility-reader surfaces after their content is migrated.
3. Replace legacy strategy/planning heartbeats with one Pulse plus only the
   project-relevant report, source, and Dogfood cron records.
4. Define the project's descriptive products, capability refs, selected
   objective priorities, metric providers, and side-effect gates before live
   activation.
5. Reinstall from the canonical Farplane repo, validate the clean project, and
   observe one post-install Pulse before calling the migration complete.

Proof commands:

```bash
farplane install
farplane doctor --json
farplane project snapshot --project-root . --json
python3 bin/validators/check_farplane_project_files.py --root .
```

## 1.9.0

Date: 2026-07-12

Primary change: replace the Markdown charter and duplicated optimization block
with one typed project contract. `farplane/harness.yaml` owns identity,
descriptive products, capability references, selected objectives/guards, and
protected policy. `farplane/metrics.yaml` owns reusable metric meaning,
direction, freshness, and guard rules.

Changed surfaces:

- `farplane/harness.md` and `metrics.yaml#optimization` are retired with no
  compatibility readers.
- project and product metric refs select active objectives with globally unique
  priorities; hard guards are selected at project scope.
- the project snapshot exposes `metrics.selection` and typed charter/product
  fields.
- Reward rows use stable IDs and terminal `accept|kill` decisions; `monitor`
  remains live for its next check-in.
- Core owns portable file events, routes, mining runs, and lean reports; UI is
  an editor/renderer adapter.

Migration steps:

1. Convert charter headings into `harness.yaml.identity`, constraints,
   authority, products, feature definition, and capability refs.
2. Move objective IDs/priorities and guard IDs to `harness.yaml`; move
   direction, `max_age_days`, and guard operator/threshold into each metric
   definition.
3. Migrate every Reward row to the stable V1 schema and remove legacy score
   fields after terminal outcomes have explicit evidence.
4. Configure file-event routes through Core-owned `hooks.json` and
   `bindings.yaml`, regenerate the project snapshot, and update UI consumers.

Proof commands:

```bash
farplane project snapshot --project-root . --json
farplane mining routes validate --project-root . --json
python3 bin/validators/check_farplane_project_files.py --root .
python3 -m unittest bin.tests.test_farplane_project_snapshot bin.tests.test_farplane_project_file_validator
```

## 1.8.0

Date: 2026-07-12

Primary change: remove the intermediary project-goal portfolio. Human meaning
and hard constraints stay in `farplane/harness.md`; measurable objectives,
directions, guards, and metric definitions live in
`farplane/metrics.yaml`; selected commitments live only in tickets.

Changed surfaces:

- `farplane/goals.yaml`, SMART goals, current bets, and current milestones are
  removed from active projects and bootstrap templates.
- `plan-next-wave` compares proposal trajectories by expected
  metric delta, confidence, duration, signal delay, cost, risk, reversibility,
  information gain, compounding value, interference, and prerequisites.
- the generated project snapshot exposes `tabs.objectives`, charter fields,
  and metric optimization state; it no longer exposes `tabs.goals`.

Migration steps:

1. Move mission, thesis, non-tradeoffs, authority, and stable capability refs
   from `goals.yaml` into `harness.md` when they are not already present.
2. Move only measurable objective metric IDs, directions, priorities, and hard
   guard thresholds into `metrics.yaml#optimization`; keep unmeasured values as
   charter principles instead of fake metrics.
3. Convert any still-active selected bet into an ordinary ticket with
   `program.md`/`progress.md` when it needs long-running state, then delete
   `farplane/goals.yaml`.
4. Bump the manifest to `1.8.0`, regenerate primitive/project snapshots, and
   update UI consumers from Goals to Objectives.

Proof commands:

```bash
farplane metrics primitives --project-root . --date <YYYY-MM-DD> --json
farplane project snapshot --project-root . --date <YYYY-MM-DD> --json
python3 bin/validators/check_farplane_project_files.py --root .
python3 -m unittest bin.tests.test_farplane_project_snapshot bin.tests.test_farplane_project_file_validator
```

## 1.7.0

Date: 2026-07-11

Primary change: adopt the Farplane V1 one-board project contract. Product files and
product-scoped controllers are retired; reusable artifact workflows remain
project-local capability skills. `farplane/metrics.yaml` owns metric meaning,
while `farplane/bindings.yaml.metric_bindings` owns refresh mechanics with
exact metric-ID parity. QA and review evidence is ticket-local, and clean
projects no longer create a generic run ledger or review directory.

Changed surfaces:

- `MANIFEST_TEMPLATE.json` requires `farplane/metrics.yaml`, keeps
  `farplane/hooks.json` optional, and removes product and generic review paths.
- `bootstrap.sh` creates one Work Pulse automation contract plus separate cron
  sources and no product tree, product registry, run ledger, or review bucket.
- Core snapshots and validators load definitions from `metrics.yaml` and
  refresh recipes from `bindings.metric_bindings`; no legacy fallback remains.
- Ticket QA and completion review write to
  `tickets/TASK-XXXX/artifacts/{qa,review}/`.

Migration steps:

1. Remove active readers of `farplane/products/` and `farplane/products.json`,
   then delete those files; keep useful workflows as capability skills.
2. Create `farplane/metrics.yaml`, move semantic metric fields there, and keep
   only `refresh` under matching `bindings.metric_bindings` IDs.
3. Remove `.farplane/reviews/` and `.farplane/state/run-ledger.json`; move any
   durable QA/review receipts to their owning tickets.
4. Bump `farplane/manifest.json` to `1.7.0`, regenerate the project snapshot
   and graph/registry projections, and validate a clean bootstrap fixture.

Proof commands:

```bash
python3 bin/validators/check_farplane_project_files.py --root .
python3 -m unittest bin.tests.test_farplane_project_snapshot bin.tests.test_farplane_primitive_metrics
python3 skills/pulse-update/scripts/test_list_pulse_board.py
python3 docs/features/validate_features.py
python3 skills/skill-maintenance/scripts/check_skills.py
python3 bin/validators/check_doc_refs.py
```

## 1.6.17

Date: 2026-07-09

Primary change: make product-local `product.md` files and generated
`farplane/products.json` the active product-loop substrate. The retired
top-level `farplane/products.md` and `farplane/ops-memory.md` surfaces are no
longer required by new project manifests. Customer/person research uses ignored
`.farplane/crm/reports/` Markdown reports with a derived index instead of a
tracked CRM pipeline file.

Changed surfaces:

- `MANIFEST_TEMPLATE.json` bumps `farplane-framework` to `1.6.17`.
- Project manifests track `farplane/products/` and generated
  `farplane/products.json`.
- `init-advisor` scaffolds `farplane/products/core/product.md`,
  `farplane/products/core/skill.md`, `farplane/products.json`, and
  `.farplane/crm/`.
- `farplane/automations.toml` remains the automation config surface.

Migration steps:

1. Bump `farplane/manifest.json` `spec_version` and
   `template_uses.farplane-framework` to `1.6.17`.
2. Move active product-loop strategy into
   `farplane/products/<product>/product.md`.
3. Regenerate or check `farplane/products.json` from product-local
   `product.md` files.
4. Keep experiments and learning in product-local `progress.md`; keep customer
   research in `.farplane/crm/reports/`.

Proof commands:

```bash
python3 bin/validators/check_farplane_project_files.py
python3 bin/validators/render_product_index.py --check
```

## 1.6.14

Date: 2026-07-03

Primary change: remove the separate metric UI projection and make
`.farplane/project/ui/latest.json` the only UI read model. Core primitive
metrics still write daily readings and observations; `farplane project
snapshot` now owns metric series, content metric cards, source gaps, and tab
payloads.

Changed surfaces:

- `MANIFEST_TEMPLATE.json` bumps `farplane-framework` from `1.6.13` to
  `1.6.14`.
- Project manifests ignore `.farplane/project/ui/` instead of a separate metric
  UI projection directory.
- `farplane metrics primitives` remains the collection command.
- `farplane project snapshot` is the supported UI/read-model command.

Migration steps:

1. Bump `farplane/manifest.json` `spec_version` and
   `template_uses.farplane-framework` to `1.6.14`.
2. Stop calling the retired metric compiler command.
3. Render Overview, Goals, Products, Distribution, Cadence, Kanban, Proof, and
   Memory/Reports from `.farplane/project/ui/latest.json`.
4. Read KPI chart cards from `snapshot.metrics.series[]` and content metric
   cards from `snapshot.metrics.contents[]`.

Proof commands:

```bash
python3 -m unittest discover -s bin/tests
python3 bin/farplane.py metrics primitives --project-root . --date <YYYY-MM-DD> --json
python3 bin/farplane.py project snapshot --project-root . --date <YYYY-MM-DD> --json
python3 bin/validators/check_farplane_project_files.py --root .
python3 bin/validators/check_doc_refs.py
```

## 1.6.13

Date: 2026-07-02

Primary change: migrate project bindings from Markdown-wrapped YAML to a
canonical YAML file. `farplane/bindings.yaml` now owns non-secret project
coordinates and prompt-only metric recipes directly; `farplane/bindings.md` is
retired for current Farplane projects while metric tooling keeps a legacy
fallback for older projects.

Changed surfaces:

- `MANIFEST_TEMPLATE.json` bumps `farplane-framework` from `1.6.12` to
  `1.6.13`.
- `BINDINGS_TEMPLATE.yaml` bumps to `0.3.3` and replaces the retired
  `BINDINGS_TEMPLATE.md`.
- Project manifests track `farplane/bindings.yaml`.
- Project-file validation parses bindings as YAML and rejects leftover
  `farplane/bindings.md`.

Migration steps:

1. Rename `farplane/bindings.md` to `farplane/bindings.yaml`.
2. Remove the Markdown title, policy prose, and fenced YAML wrapper; keep
   `kind`, `framework_template_version`, `project`, `integrations`, and
   `metrics` as top-level YAML keys.
3. Bump `framework_template_version` in bindings to `0.3.3`.
4. Bump `farplane/manifest.json` `spec_version` and
   `template_uses.farplane-framework` to `1.6.13`.

Proof commands:

```bash
python3 -m unittest bin.tests.test_farplane_project_snapshot bin.validators.test_check_farplane_project_files
python3 bin/validators/check_farplane_project_files.py --root .
python3 bin/validators/check_doc_refs.py
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

## 1.6.12

Date: 2026-07-02

Primary change: add a local owned-content ledger for autonomous growth loops.
Farplane Core owns `.farplane/content/ledger.jsonl` and the `farplane content`
CLI contract; publishing/account skills append rows after confirmed approved
posting; metric refresh uses the ledger as the fetch target list for
distribution KPIs. Farplane UI may render this as a distribution tab later, but
does not own the schema.

Changed surfaces:

- `MANIFEST_TEMPLATE.json` bumps `farplane-framework` from `1.6.11` to
  `1.6.12`.
- Standard ignored paths include `.farplane/content/`.
- `farplane content add/list` manages the local JSONL ledger.
- X and Instagram account skills must record confirmed publishes in the ledger.

Migration steps:

1. Bump `farplane/manifest.json` `spec_version` and
   `template_uses.farplane-framework` to `1.6.12`.
2. Add `.farplane/content/` as an ignored runtime path.
3. After approved posting, run `farplane content add` with platform, external
   ID or URL, status, approval, publish timestamp, campaign, KPIs, and approval
   ref.
4. Point distribution metric refresh prompts at `.farplane/content/ledger.jsonl`
   for per-post fetch targets.

Proof commands:

```bash
python3 -m unittest bin.tests.test_farplane_content
python3 bin/farplane.py content add --project-root /tmp/fp --platform instagram --external-id demo --kpis instagram_views --status posted --approval approved
python3 bin/validators/check_farplane_project_files.py --root .
```

## 1.6.11

Date: 2026-07-02

Primary change: make SMART-goal KPI targets parseable. `farplane/goals.yaml`
keeps strategic targets, but each KPI under `smart_goals[].kpis` now uses an
`id`, numeric `target`, and `direction` pair so the project snapshot can
derive target-hit status without putting targets back into `bindings.yaml`.

Changed surfaces:

- `MANIFEST_TEMPLATE.json` bumps `farplane-framework` from `1.6.10` to
  `1.6.11`.
- `GOALS_TEMPLATE.yaml` bumps to `0.4.3` and shows KPI target pairs.
- `farplane project snapshot` overlays KPI target metadata from `goals.yaml` onto
  metric definitions while preserving legacy binding-target compatibility.

Migration steps:

1. Bump `farplane/manifest.json` `spec_version` and
   `template_uses.farplane-framework` to `1.6.11`.
2. Rewrite SMART-goal KPI entries from string IDs to target pairs:
   `{ id, target, direction }`.
3. Use `direction: above` for growth targets and `direction: below` for
   guardrail targets.
4. Keep units, chart display, pinned status, and refresh prompts in
   `farplane/bindings.yaml`.

Proof commands:

```bash
python3 -m unittest bin.tests.test_farplane_project_snapshot
python3 bin/farplane.py project snapshot --project-root . --date 2026-07-02 --json
python3 bin/validators/check_farplane_project_files.py --root .
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

## 1.6.10

Date: 2026-07-02

Primary change: simplify KPI collection to prompt-only metric recipes plus one
daily metrics JSON file. `farplane/bindings.yaml` metric recipes no longer carry
targets, provider routes, write paths, or observation blocks; interval update
collects each KPI reading into `.farplane/metrics/daily/YYYY-MM-DD.json`, and
Core compiles daily readings into UI JSON.

Changed surfaces:

- `MANIFEST_TEMPLATE.json` bumps `farplane-framework` from `1.6.9` to
  `1.6.10`.
- `BINDINGS_TEMPLATE.yaml` bumps to `0.3.2` and uses prompt-only `refresh`
  strings for metric recipes.
- `interval-update` owns the daily metric refresh workflow and daily JSON write
  contract.
- `farplane project snapshot` reads daily metric files and derives daily diffs,
  cumulative totals, best-daily values, source gaps, and pinned KPI cards.

Migration steps:

1. Bump `farplane/manifest.json` `spec_version` and
   `template_uses.farplane-framework` to `1.6.10`.
2. Remove `target`, `observation`, `source`, `route`, `writes`, `paths`,
   `repo`, and `update_prompt` from `bindings.metrics.*`.
3. Add `refresh` prompt strings to each metric recipe and keep SMART targets in
   `farplane/goals.yaml`.
4. Write daily readings to `.farplane/metrics/daily/YYYY-MM-DD.json`:
   `{ date, metrics: { [metric_id]: { value, status, payload? } } }`.
5. Count ticket-derived KPIs during interval refresh by matching
   `Reward.kpi_rewards[].kpi_id`, then store the count as a normal daily metric
   value.
6. Run the project snapshot after daily readings exist.

Proof commands:

```bash
python3 -m unittest bin.tests.test_farplane_project_snapshot
python3 bin/farplane.py project snapshot --project-root . --date 2026-07-02 --json
python3 bin/validators/check_farplane_project_files.py --root .
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

## 1.6.9

Date: 2026-07-01

Primary change: make KPI refresh agent-owned. Metric recipes now describe
observation instructions and update prompts; interval agents or skills write
`.farplane/metrics/observations/<workflow>/<date>.json`, and Core only compiles
those observations into UI JSON.

Changed surfaces:

- `MANIFEST_TEMPLATE.json` bumps `farplane-framework` from `1.6.8` to `1.6.9`.
- `BINDINGS_TEMPLATE.yaml` bumps to `0.3.1` and uses `observation` blocks instead
  of `source` blocks for metric recipes.
- `farplane project snapshot` is the supported KPI UI projection command.

Migration steps:

1. Bump `farplane/manifest.json` `spec_version` and
   `template_uses.farplane-framework` to `1.6.9`.
2. Rename metric recipe `source` blocks to `observation` blocks.
3. Set each `observation.writes` path to
   `.farplane/metrics/observations/<workflow>`.
4. Update interval prompts to write observation snapshots before running the UI
   compiler.

Proof commands:

```bash
python3 -m unittest bin.tests.test_farplane_project_snapshot
python3 bin/farplane.py project snapshot --project-root . --date 2026-07-01 --json
python3 bin/validators/check_farplane_project_files.py --root .
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

## 1.6.8

Date: 2026-07-01

Primary change: move metric source, chart, pinned, unit, and update-hint
ownership into `farplane/bindings.yaml` metric recipes while keeping
`farplane/goals.yaml` focused on strategic KPI IDs and interpretation.

Changed surfaces:

- `MANIFEST_TEMPLATE.json` bumps `farplane-framework` from `1.6.7` to `1.6.8`.
- `GOALS_TEMPLATE.yaml` bumps to `0.4.2` and uses KPI IDs only under SMART goals.
- `BINDINGS_TEMPLATE.yaml` bumps to `0.3.0` and replaces custom
  `project-bindings` plus provider `provides` lists with one YAML
  `Project Config` block containing `project`, `integrations`, and `metrics`
  whose source/update prompt lives inline under each KPI.
- Metric snapshots use canonical `bindings.metrics` recipes; older tracked-KPI,
  metric-provider, and provider-first fallback grammar is superseded rather than
  preserved in the runtime loader.
- UI snapshots carry `pinned` metadata from metric recipes.

Migration steps:

1. Bump `farplane/manifest.json` `spec_version` and
   `template_uses.farplane-framework` to `1.6.8`.
2. Move metric metadata from `farplane/goals.yaml` KPI maps into
   `farplane/bindings.yaml` `metrics.<metric_id>`.
3. Replace provider `provides` lists with metric recipes that include an
   inline `source` block and `update_prompt`.
4. Keep goals readable: SMART goals list KPI IDs and interpretation only.
5. Run the project snapshot smoke and project-file validators.

Proof commands:

```bash
python3 -m unittest bin.tests.test_farplane_project_snapshot
python3 bin/farplane.py project snapshot --project-root . --date 2026-07-01 --json
python3 bin/validators/check_farplane_project_files.py --root .
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

## 1.6.7

Date: 2026-07-01

Primary change: superseded transitional KPI wiring that briefly used
goal-local chart metadata and provider-first feedback coordinates for autonomy
time and GitHub repo adoption. Projects should migrate directly to `1.6.8`.

Changed surfaces:

- `MANIFEST_TEMPLATE.json` bumps `farplane-framework` from `1.6.6` to `1.6.7`.
- `GOALS_TEMPLATE.yaml` bumps to `0.4.1` and shows one-key KPI maps with
  `aggregation`, `cumulative`, `target`, `unit`, and `display`.
- `BINDINGS_TEMPLATE.yaml` bumps to `0.2.0` and added an earlier provider-first
  feedback-coordinate section. This shape is superseded by `1.6.8` inline
  metric recipes.
- The retired operating-memory template had added autonomy-time and
  repo-adoption tracked-feedback refs before the product-strategy migration.
- Framework docs describe the `goals.yaml` KPI keys plus `bindings.yaml` provider
  loop, daily/cumulative chart semantics, and source-gap behavior.

Migration steps:

1. Bump `farplane/manifest.json` `spec_version` and
   `template_uses.farplane-framework` to `1.6.7`.
2. Keep SMART goal KPI keys beside each goal axis; use one-key KPI maps only
   when chart metadata is needed.
3. Prefer the `1.6.8` migration instead: author inline metric recipes in
   `farplane/bindings.yaml`; missing access becomes a source gap.
4. Superseded by the product-strategy migration: add autonomy-time and repo
   adoption refs to the owning product strategy when relevant. Store raw
   values in metric snapshots, not product strategy.

Proof commands:

```bash
python3 -m unittest bin.tests.test_farplane_project_snapshot
python3 bin/farplane.py project snapshot --project-root . --date 2026-07-01 --json
python3 bin/validators/check_farplane_project_files.py --root .
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

## 1.6.6

Date: 2026-07-01

Primary change: historically made the now-retired operating-memory surface a
standard generated project file with a reusable template and documented
sections. This was later superseded by product-local strategy in `product.md`.

Changed surfaces:

- `MANIFEST_TEMPLATE.json` bumps `farplane-framework` from `1.6.5` to `1.6.6`.
- Standard tracked paths temporarily included the operating-memory file.
- Bootstrap temporarily copied the retired operating-memory template.
- Project-file and lifecycle docs temporarily described operating-memory
  sections such as focus, active projects, tracked feedback, frontier,
  constraints, parking, recent decisions, and Pulse notes.

Migration steps:

1. Bump `farplane/manifest.json` `spec_version` and
   `template_uses.farplane-framework` to `1.6.6`.
2. Superseded: do not add the retired operating-memory file.
3. Keep raw metric readings in `.farplane/metrics/**`; use product strategies
   for active project context, feedback refs, source gaps, and next-frontier
   notes.

Proof commands:

```bash
bash -n skills/init-advisor/scripts/bootstrap.sh
python3 bin/validators/check_farplane_project_files.py --root .
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

## 1.6.4

Date: 2026-06-28

Primary change: make both Documentation OS source layers explicit in generated
projects.

Changed surfaces:

- `MANIFEST_TEMPLATE.json` bumps `farplane-framework` from `1.6.3` to `1.6.4`.
- Standard tracked paths now include `docs/systems/README.md`.
- Bootstrap creates both `docs/features/` and `docs/systems/`.
- Bootstrap copies `FEATURES_README_TEMPLATE.md` and
  `SYSTEMS_README_TEMPLATE.md`.
- Bootstrap closeout explains that feature specs live in
  `docs/features/FEAT-*.md`, while system/product grouping and boundaries live
  in `docs/systems/*.md`.

Related template baseline:

- `tickets/templates/ticket.md` is already `ticket-template` `0.1.3`, from the
  ticket planning-shape update. The framework manifest still tracks the same
  `tickets/templates/ticket.md` path, so `1.6.4` does not add a new ticket
  template path; migrations should still check that projects have adopted the
  current ticket template shape before claiming full framework health.

Migration steps:

1. Bump `farplane/manifest.json` `spec_version` and
   `template_uses.farplane-framework` to `1.6.4`.
2. Ensure `docs/features/README.md` exists and describes feature specs as the
   canonical `FEAT-*` capability surface.
3. Ensure `docs/systems/README.md` exists and describes system/product grouping
   and boundaries.
4. Replace canonical `docs/specs` guidance with `docs/features` for feature
   specs and `docs/systems` for product/system grouping.
5. Preserve existing `docs/specs` content until each file is moved to the right
   owner or captured in a follow-up migration ticket.
6. Confirm `tickets/templates/ticket.md` is on `ticket-template` `0.1.3` or
   record a separate ticket-template migration follow-up.

Proof commands:

```bash
rg -n "docs/specs|specs/README" AGENTS.md PROJECT_RULES.md ARCHITECTURE.md farplane docs templates tickets qa .agents
bash -n skills/init-advisor/scripts/bootstrap.sh
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

## 1.6.3

Date: 2026-06-27

Primary change: move the generated project spec index from `docs/specs` to
`docs/features`.

Changed surfaces:

- `MANIFEST_TEMPLATE.json` bumped `farplane-framework` from `1.6.2` to `1.6.3`.
- Standard tracked paths replaced the legacy spec index with
  `docs/features/README.md`.
- Generated project guidance began treating feature docs as first-class
  capability specs under the Documentation OS.

Migration steps:

1. Add `docs/features/README.md`.
2. Replace project guidance that says the legacy spec index is the canonical
   feature spec index.
3. Keep or migrate existing legacy spec files based on owner fit; do not
   delete valuable project docs blindly.

## 1.6.2

Date: 2026-06-26

Primary change: include generated `.gitignore` policy in the standard tracked
project substrate.

Changed surfaces:

- `MANIFEST_TEMPLATE.json` bumped `farplane-framework` from `1.6.1` to `1.6.2`.
- Standard tracked paths added `.gitignore`.
- Bootstrap appends `GITIGNORE_TEMPLATE` so local runtime state and active
  ticket work stay out of commits by default.

Migration steps:

1. Add or update the Farplane `.gitignore` block.
2. Confirm `.farplane/` runtime state is ignored.
3. Confirm active ticket-work ignore behavior matches the project policy.
