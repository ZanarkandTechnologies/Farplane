---
name: coderabbit-review
description: Use when you want a heavyweight external CodeRabbit CLI review pass on local changes or a PR-sized branch, usually before push or on a PR branch rather than inside the Stop-hook loop.
tier: 2
source: local
allowed-tools: Read, Glob, Grep, Bash
---

# CodeRabbit Review

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Confirm `coderabbit --version` works in the repo.
- [ ] Confirm auth status with `coderabbit auth status --agent` or
  `coderabbit auth status`.
- [ ] Choose the stage: `pre-commit`, `pre-push`, `pr`, or direct agent review.
- [ ] Prefer `pre-push` or `pr` for the heavy default path.
- [ ] Use the repo runner for shell or git-hook entrypoints.
- [ ] Use raw `coderabbit review --agent` when Codex should read and fix the
  findings.
- [ ] Summarize Critical, Warning, and Info findings.
- [ ] Decide whether to fix now, rerun, or defer explicitly.
- [ ] Do not treat this as a Stop-hook default.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this for the heavier external review pass.

This skill is for CodeRabbit CLI review before push, on a PR branch, or during
an explicit agent review-fix loop. It is not the default internal `review`
skill, and it should not be wired into the Stop hook by default.

## Job

1. Confirm the repo is in a sane git state and that `coderabbit` is available.
2. Choose the right stage: `pre-commit`, `pre-push`, `pr`, or direct
   agent-driven review.
3. Run CodeRabbit with the correct `--type`, `--base`, and output mode.
4. Summarize findings by severity and decide whether to fix now or defer.
5. If the workflow calls for fixes, address the issues and rerun until the
   review is clean enough for the current gate.
6. Leave a concrete summary of what was checked, what remains, and whether the
   branch is ready to push.

## Use When

- the user explicitly asks for CodeRabbit review
- the branch is ready for a heavier pre-push or PR-quality review pass
- the change set is important enough to justify an external AI review
- you want CodeRabbit findings in addition to the repo's internal review loop

## Do Not Use When

- the user wants the normal internal `review` skill only
- you are inside the Stop-hook loop and trying to keep end-of-turn latency low
- the diff is still noisy or huge enough that a heavy review would be wasteful
- the CLI is not installed or authenticated and the user did not ask you to
  fix setup

## First-Load Checklist

Ensure an agent can execute the core path after only reading this file.

- Trigger conditions:
  - "run CodeRabbit"
  - "review this before push"
  - "do a PR review with the CodeRabbit CLI"
  - "use the CodeRabbit skill"
- Workflow:
  1. confirm `coderabbit --version` works and check auth status
  2. choose the stage: `pre-commit`, `pre-push`, `pr`, or direct agent mode
  3. prefer the repo helper for stage-based shell workflows
  4. use raw `coderabbit review --agent` when Codex itself should consume the
     findings and fix issues
  5. summarize Critical, Warning, and Info findings
  6. fix substantive issues when asked or when the workflow clearly implies it
  7. rerun or explicitly record what remains before push
- Core decision branches:
  - fresh local changes before commit -> `python3 skills/coderabbit-review/scripts/run_review.py --stage pre-commit`
  - branch-level gate before push -> `python3 skills/coderabbit-review/scripts/run_review.py --stage pre-push`
  - PR-ready branch review -> `python3 skills/coderabbit-review/scripts/run_review.py --stage pr`
  - agent-driven fix loop -> `coderabbit review --agent ...`
- Top gotchas:
  - do not put this on the Stop hook or make it a mandatory every-turn check
  - do not run a heavy review on a giant unfocused diff when the real fix is to
    shrink the review scope
  - do not claim success if CLI/auth/setup failed or the findings were not
    actually read
- Outcome contract:
  - one stage is chosen explicitly
  - the final command or helper invocation is recorded
  - findings are summarized by severity
  - the rerun or push-readiness decision is explicit

## Documentation Index

- Stage policy: [`references/stage-matrix.md`](references/stage-matrix.md)
- Hook recipes: [`references/hook-recipes.md`](references/hook-recipes.md)
- Helper runner: [`scripts/run_review.py`](scripts/run_review.py)
- Sample hooks:
  - [`scripts/pre-commit.sample`](scripts/pre-commit.sample)
  - [`scripts/pre-push.sample`](scripts/pre-push.sample)

## Default Policy

- prefer `pre-push` or `pr` for the normal heavyweight workflow
- treat `pre-commit` as opt-in for risky local slices, not the default
- use `coderabbit review --agent` when Codex should read findings and fix them
- use the repo helper when you want stage-aware defaults or a git-hook entrypoint
- keep the branch small and explicit; CodeRabbit's own Codex integration guide
  says reviews may take 8 to 30+ minutes on larger scopes

## Command Patterns

Agent-driven fix loop:

```bash
coderabbit review --agent --base main --type committed
```

Human-readable branch review:

```bash
python3 skills/coderabbit-review/scripts/run_review.py --stage pre-push
```

Fresh local review before commit:

```bash
python3 skills/coderabbit-review/scripts/run_review.py --stage pre-commit
```

PR-sized review against a chosen base:

```bash
python3 skills/coderabbit-review/scripts/run_review.py --stage pr --base main
```

## Workflow

1. Check `git status --short` and avoid reviewing an obviously messy branch.
2. Check `coderabbit --version`.
3. Check `coderabbit auth status --agent`.
4. Pick the stage:
   - `pre-commit` -> local uncommitted changes
   - `pre-push` -> committed branch diff against the default base branch
   - `pr` -> same as pre-push, but framed as the PR gate
   - agent loop -> raw `coderabbit review --agent`
5. Run the command.
6. Read the findings and group them into:
   - must-fix before push
   - safe defer
   - informational only
7. Fix and rerun when the request or gate calls for it.
8. Leave a final summary that says whether the branch is ready to push.

## Setup and Failure Rules

- If `coderabbit` is missing, stop and say so plainly.
- If auth is missing, stop and point to `coderabbit auth login --agent` for
  agent workflows or `coderabbit auth login` for manual workflows.
- If the branch is too large, narrow scope instead of pretending the slow pass
  is the normal path.
- If the user asks for PR-comment autofix from GitHub threads, that is a
  follow-up workflow, not this skill's base path.
