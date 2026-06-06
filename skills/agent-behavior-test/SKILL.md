---
name: agent-behavior-test
description: Use when the operator wants an isolated agent or Codex exec run captured as a visible behavior probe for a skill, prompt, workflow, or narrow feature path, with logs, command events, final output, artifacts, and a scored evidence report.
tier: 2
source: local
allowed-tools: Read, Glob, Grep, Bash
---

# Agent Behavior Test

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Define the exact behavior under test and the target persona or skill caller.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) to inspect the
  owning skill, feature docs, ticket, existing tests, or prior artifacts before
  launching the child run.
- [ ] Confirm this is a run-capture/conformance probe; use `agent-qa-test` as
  the orchestrator when the operator wants adversarial proof or full readiness.
- [ ] Choose CLI JSONL, native subagent, or both, and name why that runner fits
  the proof target.
- [ ] Write the child prompt with visible checkpoints, forbidden shortcuts, and
  the final report shape.
- [ ] Save child-agent artifacts under the ticket, experiment, or declared run
  directory.
- [ ] Score only visible behavior: events, commands, file/artifact evidence,
  checkpoint ledger, and final output.
- [ ] Use [advise](../advise/SKILL.md) when runner choice, schema strictness, or
  pass threshold has real tradeoffs.
- [ ] Use [review](../review/SKILL.md) before treating a new behavior-test
  fixture or repeated workflow as trustworthy.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this skill when the task is to test behavior by launching a separate agent
run as an end user, QA lane, skill caller, or workflow canary, then preserving
what that child run visibly did.

This is the instrumented run-capture primitive. It answers: did the child agent
load the right context, follow the skill or prompt contract, run the expected
commands, create the required artifacts, and report a scored visible outcome?

It is not the full adversarial QA loop. When the operator asks to "test this
properly", app readiness is in question, or evidence needs a skeptical second
lane plus fix/rerun reconciliation, use `agent-qa-test` as the public
orchestrator and use this skill for the captured tester run when durable
child-agent logs matter.

This is broader than skill creation. It covers:

- testing a new or changed skill
- asking a fresh agent to use a newly built app feature
- checking whether a prompt or workflow makes the agent follow the intended
  steps
- capturing visible drift before the parent thread loses context

## First-Load Workflow

1. Define the behavior under test: target skill, app feature, prompt, workflow,
   or ticket behavior.
2. Choose the runner:
   - use `codex exec --json` when a durable event log, final output file, or
     output schema matters
   - use a native subagent when Desktop context, tool access, or an existing
     role prompt matters more than full event capture
   - use both only when native role behavior must be compared with CLI behavior
3. Write a compact test prompt that tells the child agent to produce visible
   checkpoints and a final JSON behavior report.
4. Create an artifact folder under the relevant ticket, experiment, or
   `experiments/agent-behavior-test/`.
5. Run the child agent and save at least:
   - `prompt.md`
   - `events.jsonl` or `subagent-report.md`
   - `stderr.log` when using CLI
   - `last-message.txt` or `final-report.json`
   - `score.json` or a compact scored verdict
6. Score visible behavior only: commands run, files read or written, checkpoint
   ledger, artifacts produced, final answer shape, and declared skipped steps.
7. Feed failures back to the owning surface: skill, app code, prompt, test
   fixture, ticket proof contract, or follow-up ticket.

## Core Branches

- **Skill behavior test**: require the child agent to load the skill, follow
  its Todo List, execute the requested task, and produce a todo
  ledger with evidence for each required step.
- **Narrow feature behavior probe**: require the child agent to act like a
  target user, exercise one feature path, capture logs or screenshots when
  available, and report where the product confused or blocked it. Use
  `agent-qa-test` for full feature readiness or adversarial proof.
- **Prompt or workflow test**: require visible checkpoints for the intended
  workflow phases and compare the emitted ledger with the expected sequence.
- **Regression canary**: run the same prompt against old and new behavior, then
  compare final reports and event logs.

## Gotchas

- Do not try to inspect hidden chain-of-thought. Test visible checkpoints,
  commands, artifacts, and final structured reports instead.
- Do not use TUI scraping as the default. Prefer `codex exec --json`; PTY/TUI
  scraping is brittle because it captures presentation rather than stable
  events.
- Do not let the child agent self-certify with prose alone. Require artifact
  paths, commands, screenshots/logs when relevant, and a machine-readable
  verdict.

## Judgment Questions

Use `advise` when these choices materially affect confidence or cost:

- CLI event log vs native subagent role
- one exploratory agent run vs repeated fixture regression
- free-form report vs JSON schema
- ticket artifact vs experiment artifact
- whether failure belongs to the feature, the skill, the test prompt, or weak
  instrumentation

## Outcome Contract

A completed behavior test leaves a durable artifact folder with:

- the exact child-agent prompt
- the captured event stream or subagent report
- final visible output
- scored behavior verdict
- explicit gaps and follow-up owner

That artifact folder can stand alone for skill/prompt conformance checks, or it
can become tester-lane evidence inside an `agent-qa-test` pass.

For CLI runs, start with
[codex-exec-runner.md](references/codex-exec-runner.md). Use
`scripts/run_codex_exec_behavior_test.py` when a simple one-shot Codex exec run
is enough.
