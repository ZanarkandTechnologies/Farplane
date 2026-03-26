---
name: bash-efficiency
version: 1.0.0
description: "Bash efficiency workflow skill for shell-heavy tasks. Use when handling multi-step filesystem/build/debug work and when command safety, speed, and reproducibility matter."
allowed-tools: Read, Glob, Grep, Bash
---

# Bash Efficiency Skill

Use this skill when:

- A task needs many shell commands or multi-step terminal execution.
- You need to avoid wasteful patterns (retyping, recreating, manual copy/paste loops).
- You need safe command execution with preview, verification, and rollback notes.

## Problem

Agents often lose time by recreating files, retyping data, and running risky commands without preview or rollback structure. This skill enforces efficient, repeatable bash workflows with clear safety gates.

## First-Load Contract (Non-Negotiable)

### Trigger Conditions

Activate this skill when any of the following appears:

- "Move/rename/copy lots of files"
- "Run build/debug/test steps from terminal"
- "Do a bulk replace or data transform"
- "Use bash efficiently" or "optimize terminal workflow"
- "Delegate shell-heavy work to subagent"

### Workflow (7 Steps)

1. **Classify the task**: single safe command vs multi-step shell workflow.
2. **Preflight**: verify paths/tools; preview scope with read-only checks (`ls`, `tree`, `rg`, `wc`).
3. **Choose efficient primitives**: transform in place (`mv`, `cp -a`, pipes, redirection, `jq`/`yq`).
4. **Run with safety gates**: dry-run where possible, then execute.
5. **Verify effects**: confirm expected files/output/state changed and nothing else.
6. **Report clearly**: commands used, key outputs, files touched, rollback notes.
7. **Stabilize repetition**: promote recurring command chains into script/Make target.

### Core Decision Branches

- **Single command + low risk** -> run directly in main agent with concise verification.
- **Multi-step / shell-heavy / risky** -> delegate to `bash-operator` subagent.
- **Potentially destructive** (`delete`, bulk replace, overwrite) -> require preview + explicit verification before final execution.
- **Unclear scope or path ambiguity** -> stop and ask before execution.

### Top 3 Gotchas

1. Recreating files when rename/move would do (`mv` instead of rewrite).
2. Retyping file contents into commands instead of processing files directly.
3. Running broad replace/delete operations without a preview step.

### Outcome Contract

When this skill is used, outputs must include:

1. Command plan (or executed command list)
2. Verification evidence (what changed)
3. Rollback guidance for non-trivial operations
4. Delegation decision (main agent vs `bash-operator`)
5. Expected vs observed diff and fix plan when execution fails or deviates

## Default Bash-Efficiency Rules

Principle: **Don't retype. Don't recreate. Transform in place.**

- Rename/move: `mv old new`, `mkdir -p dir && mv *.log dir/`
- Preserve metadata when copying: `cp -a src/ dest/`
- Search before acting: `rg 'pattern' -n`
- Process files directly: `python script.py < input.json > output.json`
- Prefer pipes over temp files: `cmd1 | cmd2 | cmd3`
- Batch JSON/YAML edits: `jq`, `yq`
- For repeated workflows, codify in `scripts/` or `Makefile`

## Subagent Delegation Policy

Delegate to `bash-operator` when:

- More than one dependent shell step is required
- Filesystem mutation is broad or potentially risky
- Build/debug workflow requires iterative terminal loops

Keep in main agent when:

- One command answers the user request safely
- No broad mutation and verification is trivial

## References

- [references/patterns.md](references/patterns.md) - common efficient command patterns
- [references/safety-and-rollback.md](references/safety-and-rollback.md) - execution guardrails
- [references/bash-operator-expected-output.md](references/bash-operator-expected-output.md) - ASCII expected report spec for visual QA
- [prompts/operator.md](prompts/operator.md) - copy/paste delegation prompt
