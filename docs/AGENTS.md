# Docs Instructions

This tree owns durable human-readable context. Keep the document set as small
as possible while maximizing reader quality, source-of-truth clarity, and
machine-checkable outputs.

## Layout

Nothing else belongs at the top of `docs/`. "Generated" files are never
hand-edited; run their generator.

- `AGENTS.md`: these rules.
- `HISTORY.md`: meaningful milestones and migrations.
- `MEMORY.md`: current project invariants worth retrieving outside their owner.
- `prd.md`: the engine PRD.
- `guides/`: how a Farplane project works (work loop, skills, project files,
  CLI, hooks and runtime, Wiki and entities, reporting, graphs).
- `fundamentals/`: doctrine — reusable theory and background.

Removed on 2026-10-14: `docs/contracts/` (its files moved to their owning
skill and validator), `docs/doc-audit/`, `docs/bootstrap-brief.md`, and
`docs/TASTE.md`. Later that day the review rubrics moved into the `review`
skill (`skills/review/references/rubrics/`) so installed copies can reach them,
and `fundamentals/data-visualization.md` gave way to the `dataviz` skill.
On 2026-10-15 the `skills/`, `templates/` and `sources/` folders moved out:
skill-system docs and templates to the `harness` skill, the generated registries
to `skills/registry.jsonl` and `config/template-registry.jsonl`, the report
template to `report-gen`, and the source registry to `farplane/sources/`.
Also on 2026-10-15 `features/` and `systems/` were retired (behavior contracts
moved to their owning skills, the systems map to `ARCHITECTURE.md`) and
`farplane-framework/` became `guides/`.

## Doc Or Skill

Installed skills are symlinked into `~/.claude/skills/` and `~/.codex/skills/`
and run in other projects, where this `docs/` folder does not exist.

- Skill (`SKILL.md` or its `references/`): anything an agent loads to do a
  task — procedure, rubric, template it fills, checklist. Test: would the skill
  break if the Farplane repo were not on disk? Then it belongs in the skill.
  Cross-skill calls name the skill and input (`review` with family
  `implementation-plan`), never a path into `docs/`.
- `docs/`: records of how Farplane itself is designed and decided — PRD,
  guides, doctrine, history, memory — read by people and by agents
  maintaining this repo.
- Next to its code or config: anything a script reads (schemas, registries,
  source lists).

## Strategy

- Update an existing owner before creating a new doc.
- Behavior contracts live in their owning skill (`SKILL.md` or its
  `references/`), or next to the code that enforces them.
- The systems map lives in `ARCHITECTURE.md` (its Systems table).
- Put reusable theory, doctrine, and background in `docs/fundamentals/`.
- Put how-a-project-works narrative in `docs/guides/`.
- Put generated or machine-readable inventories behind their owning source
  files; do not hand-author duplicate truth.
- YAML frontmatter is a path-owned contract, not a free-form metadata bag.
  `bin/core/document_contract.py` owns the strict document types checked by
  `bin/validators/check_doc_frontmatter.py`; add a field only to its owning
  contract and its fixture coverage.
- Put task-local plans, proof, and bulky evidence in tickets or artifacts.
- Put temporary research outside tracked docs unless it has a current owner.

## Stale Docs

Delete stale docs instead of preserving archives by default. Before deleting,
move any current contract, lesson, or source decision into the smallest active
owner: a skill, guide, fundamentals doc, ticket, or generated registry source.
