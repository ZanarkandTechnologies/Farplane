---
skill: recap-idea + recap-task
date: 2026-08-29
change_type: structure
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref:
  - skills/recap-idea/SKILL.md@114-lines
  - skills/recap-task/SKILL.md@197-lines-template-0.4.0
after_ref:
  - skills/recap-idea/SKILL.md@87-lines-template-0.6.2
  - skills/recap-task/SKILL.md@100-lines-template-0.6.2
reasoning_basis: reviewer
proof_artifacts:
  - skills/recap-idea/evals/evals.json
  - skills/recap-task/evals/evals.json
  - .farplane/evals/runs/20260829T045013Z-recap-idea-template-062-20260829/summary.json
  - .farplane/evals/runs/20260829T045013Z-recap-task-template-062-20260829/summary.json
  - .farplane/evals/runs/20260829T045249Z-recap-task-template-062-repair-20260829/summary.json
  - .farplane/evals/runs/20260829T045422Z-recap-idea-template-062-boundary-20260829/summary.json
  - .farplane/evals/runs/20260829T045422Z-recap-task-template-062-boundary-20260829/summary.json
eval_required: yes
---

# Recap Template-First Modernization

## Change

- Before: `recap-task` used the `0.4.0` checklist shape, carried rendering rules
  in first load, and spread one eval packet across four example files.
- After: both shortcuts use `0.6.2` Golden Workflow Nodes. Render shapes live
  in conditional template references, and the task eval uses one fixture packet.
- Why: agents should decide which template applies, fill it, and stop; they do
  not need a long rulebook in first load.
- Tradeoff accepted: uncommon formatting detail loads only after a template is
  selected rather than being visible in every invocation.

## Refinement Decisions

| Unit | Decision | Reason |
| --- | --- | --- |
| Trigger, signature, decisive routing | keep + rewrite | Required on first load; rewritten into current contract fields. |
| View selection and proof-conflict logic | keep | These signals change the chosen template and safe claim. |
| Repeated formatting instructions | move | Owned by `references/visual-templates.md` and `references/templates.md`. |
| Checklist-era nested rules | merge | Four or three bounded nodes now carry only executable decisions and asserts. |
| Four warehouse example files | delete + replace | One eval fixture preserves the same ticket, history, evidence, and worktree boundary. |
| Generic caution and repeated recap prose | delete | It did not change routing beyond the remaining nodes, templates, and gotchas. |

## Loss Check

- Preserved: idea/task trigger boundary, six visual routes, Mermaid-first UI
  playback, open conflicts, source authority, proof-state separation, freshness,
  task-scoped changes, quick/full/source-gap modes, attempt history, literal
  source paths, and read-only behavior.
- Removed from first load: full output skeletons, repeated timeline/path rules,
  and explanations duplicated by templates or eval assertions.
- Installed copies under `~/.codex/skills/` remain outside this repo-source change.

## Proof

- `farplane lint evals --changed --json`: pass; 82 manifests checked.
- `check_skills.py --write`: pass; 13 checks and 114 registry rows.
- JSON parse: pass for both eval manifests.
- `recap_idea_selects_user_visible_ui_flow_01`: pass at `1.0`.
- `recap_idea_rejects_status_only_01`: pass at `1.0`.
- `recap_task_names_missing_durable_context_01`: pass at `1.0`.
- The first compacted proof-conflict run scored `0.875`: it returned the right
  warning but abbreviated the required full ledger. N3 now makes `full` a hard
  branch for proof conflicts; `recap_task_surfaces_conflicting_completion_01`
  then passed at `1.0`.
- Independent review: initial `TAS-B` identified the missing failed-run artifact
  above as the only blocker; the skill contracts, template placement, prose,
  fixture consolidation, registry rows, and behavior receipts passed.
