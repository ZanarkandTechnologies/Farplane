# Orchestrator Subagent Loop

Date: 2026-04-07

## Goal

Define the intended build-phase orchestration behavior when the main agent is
acting as orchestrator through the user-facing `$impl` skill.

`$impl` is the build-phase entrypoint for one selected ticket. It runs
ephemerally, launches the needed worker lanes, writes progress back to the
ticket/progress surface, and exits. It is not a permanent orchestration pane.

## Main Principle

The main agent should orchestrate a work package, not personally do every step.

For a selected work package, the default execution pattern is:

1. **builder** subagent implements
2. **reviewer** subagent reviews against the ticket + review gate
3. **qa** subagent gathers evidence
4. **evidence-check** subagent verifies whether the QA evidence actually makes
   sense
5. the main agent integrates the outputs and decides the next iteration

The visible runtime surface is the worker lanes, not a long-lived hidden
orchestrator.

## Ticket Selection

`$impl` should choose the ticket this way:

1. explicit ticket path or ticket id from the invocation
2. active ticket from ambient run state only when that state is unambiguous

Do not silently switch to another ready ticket while the selected ticket is
still active.

## Ownership Rules

### Main agent

Owns:

- active ticket/work package state
- progress surface updates
- sequencing of subagents
- ticket selection and orchestration re-entry
- final interpretation of builder/reviewer/QA outputs
- final handoff to the Stop hook

Does not delegate away:

- integration authority
- queue-state mutation
- final completion claim

### Builder subagent

Owns:

- implementation within the declared scope
- local validation needed to support the change

Does not own:

- final review verdict
- final QA evidence judgment
- final merge/integration decision

### Reviewer subagent

Owns:

- scoring the work against the applicable rubric
- identifying blocking weaknesses
- saying whether another build pass is required

### QA subagent

Owns:

- collecting evidence
- recording steps and observations
- attaching screenshots/logs when required

### Evidence-check subagent

Owns:

- checking whether the collected QA evidence actually supports the claimed QA
  verdict
- catching weak, contradictory, or low-context evidence

## Iteration Loop

The intended loop is:

```pseudo
main agent reads selected ticket + progress
spawn builder
spawn reviewer
spawn qa
spawn evidence-check
main agent reconciles outputs
if reviewer or evidence-check says revise:
  write next action and hand off through Stop hook / follow-up message
else:
  hand off to Stop hook
```

## Stop-Hook Re-entry

Stop-hook and judge verdicts remain the continuation/completion gate.

When the verdict says the same ticket should continue:

- reuse the existing verdict fields
- reuse `orchestrator_message` as the follow-up instruction
- re-enter the same `$impl` orchestration contract for the same selected ticket

Do not add a second orchestrator-only continuation artifact.

## Guardrails

- reviewer and QA are separate by default
- evidence-check exists because QA evidence can be weak or overconfident
- subagents may work in worktrees or file-scoped ownership later, but that is
  not required for this contract
- integration remains singular
- keep the orchestrator ephemeral
