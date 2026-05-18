---
name: desloppify
version: 0.1.0
description: "Use when the operator wants repo-quality cleanup driven by the `desloppify` CLI. This skill supports two modes: the main agent delegates one bounded worker for the scan/next/resolve loop, while a delegated worker runs the CLI directly without spawning again. If worker mode hits nested `desloppify review --run-batches --runner codex` work, it must stop and hand control back instead of nesting another Codex runner."
tier: 3
group: repo-health
source: local
allowed-tools: Read, Grep, Bash
---

# Desloppify

Use this when the operator explicitly asks to run `desloppify`, improve code
quality with the `desloppify` CLI, or delegate a cleanup pass to a worker.

Do not use this for review-only requests. Use `review` when the user wants
findings without the CLI-driven fix loop.

## First-Load Contract

### Trigger Conditions

- The user names `desloppify` or asks for the `desloppify` CLI workflow
- The task is code cleanup or anti-slop improvement, not just review notes
- A scan/queue/fix loop is appropriate

### Workflow (8 Steps)

1. Decide whether you are in `main-agent mode` or `worker mode`.
2. Inspect repo docs, `.gitignore`, and obvious exclude candidates before the
   first scan.
3. In `main-agent mode`, spawn one worker subagent and give it the exact
   handoff instruction below. Do not run the whole cleanup loop in the
   coordinator unless there is a concrete reason not to delegate.
4. In worker mode, ensure Python 3.11+ is available, then run:
   `pip install --upgrade "desloppify[full]"` and
   `desloppify update-skill codex`.
5. Ensure `.desloppify/` is ignored and exclude obvious non-source paths with
   `desloppify exclude <path>`.
6. Run `desloppify scan --path <target>` and then `desloppify next`.
7. Fix the current queue item, run the exact resolve command shown by
   `desloppify next`, then repeat `desloppify next` until the queue is empty or
   a real blocker appears.
8. Rescan periodically, record score/progress, and surface any questionable
   exclude candidates or blockers.

### Mode Selector

- `main-agent mode`:
  - use this by default when the operator invokes the skill in a normal session
    and the cleanup loop is likely to take multiple turns
  - spawn one bounded subagent to use the `desloppify` CLI; reference
    `desloppify` skill subagent mode in the handoff
  - use the example handoff instruction below instead of improvising a new
    worker contract
  - own integration, questionable excludes, and any follow-up after the worker
    returns a blocker
- `worker mode`:
  - use this when the prompt explicitly says you are the delegated
    `desloppify` worker, or the parent agent says to use the skill in worker
    mode
  - run the CLI loop directly
  - do not spawn another worker
  - if `desloppify next` or the current plan requires
    `desloppify review --run-batches --runner codex`, stop and hand control
    back instead of nesting another Codex runner

Do not route this skill to `reviewer` or completion-gate roles. `desloppify`
is an execution workflow, not a judging workflow.

### Main-Agent Handoff

When delegating, include the same skill name in the worker prompt so the worker
loads this skill again.

Example spawn instruction:

```text
Spawn a subagent to use the desloppify CLI for /repo/path.
Ref: desloppify skill subagent mode.
You are that delegated desloppify worker.
Do not spawn another worker.
Own install/update, exclude review, scan, next, fix, resolve, and periodic rescan.
Surface any non-obvious exclude candidate before excluding it.
If `desloppify` requires nested `review --run-batches --runner codex`, stop and report that blocker instead of running it.
Write progress back to <ticket-or-doc-path>.
```

### Core Decision Branches

- `Repo-wide or multi-turn cleanup` -> main agent spawns one worker
- `Already inside delegated worker` -> execute directly; never recurse
- `Worker hits nested runner-codex review` -> stop, report blocker, and return
  control to the main agent
- `Questionable exclude candidate` -> stop and ask the operator before
  excluding it
- `User only wants findings or audit` -> use `review` instead
- `No Python 3.11+ or install is blocked` -> record the blocker and stop

### Top 3 Gotchas

1. Spawning nested workers because the main agent and worker roles were not made
   explicit.
2. Letting worker mode invoke nested `desloppify review --run-batches --runner codex`
   instead of handing the blocked subjective-review branch back to the main
   agent.
3. Excluding source or config paths that are merely noisy rather than genuinely
   generated, vendored, or disposable.
4. Free-styling the backlog instead of following `desloppify next` and the
   exact resolve command it provides.

### Outcome Contract

When this skill is used, the final artifact or response must include:

1. mode used: `main-agent` or `worker`
2. scan target path
3. install/update status for `desloppify`
4. confirmed excludes plus any questioned-but-not-excluded paths
5. latest scan/strict score or blocker
6. last resolved queue item and the current `next` state
7. whether nested subjective review blocked worker mode
8. any follow-up action needed outside the CLI loop

## Exclude Rules

Exclude only paths that are obviously generated, vendored, machine-local, or
non-source for the target pass. Common safe candidates include:

- build output such as `dist/`, `build/`, `.next/`, `coverage/`
- vendored dependencies such as `node_modules/`, `vendor/`
- generated SDKs or codegen output when the repo already treats them as derived
- worktree/runtime/state paths such as `.git/`, `.harness/`, `.desloppify/`

If a path contains hand-edited source, docs, tests, or config, treat it as
questionable and ask before excluding.

## Queue Discipline

- `desloppify next` is the execution queue. Follow it.
- Use `desloppify backlog` only to inspect non-current work.
- Use `desloppify plan` or `desloppify plan queue` only when reprioritizing or
  clustering related issues is actually needed.
- Rescan after a meaningful batch of fixes or when the queue instructions tell
  you to.
- If the current queue item requires nested Codex review batches, do not keep
  drilling downward from worker mode. Return that blocker to the main agent.
