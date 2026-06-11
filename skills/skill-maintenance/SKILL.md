---
name: skill-maintenance
description: "Turn bulk skill-system changes into updated frontmatter, checklists, registry sync, audits, and validation proof."
tier: 3
group: skills
source: local
skill_template_version: "0.2.0"
feature_refs:
  - FEAT-0037
  - FEAT-0040
  - FEAT-0044
---

# Skill Maintenance

## Context

Skill maintenance is the owner for bulk Farplane skill upkeep: template
onboarding, tier/source metadata, generated registry sync, todo-list shape,
link hygiene, source ownership, and consolidation planning. Use this skill to
make skill-system work repeatable instead of hiding rollout state in chat.

## Skill Signature

```text
maintain_skills(accepted_change, targets?, rollout_scope?) -> applied_change + registry_checks + audit_records?
state: reads(skill-system docs, target skills, registries, active ticket, prior audits); writes(SKILL.md, references?, registry, audits?, proof notes)
gates: template_structure_valid; source_owner_preserved; registry_synced; audit_recorded_or_skipped; review_or_blocker_recorded
routes: gap-analysis | skill-creator | eval | advise | deliberative-advice | review | execute
fails: bulk-edits without prototype; marks version without structure; edits installed copies as source of truth
```

```text
audit_skill_structure(skill, change, reasoning, evidence?) -> audits/YYYY-MM-DD-<short-change>.md + binary_rubric + followups
state: reads(SKILL.md, references, eval_task.json?, prior audits, reasoning notes, run artifacts?, reviewer receipts?); writes(skill-local audit record)
gates: first_principles_recorded; pass_fail_not_score; before_after_named; evidence_unknown_not_guessed
routes: advise | deliberative-advice | eval | review
fails: invents numeric health score; duplicates git last-edited state; claims task_success_rate without run artifacts
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Load the current skill-system baseline before editing.
   - [ ] Read `docs/skills/system.md`, `docs/skills/README.md`,
     the relevant anchored section of `docs/skills/best-practices.md`,
     `docs/skills/registry.jsonl`, active tickets, and the target skill files.
     Load the full best-practices file only for broad skill-system audits or
     standard-setting changes.
- [ ] 2. Classify the maintenance operation for each target skill.
   - [ ] 1. Template onboarding, signature rollout, or version audit.
   - [ ] 2. Todo-list or reference cleanup.
   - [ ] 3. Tier, source, group, feature-ref, method, or common-chain metadata
     update.
   - [ ] 4. Consolidation, split, or external-source ownership change.
   - [ ] 5. Structure audit or before/after behavior audit.
- [ ] 3. Route non-mechanical choices before editing.
   - [ ] Use [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
     when upstream or external skill examples should change the local contract.
   - [ ] Use the native planning phase or `harness-advisor` when tier, source,
     group, method ownership, or consolidation choices have real tradeoffs.
   - [ ] Use
     [advice and proof routing](../../docs/skills/best-practices.md#advice-and-proof-routing)
     before changing shared standards, Tier 1 primitives, meta skills, `eval`,
     templates, reviewer rubrics, or cross-skill policy.
- [ ] 4. Record the edit boundary for each target skill.
   - [ ] Identify source ownership, related skills, adopted `FEAT-####`
     records, first-load dependencies, proof surfaces, and files that may
     change.
   - [ ] When the source change started in `~/.codex/skills`, preview the pull
     into repo source with `python3 ../../bin/import_installed_skills.py --skills <name> --dry-run`
     from this skill package, then import with explicit `--overwrite` only when
     replacing an existing repo package is intentional.
- [ ] 5. Prototype broad rewrites on a representative sample before scaling.
   - [ ] Include a mix of Tier 1, Tier 2, and complex Tier 3 packages when the
     migration will affect many skills.
- [ ] 6. Edit each target `SKILL.md` so first-load work is executable.
   - [ ] Keep `description` as one sentence under 220 characters using
     `Verb input/context into output/artifact when call-condition`.
   - [ ] Put required actions in the marker-delimited `## Todo List`.
   - [ ] Keep every-invocation rules in `SKILL.md`.
   - [ ] Move conditional branches, examples, templates, long rubric detail,
     model maps, delegated prompts, and rare-path recipes into references.
   - [ ] Move actor identity, subagent spawning, caller routing, tool-use policy,
     and artifact writeback out of reusable skills unless the skill is explicitly
     an orchestration skill.
- [ ] 7. Verify template structure before marking a skill onboarded.
   - [ ] Check the actual `SKILL.md` headings, todo shape, and `## Skill
     Signature` against the current template before setting or keeping
     `skill_template_version`.
   - [ ] Prune redundant `todos.md` once direct todo-list content matches.
- [ ] 8. Validate the skill system with `python3 scripts/check_skills.py --write`
   from this skill package.
- [ ] 9. Reinstall touched local skills and inspect the live copy before judging
   Codex behavior.
   - [ ] Use `bash ../../install.sh --skills-only --skills <names> --target ~/.codex`
     from this skill package when the user is checking installed behavior.
   - [ ] Re-read `~/.codex/skills/<name>/SKILL.md` for at least one touched skill
     before claiming the visible checklist changed.
- [ ] 10. Review readiness before completion.
   - [ ] For material skill changes, write or update
     `skills/<skill-name>/audits/YYYY-MM-DD-<short-change>.md` using
     [skill-audit.md](templates/skill-audit.md), or explicitly record why the
     change is tiny enough to skip an audit record.
   - [ ] Record first-principles reasoning first: objective, placement logic,
     expected before/after behavior, tradeoff accepted, and proof needed.
   - [ ] Check structure metrics for each material target:
     `first_load_sufficiency`, `reference_load_precision`,
     `missing_context_rate`, `noisy_context_rate`,
     `duplicated_instruction_count`, `prompt_size_tokens`,
     `task_success_rate`, `review_tas_rate`, `maintenance_locality`, and
     `composition_clarity`.
   - [ ] Choose review depth with
     [docs/skills/best-practices.md](../../docs/skills/best-practices.md#structure-optimization):
     direct self-check for tiny mechanical edits, `advise` for normal recent
     skills, and `deliberative-advice` for Tier 1, meta, `eval`, stale,
     high-blast-radius, cross-skill, or precedent-setting structure changes.
   - [ ] For material skill-system changes, delegate final review to the native
     `reviewer` subagent with a reviewer handoff.
   - [ ] Use the Tier 0 execution/writeback phase for final proof, docs
     writeback, and ticket evidence when the pass needs durable closeout.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this when working on the skill system itself: tier metadata, direct todo
lists, legacy `todos.md` cleanup, source ownership, registry sync, link
hygiene, or consolidation planning.

## Core Rules

- Follow `docs/skills/system.md` for the tier model, source ownership,
  frontmatter contract, template versioning, feature tracking, and todo-link
  rules.
- Follow the relevant anchored section of `docs/skills/best-practices.md` for
  first-load todo-list shape, structure optimization metrics, reference
  placement, repeatability, and review gates. Do not load the full file for
  ordinary one-skill edits unless the placement or standard is broad enough to
  need it.
- `SKILL.md` is the first-load source of truth. Required todo items belong in a
  direct marker-delimited `## Todo List` section.
- First-load sufficiency has priority over modular neatness. Do not move required
  every-invocation context, gates, routing, proof, or output contracts into
  references just to make `SKILL.md` shorter.
- Keep logic in `SKILL.md` when it affects every invocation: trigger boundary,
  required order, decision routing, escalation, stop conditions, hard gates,
  output contract, and high-risk guardrails.
- Use the `docs/skills/best-practices.md#structure-optimization` metrics to
  decide whether a rule belongs in first-load `SKILL.md`, a reference,
  template, eval, or review check.
- Use `docs/skills/best-practices.md#placement-boundaries` to decide between
  `SKILL.md`, skill-local references, shared docs, templates, and evals based
  on access frequency, owner scope, depth, and length.
- Route review depth from the same metrics: use `advise` for ordinary recent
  skills and `deliberative-advice` when the skill is Tier 1, meta, `eval`,
  stale, far from the current template, high-traffic, cross-skill, or
  precedent-setting.
- Route advice and proof before editing: first-principles for obvious local
  choices, `advise` for ordinary local tradeoffs, `deliberative-advice` for
  standards or compounding surfaces, `research` for missing evidence, `eval` for
  behavioral claims, and reviewer for final readiness.
- Use `references/*` for conditional branches, examples, templates, long rubric
  detail, model maps, delegated prompts, and rare-path recipes.
- If a reference must be read every time, promote the needed logic into
  `SKILL.md`.
- Treat `todos.md` as a legacy/transitional input only. Delete it once it
  matches the direct `SKILL.md` todo list; reconcile divergent duplicates
  manually.
- External skills should carry `source: external` and usually `upstream_url`;
  local Farplane policy belongs in local callers.
- Router-style todos choose methods conditionally. They do not run every method
  in sequence.
- Complex Tier 3 pipeline skills should expose their domain as
  `Model + MethodRegistry + TodoRecipe + Templates + Proof` when that makes the
  workflow easier to scan. Keep the algebra in `SKILL.md` or a targeted
  `references/model.md`; do not add per-skill `README.md` files for this.
- Material skill changes should create a skill-local audit record at
  `skills/<skill-name>/audits/YYYY-MM-DD-<short-change>.md`. Use binary
  `pass` / `fail` / `unknown` rubric rows rather than numeric health scores.
  Do not add `health_score` or `last_edited` to `SKILL.md` front matter; derive
  freshness from git history and audit records.
- First-principles review is the default skill-structure review engine. Use evals,
  variant tournaments, or reviewer receipts only when reasoning cannot settle a
  choice, reviewers disagree, a regression guard is needed, or a claim depends
  on measured behavior.

## Workflow

1. Read `docs/skills/system.md`, `docs/skills/README.md`, the relevant anchored
   section of `docs/skills/best-practices.md`, `docs/skills/registry.jsonl`,
   and the target skill files.
2. Use [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
   when comparing external skill examples or upstream instructions.
3. Use the native planning phase or `harness-advisor` when
   tier/source/consolidation choices have real tradeoffs.
4. For broad migrations such as todo-list embedding or reference pruning, use
   [prototyping](../prototyping/SKILL.md) on a small representative set before
   running bulk commands.
5. Use `python3 ../../bin/import_installed_skills.py --skills <name> --dry-run`
   when a desired skill change exists only in `~/.codex/skills`; import without
   `--dry-run` only after confirming the package, and use `--overwrite` only for
   intentional repo-source replacement.
6. Update `SKILL.md` frontmatter only for manual fields: `tier`, `source`,
   `description`, optional `skill_template_version`, optional `feature_refs`,
   Tier 3 `group`, optional `methods`, optional `common_chains`, and optional
   `upstream_url`. Keep `description` as the functional routing definition, not
   a trigger catalog or mini manual. Use `feature_refs` only for compact
   `FEAT-####` handles already present in `docs/features/registry.jsonl`. Use
   `skill_template_version` only when the skill has been onboarded to a known
   structural template baseline; absence means not onboarded yet.
7. Put the anti-forgetting todo list directly in `SKILL.md` under
   `## Todo List`:
   - project/docs context first
   - required workflow and branch checks second
   - proof/writeback last
   - keep optional detail in references with clear read conditions
   - keep or create `todos.md` only as a temporary migration input
8. Run the standard skill-system check:

```bash
python3 scripts/check_skills.py --write
```

This command normalizes direct `## Todo List` sections, prunes
redundant `todos.md` files, regenerates the registry, verifies registry
metadata, checks todo-list tier edges, compiles the registry/check scripts, and
prints a compact summary. Use the lower-level commands only when debugging a
specific failure:

```bash
python3 scripts/sync_skill_checklists.py --write
python3 ../../bin/sync_skill_registry.py --write
python3 ../../bin/sync_skill_registry.py --check
python3 ../../bin/check_skill_todo_tiers.py --allow-peer-tier3
```

9. Use the Tier 0 execution/writeback phase for final proof, docs writeback,
   and ticket evidence after skill changes.
10. For material skill edits, write the skill-local audit record with
   first-principles reasoning, before and after behavior, optional proof
   artifacts or explicit evidence gaps, binary rubric rows, and followups.

## Outcome Contract

- Skill frontmatter remains minimal and valid. Skills may carry `feature_refs`
  for adopted harness feature handles. Onboarded skills may carry
  `skill_template_version`; missing values remain visible in the generated
  registry and `check_skills.py --template-version <version>` report.
  Versioned skills fail the check when their structure no longer matches the
  template promise.
- Skill `description` fields are one-sentence functional routing definitions
  under 220 characters and name the input/context, output/artifact, and call
  condition when those are not obvious.
- Broad skill migrations include a representative `Prototype Note` before full
  batch application.
- `SKILL.md` contains the required first-load todo list and high-signal logic.
- Transitional `todos.md` files are removed when redundant or left only when a
  human must reconcile divergent content.
- Complex Tier 3 skills keep any algebraic project/component/method model
  concise, discoverable, and subordinate to the `SKILL.md` first-load contract.
- `docs/skills/registry.jsonl` is regenerated, not hand-edited.
- External-source skills remain easy to refresh.
- Consolidation candidates are ticketed or documented before hard migration.
- Material skill changes leave a skill-local audit record, or state why the
  change was mechanical enough to skip one.
- `python3 scripts/check_skills.py --write` passes
  before completion is claimed.

## Templates

Use `skills/skill-creator/references/SKILL_TEMPLATE.md` as the structural
baseline when onboarding a skill to `skill_template_version: "0.2.0"`.

Use `templates/skill-audit.md` for skill-local audit records.

## Gotchas

- Do not mark a skill as onboarded to a template version unless its structure
  actually follows that template.
- Do not add a verbose type schema when a compact `## Skill Signature` captures
  callable behavior, state, gates, routes, and failure modes.
- Do not bypass the template-structure validator by treating
  `skill_template_version` as metadata-only.
- Do not let generated registry rows become a hand-edited source of truth.
- Do not bulk-edit every skill before proving the pattern on a representative
  sample.
- Do not move Farplane wrapper behavior into external-source skills.

## Reference Map

- [docs/skills/system.md](../../docs/skills/system.md) - tier model, source
  ownership, frontmatter contract, template versioning, feature tracking, and
  todo-link rules.
- [docs/skills/README.md](../../docs/skills/README.md) - human skill selection
  guide, generated registry surface, and maintenance commands.
- [docs/skills/best-practices.md](../../docs/skills/best-practices.md) -
  first-load shape, structure optimization metrics, reference placement,
  repeatability, and review gates.
- [../skill-creator/references/SKILL_TEMPLATE.md](../skill-creator/references/SKILL_TEMPLATE.md)
  - current baseline skill template.
- [templates/skill-audit.md](templates/skill-audit.md) - binary before/after
  audit record template for material skill changes.
- [scripts/check_skills.py](scripts/check_skills.py) - standard validation and
  template-version report.

## Output

- Updated `skills/*/SKILL.md` files.
- Regenerated `docs/skills/registry.jsonl`.
- Skill-local audit records for material skill changes, or an explicit skip
  reason for mechanical edits.
- A passing `python3 scripts/check_skills.py --write`
  result, or an explicit blocker with the exact failing command.
