---
skill: commit
date: 2026-09-13
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/commit/SKILL.md@0.2.0
after_ref: skills/commit/SKILL.md@0.3.0
reasoning_basis: first_principles
proof_artifacts:
  - skills/commit/evals/evals.json
eval_required: yes
---

# Commit request-owned staging audit

## Change

- Before: the shortcut refused to act unless the operator curated the index.
- After: it resolves the requested task boundary, stages owned paths or cached
  hunks, commits once, and verifies unrelated work remains.
- Why: “commit this change” already identifies the intended work. Requiring a
  separate staging handoff breaks the shortcut and shifts Git mechanics to the
  operator.
- Tradeoff accepted: the skill stops when existing staged ownership cannot be
  separated safely; guessing would risk committing someone else's work.

## Proof

- Five integration tests prove explicit-file commits, unrelated staged and
  unstaged preservation, cached-patch hunk isolation, same-file staged-hunk
  preservation, and broad-path rejection.
- Skill evals cover whole-file staging, mixed generated files, and an
  inseparable pre-staged boundary.
- Full skill-system validation passed 13 checks.
- Initial independent review returned TAS-C because the staged-only helper could
  not preserve unrelated index entries. The helper now commits through a
  temporary index and restores staged changes over the prospective tree. A
  second TAS-C found same-file staged hunks were demoted by path reset; the
  helper now preflights and installs a restored index. A third TAS-C found Git
  pathspec magic could bypass broad-path rejection; the helper now accepts only
  explicit repo-contained leaf files. Final independent review: TAS-A with no
  actionable findings.
