---
title: Skill Maintenance Eval Fixture Sandbox
owner: skills/skill-maintenance
status: draft
updated: 2026-06-12
---

# Skill Maintenance Eval Fixture Sandbox

Use this reference when writing or running evals that ask `skill-maintenance` to
inspect or repair bad skill packages. These evals must not mutate the real
`skills/` tree unless the runner owns an isolated checkout.

```text
skill_maintenance_fixture_eval(fixture_repo, task, proof_command)
  -> sandbox_root + repaired_fixture? + validation_report
```

## Fixture Owner

Seed bad skills under:

```text
skills/skill-maintenance/tests/fixtures/bad-skill-repo/
```

This fixture path is intentionally nested below `skills/skill-maintenance/tests`
so normal skill registry generation does not treat the bad skills as real
Farplane skills.

## Safe Run Pattern

For real repair tests, create a temp worktree and overlay the fixture there:

```bash
tmp="$(mktemp -d)"
rsync -a --exclude .git ./ "$tmp/farplane/"
rsync -a skills/skill-maintenance/tests/fixtures/bad-skill-repo/ "$tmp/farplane/"
cd "$tmp/farplane"
```

Then run repair commands inside `"$tmp/farplane"` only. Never point a mutation
eval directly at the real repo root unless the runner has created an isolated
checkout for that run.

## Eval Task Rules

Skill-maintenance eval queries should:

- name the fixture path or sandbox requirement;
- ask for an inspect/repair plan or sandboxed repair, not a live repo mutation;
- include reference points for source ownership, prototype-before-bulk,
  registry sync, audit records, and validation;
- reject completion claims without proof artifacts from the sandbox;
- keep AGI Toy Shop as the clean-room company context, while bad skill files
  provide the concrete filesystem evidence.

## Seed Bad Skills

Current fixture bad skills:

- `bad-signature-rollout`: promises template version `0.2.0` but has a weak
  first-load shape, generic job section, and non-actionable todo.
- `installed-copy-only`: simulates a desired behavior existing in an installed
  copy while repo source still needs a dry-run import or explicit source-owner
  decision.

## Acceptance

An eval using this fixture is good when the target answer:

- refuses to mutate real source unless the runner owns the sandbox;
- explains the sandbox path or temp-copy plan;
- diagnoses the seeded bad skill before repair;
- chooses the smallest representative repair before broad rollout;
- names the validation command and expected evidence;
- preserves repo source ownership and treats installed copies as inputs, not
  default source of truth.
