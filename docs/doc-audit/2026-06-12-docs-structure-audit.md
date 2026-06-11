---
date: 2026-06-12
kind: docs-structure-audit
status: applied
scope:
  - docs/
  - README.md
  - ARCHITECTURE.md
  - AGENTS.md
---

# Docs Structure Audit

## Question

Should Farplane compress, remove, or relocate parts of `docs/`, especially empty
folders, archived specs, assets, features, policies, and legacy research?

## Current Shape

`docs/` contains 10 top-level subdirectories:

| Path | Files | Role | Initial verdict |
| --- | ---: | --- | --- |
| `docs/archive/` | 16 | Superseded specs and cold research evidence | Keep as cold historical context. |
| `assets/` | 1 | README hero image and future repo-level media | Keep as top-level asset owner. |
| `docs/doc-audit/` | 1 generated + this audit | Generated doc graph/report and manual docs audits | Keep. |
| `docs/features/` | 4 | Structured feature registry plus validator | Keep; it is an active machine-readable system of record. |
| `docs/review/` | 21 | Review rubric docs | Keep; active owner for review rubric bodies. |
| `docs/skills/` | 5 | Skill system docs and generated registry | Keep. |
| `docs/sources/` | 4 | Structured source provenance registry plus validator | Keep; active machine-readable source dedupe. |
| `docs/specs/` | 16 | Canonical harness specs | Keep, but consolidate low-reference specs. |

Applied cleanup removed `docs/policies/` and the active `docs/research/` tree.

## Findings

### Empty Folders

`docs/policies/` was the only empty directory. It had no active files and no
clear current contract, so it was deleted.

### Archive

`docs/archive/specs/*` is intentionally referenced from `docs/specs/README.md`
as superseded context. This is useful while recent migrations are still being
understood, but it should not be an always-growing second spec tree.

Recommended rule:

```text
archive_spec(spec) -> keep only when active docs link it as superseded context
```

Archive can stay, but add a retention rule: archived specs with no active
backlink, no ticket backlink, and no source-registry value should be deleted or
moved to ticket history.

### Assets

The README hero image moved from `docs/assets/farplane-hero.png` to
`assets/farplane-hero.png`:

```text
README.md -> assets/farplane-hero.png
```

This gives future generated media and brand assets a normal top-level owner
instead of hiding repo-level media under docs.

Recommended boundary:

```text
assets/* = reusable product/brand/media assets outside docs
```

### Features

`docs/features/` is not narrative docs. It is a structured registry used by
skills, validators, tickets, and harness-scout. Keep it. It answers:

- what feature exists?
- where does it live?
- what source/ticket/evidence supports it?
- what known limits should future agents preserve?

Compression target is not deletion; it is avoiding duplicate prose in
`harness-techniques.md` and feature rows.

### Sources

`docs/sources/` is also active structured state. It dedupes external or
operator-provided inspirations before they become features. Keep it. It is
paired with `docs/features/`.

### Research

`docs/research/` was the highest cleanup opportunity. Current contents were
mostly historical April/May web research and comparisons. Several old agent
prompts referred to subfolders such as `docs/research/explorer/`,
`docs/research/librarian/`, `docs/research/remote-documentation/`, and
`docs/research/design/`, but those directories did not exist in the tracked
tree.

Applied migration:

1. Moved all tracked research memos to `docs/archive/research/`.
2. Updated active agent prompts away from non-existent `docs/research/*`
   write targets.
3. Kept active research work pointed at tickets, experiments, source records,
   feature records, or explicit caller-provided artifact paths.

### Specs

`docs/specs/` is large, but mostly intentional. The strongest active specs are:

- `harness-algebra.md`
- `harness-engineering-doctrine.md`
- `harness-techniques.md`
- `filesystem-lifecycle.md`
- `self-improvement-contracts.md`
- `review-gates.md`
- `spec-first-execution-loop.md`
- `invocation-and-adapters.md`

Potential compression candidates:

- `diagram-first-conventions.md`: folded into `skills/diagramming/SKILL.md`,
  then removed as a standalone spec.
- `spec-authoring-contract.md`: kept because it is still an active cross-skill
  contract referenced by `deep-system-design`, `spec-to-ticket`, `impl-plan`,
  the feature registry, and `harness-techniques.md`.
- `first-principles-planning.md`: useful doctrine, but may belong in
  `impl-plan`, `prd`, and `spec-to-ticket` references if it is not a canonical
  cross-spec.

Do not compress `harness-algebra.md` just because it is long. It is the current
math spec and directly supports harness-advisor reasoning.

## Recommended Cleanup Plan

### Pass 1: Mechanical Prune

```text
delete_empty_docs_dirs() -> remove docs/policies
```

Status: applied.

### Pass 2: Research Contract Cleanup

```text
normalize_research_surface(old_agent_prompts, current_research_skill)
  -> updated agent prompts + kept research artifacts + archived stale memos
```

Status: applied for active prompts. Historical archived files and archived
tickets may still mention old paths as historical text.

### Pass 3: Spec Compression

```text
compress_specs(specs, backlinks, owner_surface)
  -> keep | fold_into_skill | fold_into_spec_index | archive | delete
```

Status:

1. `docs/specs/diagram-first-conventions.md`: removed after folding the rule
   into `skills/diagramming/SKILL.md`.
2. `docs/specs/spec-authoring-contract.md`: kept as active cross-skill
   contract.
3. `docs/specs/first-principles-planning.md`: kept for now.

Do not batch all specs at once.

### Pass 4: Archive Retention Rule

```text
archive_retention(archive_doc)
  -> keep_when_linked | move_to_ticket_history | delete
```

Add the rule to `docs/specs/README.md` or `docs/specs/doc-governance.md`, then
review archived specs against it.

## Recommendation

Applied cleanup:

1. Deleted `docs/policies/`.
2. Moved README media from `docs/assets/` to `assets/`.
3. Moved tracked `docs/research/` files to `docs/archive/research/`.
4. Updated active agent prompts away from retired research subfolders.
5. Folded `diagram-first-conventions.md` into `skills/diagramming/SKILL.md`.

Hold off on deleting `docs/archive/`, `docs/features/`, `docs/sources/`, or
`docs/specs/spec-authoring-contract.md`.
