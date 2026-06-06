# Meta Harness Automation

Date: 2026-06-06

## Goal

Show how Farplane grows, audits, and maintains itself without scattering
meta-work across chat, one-off tickets, or duplicate registries.

This is the map for "what supports the harness improving the harness?"

## Core Model

```text
SelfGrowingHarness :=
  FeatureRegistry
+ SkillRegistry
+ SkillMaintenance
+ SourceIngestion
+ EvaluationAndBehaviorTests
+ FailureCapture
+ ReviewAndProof
+ DurableMemory
```

Each piece has a different job:

- `docs/features/registry.jsonl` is the central catalog of supported harness
  features, including skill-applicable features with `category: "skills"`.
- `docs/skills/registry.jsonl` is the generated inventory of skill packages.
- `skills/skill-maintenance` owns bulk skill upkeep, registry sync, checklist
  migration, tier/source metadata, and skill-system validation.
- `skills/harness-scout` and `docs/sources/registry.jsonl` ingest outside
  ideas before they become local features.
- `skills/eval`, `skills/agent-behavior-test`, `skills/agent-qa-test`, and
  `bin/check_skill_capabilities.py` prove behavior and capability claims.
- `skills/repent`, `docs/TROUBLES.md`, and `experiments/hardcases/` turn
  corrected failures into reusable learning pressure.
- `skills/review` and ticket proof contracts stop self-approval before changes
  are treated as ready.
- `docs/HISTORY.md`, `docs/MEMORY.md`, and `docs/features/registry.jsonl`
  preserve the timeline, durable rules, and supported capability map.

## Supported Feature Catalog

Farplane uses one feature registry for harness capabilities:

```text
docs/features/registry.jsonl
```

Skill-applicable capabilities should use `category: "skills"` in that registry
instead of creating a separate skill feature registry. The feature row should
explain:

- the stable `FEAT-####` handle
- the live surfaces that own the behavior
- the evidence that proves the feature is implemented, partial, designed, or
  proposed
- the current known limits
- any metrics or scorecards used to judge future progress

Examples today include:

- `FEAT-0022` Tiered skill dependency loading
- `FEAT-0024` Skill capability sanity tests
- `FEAT-0030` On-demand skill plugin packaging
- `FEAT-0033` Embedded skill checklist install

When a future skill frontmatter field records feature adoption, it should
reference these `FEAT-####` handles rather than inventing loose feature names.

## Skill Standards

Skill package truth stays split by purpose:

- `skills/*/SKILL.md` frontmatter carries package-local metadata.
- `docs/skills/registry.jsonl` derives inventory facts from skill files.
- `docs/features/registry.jsonl` declares supported harness features.
- `skills/skill-maintenance` reports which skill packages are stale, missing a
  recommended feature, or claiming a feature without matching proof.

Use `skill_template_version` only for the structural skill template baseline
when that field exists. Use feature references for optional capabilities such
as capability tests, eval readiness, source sync, install rendering, or
behavior-test proof.

Do not store long migration histories in every skill. Git history, the feature
registry, generated skill registry, and maintenance checks should explain what
changed and what still needs work.

## Meta Feature Loop

When Farplane learns or adopts a new harness capability:

1. Use `harness-advisor` to decide the owning surface.
2. If the capability is real enough to track, add or update one
   `docs/features/registry.jsonl` row.
3. If the capability affects skills, keep it in the same registry with
   `category: "skills"`.
4. Update the owning skill, spec, hook, validator, ticket contract, or
   subagent prompt.
5. Run the smallest relevant validator or behavior test.
6. Write durable history or memory only when the change affects how future work
   should operate.
7. Let `skill-maintenance` own broad skill rollout checks instead of embedding
   rollout state in chat.

## Current Limits

- Skill feature adoption is not yet a generated per-skill field.
- `skill_template_version` is a proposed structural baseline field, not a
  current registry requirement.
- Skill health monitoring is still local and artifact-driven. Farplane does not
  run a hidden daemon or background scheduler.
- Feature rows are provenance and support records, not a substitute for tests,
  tickets, or review evidence.

## Validation

Use the checks that match the surface changed:

```bash
python3 docs/features/validate_features.py
python3 skills/skill-maintenance/scripts/check_skills.py --write
python3 bin/check_skill_capabilities.py validate
python3 bin/check_harness_invariants.py
python3 bin/check_doc_parity.py
```
