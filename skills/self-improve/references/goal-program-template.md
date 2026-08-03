---
kind: goal-program-template
mode: skill_improvement
status: active
owner: skills/self-improve
---

# Self-Improve Goal Program Preset

Instantiate this compact preset into the owning ticket's `program.md` through
`goal-advisor`. The ticket owns scope and proof; Goal Advisor separately owns
the Files-listed native Goal launcher.

````markdown
---
kind: goal-program
mode: skill_improvement
trigger: native_goal
status: draft
approval: pending
compiled_from_ticket_updated_at: <ticket-updated-at>
generated_prompt: <native-goal-prompt-path>
---

# Self-Improve: <target-skill>

```yaml
files:
  - <ticket.md>
  - <program.md>
  - <hypothesis-tree.json>
  - <progress.md>
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
  rule: choose execute | diagnose | report_now | request_feedback | stop; use leverage-advisor only for real multi-option judgment
  before_each_experiment:
    inputs:
      - this program.md policy
      - eligible pending hypothesis-tree.json leaves
      - progress.md learnings and prior decisions
      - current complete-suite Eval evidence
      - remaining phase budget and patience
    output: one next experiment + expected observation + falsifier + expected reward + reward basis + material selection rationale + replan conditions
    rule: execute a mechanically implied move directly; otherwise invoke leverage-advisor; verify eligibility and budget fit

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
  - observe ticket, program, tree, latest 80 progress lines, current evidence, and remaining budget
  - choose execute | diagnose | report_now | request_feedback | stop; use leverage-advisor only when several moves need judgment
  - preregister and run the one selected round in the current phase
  - update the selected tree node with its result and insight; add only bounded diagnostic children for surprising, invalid, prerequisite-uncertain, or causally ambiguous evidence
  - append selection, tree mutation, evidence, decision, learned constraint, and next action to progress.md
  - continue, transition, block, or complete from the phase rules

drift:
  - regenerate from a fresh baseline if the ticket timestamp or suite changes

stop:
  blocked: harden ends before the target passes, or the packet becomes stale
  complete: final full-suite verification passes on the shortest retained candidate
```

Never trade required behavior for length. The Goal chooses; Leverage Advisor
conditionally compares; Eval measures; the tree owns current search state and
progress owns chronology. Do not create another loop owner or target-local
state.
````
