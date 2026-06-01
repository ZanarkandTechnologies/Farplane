# Work Skill Support

## Purpose

`$work` is the Work Admission surface for Codexter. It decides how a prompt,
ticket, ticket batch, board-selected unit, epic, or metric loop should use the
existing Codexter system before compute is spent.

It does not replace `impl-plan`, `$impl`, `batch-work`, `$ralph`, or native
Codex `/goal`. It classifies the work unit and chooses the right combination of
those surfaces.

## Public API / Entrypoints

- `SKILL.md`: operator-facing Work Admission contract
- `SKILL.md` Important Checklist: anti-forgetting checklist for classification, proof, and routing

## Minimal Example

```text
$work tickets/TASK-0178/ticket.md
```

`$work` reads the ticket, classifies the ambition and proof needs, decides
whether a native `/goal` is warranted, and routes to direct work, `impl-plan`,
`$impl`, `batch-work`, `$ralph`, `spec-to-ticket`, or autoresearch as needed.

## How to Test

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
python3 skills/skill-maintenance/scripts/generate_skill_graph.py
```

