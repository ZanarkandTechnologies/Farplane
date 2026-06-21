---
title: "Skill Program Model Findings"
status: draft
owner: skill-system
created_at: 2026-06-19
updated_at: 2026-06-19
tags:
  - farplane
  - skills
  - programs
  - agents
  - budget
refs:
  - docs/specs/program-notation.md
  - docs/skills/system.md
  - docs/fundamentals/harness-algebra.md
  - docs/specs/goal-loop-contract.md
  - skills/agent-qa-test/SKILL.md
  - skills/agent-behavior-test/SKILL.md
  - skills/eval/SKILL.md
---

# Skill Program Model Findings

## Purpose

Capture the current working model for program-shaped skills, higher-order
workflows, and budget modifiers before turning the idea into active doctrine,
skill edits, or a ticket.

This is a draft thinking artifact. It records useful distinctions that are
still being tested.

## Current Hypothesis

Farplane skills should keep the familiar callable signature:

```text
skill(input, context?, budget?) -> output + evidence? + state_delta?
```

The new idea is that a skill's body can be understood as a prompt-program:
ordered instruction blocks an agent follows inside the thread, not necessarily
software code that is written and executed.

The inputs to these programs are often text prompts or instruction blocks, not
only structured data.

```text
program = setup_instructions
        + delegated_agent_instructions
        + verification_instructions
        + fix_or_stop_rule
```

This makes the programming analogy useful without forcing every skill into a
runtime framework.

## Agent Runs

A skill is normally equipped to an agent. The primitive is therefore not
`run(skill)`, but an agent run with one or more equipped skills.

```text
agent(spec + skills + context).run(task_prompt) -> result + evidence?
```

For skill behavior, the harness can instantiate a fresh agent with the target
skill equipped, give it a scenario, and observe whether the agent follows the
skill's contract.

```text
behavior_probe(skill, scenario_prompt, expected_behavior)
  -> observed_behavior + artifacts + score_or_findings
```

`agent-behavior-test` is currently close to this: it captures an isolated child
agent run and scores visible behavior.

## QA As Prompt Program

Agentic QA is not mainly about writing unit tests. It is about writing a clear
scenario and a program for a tester agent to execute.

```text
qa_program = {
  scenario_setup:
    "<instructions for environment, feature, files, route, or skill context>"

  tester_task:
    "<instructions for the subagent to use the feature or skill end to end>"

  verification:
    "<instructions for what evidence, bugs, screenshots, logs, artifacts, or
    skipped states must be reported>"

  loop:
    "while bugs are found: fix bugs, rerun the tester, and reconcile evidence"
}
```

`agent-qa-test` is therefore better described as a QA prompt-program and
fix/rerun loop than as a generic `test` primitive.

```text
agent_qa_test(target, scenario_prompt, success_claim, qa_policy?)
  -> tester_evidence + bugs + fixes_or_rerun + verdict
```

The important skill value is parameter filling:

- what scenario to test
- how to initialize the target
- which agent instructions to give the tester
- what evidence would prove or falsify success
- when to fix, rerun, block, or stop

## Eval Boundary

`eval` owns benchmark-like and repeatable behavior tests: task sets, judges,
scores, run artifacts, and reusable regression cases.

Agentic QA owns operated scenario proof: a subagent tries the feature, workflow,
or equipped skill according to instructions and reports what broke.

```text
eval(subject, tasks, judge) -> scores + failures
agent_qa_test(subject, scenario_prompt, success_claim) -> bugs + evidence + verdict
```

If a QA scenario becomes stable, high-value, and repeatable, it can later become
an eval case. Until then, it is a flexible prompt-program.

## Higher-Order Workflows

Some workflows consume another skill, prompt-program, or capability as input.
They are higher-order workflows, but they are not all skill modifiers.

```text
higher_order_workflow(subject_skill_or_program, policy?) -> report_or_state_delta
```

Examples:

```text
agent_qa_test(skill_or_app, scenario_prompt, success_claim)
  -> bugs + evidence + verdict
```

```text
rollout(skill_or_program, cases, rollout_policy)
  -> staged_results + hold_or_promote
```

```text
eval(skill_or_prompt, task_set, judge)
  -> score_report + failures
```

These workflows take another skill or program as an input, but their purpose is
to operate, prove, score, or stage it. They do not necessarily return a modified
skill.

## Skill Modifiers

A skill modifier is a narrower concept. It takes a skill program and returns a
modified skill program with the same user-facing output contract.

```text
skill_modifier(config)(skill_program) -> modified_skill_program
```

Budget is the clearest candidate:

```text
budget(config)(advise)
  -> advise_with_more_depth_or_lanes
```

For example:

```text
advise(decision, budget={lanes: 5})
  = run five advice agents with different perspective prompts
  + synthesize results
  + return the normal advise output contract
```

The output remains:

```text
options + recommendation + tradeoff + next_step
```

Budget changes the internal program, not the meaning of the skill.

## Rollout Boundary

Rollout is a higher-order workflow, not necessarily a skill modifier.

```text
rollout(skill_or_program, cases, policy)
  -> rollout_report + promoted_or_held_state
```

Program shape:

```text
cases = gather_cases()

while apply(skill, sample(cases)) is not satisfactory:
  feedback = evaluate_sample(skill, sample(cases))
  refine(skill_or_instructions, feedback)

for batch in expand(cases):
  results = apply_many(skill, batch)
  if results fail:
    hold_or_refine()
  else:
    promote_next_batch()
```

This may refine the skill instructions, but the primary output is staged proof
and rollout state, not a guaranteed transformed skill.

## Open Questions

1. What is the exact test for calling something a skill modifier rather than a
   higher-order workflow?
2. Should budget become the first explicit skill modifier, or remain a
   documented parameter convention until more examples prove the need?
3. Should QA prompt-program writing become its own reusable skill, separate
   from `agent-qa-test`, or should it remain a method inside that skill?
4. Which stable QA scenarios should promote into `eval` cases?
5. Where should the prompt-program primitive live: `templates/global/AGENTS.md`,
   `docs/skills/system.md`, `docs/specs/program-notation.md`, or a new
   fundamentals section?

## Working Rules

- Keep normal skill signatures. Do not replace them with a new programming
  taxonomy.
- Treat prompt-programs as instruction sequences an agent follows, not
  necessarily code that must be generated and executed.
- Use software-program analogies when they clarify control flow, state,
  delegation, and stop conditions.
- Do not call every higher-order workflow a skill modifier.
- Reserve "skill modifier" for workflows that preserve the target skill's
  user-facing output contract while changing its internal execution shape.
- Treat `agent-qa-test` as scenario plus tester instructions plus verification
  plus fix/rerun loop.
- Treat `agent-behavior-test` as isolated equipped-agent behavior capture.
- Treat `eval` as the owner for repeatable task/judge/scoring artifacts.

## Current Best Summary

```text
Base skill:
  skill(input, context?, budget?) -> output + evidence? + state_delta?

Prompt-program:
  setup_instructions + agent_task_instructions + verification_instructions
  + stop_or_loop_rule

Higher-order workflow:
  workflow(skill_or_program, policy?) -> proof_report | rollout_state | score

Skill modifier:
  modifier(config)(skill_program) -> modified_skill_program
```

Budget is likely a skill modifier. QA, rollout, and eval are better understood
as higher-order workflows unless they explicitly return a modified skill
program with the same output contract.
