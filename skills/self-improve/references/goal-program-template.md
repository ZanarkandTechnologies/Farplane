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
  owner: leverage-advisor
  roadmap:
    objective: <optimization objective>
    candidates: <initial intervention frontier or project-local catalog ref>
    first_proof: <baseline-grounded first experiment>
    contingencies: <positive, flat, negative, invalid, and budget branches>
  before_each_experiment:
    inputs:
      - this program.md roadmap
      - progress.md learnings and prior decisions
      - current complete-suite Eval evidence
      - remaining phase budget and patience
    output: one next experiment + hypothesis + falsifier + rejected alternatives + replan conditions
    rule: invoke leverage-advisor; do not continue a fixed roadmap order

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
  - use leverage-advisor on the roadmap plus progress.md learnings, current evidence, and remaining budget
  - preregister and run the one selected round in the current phase
  - append selected move, rejected alternatives, hypothesis, measurements, evidence, decision, learned constraint, and next action to progress.md
  - continue, transition, block, or complete from the phase rules

drift:
  - regenerate from a fresh baseline if the ticket timestamp or suite changes

stop:
  blocked: harden ends before the target passes, or the packet becomes stale
  complete: final full-suite verification passes on the shortest retained candidate
```

Never trade required behavior for length. Leverage Advisor chooses the move;
native Goal continues; Eval measures; this ticket's program/progress own state.
Do not create another loop owner or target-local state.
````
