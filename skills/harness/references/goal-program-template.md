---
kind: goal-program-template
mode: skill_improvement
status: active
owner: skills/harness
---

# Self-Improve Goal Program Preset

Instantiate this compact preset into the owning GitHub issue's `## Goal
program` section through `goal-advisor`. The ticket sections own scope and
proof; Goal Advisor separately owns the Files-listed native Goal launcher
in a separate `**Goal launcher**` comment.

````markdown
### Goal Mode: Self-Improve <target-skill>

```yaml
mode: skill_improvement
trigger: native_goal
approval: pending
compiled_from_ticket_sha: <first 12 hex of sha256(body above ## Goal program)>
```

```yaml
files:
  - <owner/repo#n>
  - <.farplane/goal-advisor/issue-<n>/hypothesis-tree.json>
  - <target-skill>/SKILL.md
  - <target-skill>/evals/evals.json

metric:
  provider: eval
  command: <eval-command>
  performance: <metric and passing target>
  length: <length-metric>
  guards: <guards>
  suite: frozen_for_this_goal

selection:
  owner: active-goal
  hypothesis_tree: <hypothesis-tree.json>
  source_stage:
    inputs: <local failures, supplied refs, configured Feed Scout signals, or bounded research>
    extracts: <techniques, mechanisms, variables, failure conditions, source refs>
  rule: choose execute | diagnose | report_now | request_feedback | stop; use goal-advisor references/choose-next.md only for real multi-option judgment
  before_each_experiment:
    inputs:
      - this ## Goal program policy
      - eligible pending hypothesis-tree.json leaves
      - Goal turn comment learnings and prior decisions
      - current complete-suite Eval evidence
      - remaining phase budget and patience
    output: one next experiment + expected observation + falsifier + expected reward + reward basis + material selection rationale + replan conditions
    rule: execute a mechanically implied move directly; otherwise apply goal-advisor references/choose-next.md; verify eligibility and budget fit

loop:
  round: one bounded target edit followed by the complete frozen eval
  harden:
    max_rounds: <n>
    patience: <n>
    accept: performance improves and guards pass
    exit: target and guards pass -> refine; budget exhausted -> block
  refine:
    max_rounds: <n>
    patience: <n>
    accept: target is preserved, guards pass, and length decreases
    reject: restore the shortest passing candidate
    exit: patience or budget exhausted -> final verification

after_each_turn:
  - observe the issue body, tree, newest Goal turn comments within 80 lines, current evidence, and remaining budget
  - choose execute | diagnose | report_now | request_feedback | stop; use the choose-next comparison only when several moves need judgment
  - preregister and run the one selected round in the current phase
  - update the selected tree node with its result and insight; add only bounded diagnostic children for surprising, invalid, prerequisite-uncertain, or causally ambiguous evidence
  - post one Goal turn comment with selection, tree mutation, evidence, decision, learned constraint, and next action; rewrite ## Current Goal state
  - continue, transition, block, or complete from the phase rules

drift:
  - regenerate from a fresh baseline if compiled_from_ticket_sha or the suite changes

stop:
  blocked: harden ends before the target passes, or the packet becomes stale
  complete: final full-suite verification passes on the shortest retained candidate
```

Never trade required behavior for length. The Goal chooses; the choose-next
comparison conditionally ranks; Eval measures; the tree owns current search state and
Goal turn comments own chronology. Do not create another loop owner or target-local
state.
````
