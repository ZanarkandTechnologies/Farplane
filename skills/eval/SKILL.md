---
name: eval
description: "Turn agent, prompt, or skill behavior into local eval tasks, boolean or tier judges, run artifacts, and verdicts."
tier: 3
group: operations
source: local
template_uses:
  skill-template: "0.3.0"
  skill-eval-task: "0.2.0"
  skill-qa-checklist: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
methods:
  - id: eval:onboarding
    class: internal
    output: eval-suite-setup
  - id: eval:consolidate
    class: internal
    output: eval-consolidation-report
  - id: eval:behavior-trace
    class: internal
    output: behavior-trace-evidence
  - id: eval:experiment
    class: internal
    output: experiment-eval-report
allowed-tools: Read, Glob, Grep, Bash
---

# Eval

## Context

Use this skill to create, run, repair, or consolidate a real eval for an agent,
prompt, skill, or workflow. Skill comparisons keep one Agent Skills
`evals/evals.json` and use Promptfoo; project suites and behavior traces use the
existing `.farplane/evals` runner. This skill owns eval semantics and artifacts;
Farplane Office owns rendering, history, and drilldown.

Use AGI Toy Shop for generic clean-room cases. Use a real repo fixture only
when its files are the behavior under test.

## Skill Signature

```text
eval(task_intent, expected_behavior?, mode = proof, target?, expectation?)
  -> EvalResult
reads: existing eval rows, target skill or prompt, fixtures, QA, task context
does: authors or selects cases, runs the fitting executor, inspects evidence
writes: eval rows, run artifacts, or consolidation receipts
returns: mode, cases, artifacts, verdict or delta, limitations, and next fix
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the behavior and proof path.
  - [ ] Read `qa_checklist.md`; bind the expected behavior, target, mode, suite,
        baseline, side-effect boundary, and finish proof. Reject wording-only or
        untestable claims.
  - [ ] Use `scripts/run_promptfoo.py --dry-run` for a skill comparison and
        `.farplane/evals/run_evals.py status` for project suites or behavior
        traces. Load [onboarding](references/onboarding.md) if setup is missing.
  - [ ] Keep skill-specific cases under `skills/<skill>/evals/evals.json`,
        active cross-skill cases under `.farplane/evals/tasks`, and reusable
        examples under `skills/eval/examples`.
- [ ] 2. Author or select honest cases.
  - [ ] For skill rows, write a natural `prompt`, human-readable
        `expected_output`, optional `files`, and one canonical `assertions`
        list. Use typed `metadata.farplane` only for a current UI/runtime/link
        consumer; put experimental fields under `extensions`.
  - [ ] Keep invocation, routing policy, expected answer, and reference points
        out of the user prompt. Run `farplane lint evals --changed` and
        `scripts/check_eval_queries.py --root .`, then apply `qa_checklist.md`
        to material rows.
  - [ ] Keep sanitized, reusable difficult cases in the normal runnable suite,
        not a separate metadata backlog.
  - [ ] Load [eval best practices](references/eval-best-practices.md) and the
        [writing rubric](references/eval-writing-rubric.md) when creating or
        reviewing rows; load [surface ownership](references/eval-surface-ownership.md)
        when placement is unclear.
- [ ] 3. Run the smallest faithful proof.
  - [ ] For Promptfoo comparisons, use one streaming-enabled provider profile;
        candidate and baseline share the task, model, evaluator, budget,
        sandbox, approvals, and network settings. Inspect raw rows, normalized
        summary, copied workspaces, and source-hash evidence.
  - [ ] For `behavior_trace`, load the [golden trace](examples/golden/behavior-trace.md),
        run one worker, and inspect prompt, JSONL events, logs, final output,
        command/usage scores, schema validation, and artifact inventory. Route
        native-subagent-only capture to
        [agent-qa-test](../agent-qa-test/SKILL.md).
  - [ ] For `experiment`, preregister the aggregate expectation, horizon,
        confidence, falsifier, and surprise trigger outside task grading fields.
        Compare observed versus expected results; route material misses or
        implausible wins to `agent-qa-test:experiment`.
  - [ ] For the weekly drain, load
        [eval consolidation](references/eval-consolidation.md), fetch changed
        eval files, and apply its one-file loss check while preserving distinct
        failures.
- [ ] 4. Inspect evidence and place the fix.
  - [ ] Read task details and raw artifacts before claiming a verdict. Report
        verdict counts, failures, deltas, likely cause, limitations, and the
        smallest next fix.
  - [ ] Fix the skill, fixture, checklist, profile, or runner owner; never make
        a failing case pass by teaching the answer in its prompt.
  - [ ] Send reusable runtime prevention from assertions through
        [skill-maintenance](../skill-maintenance/SKILL.md); keep rare benchmark
        points in evals. Use [self-improve](../self-improve/SKILL.md) only for
        measured variant search with an owning ticket.
- [ ] 5. Finish with independent proof.
  - [ ] Reapply `qa_checklist.md` and the owning validators. For Tier 1, meta,
        `eval`, cross-skill, or precedent-setting changes, record the
        the high-stakes design decision and use an independent reviewer.
  - [ ] Do not claim task or review-rate improvement without run artifacts or a
        reviewer receipt. Return the artifact path and next fix.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Reference Map

- Load [Agent Skills artifact contract](references/agent-skills-artifact-contract.md)
  when producing or consuming schema-v2 grading, timing, comparison, or task
  artifacts.
- Load [core lifecycle](references/core-lifecycle.md) before claiming coverage
  for the bounded Farplane lifecycle suite.
- Load [skill structure cases](references/eval-skill-structure-cases.md) for
  Tier 1, meta, `eval`, or cross-skill structure coverage.
- Load [automation prompt](references/automation-prompt.md) only when installing
  or updating the weekly consolidation automation.
- The weekly drain's reference workflow uses the shared
  [consolidation primitive](../consolidate/SKILL.md); do not load it for normal
  proof or regression runs.

## Gotchas

- A natural query tests the skill; a checklist-shaped query tests prompt memory.
- `expected_output` and assertions grade a case. An experiment expectation
  forecasts aggregate change before results are read; do not merge them.
- Behavior traces use one worker so file deltas stay attributable. Never store
  raw private transcripts, secrets, handles, or unsanitized user context.

## Output

Return one `EvalResult`: mode, cases or changed rows, run artifact paths,
verdict or observed delta, surprise status when applicable, limitations, and
the smallest next fix.
